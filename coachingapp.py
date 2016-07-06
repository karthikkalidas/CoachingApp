import sys
import os
import sqlite3

#Connection and Cursor
conn = sqlite3.connect('coaching.db')
c = conn.cursor()
StudentList=[]

class Student:

	def __init__(self, s_name, s_batch, s_marks, s_rank):
		self.s_name=s_name
		self.s_batch=s_batch
		self.s_marks=s_marks
		self.s_rank=s_rank

def create_table():
	c.execute("CREATE TABLE IF NOT EXISTS coaching(Name TEXT, Batch TEXT, Marks TEXT, Rank REAL)")		

def add_student():
	s_name=input("Enter Student's Name : ")
	s_marks=input("Enter Student's Marks : ")
	c.execute("INSERT INTO coaching(Name, Marks1) VALUES (?, ?)",(s_name, s_marks))
	conn.commit()
	rank_generate()
	batch_generate()
	c.execute('SELECT Batch FROM coaching WHERE Name = ?',(s_name))
	s_batch =c.fetchall()
	c.execute('SELECT Rank FROM coaching WHERE Name = ?',(s_name))
	data=c.fetchall()
	s_rank =str(data[0])
	new_student=Student(s_name,s_batch,s_marks,s_rank)
	StudentList.append(new_student)

def rank_generate():
	c.execute('SELECT Marks1 FROM coaching ORDER BY Marks1 DESC')
	data = c.fetchall()
	for i in range(1,len(data)+1):
		c.execute('UPDATE coaching SET Rank = ? WHERE Marks1 = ?',(i,str(data[i-1][0])))   
		conn.commit()

#Batches of 3
def batch_generate():
	c.execute('SELECT Rank FROM coaching ORDER BY Marks1 DESC')
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

def latest_marks(s_name):
	c.execute('SELECT * FROM coaching WHERE ID = (SELECT MAX(ID) FROM coaching) AND Name = ?',s_name)  
	data = c.fetchall()
	for row in data:
		print(row)

def studentbatch_view(s_name):
	c.execute('SELECT Rank FROM coaching WHERE Name = ?',s_name)
	data = c.fetchall()
	for row in data:
		print(row)

def new_test_marks():
	testno=input("Enter Test Number : ")
	c.execute('ALTER TABLE coaching ADD COLUMN ? TEXT','Marks'+testno)
	conn.commit()

def adminint():
	os.system('clear')
	func=int(input("Choose Any Number : \n\n(1) Add Student\n(2) View Database\n\n"))
	os.system('clear')
	if func == 1:
		add_student()
	elif func == 2:
		read_from_db()
	else:
		print("Your option doesn't make sense to me")

def studentint():
	os.system('clear')
	s_name=input("Enter Your Name : ")
	os.system('clear')
	func=int(input("Choose Any Number : \n\n(1) View Latest Marks\n(2) View Batch\n(3) View Performance History\n"))
	os.system('clear')
	if func == 1:
		latest_marks(s_name)
	elif func == 2:
		studentmarks_view(s_name)
	else:
		print("Your option doesn't make sense to me")


create_table()
studentint()
# studentint()