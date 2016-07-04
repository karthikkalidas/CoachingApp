import sys
import sqlite3

#Connection and Cursor
conn = sqlite3.connect('coaching.db')
c = conn.cursor()

class Student:
    def __init__(self, s_name, s_batch, s_marks, s_rank):
        self.s_name=s_name
        self.s_batch=s_batch
        self.s_marks=s_marks
        self.s_rank=s_rank

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS coaching(Name TEXT, Batch TEXT, Marks TEXT, Rank REAL)")


def data_entry():
    c.execute("INSERT INTO coaching(Name, Batch, Marks) VALUES (?, ?, ?)",
          (s_name, s_batch, s_marks))

    conn.commit()

def add_student():
	s_name = input("Enter Student's Name : ")
	s_marks = input("Enter Student's Marks : ")
	new_student=Student

def rank_generate():
	c.execute('SELECT Marks FROM coaching ORDER BY Marks DESC')
	c.execute('UPDATE coaching SET Rank = 99 WHERE Marks = (SELECT Marks FROM coaching ORDER BY Marks DESC)' )
    data = c.fetchall()

Update MyTable
    Set ListOrder=ListOrder+1
        Where ListOrder=(Select ListOrder-1 From MyTable where BookMark='f')




    
def read_from_db():
    c.execute('SELECT * FROM coaching')
    data = c.fetchall()
    print(data)
    for row in data:
        print(row)

def adminint():

