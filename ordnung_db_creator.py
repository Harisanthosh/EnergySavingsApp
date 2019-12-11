import pandas as pd
import sqlite3

db = sqlite3.connect('energy.db')
# dfs = pd.read_excel('Energy Demand FT.xlsx', sheet_name=None, header = 4, skiprows = range(1, 5))
dfs = pd.read_excel('Energy Demand FT.xlsx', sheet_name=None, header = 4)
for table, df in dfs.items():
    df.to_sql(table, db)