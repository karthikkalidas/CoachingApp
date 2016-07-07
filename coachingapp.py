import sys
import os
import sqlite3
from itertools import chain

#Connection and Cursor
conn = sqlite3.connect('coaching.db')
c = conn.cursor()
Marks_HistoryList=[]


def create_table():
	c.execute("CREATE TABLE IF NOT EXISTS coaching(Name TEXT, Batch TEXT, Marks_History TEXT, Total_Marks REAL, Rank REAL)")		

def marks_list_generate(s_name):
	c.execute('SELECT Marks_History FROM coaching WHERE Name = ?',(s_name))
	data=c.fetchall()
	Marks_HistoryList=list(chain.from_iterable(data))
	if (Marks_HistoryList[0]==None):
		del Marks_HistoryList[0]
	return Marks_HistoryList

def Total_Marks_generate():
	c.execute('SELECT Marks_History FROM coaching')
	data = c.fetchall()      
	for i in range(1,len(data)+1):
		c.execute('SELECT Marks_History FROM coaching WHERE rowid = ?',str(i))
		data=c.fetchall()
		listconv1=list(chain.from_iterable(data)) 
		strconv=str(listconv1[0])
		
 #CONVERT STRING TO LIST NOT TUPLE LIST TO LIST
 #
 #
 #
 #
		

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

def add_student():
	s_name=input("Enter Student's Name : ")
	c.execute("INSERT INTO coaching(Name) VALUES (?)",(s_name))
	conn.commit()

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
			s_name=input("Enter a valid Student Name : ")
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

#On the basis of overall test marks
def rank_generate():
	c.execute('SELECT Total_Marks FROM coaching ORDER BY Total_Marks DESC')
	data = c.fetchall()
	for i in range(1,len(data)+1):
		c.execute('UPDATE coaching SET Rank = ? WHERE Total_Marks = ?',(i,str(data[i-1][0])))   
		conn.commit()

#Batches of 3
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

def read_from_db():
	c.execute('SELECT * FROM coaching')
	data = c.fetchall()
	for row in data:
		print(row)
	input("\n\nPRESS ENTER TO CONTINUE :")

def latest_marks(s_name):
	Marks_HistoryList=marks_list_generate(s_name)
	print("Marks : "+ Marks_HistoryList[-1])

def studentbatch_view(s_name):
	c.execute('SELECT Batch FROM coaching WHERE Name = ?',s_name)
	data = c.fetchall()
	for row in data:
		print(row)

def studentperf_view(s_name):
	c.execute('SELECT Marks_History FROM coaching WHERE Name = ?',s_name)
	data = c.fetchall()
	for row in data:
		print(row)

def adminint():
	os.system('clear')
	while True:
		try:
			func=int(input("Choose Any Number : \n\n(1) Update Marksheet\n(2) View Database\n(3) Add Student\n\n"))

		except ValueError:
			os.system('clear')
			func=int(input("Choose A Proper Number : \n\n(1) Update Marksheet\n(2) View Database\n(3) Add Student\n\n"))

		else:
			break

	os.system('clear')
	if func == 1:
		update_marksheet()
	elif func == 2:
		read_from_db()
	elif func == 3:
		add_student()
	else:
		print("Your option doesn't make sense to me")
	os.system('clear')

def studentint():
	os.system('clear')
	s_name=input("Enter Your Name : ")
	os.system('clear')
	func=int(input("Choose Any Number : \n\n(1) View Latest Marks\n(2) View Batch\n(3) View Performance History\n"))

	while True:
		if isinstance(func, int):
			break
		else:
			func=int(input("Choose A Valid Number : \n\n(1) View Latest Marks\n(2) View Batch\n(3) View Performance History\n"))

	os.system('clear')
	if func == 1:
		latest_marks(s_name)
	elif func == 2:
		studentbatch_view(s_name)
	elif func==3:
		studentperf_view(s_name)
	else:
		print("Your option doesn't make sense to me")
	os.system('clear')

#Main
create_table()
os.system('clear')
print("COACHING APP\n")
while True:
	inp=int(input("Choose a Number : \n\n1)ADMINISTRATOR \n2)STUDENT \n\n"))
	if inp==1:
		adminint()
	elif inp==2:
		studentint()
	else:
		os.system('clear')
		inp=int(input("Choose a Number : \n\n1)ADMINISTRATOR \n2)STUDENT \n\n"))