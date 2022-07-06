import json


def get_outcomes():
    """ Get and return ICD codes """""
    f = open('icd_codes.json')
    outcomes_ = json.load(f)
    f.close()
    return json.loads(outcomes_[0])


def get_psyc_count(year, age_low, age_high, diagnoses):
    """
    calculates the number of psychiatric diagnoses between age_low and age_high per zip code within a year
    :param year: the year of Medicaid to query
    :param age_low: lower bound of the population age
    :param age_high: upper bound of the population age
    :param diagnoses: a list of ICD codes to match the Medicaid diagnoses
    :return: sql_query: the PostgreSQL statement to pass into the engine
    """
    diag_string = ",".join(diagnoses)
    sql_query = f"""SELECT * FROM (
    SELECT COUNT(bene_id) AS diag_count, zip  FROM
    (
    SELECT ad.year, ad.bene_id, admission_date, dob, diagnosis, zip, DATE_PART('year', admission_date) - DATE_PART('year', dob) AS age FROM medicaid.admissions AS ad
    INNER JOIN medicaid.beneficiaries AS bene ON ad.bene_id = bene.bene_id 
    INNER JOIN medicaid.enrollments on enrollments.bene_id = ad.bene_id 
    WHERE ad.year = {year} and enrollments.year = {year}-- want the year patients is admitted and enrolled for accurate zipcode
    ) 
    AS bene_age -- calculates age
    WHERE age >= {age_low} and age <= {age_high} --column alias cannot be used directly in the query 
    AND diagnosis && '{{{diag_string}}}'
    GROUP BY zip
    ) AS psyc_zip -- calculates psyc diagnosis by zipcode
    """

    return sql_query


def get_hosp_admin_count(year, age_low, age_high):
    """
    calculates the beneficiaries of certain ages per zipcode
    :param year: the year of Medicaid to query
    :param age_low: lower bound of the population age
    :param age_high: upper bound of the population age
    :return: sql_query: the PostgreSQL statement to pass into the engine
    """
    sql_query = f"""SELECT * FROM (
    SELECT COUNT(bene_id) AS admin_count, zip  FROM
    (
    SELECT ad.year, ad.bene_id, admission_date, dob, diagnosis, zip, DATE_PART('year', admission_date) - DATE_PART('year', dob) AS age FROM medicaid.admissions AS ad
    INNER JOIN medicaid.beneficiaries AS bene ON ad.bene_id = bene.bene_id 
    INNER JOIN medicaid.enrollments on enrollments.bene_id = ad.bene_id 
    WHERE ad.year = {year} and enrollments.year = {year}-- want the year patients is admitted and enrolled for accurate zipcode
    ) 
    AS bene_age -- calculates age
    WHERE age >= {age_low} and age <= {age_high} --column alias cannot be used directly in the query 
    GROUP BY zip
    ) AS all_zip -- calculates psyc diagnosis by zipcode
    """

    return sql_query


def get_diag_vs_all_diag(year, age_low, age_high, diagnoses):
    """
    returns a table containing columns: 1)% of diagnoses divided by all admissions 2) diagnoses count 3) total admission count 4) zip code
    :param year: the year of Medicaid to query
    :param age_low: lower bound of the population age
    :param age_high: upper bound of the population age
    :param diagnoses: a list of ICD codes to match the Medicaid diagnoses
    :return: sql_query: the PostgreSQL statement to pass into the engine
    """
    diag_string = ",".join(diagnoses)

    sql_query = f"""
    SELECT diag_count / cast(admin_count AS FLOAT ) AS diag_vs_all_diag, --cast float, otherwise integer division by default
    diag_count, admin_count, all_zip.zip
    FROM 
    (
    
    /* subqery to find all hospital admissions by zipcode */
    SELECT COUNT(bene_id) AS admin_count, zip  FROM
      (
    SELECT ad.year, ad.bene_id, admission_date, dob, diagnosis, zip, DATE_PART('year', admission_date) - DATE_PART('year', dob) AS age FROM medicaid.admissions AS ad
    INNER JOIN medicaid.beneficiaries AS bene ON ad.bene_id = bene.bene_id 
    INNER JOIN medicaid.enrollments on enrollments.bene_id = ad.bene_id 
    WHERE ad.year = {year} and enrollments.year = {year}-- want the year patients is admitted and enrolled for accurate zipcode
      ) AS bene_age -- calculates age
    WHERE age >= {age_low} and age <= {age_high} --column alias cannot be used directly in the query 
    GROUP BY zip
    ) AS all_zip -- all hospital admissions
    
    LEFT JOIN (
    
    /* subquery to find admissions identified by ICD codes*/
    SELECT COUNT(bene_id) AS diag_count, zip  FROM
      (
    SELECT ad.year, ad.bene_id, admission_date, dob, diagnosis, zip, DATE_PART('year', admission_date) - DATE_PART('year', dob) AS age FROM medicaid.admissions AS ad
    INNER JOIN medicaid.beneficiaries AS bene ON ad.bene_id = bene.bene_id 
    INNER JOIN medicaid.enrollments on enrollments.bene_id = ad.bene_id 
    WHERE ad.year = {year} and enrollments.year = {year}-- want the year patients is admitted and enrolled for accurate zipcode
      ) AS bene_age -- calculates age
    WHERE age >= {age_low} and age <= {age_high} --column alias cannot be used directly in the query 
    AND diagnosis && '{{{diag_string}}}'
    
    GROUP BY zip
    ) as diag_zip -- admissions that have the above diagnoses
    
    ON all_zip.zip = diag_zip.zip -- join by zip code. 
    
    ORDER BY diag_vs_all_diag DESC NULLS last ; --NULL has the largest value in Postgres
    """

    return sql_query


