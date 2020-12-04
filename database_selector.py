import sqlite3

NAME = 1
EMAIL = 2
PHONE = 4
DEPARTMENT = 8
REG_NO = 16
BLOOD_GROUP = 32

parameters_lis = [1,2,4,8,16,32]


class manager():

	#constructor of the class parameter = name of the file 
	def __init__(self,name):
		self.file_name = name
		#connecting to the database
		self.conn = sqlite3.connect(self.file_name)


	# to query the database parameters = (value : value of the query , prameter: which field you want to serach for)
	def search_parameter(self, value,parameter="NAME"):

		#quering the database
		y = self.conn.execute("SELECT * FROM STUDENTS WHERE {} like '{}%'".format(parameter,value))

		#converting ouput from class object to list
		output = [x for x in y]

		#returning the output as a list 
		return output


	# forming the data field of the packet from the data returned for the search parameter function 
	def format_data(self, data,response_format):

		stri = ""

		#loop through every record
		for individual in data:
			index = 1

			
			for u in parameters_lis:
				#check whether the particular columun require or not	
				if(response_format&u!=0):
					#if requred adding to the sring sperating it by linefeed
					stri= stri+str(individual[index])+"\n"


				index = index+1

			#serperating earch individual record by extra line feed
			stri = stri+"\n"

			

		return stri



# y = manager("test.db")

# print(y.format_data(y.search_parameter("navdeep singh","name")))