import mysql.connector

conn = mysql.connector.connect(host="10.1.10.11",port="3306",user="dimitar",password="Butel1Butel",database="dimitar")

cursor=conn.cursor()
counter = 3
while counter!=0:
    insert_query = " INSERT INTO test (id, state) VALUES (2,1)"
    cursor.execute(insert_query)
    counter=counter-1

conn.commit()