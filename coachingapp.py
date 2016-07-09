import sys
import os
import sqlite3
from itertools import chain

#Connection and Cursor
conn = sqlite3.connect('coaching.db')
c = conn.cursor()
Marks_HistoryList=[]

#Creates table where everything is stored
def create_table():
	c.execute("CREATE TABLE IF NOT EXISTS coaching(Name TEXT,Password TEXT, Batch TEXT, Marks_History TEXT, Total_Marks REAL, Rank REAL)")		

#Generating a list of marks form Marks_History
def marks_list_generate(s_name):
	c.execute('SELECT Marks_History FROM coaching WHERE Name = ?',(s_name))
	data=c.fetchall()
	Marks_HistoryList=list(chain.from_iterable(data))

	if (Marks_HistoryList[0]==None):
		del Marks_HistoryList[0]
	return Marks_HistoryList

#Generating the Total_Marks Column
def Total_Marks_generate():
	c.execute('SELECT Marks_History FROM coaching')
	data = c.fetchall()   

	for i in range(1,len(data)+1):
		c.execute('SELECT Marks_History FROM coaching WHERE rowid = ?',str(i))
		data=c.fetchall()
		listconv1=list(chain.from_iterable(data)) 
		strconv=str(listconv1[0])
		
		if(',' in strconv):
			Marks_HistoryList=strconv.split(',')
		else:
			Marks_HistoryList=[strconv]

		if (Marks_HistoryList[0]=='None'):
			del Marks_HistoryList[0]

		Marks_HistoryList = map(int, Marks_HistoryList)
		total_marks=sum(Marks_HistoryList)
		c.execute('UPDATE coaching SET Total_Marks = ? WHERE rowid = ?',(total_marks,str(i)))   
		conn.commit()

#Enrollment of a new student into the institute 
def add_student():
	s_name=input("Enter Student's Name : ")
	s_pass=input("Enter Student's Password : ")
	c.execute("INSERT INTO coaching(Name, Password) VALUES (?,?)",(s_name,s_pass))
	conn.commit()

#Updating Marks_History for a student
def update_marksheet():
	s_name=input("Enter Student's Name : ")
	c.execute('SELECT Name FROM coaching')
	data = c.fetchall()
	NameList=list(chain.from_iterable(data))

	while True:

		if (NameList==[]):	
			print("Please add a student first")
			quit()
		elif s_name not in NameList:
			s_name=input("This student is not enrolled. Try again : ")
		else:
			break

	s_marks=input("Enter Student's Latest Marks : ")
	Marks_HistoryList=marks_list_generate(s_name)
	Marks_HistoryList.append(s_marks)

	if(len(Marks_HistoryList)>1):
		s_marks_history = ','.join(Marks_HistoryList)
	else:
		s_marks_history = Marks_HistoryList[0]

	c.execute('UPDATE coaching SET Marks_History = ? WHERE Name = ?',(s_marks_history, s_name))
	conn.commit()
	Total_Marks_generate()
	rank_generate()
	batch_generate()

#Generating the Rank Column on the basis of overall test marks
def rank_generate():
	c.execute('SELECT Total_Marks FROM coaching ORDER BY Total_Marks DESC')
	data = c.fetchall()

	for i in range(1,len(data)+1):
		c.execute('UPDATE coaching SET Rank = ? WHERE Total_Marks = ?',(i,str(data[i-1][0])))   
		conn.commit()

#Generating the Bathc Column. Batches of 3
def batch_generate():
	c.execute('SELECT Rank FROM coaching ORDER BY Total_Marks DESC')
	data = c.fetchall()
	batch_count=0

	for i in range(1,len(data)+1):

		if(i%3==1):
			batch_count+=1
			batch_letter=chr(ord('A')+batch_count-1)
			c.execute('UPDATE coaching SET Batch = ? WHERE Rank = ?',(batch_letter,i))   
			conn.commit()
		else:
			c.execute('UPDATE coaching SET Batch = ? WHERE Rank = ?',(batch_letter,i))  
			conn.commit()

#Viewing the table
def read_from_db():
	c.execute('SELECT * FROM coaching')
	data = c.fetchall()

	for row in data:
		print(row)

	input("\n\nPRESS ENTER TO CONTINUE :")

