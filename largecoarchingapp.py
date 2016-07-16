import sys
import time
import os
import sqlite3
from itertools import chain

#Connection and Cursor
conn = sqlite3.connect('largecoaching.db')
c = conn.cursor()
Marks_HistoryList=[]
testid=0

#Admin starts a new test
def New_Test():
	global testid
	testid+=1

#Creates table where everything is stored
def create_table():
	c.execute("CREATE TABLE IF NOT EXISTS largecoaching(Student TEXT,Student_Password TEXT, Batch TEXT, Teacher TEXT, Teacher_Password TEXT, Marks_History TEXT, Total_Marks REAL, Rank REAL)")		

#Generating a list of marks form Marks_History
def marks_list_generate(s_name):
	c.execute('SELECT Marks_History FROM largecoaching WHERE Student = ?',(s_name))
	data=c.fetchall()
	Marks_HistoryList=list(chain.from_iterable(data))

	if (Marks_HistoryList[0]==None):
		del Marks_HistoryList[0]
	return Marks_HistoryList

#Generating the Total_Marks Column
def Total_Marks_generate():
	c.execute('SELECT Marks_History FROM largecoaching')
	data = c.fetchall()   

	for i in range(1,len(data)+1):
		c.execute('SELECT Marks_History FROM largecoaching WHERE rowid = ?',str(i))
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
		c.execute('UPDATE largecoaching SET Total_Marks = ? WHERE rowid = ?',(total_marks,str(i)))   
		conn.commit()

#Enrollment of a new student into the institute 
def add_student():
	s_name=input("Enter Student's Name : ")
	s_pass=input("Enter Student's Password : ")
	c.execute("INSERT INTO largecoaching(Student, Student_Password) VALUES (?,?)",(s_name,s_pass))
	conn.commit()

#Updating Marks_History for a student
def update_marksheet():
	s_name=input("Enter Student's Name : ")
	c.execute('SELECT Student FROM largecoaching')
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

	c.execute('UPDATE largecoaching SET Marks_History = ? WHERE Student = ?',(s_marks_history, s_name))
	conn.commit()
	Total_Marks_generate()
	rank_generate()
	batch_generate()

#Generating the Rank Column on the basis of overall test marks
def rank_generate():
	c.execute('SELECT Total_Marks FROM largecoaching ORDER BY Total_Marks DESC')
	data = c.fetchall()

	for i in range(1,len(data)+1):
		c.execute('UPDATE largecoaching SET Rank = ? WHERE Total_Marks = ?',(i,str(data[i-1][0])))   
		conn.commit()

#Generating the Batch & Teacher Column. Batches of 3
def batch_generate():
	c.execute('SELECT Rank FROM largecoaching ORDER BY Total_Marks DESC')
	data = c.fetchall()
	batch_count=0

	for i in range(1,len(data)+1):

		if(i%3==1):
			batch_count+=1
			batch_letter=chr(ord('A')+batch_count-1)
			teacher_name = input("Enter Teacher's Name for Batch: "+batch_letter)
			c.execute('UPDATE largecoaching SET Batch = ?, Teacher = ? WHERE Rank = ?',(batch_letter,teacher_name,i))   
			conn.commit()
		else:
			c.execute('UPDATE largecoaching SET Batch = ? WHERE Rank = ?',(batch_letter,teacher_name,i))  
			conn.commit()

def reminder_check(t_name):
	remcheck = 0
	c.execute('SELECT Marks_History FROM largecoaching WHERE Teacher = ?',(t_name))
	data=c.fetchall()
	Marks_HistoryList=list(chain.from_iterable(data))

	for i in range(0,len(Marks_HistoryList)):

		if (Marks_HistoryList[0]==None):
			del Marks_HistoryList[0]

		try:
			latest_marks=Marks_HistoryList[testid]
		except ValueError:
			remcheck=1
		else:
			break

	return remcheck

def reminder():
	if(remcheck==1):
		rem='REMINDER : UPDATE MARKSHEET'
		print('\n\n')

		for i in range(5)
		    sys.stdout.write('\r'+rem)
		    sys.stdout.flush()
		    time.sleep(0.5)
		    sys.stdout.write('\r'+' '*len(rem))
		    sys.stdout.flush()
		    time.sleep(0.5)

		input("Press Enter to continue")




def teacherbatch_view(t_name):
	c.execute('SELECT Student, Rank FROM largecoaching WHERE Teacher = ?',t_name)
	data = c.fetchall()

	for row in data:
		print(row)

	input("\n\nPRESS ENTER TO CONTINUE :")

