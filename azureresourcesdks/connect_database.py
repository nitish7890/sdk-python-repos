import pyodbc
server = 'sixserver1.database.windows.net'
database = 'DemoDataBase'
username = 'azureadmin'
password = 'Test@123' 
driver= '{ODBC Driver 17 for SQL Server}'


with pyodbc.connect('DRIVER= '+ driver + '; SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
         cursor.execute('''DROP TABLE IF EXISTS dbo.Home
CREATE TABLE dbo.Teacher(
 	[Teacher ID] int,
 	[Teacher Name] nvarchar(20),
 	Stream nvarchar(20)
)''')

