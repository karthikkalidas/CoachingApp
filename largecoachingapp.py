import sys
import time
import os
import sqlite3
from itertools import chain

#Connection and Cursor
conn = sqlite3.connect('coaching.db')
c = conn.cursor()
Marks_HistoryList=[]

#Creates a table with student data
def create_coachingtable():
	c.execute("CREATE TABLE IF NOT EXISTS coaching(Student TEXT,Student_Password TEXT, Batch TEXT, Marks_History TEXT, Total_Marks REAL, Rank REAL)")	

#Creates a table with teacher data
def create_teachertable():
	c.execute("CREATE TABLE IF NOT EXISTS teacher(Teacher TEXT, Teacher_Password TEXT, Batch TEXT, Reminder TEXT)")	

#Creates a table with exam data
def create_testtable():
	c.execute("CREATE TABLE IF NOT EXISTS test(Test_ID TEXT, Test_Name TEXT, MarkList_Status TEXT)")	

#ADMINISTRATOR
#ADMINISTRATOR 
#ADMINISTRATOR
#ADMINISTRATOR 
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
		coachingint()
	else:
		print("Your option doesn't make sense to me")

	os.system('clear')

#Sets Reminder for teachers
def remind_teachers():
	c.execute('SELECT Test_ID FROM test')
	data=c.fetchall()
	testid=len(data)

	if(testid==0):
		input("You have not started a test. PRESS ENTER to start a new test : ")
		new_test()

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

		Marks_HistoryLength=len(Marks_HistoryList)

		if(Marks_HistoryLength<testid):
			os.system('clear')
			c.execute('SELECT Batch FROM coaching WHERE rowid = ?',str(i))
			data=c.fetchall()
			listconv1=list(chain.from_iterable(data)) 
			t_batch=str(listconv1[0])
			c.execute("UPDATE teacher SET Reminder = ? WHERE Batch = ?",('1',t_batch))
			conn.commit()	

#Checks if all the teachers have uploaded the marks
def marks_uploadcheck():
	c.execute('SELECT Test_ID FROM test')
	data=c.fetchall()
	testid=len(data)

	if(testid==0):
		input("You have not started a test. PRESS ENTER to start a new test : ")
		new_test()

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

		Marks_HistoryLength=len(Marks_HistoryList)

		if(Marks_HistoryLength<testid):
			print("Teachers have not uploaded marks!\n\n")
			input("PRESS ENTER TO CONTINUE : ")
			coachingint()

#Starts a new test
def new_test():
	marks_uploadcheck()
	testid=0
	testid+=1
	test_name=input("Enter Test's Name : ")
	c.execute("INSERT INTO test(Test_ID, Test_Name) VALUES (?,?)",(testid,test_name))
	conn.commit()
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
	c.execute('SELECT Student FROM coaching')
	data = c.fetchall()
	NameList=list(chain.from_iterable(data))
	c.execute("INSERT INTO coaching(Student, Student_Password,Batch) VALUES (?,?,?)",(s_name,s_pass,input('Enter Batch of Student : ')))
	conn.commit()

#Generating the Batch & Teacher Column. Batches of 3
def remap_batches():
	marks_uploadcheck()
	c.execute('SELECT Rank FROM coaching ORDER BY Total_Marks DESC')
	data = c.fetchall()

	for i in range(1,len(data)+1):

		if(i%3==1):
			batch=input('Enter Batch Name as per order : ')
			c.execute('UPDATE coaching SET Batch = ? WHERE Rank = ?',(batch,i))  
			conn.commit()
		else:
			c.execute('UPDATE coaching SET Batch = ? WHERE Rank = ?',(batch,i))  
			conn.commit()

#STUDENT
#STUDENT
#STUDENT
#STUDENT
#STUDENT Interface
def studentint(s_name):
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
		coachingint()
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
			print("Please enroll as a student\n\n")
			input("PRESS ENTER TO CONTINUE : ")
			coachingint()
		elif s_name not in NameList:
			s_name=input("You dont seem to be enrolled. Try again : ")
		else:
			return s_name
			break

#Check for the student's password
def s_passcheck(s_name):
	os.system('clear')
	s_pass=input("Enter Your Password : ")
	c.execute('SELECT Student_Password FROM coaching WHERE Student = ?',s_name)
	data = c.fetchall()
	PassList=list(chain.from_iterable(data))

	while True:

		if (PassList==[]):	
			print("Please enroll as a student\n\n")
			input("PRESS ENTER TO CONTINUE : ")
			coachingint()
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

