import sqlite3
import os
import pandas as pd


df = pd.read_csv("2018batch.csv")



lis = ["Name","Email","Reg No","Department","Mobile No","Blood Group"]


all_data = []
for k in range(0,132):
	temp = {}
	for row in lis:
		temp[row] = str(df[row][k]).lower()
	all_data.append(temp)

print(all_data)


blood_map = {"a+":0,"b+":1,"a-":2,"b-":3,"ab-":4,"ab+":5,"o+":6,"o-":7}


# for k in all_data:
# 	for keys in lis:
# 		k[keys]= k[keys].lower()

count = 0

ranges = [25,47,80,106,132]

for k in all_data:
	cat = 0
	for r in ranges:
		if(count<r):
			break
		cat = cat +1

	print(cat)
	k["Department"]=cat 
	count=count+1

for k in all_data:
	if k["Blood Group"] in blood_map.keys():
		k["Blood Group"] = blood_map[k["Blood Group"]]
	else:
		# print(k["Blood Group"])
		k["Blood Group"] = 1




os.remove("test.db")

conn = sqlite3.connect('test.db')
print ("Opened database successfully");



def create_table(conn):
	conn.execute('''
	CREATE TABLE STUDENTS (  
	ID INTEGER PRIMARY KEY AUTOINCREMENT,  
	NAME VARCHAR(255),  
	EMAIL VARCHAR(255),
	PHONENUMBER VARCHAR(255),
	DEPARTMENT INT,   
	REG_NO VARCHAR(255) ,  
	BLOOD_GROUP INT
	);''')
print ("Table created successfully");


create_table(conn)
# 
def insert_table(conn,all_data):

	for data in all_data:
		stri = f"'{data['Name']}','{data['Email']}','{data['Mobile No']}',{data['Department']},'{data['Reg No']}',{data['Blood Group']}"

		conn.execute('''
		INSERT INTO STUDENTS(NAME, EMAIL,PHONENUMBER,DEPARTMENT,REG_NO,BLOOD_GROUP)
		VALUES ({});
		'''.format(stri))

	conn.commit()

def select(conn):
	cursor = conn.execute("select * from STUDENTS")
	for row in cursor:
		print(row)






insert_table(conn,all_data )

select(conn)

conn.close()