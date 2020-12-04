NAME = 1
EMAIL = 2
PHONE = 4
DEPARTMENT = 8
REG_NO = 16
BLOOD_GROUP = 32

NAME_SEARCH = 0
EMAIL_SEARCH = 1
PHONE_SEARCH = 2
DEPARTMENT_SEARCH = 3
REG_NO_SEARCH = 4
BLOOD_GROUP_SEARCH = 5

mapping = {NAME_SEARCH:"name",EMAIL_SEARCH:"email",PHONE_SEARCH:"phonenumber",DEPARTMENT_SEARCH:"DEPARTMENT",REG_NO_SEARCH:"REG_NO",BLOOD_GROUP_SEARCH:"BLOOD_GROUP"}

import encrypter as enc
import time
import threading
import database_selector as db
INT = "i"
STR = "s"
NETWORK_DELAY = 0.01

# definiton = [(4,INT),(1,INT),(1,INT),(0,STR)]

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

	# print(outputs)
	return outputs


import socket

 

localIP     = "localhost"

localPort   = 20001

BUFFER_SIZE  = 200

 



# Create a datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

 
UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)
# UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT , 1)

# Bind to address and ip



UDPServerSocket.bind((localIP, localPort))



def handle_response(message,address):
	connector = db.manager("test.db")

	#4:id,1:query_type,1:response_type,0:data
	definiton = [(4,INT),(1,INT),(1,INT),(0,STR)]
	decoded_message = universal_decoder(message,definiton)

	print(decoded_message)
	message_id = decoded_message[0]
	query_type = mapping[decoded_message[1]]
	response_type = decoded_message[2]
	value = decoded_message[3]

	#reciving data from the database in the from of string chunks seprated by linefeed
	data=connector.format_data(connector.search_parameter(value,query_type),response_type)


	list_of_packets = create_response(message_id,data)

	send_data(list_of_packets,address)
	#closing connetion with database
	connector.conn.close()


#arguments list of packets,adress
def send_data(lis,addr):

	sending_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)	
	for packet in lis:
		time.sleep(NETWORK_DELAY)
		sending_socket.sendto(packet, addr)

	


#gist : takes message id and data and return packets list by forming arguable headers
# arguments message_id(int),data(string)
def create_response(message_id,data):

	# subtracting header bytes fromt the buffer size
	bufferSize  = BUFFER_SIZE -4 -1 -1 


	#calculating remaining total number of packets - 1
	fragment_remiaing = len(data)//bufferSize

	if(len(data)%bufferSize==0 and len(data)!=0):
		fragment_remiaing = fragment_remiaing-1


	neighbours = fragment_remiaing + 1
	id_bytes = message_id.to_bytes(4, byteorder='big')
	fragment_remiaing_bytes = fragment_remiaing.to_bytes(1, byteorder='big')
	total_packets_bytes = neighbours.to_bytes(1,byteorder="big")

	calculated_key = enc.key_calculator(message_id)
	data = enc.encrypt(calculated_key,data)

	data_bytes = data.encode('utf-8')

	bytes_to_send = id_bytes


	lis=[]
	for k in range(0,len(data),bufferSize):

		end = min(len(data),(k+bufferSize))
		fragment_remiaing_bytes = fragment_remiaing.to_bytes(1, byteorder='big')
		lis.append((bytes_to_send+total_packets_bytes+fragment_remiaing_bytes+ data_bytes[k:end]))
		fragment_remiaing = fragment_remiaing-1

	if(len(lis)==0):
		#if no record found in the database
		lis.append(bytes_to_send+(int(0)).to_bytes(1,byteorder="big")+fragment_remiaing_bytes+"No records found !!".encode("utf-8"))
					
	# returning list of packets (with headers and data)
	return lis





print("UDP server up and listening")

 

# Listen for incoming datagrams

while(True):
	


	#to reject the packet having size greater than BUFFER_SIZE
	try:
		bytesAddressPair = UDPServerSocket.recvfrom(BUFFER_SIZE)
	except Exception:
		continue
	message = bytesAddressPair[0]
	address = bytesAddressPair[1]





	# clientMsg = "Message from Client:{}".format(message)
	clientIP  = "Client IP Address:{}".format(address)
	# # decode_message(message)

	print(clientIP)

	if(threading.active_count()<10):
		threading.Thread(target=handle_response,name="sending data thread", args=(message,address,)).start()
	