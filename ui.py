from tkinter import *
import os
import subprocess
from subprocess import PIPE,STDOUT
import pyperclip
from lru_cache import LRUCache

ARR = ['Name', 'Email', 'Phone No.', 'Department','Registration No.','Blood Group']
BLOODARR = ["A+","B+","A-","B-","AB-","AB+","O+","O-"]
DEPARTMENTARR = ["Chemical Engineering",
					"Civil Engineering",
					"Computer Science Engineering",
					"Electrical Engineering",
					"Mechanial Engineering"]



blood_type=0
department_for_search=0
search_selection = 0
#indicator to check wheter option menu is there isntead of entry
option_menu = None
variable1= None
row0=None
entry=None

# def set_blood(value):
# 	global blood_type
# 	blood_type = value
# 	# print(blood_type)

# def set_department(value):
# 	global department_for_search
# 	department_for_search = value




def clear_Entries(en):
	# checking on variable of dropdown1
	if(variable.get()==ARR[3]):
		# setting variable of dropdown2
		variable1.set(DEPARTMENTARR[2])
		# print("here1")

	elif(variable.get()==ARR[5]):
		variable1.set(BLOODARR[1])
		# print("here2")
	else:
		print("this is variable",variable)
		entry.delete(0,END)
		entry.insert(0,"")
	for i in lng.vars:
		i.set(0)
	lng.vars[0].set(1)

def setall():
	for i in lng.vars:
		i.set(1)

def allstates(): 
	Query_For=list(lng.state())
	#print(Query_For)
	return Query_For

# def fetch(en,variable):
# 	Search_by={}
# 	Search_by[variable.get()]=entry.get()
# 	return Search_by

def binToDec(arr):
	answer=0
	for i in range(0,len(arr)):
		answer+=arr[i]*(2**i)
	return answer

# def send_query(en,variable,T):

# 	if(search_selection==5):

# 		value = str(blood_type)
# 		query_type=str(5)
# 		search_flags = allstates()
# 		response_type = str(binToDec(search_flags))
# 		T.delete('1.0',END)


# 	elif(search_selection ==3 ):
# 		value = str(department_for_search)
# 		query_type = "3"
# 		search_flags = allstates()
# 		response_type = str(binToDec(search_flags))
# 		T.delete('1.0',END)

# 	else:
# 		# print(type(entry),entry)
# 		search_flags = allstates()
# 		search_by= fetch(entry,variable)
# 		print("search_flags\n",search_flags)
# 		print("search_by\n",search_by)
# 		print("\n")
# 		T.delete('1.0',END)
		
# 		value=str(entry.get())
# 		query_type=str(ARR.index(variable.get()))
# 		response_type=str(binToDec(search_flags))

# 	#if running on windows machine
# 	if os.name=="nt":
# 		query_string="python client.py \""+value+"\" "+query_type+" "+response_type    
# 	#else
# 	else :
# 		query_string="python3 client.py \""+value+"\" "+query_type+" "+response_type

# 	print(query_string)

# 	# response_string = os.system("python3 client.py nav 0 63")
# 		# response_string = os.system(query_string + "> output_file.txt")
# 	command = query_string
# 	process = subprocess.run(command, stdout=PIPE, stderr=PIPE,shell=True)
# 	response_string = process.stdout.decode("utf-8")
# 	# response_string="would be output"
# 	T.insert(END,response_string)
	
##########-----------------------------------
def send_query(en,variable,T):

	if(search_selection==5):

		value = str(BLOODARR.index(variable1.get()))
		# query_type=str(5)
		# search_flags = allstates()
		# response_type = str(binToDec(search_flags))
		# T.delete('1.0',END)


	elif(search_selection ==3 ):
		value = str(DEPARTMENTARR.index(variable1.get()))
		# query_type = "3"
		# search_flags = allstates()
		# response_type = str(binToDec(search_flags))
		# T.delete('1.0',END)

	else:
		# print(type(entry),entry)
		value=str(entry.get())

		# search_by= fetch(entry,variable)

	search_flags = allstates()
	print("search_flags\n",search_flags)
	print("search_by\n",variable.get(),":",value)
	T.delete('1.0',END)
		
	query_type=str(ARR.index(variable.get()))
	response_type=str(binToDec(search_flags))

	#search if the response is in cache first
	cache_key = (value,query_type,response_type)
	response_string = cache.get(cache_key)
	if response_string != -1:
		T.insert(END,response_string)
		return

	#if running on windows machine
	if os.name=="nt":
		query_string="python client.py \""+value+"\" "+query_type+" "+response_type    
	#else
	else :
		query_string="python3 client.py \""+value+"\" "+query_type+" "+response_type

	print("queryString:",query_string,"\n")
	# response_string = os.system("python3 client.py nav 0 63")
		# response_string = os.system(query_string + "> output_file.txt")
	command = query_string
	process = subprocess.run(command, stdout=PIPE, stderr=STDOUT,shell=True)
	response_string = process.stdout.decode("utf-8")
	#print(response_string,"uuuiiii")
	# response_string="would be output"

	#store the response in cache if it wasn't previously available
	cache.put(cache_key,response_string)
	T.insert(END,response_string)
####------------------------------


class Checkbar(Frame):
	 def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
			Frame.__init__(self, parent)
			self.vars = []
			for pick in picks:
				 var = IntVar()
				 chk = Checkbutton(self, text=pick, variable=var)
				 chk.pack(side=side, anchor=anchor, expand=YES)
				 self.vars.append(var)
	 def state(self):
			return map((lambda var: var.get()), self.vars)





