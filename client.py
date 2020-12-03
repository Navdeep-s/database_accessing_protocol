import sys


NAME = 1
EMAIL = 2
PHONE = 4
DEPARTMENT = 8
REG_NO = 16
BLOOD_GROUP = 32

message_id = 1


print_dic = {NAME:"Name",EMAIL:"Email Id",PHONE:"Phone no.",DEPARTMENT:"Department",REG_NO:"Entry No",BLOOD_GROUP:"Blood Group"}



NAME_SEARCH = 0
EMAIL_SEARCH = 1
PHONE_SEARCH = 2
DEPARTMENT_SEARCH = 3
REG_NO_SEARCH = 4
BLOOD_GROUP_SEARCH = 5



MAX_QUERY_TRY = 5

blood_group_mapping= {0:"A+",1:"B+",2:"A-",3:"B-",4:"AB-",5:"AB+",6:"O+",7:"O-"}
department_mapping = {0:"Chemical Engineering",
					1:"Civil Engineering",
					2:"Computer Science Engineering",
					3:"Electrical Engineering",
					4:"Mechanial Engineering"}

INT = "i"
STR = "s"

def universal_decoder(arr,definiton):
	outputs = []
	counter = 0
	for k in definiton:
		temp_bytes = arr[counter:counter+k[0]]
		if(k[0]==0):
			temp_bytes = arr[counter:]
		if(k[1]==INT):
			outputs.append(int.from_bytes(temp_bytes, byteorder='big'))
		elif(k[1]==STR):
			outputs.append(temp_bytes.decode("utf-8"))
		counter = counter + k[0]

	return outputs




import socket



def create_message(query_type,response_type,value):
	global message_id 
	message_id = 45
	bytes_to_send = message_id.to_bytes(4, byteorder='big')
	bytes_to_send = bytes_to_send+query_type.to_bytes(1, byteorder='big')
	bytes_to_send = bytes_to_send+response_type.to_bytes(1, byteorder='big')
	bytes_to_send = bytes_to_send+value.encode("utf-8")

	return bytes_to_send



def decode_response(arr):
	id_bytes = arr[0:4]
	fragment_number_bytes = arr[4:5]
	number_of_answers_bytes = arr[5:6]
	data_len_bytes = arr[6:10]
	data_bytes = arr[10:]


	message_id =int.from_bytes(id_bytes, byteorder='big') 
	fragment_number =int.from_bytes(fragment_number_bytes, byteorder='big') 
	number_of_answers =int.from_bytes(number_of_answers_bytes, byteorder='big') 
	data_len =int.from_bytes(data_len_bytes, byteorder='big') 
	data = data_bytes.decode("utf-8")

	print(message_id,fragment_number,number_of_answers,data_len,data)





def make_sense(data,response_type):

	chunks = data.split("\n\n")

	output=[]
	lis = [1,2,4,8,16,32]
	for chunk in chunks:
		if(chunk==""):
			break
		dict_out = {}
		rows = chunk.split("\n")
		
		row_index =0
		for elem in lis:
			
			if(response_type&elem!=0):
				
				if(elem==DEPARTMENT):
					
					dict_out[elem]=department_mapping[int(rows[row_index])]	
				elif(elem==BLOOD_GROUP):
					dict_out[elem]=blood_group_mapping[int(rows[row_index])]
				elif(elem==NAME):
					dict_out[elem]=rows[row_index].title()

				else:
					dict_out[elem]=rows[row_index]
				row_index= row_index+1

			else:
				dict_out[elem]=None


		output.append(dict_out)

	return output


def print_data(lis):
	output = []
	for dic_chunk in lis:
		stri = ""
		for key in dic_chunk.keys():
			if(dic_chunk[key]!=None):
				addition = "{:<11} : {}\n".format(print_dic[key],dic_chunk[key])
				stri  = stri +addition
		output.append(stri)
	return output





msgFromClient       = "Hello UDP Server"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("localhost", 20001)
bufferSize          = 200

 


response_format = [(4,INT),(1,INT),(1,INT),(0,STR)]

# Create a UDP socket at client side

client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
client.settimeout(3)


query_tries = 1

query_type= int(sys.argv[2])
response_type = int(sys.argv[3])
value = sys.argv[1]
client.sendto(create_message(query_type,response_type,value), serverAddressPort)


data=""
total_packet_recieved = 0
while True:
	try:
		msgFromServer = client.recvfrom(1000)
	except Exception:
		print("Server Down!!")
		sys.exit()
	output = universal_decoder(msgFromServer[0],response_format)

	#check whether the reponse is not bogus
	if(message_id==output[0]):
		data = data+output[3]
		total_packet_recieved=total_packet_recieved+1
	else:
		print("recived a bogus response rejecting")
		continue

	#all packet recived
	if(output[2]==0):
		
		#if total packets field in the packet is zero 
		if(output[1]==0):
			print("No records found !!")
			break
		#if total packets recieved are not same as described in the packet
		if(total_packet_recieved!=output[1]):
			print(output[1],total_packet_recieved)
			print("One of the packet got lost")
			print("resending the query again")
			query_tries = query_tries+1
			if(query_tries>MAX_QUERY_TRY):
				print("query limit reached")
				break
			data = ""
			total_packet_recieved=0
			client.sendto(create_message(query_type,response_type,value), serverAddressPort)
			continue


		output = make_sense(data,response_type)
		final_output =print_data(output)

		print("Total responses found : {}\n".format(len(final_output)))
		for u in final_output:
			print(u)
		# print(data)


		break
		
