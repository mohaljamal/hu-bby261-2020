import sqlite3
import sys
dbname = r"library.db"
testRecords = [
    ["Cycling, The Perfect Hobby","Orcun Madran",2021],
    ["Outdoor sports and coding","Orcun Madran",2022],
    ["My name is red","Orhan Pamuk",1998],
    ["Snow","Orhan Pamuk", 2002],
    ["The New Life", "Orhan Pamuk", 1994],
    ["The Forty Rules of Love","Elif Shafak",2009],
    ["Honour","Elif Shafak",2011],
    ["Palestine : Beautiful Home","Mohammad Aljamal",2025],
    ["Liberation Day","Mustafa Kemal Ataturk",1925] ,
    ["Work Like A Machine With A Heart","Cristian Ronaldo",2022],
    ["How To Destroy The World","Donald Trump",2020]
]

#SQL query to create the books table
createTableQuery = """
CREATE TABLE IF NOT EXISTS Books
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         Title TEXT,
         Author TEXT,
         Year INTEGER,        
         CreationTime DATETIME NOT NULL DEFAULT current_timestamp
         )
    """

#SQl query to reset the table delete/and create again
deleteTableQuery = "DROP Table Books;"

#SQL query to insert a book
insertQuery = "INSERT INTO Books(Title,Author,Year) VALUES(?,?,?)"
#SQL query to update the books table
updateQuery = ''' UPDATE Books
             SET title = ? ,
                 author = ? ,
                 year = ?
             WHERE id = ?
              '''

#SQl query to delete a book
deleteQuery = "DELETE FROM Books WHERE id=?"
def createConnection():
    conn = None
    try:
        conn = sqlite3.connect(dbname)
        return conn
    except Exception as e:
        print(e)
    return conn

#function to create the Books table
def createTable():
    conn = None
    try:
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        c.execute(createTableQuery)
    except Exception as e:
        print(e)
    conn.close()

#function to empty the books table, it deletes the table and create it again so
#the ID is reset to 0
def EmptyDatabase():
    conn = None
    try:
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        c.execute(deleteTableQuery)
        c.execute(createTableQuery)
        conn.commit()

    except Exception as e:
        print(e)
    conn.close()

#function to add the test data to database
def AddData():
    conn = None
    try:
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        for record in testRecords:
            c.execute(insertQuery, (record[0],record[1],record[2]))
        conn.commit()
    except Exception as e:
        print(e)
    conn.close()

#function to get all the books from database
def GetAllRecords():
    conn = None
    data = []
    try:
        conn = sqlite3.connect(dbname)
        d = conn.cursor()
        d.execute("SELECT * FROM Books")
        data = d.fetchall()

    except Exception as e:
        print(e)
    conn.close()
    return data

#function to delete a row from books table
def DeleteRow(id):
    conn = None
    try:
        conn = sqlite3.connect(dbname)
        d = conn.cursor()
        d.execute(deleteQuery,[id])
        conn.commit()

    except Exception as e:
        print(e)
    conn.close()

#function to search Book by author and/or title and/or year range
def SearchBooks(title,author,yearfrom,yearto):
    conn = None
    data = []
    try:
        #construct the search query
        searchQuery = "SELECT * FROM Books WHERE 1=1 "

        if author != "":
            searchQuery = searchQuery + " AND author LIKE '%"+author+"%' "

        if title != "":
            searchQuery = searchQuery + " AND title LIKE '%"+title+"%' "

        if yearfrom != "":
            searchQuery = searchQuery + " AND year >=" + yearfrom + ""

        if yearto != "":
            searchQuery = searchQuery + " AND year <=" + yearto + ""

        conn = sqlite3.connect(dbname)
        d = conn.cursor()
        d.execute(searchQuery)
        data = d.fetchall()

    except Exception as e:
        print(e)
    conn.close()
    return data

#function to update a book with a given id
def UpdateBook(title,author,year,id):
    conn = None
    try:
        conn = sqlite3.connect(dbname)
        d = conn.cursor()
        d.execute(updateQuery,(title,author,int(year),int(id)))
        conn.commit()
    except Exception as e:
        print(e)
    conn.close()

#function to add a book
def AddBook(title, author, year):
    conn = None
    try:
        addQuery = ''' INSERT INTO Books (title,author,year)
              VALUES(?,?,?) '''

        conn = sqlite3.connect(dbname)
        d = conn.cursor()

        d.execute(addQuery, (title, author, int(year)))
        conn.commit()
    except Exception as e:
        print(e)
    conn.close()
def SearchBooksFull(input):
    conn = None
    data = []
    try:
        #construct the search query
        searchQuery = "SELECT * FROM Books WHERE author LIKE '%"+input+"%'  OR title LIKE '%"+input+"%' "

        conn = sqlite3.connect(dbname)
        d = conn.cursor()
        d.execute(searchQuery)
        data = d.fetchall()

    except Exception as e:
        print(e)
    conn.close()
    return data