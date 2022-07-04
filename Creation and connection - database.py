'''This is the file which contains the way the raw data was updated into the SQL table.
Be informed the SQL table is located in the Google Cloud Hub.''' 

import mysql.connector
from mysql.connector.constants import ClientFlag
import pandas as pd

config = {
    'user': 'root',
    'password': 'Team209',
    'host': '34.135.47.175'
    'database': 'testdb'
}

#Now we establish our connection
cnxn = mysql.connector.connect(**config)
cursor = cnxn.cursor(buffered=True)



cursor = cnxn.cursor()  # initialize connection cursor
cursor.execute('CREATE DATABASE testdb')  # create a new 'testdb' database
cnxn.close()  # close connection because we will be reconnecting to testdb


# Create a database
cursor.execute("CREATE TABLE PQR ("
               "PQR VARCHAR(8000),"
               "Type VARCHAR(10) )")

# this commits changes to the database
cnxn.commit()  


#Read the excel files
data =pd.read_excel('/content/drive/MyDrive/Raw Data/pqrs example2.xlsx', header = 0 )
data.tail()

#Upload Manual Data to SQL
for i in range (len(data['pqr'])):
  PQR, type_d = data['pqr'].iloc[i],data['tipo'].iloc[i]
  query = ("INSERT INTO PQR (PQR, Type) VALUES ('%s', '%s')" %(PQR,type_d))
  cursor.execute(query)
cnxn.commit()

#Pull the data from SQL
query = ("Select * from PQR")
cursor.execute(query)
result = cursor.fetchall()

#Create Dataframe to train the model
df = pd.DataFrame(result, columns=['pqr', 'tipo'])

