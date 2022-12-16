#  Copyright (c) 2022. Harvard University
#
#  Developed by Research Software Engineering,
#  Faculty of Arts and Sciences, Research Computing (FAS RC)
#  Authors: Michael A Bouzinier
#           Zifan Gu
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
import json
import sys
from decimal import Decimal
import pandas as pd

from psycopg2.extras import RealDictCursor

from nsaph.db import Connection

from pandas import DataFrame

######Enter your query here######
SQL = '''
SELECT diag, COUNT(diag)  FROM 
(SELECT unnest(diagnosis) as diag, year, DATE_PART('year', admission_date) - DATE_PART('year', dob) AS age FROM medicaid.admissions AS ad
INNER JOIN medicaid.beneficiaries AS bene ON ad.bene_id = bene.bene_id 
)
AS all_diag
WHERE diag IS NOT NULL AND age >= 0 AND age <= 18
GROUP BY diag
ORDER BY COUNT(diag) DESC
LIMIT 20;
'''
#################################

def query(db_ini_file: str, db_conn_name: str):
    connection = Connection(db_ini_file,
                            db_conn_name,
                            silent=True,
                            app_name_postfix=".sample_query")
    
    with connection.connect() as cnxn:
        with cnxn.cursor(cursor_factory=RealDictCursor) as cursor:
            print("Query in progres...")
            cursor.execute(SQL)
            records = cursor.fetchall()
            print("Converting returned query to dataframe...")
            df = pd.DataFrame([i.copy() for i in records])
            print("Returned {:d} rows".format(len(df)))

            return df


if __name__ == '__main__':
    df_test = query(sys.argv[1], sys.argv[2])
    df_test.to_csv("all_icd_age_0_18.csv", index=False)
                
