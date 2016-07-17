import sys
import time
import os
import sqlite3
from itertools import chain

#Connection and Cursor
conn = sqlite3.connect('coaching.db')
c = conn.cursor()
Marks_HistoryList=[]
TeacherList=[]
testid=0

#Creates a table with student data
def create_coachingtable():
	c.execute("CREATE TABLE IF NOT EXISTS coaching(Student TEXT,Student_Password TEXT, Batch TEXT, Marks_History TEXT, Total_Marks REAL, Rank REAL)")	

#Creates a table with teacher data
def create_teachertable():
	c.execute("CREATE TABLE IF NOT EXISTS teacher(Teacher TEXT, Teacher_Password TEXT, Batch TEXT, Reminder TEXT)")	










#ADMINISTRATOR Interface
def adminint():
	os.system('clear')

	while True:

		try:
			func=int(input("Choose Any Number : \n\n(1) Remind Teachers\n(2) Remap Batches\n(3) New Test - Set Reminder\n(4) Add Teacher - Batch\n(5) Add Student\n(0) Quit\n\n"))

		except ValueError:
			os.system('clear')
			func=int(input("Choose A Proper Number : \n\n(1) Remind Teachers\n(2) Remap Batches\n(3) New Test - Set Reminder\n(4) Add Teacher - Batch\n(5) Add Student\n(0) Quit\n\n"))

		else:
			break

	os.system('clear')

	if func == 1:
		remind_teachers()
	elif func == 2:
		remap_batches()
	elif func == 3:
		new_test()
	elif func==4:
		add_teacher_batch()
	elif func==5:
		add_student()
	elif func==0:
		quit()
	else:
		print("Your option doesn't make sense to me")

	os.system('clear')

def remind_teachers():
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

		try:
			latest_marks=Marks_HistoryList[testid-1]

		except ValueError:
			os.system('clear')
			c.execute('SELECT Batch FROM coaching WHERE rowid = ?',str(i))
			data=c.fetchall()
			listconv1=list(chain.from_iterable(data)) 
			t_batch=str(listconv1[0])
			c.execute("UPDATE teacher SET Reminder = ? WHERE Batch = ?",('1',t_batch))
			conn.commit()



# def remap_batches():
	

def new_test():
	global testid
	testid+=1
	remind_teachers()

#New teacher in the institute 
def add_teacher_batch():
	t_name=input("Enter Teacher's Name : ")
	t_pass=input("Enter Teacher's Password : ")
	t_batch=input("Enter Teacher's Batch : ")
	c.execute("INSERT INTO teacher(Teacher, Teacher_Password, Batch ) VALUES (?,?,?)",(t_name,t_pass,t_batch))
	conn.commit()

#Enrollment of a new student into the institute 
def add_student():
	s_name=input("Enter Student's Name : ")
	s_pass=input("Enter Student's Password : ")
	c.execute("INSERT INTO coaching(Student, Student_Password) VALUES (?,?)",(s_name,s_pass))
	conn.commit()


















#STUDENT Interface
def studentint():
	os.system('clear')

	while True:
		
		try:
			func=int(input("Choose Any Number : \n\n(1) View Latest Marks\n(2) View Batch\n(3) View Performance History\n(0) Quit\n\n"))

		except ValueError:
			os.system('clear')
			func=int(input("Choose Any Number : \n\n(1) View Latest Marks\n(2) View Batch\n(3) View Performance History\n(0) Quit\n\n"))

		else:
			break

	os.system('clear')

	if func == 1:
		latest_marks(s_name)
	elif func == 2:
		studentbatch_view(s_name)
	elif func==3:
		studentperf_view(s_name)
	elif func==0:
		quit()
	else:
		print("Your option doesn't make sense to me")

	os.system('clear')

#Check for the student's username
def s_usrnamecheck():
	os.system('clear')
	s_name=input("Enter Your Name : ")
	c.execute('SELECT Student FROM coaching')
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
	c.execute('SELECT Student_Password FROM coaching WHERE Student = ?',s_name)
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

