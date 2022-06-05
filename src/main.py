# import psycopg2
import numpy as np
# TODO: assuming package install. Check FASSE env

# defining constants
PT_ID_STR = 'QID'
PT_TABLE = 'medpar'  # TODO: check name


def first_ADATE(patients):
    """
    fetches the first admission dates of patients
    :param patients: a list of patients to fetch from
    :return: sql: query to fetch each patient's admission date
    """

    # check for duplicate patients
    pt_unique = np.unique(patients)
    if len(patients) != len(pt_unique):
        print(f'WARNING: list patients has {len(patients)} patients but {len(pt_unique)} unique values. Check duplicates')

    # PostgreSQL list convention
    pt_sql = '(' + ','.join(str(pt) for pt in pt_unique) + ')'

    # writing to SQL
    # disctinct on selects the first occurence, order by ADATE to select the first admission date
    # https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-select-distinct/
    sql = f"""
    SELECT DISTINCT ON ({PT_ID_STR}) {PT_ID_STR} FROM {PT_TABLE} 
          WHERE {PT_ID_STR} IN {pt_sql}
          ORDER BY {PT_ID_STR}, ADATE;
    """
    sql = sql_check(sql)
    print(sql)
    return sql


def sql_check(sql):
    """
    check if the statement conform to PostgreSQL standard and fix minor issues.
    :param sql: the sql statement to check
    :return: sql_clean: cleaned sql statement
    """
    sql = sql.strip()

    # TODO: more rules to come
    assert sql[-1] == ';', "Missing ';' at the end of the statement"
    return sql


def main():
    # Connect to your postgres DB
    conn = psycopg2.connect("dbname=test user=postgres")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a query
    cur.execute(first_ADATE)

    # Retrieve query results
    records = cur.fetchall()


if __name__ == "__main__":
    main()

