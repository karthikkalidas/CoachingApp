import sqlite3

#Connection and Cursor
conn = sqlite3.connect('coaching.db')
c = conn.cursor()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS coaching(Name TEXT, Batch TEXT, Marks TEXT, Rank REAL)")


def data_entry1():
    c.execute("INSERT INTO coaching(Name, Marks, Rank) VALUES (?, ?, ?)",
          ('a', 10, 0))

    conn.commit()

def data_entry2():
    c.execute("INSERT INTO coaching(Name, Marks, Rank) VALUES (?, ?, ?)",
          ('b', 20, 0))

    conn.commit()

def data_entry3():
    c.execute("INSERT INTO coaching(Name, Marks, Rank) VALUES (?, ?, ?)",
          ('c', 30, 0))

    conn.commit()

def data_entry4():
    c.execute("INSERT INTO coaching(Name, Marks, Rank) VALUES (?, ?, ?)",
          ('d', 40, 0))

    conn.commit()


def rank_generate():
    c.execute('SELECT Marks FROM coaching ORDER BY Marks DESC')
    data = c.fetchall()
    for i in range(1,len(data)+1):
      c.execute('UPDATE coaching SET Rank = ? WHERE Marks = ?',(i,str(data[i-1][0])))   
      conn.commit()

#Batches of 3
def batch_generate():
    c.execute('SELECT Rank FROM coaching ORDER BY Marks DESC')
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

# def drop_table():
#   c.execute('DROP TABLE coaching.coaching')
#   c.commit()

# drop_table()  
create_table()
data_entry1()
data_entry2()
data_entry3()
data_entry4()
rank_generate()
batch_generate()

# read_from_db()




