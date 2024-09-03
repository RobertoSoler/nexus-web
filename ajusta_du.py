import sqlite3
import datetime
from datetime import datetime
from datetime import date
from workadays import workdays

#---------------------------------------
try:
    sqliteConnection = sqlite3.connect('C:/Users/procs/OneDrive/DATABASES/BRLMarket.db')
    cursor = sqliteConnection.cursor()
    print("Database successfully Connected to SQLite")
except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
#---------------------------------------

def load_venctos():
    query = "SELECT * FROM vencimentos"
    query_run = cursor.execute(query)
    series = cursor.fetchall()
    return series

d1 = date.today()

dados = load_venctos()

for k in dados:
    d = k[0]
    print(d)
    d2 = datetime.strptime(d,'%Y-%m-%d').date()
    du = workdays.networkdays(d1, d2)
    query = "UPDATE vencimentos SET du=" + str(du) + " WHERE data='" + d + "'"
    query_run = cursor.execute(query)
    print(query)

sqliteConnection.commit()
sqliteConnection.close()
