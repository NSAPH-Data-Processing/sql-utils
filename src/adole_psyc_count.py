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


def get_bene_count(year, age_low, age_high):
    """
    calculates the beneficiaries of certain ages per zipcode
    :param year: the year of Medicaid to query
    :param age_low: lower bound of the population age
    :param age_high: upper bound of the population age
    :return: sql_query: the PostgreSQL statement to pass into the engine
    """
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
    GROUP BY zip
    ) AS psyc_zip -- calculates psyc diagnosis by zipcode
    """

    return sql_query


def main():
    outcomes = get_outcomes()
    psyc_icd = outcomes['psychiatric']['icd9']
    get_psyc_count(2012, 10, 18, psyc_icd)
    print(get_bene_count(2012, 10, 16))


if __name__ == "__main__":
    main()
