import json
import sys
from decimal import Decimal
import pandas as pd
from psycopg2.extras import RealDictCursor
from nsaph.db import Connection
from pandas import DataFrame

########################################################
# This file shows a simple case of creating an empty table on Superset.
# Sample CSV is found here: https://dataverse.harvard.edu/file.xhtml?fileId=5810568&version=1.0
########################################################

df = pd.read_csv("csv/Study_dataset_2010.csv")
data_types = df.dtypes

dtype_list = [str(dtype) for dtype in data_types]
column_names = df.columns

### creating database ###
# data dictionary for converting python variable types to Psql data types
python_sql_dict = {'int64':'INT', 'float64':'numeric', 'object':'VARCHAR(255)'} # work in progress as more variables are encountered. TODO: datetime

column_dtype = []
for index, dtype in enumerate(dtype_list):
    # writing the table schema
    column_dtype.append((column_names[index] + ' ' + python_sql_dict[dtype]))
    
columns_dtype_str = ',\n'.join(column_dtype)

SCHEMA = 'change_schema_name'
TABLE_NAME = 'change_table_name'
SQL = f"""DROP TABLE IF EXISTS {SCHEMA}.{TABLE_NAME} CASCADE;
CREATE TABLE  {SCHEMA}.{TABLE_NAME}
(
{columns_dtype_str}
);"""



def query(db_ini_file: str, db_conn_name: str):
    connection = Connection(db_ini_file,
                            db_conn_name,
                            silent=True,
                            app_name_postfix=".sample_query")
    
    with connection.connect() as cnxn:
        with cnxn.cursor(cursor_factory=RealDictCursor) as cursor:
            print("Executing SQL command...")
            cursor.execute(SQL)
            return df


if __name__ == '__main__':
    df_test = query(sys.argv[1], sys.argv[2])
                