#Viewing the student's marks in the latest test
def latest_marks(s_name):
	c.execute('SELECT Marks_History FROM coaching WHERE Student = ?',s_name)
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
	c.execute('SELECT Batch FROM coaching WHERE Student = ?',s_name)
	data = c.fetchall()
	listconv1=list(chain.from_iterable(data)) 

	for row in listconv1:
		print(row)

	input("\n\nPRESS ENTER TO CONTINUE :")

#Viewing the student's performance
def studentperf_view(s_name):
	c.execute('SELECT Marks_History FROM coaching WHERE Student = ?',s_name)
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





















#TEACHER Interface
def teacherint():
	os.system('clear')
	remcheck()

	while True:
		
		try:
			func=int(input("Choose Any Number : \n\n(1) View Students\n(2) Upload Marks\n(0) Quit\n\n"))

		except ValueError:
			os.system('clear')
			func=int(input("Choose Any Number : \n\n(1) View Students\n(2) Upload Marks\n(0) Quit\n\n"))

		else:
			break

	os.system('clear')

	if func == 1:
		teacherbatch_view(t_name)
	elif func == 2:
		teacher_upload_marks(t_name)
	elif func==0:
		quit()
	else:
		print("Your option doesn't make sense to me")

	os.system('clear')

#Check for the Teacher's username
def t_usrnamecheck():
	os.system('clear')
	t_name=input("Enter Your Name : ")
	c.execute('SELECT Teacher FROM teacher')
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
	c.execute('SELECT Teacher_Password FROM teacher WHERE Teacher = ?',t_name)
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

def teacherbatch_view(t_name):
	c.execute('SELECT Student FROM largecoaching WHERE Teacher = ?',t_name)
	data = c.fetchall()

	for row in data:
		print(row)

	input("\n\nPRESS ENTER TO CONTINUE :")

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

#Teacher uploads new marksheet
def teacher_upload_marks(t_name):
	c.execute('SELECT Batch FROM teacher WHERE Teacher = ?',t_name)
	data=c.fetchall()
	listconv1=list(chain.from_iterable(data)) 
	t_batch=str(listconv1[0])
	c.execute('SELECT Student FROM coaching WHERE Batch  = ?',t_batch)
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

		c.execute('UPDATE coaching SET Marks_History = ? WHERE Student = ?',(s_marks_history, s_name))
		conn.commit()

	Total_Marks_generate()

def reminderint():
	rem='REMINDER : UPDATE MARKSHEET'
	os.system('clear')

for i in range(3):

    sys.stdout.write('\r'+rem)
    sys.stdout.flush()
    time.sleep(0.5)
    sys.stdout.write('\r'+' '*len(rem))
    sys.stdout.flush()
    time.sleep(0.5)


def remcheck(t_name):
	c.execute('SELECT Reminder FROM teacher WHERE Teacher = ?',t_name)
	data=c.fetchall()
	listconv1=list(chain.from_iterable(data)) 
	remcheck=str(listconv1[0])
	if(remcheck=='1')
		os.system('clear')
		reminderint()














#MAIN
create_coachingtable()
create_teachertable()
os.system('clear')

print("COACHING APP\n")

while True:
		
		try:
			inp=int(input("Choose a Number : \n\n(1) ADMINISTRATOR \n(2) STUDENT\n(3) TEACHER\n(0) Quit \n\n"))

		except ValueError:
			os.system('clear')
			inp=int(input("Choose a Valid Number : \n\n(1) ADMINISTRATOR \n(2) STUDENT\n(3) TEACHER\n(0) Quit \n\n"))

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

elif inp==0:
	os.system('clear')
	quit()
else:
	os.system('clear')
	inp=int(input("Choose a Valid Number : \n\n(1) ADMINISTRATOR \n(2) STUDENT\n(3) TEACHER\n(0) Quit \n\n"))

#CODE ENDS :D --------X---------



