#TEACHER
#TEACHER
#TEACHER
#TEACHER
#TEACHER Interface
def teacherint(t_name):
	os.system('clear')

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
		coachingint()
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
			print("Please enroll as a teacher \n\n")
			input("PRESS ENTER TO CONTINUE : ")
			coachingint()
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
			print("Please enroll as a teacher\n\n")
			input("PRESS ENTER TO CONTINUE : ")
			coachingint()
		elif t_pass not in PassList:
			t_pass=input("Password is incorrect!. Try again : ")
		else:
			break

#Shows the students in the teacher's batch
def teacherbatch_view(t_name):
	c.execute('SELECT Batch FROM teacher WHERE Teacher = ?',t_name)
	data=c.fetchall()
	listconv1=list(chain.from_iterable(data)) 
	t_batch=str(listconv1[0])
	c.execute('SELECT Student FROM coaching WHERE Batch = ?',t_batch)
	data = c.fetchall()
	listconv1=list(chain.from_iterable(data)) 

	for row in listconv1:
		print(row)

	input("\n\nPRESS ENTER TO CONTINUE :")

#Generating a list of marks from Marks_History
def marks_list_generate(s_name):
	c.execute('SELECT Marks_History FROM coaching WHERE Student = ?',(s_name))
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

#Generating the Rank Column on the basis of overall test marks
def rank_generate():
	c.execute('SELECT Total_Marks FROM coaching ORDER BY Total_Marks DESC')
	data = c.fetchall()

	for i in range(1,len(data)+1):
		c.execute('UPDATE coaching SET Rank = ? WHERE Total_Marks = ?',(i,str(data[i-1][0])))   
		conn.commit()

#Checks if a new test has started
def testcheck():
	c.execute('SELECT Marks_History FROM coaching')
	data = c.fetchall()
	c.execute('SELECT Test_ID FROM test')
	data2=c.fetchall()
	testid=len(data2)

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

		Marks_HistoryList = list(map(int, Marks_HistoryList))

		if(len(Marks_HistoryList)>testid):
			print("New Test has to be started first! Contact Administrator\n\n")
			input("PRESS ENTER TO CONTINUE : ")
			coachingint()

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
			print("Please add a student first\n\n")
			input("PRESS ENTER TO CONTINUE : ")
			coachingint()
		else:
			break

	testcheck()

	for i in range(0,len(NameList)):
		s_name=NameList[i]	
		Marks_HistoryList=marks_list_generate(s_name)
		s_marks=input("Enter Latest marks for Student "+s_name+" : ")
		Marks_HistoryList.append(s_marks)

		if(len(Marks_HistoryList)>1):
			s_marks_history = ','.join(Marks_HistoryList)
		else:
			s_marks_history = Marks_HistoryList[0]

		c.execute('UPDATE coaching SET Marks_History = ? WHERE Student = ?',(s_marks_history, s_name))
		conn.commit()

	Total_Marks_generate()
	rank_generate()
	c.execute("UPDATE teacher SET Reminder = ? WHERE Batch = ?",('0',t_batch))
	conn.commit()

#Reminder Interface
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

#Reminder Check
def remcheck(t_name):
	c.execute('SELECT Reminder FROM teacher WHERE Teacher = ?',t_name)
	data=c.fetchall()
	listconv1=list(chain.from_iterable(data)) 
	remcheck=str(listconv1[0])

	if(remcheck=='1'):
		os.system('clear')
		reminderint()

#COACHING
#COACHING
#COACHING
#COACHING
#COACHING INTERFACE
def coachingint():
	create_coachingtable()
	create_teachertable()
	create_testtable()
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

			studentint(s_name)

	elif inp==3:
		t_name=t_usrnamecheck()
		t_passcheck(t_name)

		while True:

			remcheck(t_name)
			teacherint(t_name)

	elif inp==0:
		os.system('clear')
		quit()
	else:
		os.system('clear')
		inp=int(input("Choose a Valid Number : \n\n(1) ADMINISTRATOR \n(2) STUDENT\n(3) TEACHER\n(0) Quit \n\n"))

#MAIN
#MAIN
#MAIN
#MAIN
coachingint()

#CODE ENDS :D --------X---------



