def draw_for(v):
	global entry,search_selection,option_menu,variable1
	# print(entry,type(entry))
	entry.destroy()
	
	
	if(option_menu!=None):
		option_menu.destroy()


	if(v=="Blood Group"):
		# entry.destroy()
		# {"a+":0,"b+":1,"a-":2,"b-":3,"ab-":4,"ab+":5,"o+":6,"o-":7}
		OPTIONS = BLOODARR
		variable1=StringVar(root)
		variable1.set(OPTIONS[1]) # default value
		option_menu = OptionMenu(row0, variable1, *OPTIONS)
		option_menu.pack(side = RIGHT, expand = YES, padx=5,fill = X) 
		search_selection=5
		# print("volla volla")


	elif(v=="Department"):
		OPTIONS = DEPARTMENTARR		
		variable1=StringVar(root)
		variable1.set(OPTIONS[2]) # default value
		option_menu = OptionMenu(row0, variable1, *OPTIONS)
		option_menu.pack(side = RIGHT, expand = YES, padx=5,fill = X) 
		search_selection=3

		# print("volla volla")



	else:
		variable1=None
		entry = Entry(row0)
		entry.insert(0,"")
		# w.pack(side=LEFT, ipadx = 5)
		entry.pack(side = RIGHT, expand = YES, padx=5,fill = X) 
		row0.pack(side=TOP,fill = X, padx = 5 , pady = 5)
		search_selection =1
		

	
		
		# print(entry,type(entry))
		# print(entry.get())

	# print("blood_type", blood_type)


##Initialize and load cache before starting
cache = LRUCache(capacity=20,expiry_time=3600) #time is in seconds
cache.load_from_file('default_cache') 

##--------------- Start----------------------
root = Tk()
root.geometry('600x700')

# ----------Heading 1
row1 = Frame(root)
a=  Label(row1,text="Search BY:").pack(side=LEFT,padx=3)
row1.pack(side=TOP,fill = X, padx = 5, pady = 5)



row0 = Frame(root)
# 1st dropdown
OPTIONS = ARR
variable = StringVar(root)
variable.set(OPTIONS[0]) # default value
w = OptionMenu(row0, variable, *OPTIONS,command =(lambda v=variable: draw_for(v)))
# Entry field
entry = Entry(row0)
entry.insert(0,"")
# first setting label on left and then arranging entry on right(full remaining space)
w.pack(side=LEFT, ipadx = 5)
entry.pack(side = RIGHT, expand = YES, padx=5,fill = X) 
row0.pack(side=TOP,fill = X, padx = 5 , pady = 5)

# ------------Heading 2
row1 = Frame(root)
a=  Label(row1,text="Query For:").pack(side=LEFT,padx=3)
row1.pack(side=TOP,fill = X, padx = 5, pady = 5)

# ----------Checkboxes
lng = Checkbar(root, ARR)

lng.pack(side=TOP,  fill=X,pady=5,padx=5)

lng.config(relief=GROOVE, bd=2)
lng.vars[0].set(1) # setting Name to be default ticked

# ------------Clear Buttton
row2 = Frame(root)
row2.pack(side=TOP,fill = X, padx = 5 , pady = 5)
Button(row2, text='Clear', command=(lambda e = entry: clear_Entries(e))).pack(side=RIGHT,padx=1)

# ------------Text Area
row3 = Frame(root)
row3.pack(side=TOP,fill = X, padx = 5 , pady = 5)
T = Text(row3,wrap=WORD)

# -------------Scrollbar
S=Scrollbar(row3)

# first fit the scrollbar on right and then fill the text area on rest of the space
S.pack(side=RIGHT,fill=Y)
T.pack(fill=X,padx=5,ipadx=5,ipady=5)

# attaching scrollbar and text area to each other
S.config(command=T.yview)
T.config(yscrollcommand=S.set)

# default text in text area
T.insert(END," To search: type the values and set required parameters\n and then press enter or click LookUp ")

# Select All button 
Button(row2, text='Select All', command=(lambda : setall())).pack(side=RIGHT,padx=1)

# On pressing enter
root.bind('<Return>', (lambda event, e = entry,v=variable,T=T: send_query(e,v,T)))
# On pressing search button
Button(row2, text='LookUp', command=(lambda e = entry,v=variable,T=T: send_query(e,v,T))).pack(side=LEFT,padx=1)

# Button(row2, text='Quit', command=root.quit).pack(side=LEFT,padx=1)



	
# import only asksaveasfile from filedialog 
# which is used to save file in any extension 
from tkinter.filedialog import asksaveasfile 
	

	
# function to call when user press 
# the save button, a filedialog will 
# open and ask to save file 
def save(Tarea): 
		files = [('All Files', '*.*'),  
						 ('Python Files', '*.py'), 
						 ('Text Document', '*.txt')] 
		file = asksaveasfile(filetypes = files, defaultextension = files)
		file.write(Tarea.get('1.0',END))
		file.close()
def copyText(Tarea):
	string = Tarea.get('1.0',END)
	# sudo apt-get install xclip xsel
	# this is necessary for ubuntu machines-- to use piperclip
	pyperclip.copy(string)
	print("should be copied")
	print("thsi is string:", string)


# Save as a File Button
row4 = Frame(root)
btn = Button(row4, text = 'Save as a File', command = (lambda Tarea=T: save(Tarea))) .pack(side=RIGHT,padx=3)

btn1 = Button(row4,text="Copy To Clipboard",command=(lambda Tarea=T: copyText(Tarea))).pack(side=RIGHT,padx=1)
btn0112131 = Button(row4,text="Clear Cache",command=cache.clear_cache).pack(side=LEFT,padx=1)

row4.pack(side=TOP,fill = X, padx = 5 , pady = 5)

mainloop()

#At last store the final cache state in file
cache.store_to_file('default_cache')