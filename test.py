import sqlite3

#Connection and Cursor
conn = sqlite3.connect('coaching.db')
c = conn.cursor()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS coaching(Name TEXT, Batch TEXT, Marks TEXT, Rank REAL)")


def data_entry1():
    c.execute("INSERT INTO coaching(Name, Batch, Marks) VALUES (?, ?, ?)",
          ('a', 'a', '10'))

    conn.commit()

def data_entry2():
    c.execute("INSERT INTO coaching(Name, Batch, Marks) VALUES (?, ?, ?)",
          ('b', 'b', '20'))

    conn.commit()

def data_entry3():
    c.execute("INSERT INTO coaching(Name, Batch, Marks) VALUES (?, ?, ?)",
          ('c','c', '30'))

    conn.commit()

def data_entry4():
    c.execute("INSERT INTO coaching(Name, Batch, Marks) VALUES (?, ?, ?)",
          ('d', 'd', '40'))

    conn.commit()


def rank_generate():
  for i in range(len(c.fetchall())):
    c.execute('UPDATE coaching SET Rank = '+str(i)+' WHERE Marks = (SELECT Marks FROM coaching ORDER BY Marks DESC)' )  
    conn.commit()

def read_from_db():
    data = c.fetchall()
    print(data)
    for row in data:
        print(row)



create_table()
data_entry1()
data_entry2()
data_entry3()
data_entry4()
rank_generate()
read_from_db()