#Viewing the student's marks in the latest test
def latest_marks(s_name):
	c.execute('SELECT Marks_History FROM coaching WHERE Name = ?',s_name)
	data = c.fetchall()      
	listconv1=list(chain.from_iterable(data)) 
	strconv=str(listconv1[0])
	
	if(',' in strconv):
		Marks_HistoryList=strconv.split(',')
	else:
		Marks_HistoryList=[strconv]

	if (Marks_HistoryList[0]=='None'):
		del Marks_HistoryList[0]

	print("Marks : "+ Marks_HistoryList[-1])

	input("\n\nPRESS ENTER TO CONTINUE :")

#Viewing the student's batch
def studentbatch_view(s_name):
	c.execute('SELECT Batch FROM coaching WHERE Name = ?',s_name)
	data = c.fetchall()
	listconv1=list(chain.from_iterable(data)) 

	for row in listconv1:
		print(row)

	input("\n\nPRESS ENTER TO CONTINUE :")

#Viewing the student's performance
def studentperf_view(s_name):
	c.execute('SELECT Marks_History FROM coaching WHERE Name = ?',s_name)
	data = c.fetchall()      
	listconv1=list(chain.from_iterable(data)) 
	strconv=str(listconv1[0])
	
	if(',' in strconv):
		Marks_HistoryList=strconv.split(',')
	else:
		Marks_HistoryList=[strconv]

	if (Marks_HistoryList[0]=='None'):
		del Marks_HistoryList[0]

	for row in listconv1:
		print(row)

	input("\n\nPRESS ENTER TO CONTINUE :")

#Check for the student's username
def usrnamecheck():
	os.system('clear')
	s_name=input("Enter Your Name : ")
	c.execute('SELECT Name FROM coaching')
	data = c.fetchall()
	NameList=list(chain.from_iterable(data))

	while True:

		if (NameList==[]):	
			print("Please enroll as a student ")
			quit()
		elif s_name not in NameList:
			s_name=input("You dont seem to be enrolled. Try again : ")
		else:
			break

	return s_name

#Check for the student's password
def passcheck(s_name):
	os.system('clear')
	s_pass=input("Enter Your Password : ")
	c.execute('SELECT Password FROM coaching WHERE Name = ?',s_name)
	data = c.fetchall()
	PassList=list(chain.from_iterable(data))

	while True:

		if (PassList==[]):	
			print("Please enroll as a student ")
			quit()
		elif s_pass not in PassList:
			s_pass=input("Password is incorrect!. Try again : ")
		else:
			break

	return s_pass

#ADMINISTRATOR Interface
def adminint():
	os.system('clear')

	while True:

		try:
			func=int(input("Choose Any Number : \n\n(1) Update Marksheet\n(2) View Database\n(3) Add Student\n(4) Quit\n\n"))

		except ValueError:
			os.system('clear')
			func=int(input("Choose A Proper Number : \n\n(1) Update Marksheet\n(2) View Database\n(3) Add Student\n(4) Quit\n\n"))

		else:
			break

	os.system('clear')

	if func == 1:
		update_marksheet()
	elif func == 2:
		read_from_db()
	elif func == 3:
		add_student()
	elif func==4:
		quit()
	else:
		print("Your option doesn't make sense to me")

	os.system('clear')

#STUDENT Interface
def studentint():
	os.system('clear')

	while True:
		
		try:
			func=int(input("Choose Any Number : \n\n(1) View Latest Marks\n(2) View Batch\n(3) View Performance History\n(4) Quit\n\n"))

		except ValueError:
			os.system('clear')
			func=int(input("Choose Any Number : \n\n(1) View Latest Marks\n(2) View Batch\n(3) View Performance History\n(4) Quit\n\n"))

		else:
			break

	os.system('clear')

	if func == 1:
		latest_marks(s_name)
	elif func == 2:
		studentbatch_view(s_name)
	elif func==3:
		studentperf_view(s_name)
	elif func==4:
		quit()
	else:
		print("Your option doesn't make sense to me")

	os.system('clear')

#MAIN
create_table()
os.system('clear')

print("COACHING APP\n")

inp=int(input("Choose a Number : \n\n(1) ADMINISTRATOR \n(2) STUDENT\n(3) Quit \n\n"))

if inp==1:

	while True:
		adminint()

elif inp==2:
	s_name=usrnamecheck()
	s_pass=passcheck(s_name)

	while True:
		studentint()

elif inp==3:
	os.system('clear')
	quit()
else:
	os.system('clear')
	inp=int(input("Choose a Number : \n\n(1) ADMINISTRATOR \n(2) STUDENT\n(3) Quit \n\n"))

#CODE ENDS :D --------X---------