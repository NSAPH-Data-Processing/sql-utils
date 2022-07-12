
def get_first_diag_label_time(diag_code):
    """
    generates the sql query needed to find the first diagnosis in hospital admissions.
    Resulting table will be formatted as
    1. bene_id | 2. admission_date | 3. diagnosis | 4. present_diag_code | 5. first_diag_diag_code | 6. first_admission_date
    present_diag_code: Boolean, indicates whether the diag_code is reported in the diagnosis of that record.
    first_diag_diag_code: Boolean, indicates whether this is the first time diag_code is reported for this beneficiary.
    first_admission_date: Datetime, representing the first day diag_code is reported for this beneficiary.
    Column 5 and 6 will be NULL if diag_code is never reported for this beneficiary.

    :param diag_code: ICD9/10 diagnosis code.
    :return: the PostgreSQL statement to pass into the engine
    """

    sql = f"""
    SELECT ad.bene_id, admission_date, diagnosis, diagnosis && '{{{diag_code}}}' AS present_{diag_code}, admission_date = first_admin_date AS first_diag_{diag_code}, first_admin_date 
    FROM medicaid.admissions AS ad
    
    LEFT JOIN (
    -- earliest admission date containing diag_code
    SELECT bene_id, min(admission_date) as first_admin_date from medicaid.admissions
    WHERE diagnosis && '{{{diag_code}}}'
    GROUP BY bene_id
    ) AS first_diag
    
    ON ad.bene_id = first_diag.bene_id 
    
    -- shows records with the diagnosis code first
    ORDER BY present_{diag_code} DESC, ad.bene_id, admission_date 
        """

    return sql


def main():
    # 770.89 is a sample ICD9 code.
    print(get_first_diag_label_time('77089'))


if __name__ == "__main__":
    main()
