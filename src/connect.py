import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from secrets import *
# import matplotlib.pyplot as plt
# import seaborn as sns
import psycopg2

print(f'postgresql://{user}:{password}@{host}:{port}/{db}')

# connect to database
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
print(engine)

connection = engine.raw_connection()

print("success")

# create cursor to execute query
cursor = connection.cursor()