#Teacher uploads new marksheet
def teacher_upload_marks(t_name):
	c.execute('SELECT Student FROM largecoaching WHERE Teacher = ?',t_name)
	data = c.fetchall()
	NameList=list(chain.from_iterable(data))

	while True:

		if (NameList==[]):	
			print("Please add a student first")
			quit()
		else:
			break

	for i in range(0,len(NameList)):

		s_marks=input("Enter latest marks for Student : "+NameList[i])	
		Marks_HistoryList=marks_list_generate(s_name)
		Marks_HistoryList.append(s_marks)

		if(len(Marks_HistoryList)>1):
			s_marks_history = ','.join(Marks_HistoryList)
		else:
			s_marks_history = Marks_HistoryList[0]

		c.execute('UPDATE largecoaching SET Marks_History = ? WHERE Student = ?',(s_marks_history, s_name))
		conn.commit()

	Total_Marks_generate()

#Viewing the table
def read_from_db():
	c.execute('SELECT * FROM largecoaching')
	data = c.fetchall()

	for row in data:
		print(row)

	input("\n\nPRESS ENTER TO CONTINUE :")

#Viewing the student's marks in the latest test
def latest_marks(s_name):
	c.execute('SELECT Marks_History FROM largecoaching WHERE Student = ?',s_name)
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
	c.execute('SELECT Batch FROM largecoaching WHERE Student = ?',s_name)
	data = c.fetchall()
	listconv1=list(chain.from_iterable(data)) 

	for row in listconv1:
		print(row)

	input("\n\nPRESS ENTER TO CONTINUE :")

#Viewing the student's performance
def studentperf_view(s_name):
	c.execute('SELECT Marks_History FROM largecoaching WHERE Student = ?',s_name)
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
def s_usrnamecheck():
	os.system('clear')
	s_name=input("Enter Your Name : ")
	c.execute('SELECT Student FROM largecoaching')
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
def s_passcheck(s_name):
	os.system('clear')
	s_pass=input("Enter Your Password : ")
	c.execute('SELECT Student_Password FROM largecoaching WHERE Student = ?',s_name)
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

#Check for the Teacher's username
def t_usrnamecheck():
	os.system('clear')
	t_name=input("Enter Your Name : ")
	c.execute('SELECT Teacher FROM largecoaching')
	data = c.fetchall()
	NameList=list(chain.from_iterable(data))

	while True:

		if (NameList==[]):	
			print("Please enroll as a teacher ")
			quit()
		elif t_name not in NameList:
			t_name=input("You dont seem to be enrolled. Try again : ")
		else:
			break

	return t_name

#Check for the Teacher's password
def t_passcheck(t_name):
	os.system('clear')
	t_pass=input("Enter Your Password : ")
	c.execute('SELECT Teacher_Password FROM largecoaching WHERE Teacher = ?',t_name)
	data = c.fetchall()
	PassList=list(chain.from_iterable(data))

	while True:

		if (PassList==[]):	
			print("Please enroll as a teacher ")
			quit()
		elif t_pass not in PassList:
			t_pass=input("Password is incorrect!. Try again : ")
		else:
			break

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

#TEACHER Interface
def teacherint():
	os.system('clear')
	remcheck=reminder_check(t_name)
	reminder()

	while True:
		
		try:
			func=int(input("Choose Any Number : \n\n(1) View Students\n(2) Upload Marks\n(3) Quit\n\n"))

		except ValueError:
			os.system('clear')
			func=int(input("Choose Any Number : \n\n(1) View Students\n(2) Upload Marks\n(3) Quit\n\n"))

		else:
			break

	os.system('clear')

	if func == 1:
		teacherbatch_view(t_name)
	elif func == 2:
		teacher_upload_marks(t_name)
	elif func==3:
		quit()
	else:
		print("Your option doesn't make sense to me")

	os.system('clear')

#MAIN
create_table()
os.system('clear')

print("COACHING APP\n")

while True:
		
		try:
			inp=int(input("Choose a Number : \n\n(1) ADMINISTRATOR \n(2) STUDENT\n(3) TEACHER\n(4) Quit \n\n"))

		except ValueError:
			os.system('clear')
			inp=int(input("Choose a Valid Number : \n\n(1) ADMINISTRATOR \n(2) STUDENT\n(3) TEACHER\n(4) Quit \n\n"))

		else:
			break

if inp==1:

	while True:
		adminint()

elif inp==2:
	s_name=s_usrnamecheck()
	s_passcheck(s_name)

	while True:
		studentint()

elif inp==3:
	t_name=t_usrnamecheck()
	t_passcheck(t_name)

	while True:
		teacherint()

elif inp==4:
	os.system('clear')
	quit()
else:
	os.system('clear')
	inp=int(input("Choose a Valid Number : \n\n(1) ADMINISTRATOR \n(2) STUDENT\n(3) TEACHER\n(4) Quit \n\n"))

#CODE ENDS :D --------X---------