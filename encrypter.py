def encrypt(key, stri):
	output = ""

	for k in stri:
		output = chr((ord(k)+key)%128)+output
	return output

def decrypt(key, stri):
	output = ""

	for k in stri:
		output = chr((ord(k)-key)%128)+output
	return output



def key_calculator(message_id):
	return (message_id%91+18)