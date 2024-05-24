import mysql.connector

cnx = mysql.connector.connect(
  user='root',
  password='',
  host='127.0.0.1',
  database='86_akk_crp'
)
cursor = cnx.cursor()