def get_diag_vs_all_enroll(year, age_low, age_high, diagnoses):
    """
    returns a table containing columns: 1)% of diagnoses divided by all enrolls 2) diagnoses count 3) total enrollee count 4) zip code
    :param year: the year of Medicaid to query
    :param age_low: lower bound of the population age, inclusive
    :param age_high: upper bound of the population age, inclusive
    :param diagnoses: a list of ICD codes to match the Medicaid diagnoses
    :return: sql_query: the PostgreSQL statement to pass into the engine
    """

    diag_string = ",".join(diagnoses)

    sql_query = f"""
    SELECT diag_final / cast(enroll_count AS FLOAT ) AS diag_vs_all_enroll, * FROM 
    (
      SELECT  
      coalesce(diag_count, 0) AS diag_final, enroll_count, all_zip.zip -- coalecse replaces all null with 0
      FROM 
      (
      SELECT COUNT(bene_id) AS enroll_count, zip  FROM
        (
        SELECT enroll.bene_id, dob, year, zip, {year} - EXTRACT(YEAR FROM dob) AS age FROM medicaid.enrollments as enroll
        INNER JOIN medicaid.beneficiaries AS bene ON enroll.bene_id = bene.bene_id 
        WHERE enroll.year = {year}-- want the year patients is admitted and enrolled for accurate zipcode
          ) AS bene_age -- calculates age
        WHERE age >= {age_low} and age <= {age_high} --column alias cannot be used directly in the query 
        GROUP BY zip
      ) AS all_zip -- all enrollments per zipcode
      
      LEFT JOIN (
        SELECT COUNT(bene_id) AS diag_count, zip  FROM
          (
          
          /*
          Even though admission date and dob can be used to calculate the exact age, using YEAR(dob) - YEAR(of interest) for consistency.
          */
        SELECT ad.year, ad.bene_id, admission_date, dob, diagnosis, zip, {year} - EXTRACT(YEAR FROM dob) AS age FROM medicaid.admissions AS ad
        INNER JOIN medicaid.beneficiaries AS bene ON ad.bene_id = bene.bene_id 
        INNER JOIN medicaid.enrollments on enrollments.bene_id = ad.bene_id 
        WHERE ad.year = {year} and enrollments.year = {year}-- want the year patients is admitted and enrolled for accurate zipcode
          ) AS bene_age -- calculates age
        WHERE age >= {age_low} and age <= {age_high} --column alias cannot be used directly in the query 
        AND diagnosis && '{{{diag_string}}}'
        
        GROUP BY zip
      ) AS diag_zip -- admissions that have the above diagnoses
      
      ON all_zip.zip = diag_zip.zip -- join by zip code. 
      
--       WHERE (diag_count > 10 AND enroll_count > 10) OR (diag_count = 0 AND enroll_count > 10) OR (diag_count > 10 AND enroll_count = 0) OR (diag_count = 0 AND enroll_count = 0)--confidentiality
    ) AS diag_w_zeros --column alias cannot be used directly in the query 
-- ORDER BY diag_vs_all_enroll DESC NULLS last ;
"""
    return sql_query


def main():
    outcomes = get_outcomes()
    psyc_icd = outcomes['psychiatric']['icd9']
    # get_psyc_count(2012, 10, 18, psyc_icd)
    # print(get_hosp_admin_count(2012, 10, 16))
    # print(get_diag_vs_all_diag(2008, 10, 16, psyc_icd))
    print(get_diag_vs_all_enroll(2012, 18, 200, psyc_icd))


if __name__ == "__main__":
    main()
