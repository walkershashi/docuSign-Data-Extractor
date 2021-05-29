import pyodbc

server = '{SEVER_ADDRESS}'
database = '{DB_NAME}'
username = '{USERNAME}'
password = '{PASSWORD}'
driver = '{ODBC Driver 17 for SQL Server}'

# Create a connection string
conn = conn = pyodbc.connect('DRIVER={};PORT=1433;SERVER={};PORT=1443;DATABASE={};UID={};PWD={}'.format(
    driver,
    server,
    database,
    username,
    password
))

# Define a cursor
cursor = conn.cursor()

# Function to insert rows into table
def insert(tableName, columns, values):
    qry = "Insert Into [dbo].[" + tableName + "] (" + ','.join(columns) + ") values {}".format(tuple(values))
    print(qry)
    
    cursor.execute(qry)
    conn.commit()

    print("Values Inserted")
