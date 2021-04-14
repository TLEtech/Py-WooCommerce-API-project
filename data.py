import pyodbc as dbc
import pandas as pd
import yaml
import json

# Variables
with open("config.yml", 'r') as configInfo:
    config = yaml.safe_load(configInfo)
Server = config['DBC']['server']
DB = config['DBC']['DB']
DBuser = config['DBC']['ReadUser']
DBuserPW = config['DBC']['PW']
ReadTable = config['DBC']['ReadTable']
ReadQuery = config['DBC']['ReadQuery']

Conn = dbc.connect('DRIVER={SQL Server};SERVER='+Server+';DATABASE='+DB+';UID='+DBuser+';PWD='+DBuserPW)
Cursor = Conn.cursor()

ReadQueryStmt = (ReadQuery+ReadTable)

df = pd.read_sql(ReadQueryStmt, Conn)

