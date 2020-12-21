from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from functools import partial
import db
import AddUpdateWindow

class MainWindow(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):

        #set menu title and dimensions
        self.master.title("Library Portal")
        self.master.geometry("640x400")


        #create the menu bar and add it to window
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        #create file menu with "Exit" item
        fileMenu = Menu(menubar,tearoff=False)

        fileMenu.add_command(label="Exit", command=self.onExit)
        menubar.add_cascade(label="File", menu=fileMenu)

        #define variable to hold search values from inputs
        self.TitleSearch = StringVar()
        self.AuthorSearch = StringVar()
        self.YearFromSearch = StringVar()
        self.YearToSearch = StringVar()
        self.FullSearch = StringVar()


        #for year integer validation
        vcmd = (self.master.register(self.validateYear),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        #create label and input for book title search
        a = Label(self.master, text="Book Title").grid(row=0, column=0)
        self.searchTitleInput = Entry(self.master,textvariable=self.TitleSearch).grid(row=0, column=1)

        #create label and input for author search
        b = Label(self.master, text="Author").grid(row=0, column=2)
        self.searchAuthorInput = Entry(self.master,textvariable=self.AuthorSearch).grid(row=0, column=3)

        #create label and input for year range search
        c = Label(self.master, text="Year From").grid(row=1, column=0)
        self.searchYearFrom = Entry(self.master,validate= 'key', validatecommand = vcmd,textvariable=self.YearFromSearch).grid(row=1, column=1)
        d = Label(self.master, text="Year To").grid(row=1, column=2)
        self.searchYearTo = Entry(self.master,validate = 'key', validatecommand = vcmd,textvariable=self.YearToSearch).grid(row=1, column=3)

        #variable to hold the command to call the search functions to inputs as parameters
        searchCallCommand = partial(self.search,self.TitleSearch,self.AuthorSearch,self.YearFromSearch,self.YearToSearch)

        #define search button
        searchButton = ttk.Button(self.master, text="Search",command=searchCallCommand).grid(row=2,column=0,padx=(20,10),pady=(10,10))
        # draw a sperator line
        ttk.Separator(self.master, orient=VERTICAL).grid(row=0,column=4, rowspan=3, sticky="ns")

        # create label and input for author search
        e = Label(self.master, text="Full Search").grid(row=0, column=5)
        self.searchFullInput = Entry(self.master, textvariable=self.FullSearch).grid(row=0, column=6)
        # variable to hold the command to call the search functions to inputs as parameters
        fullSearchCallCommand = partial(self.searchFull, self.FullSearch)

        # define search button
        searchFullButton = ttk.Button(self.master, text="Search All", command=fullSearchCallCommand).grid(row=1, column=5,
                                                                                              padx=(20, 10),
                                                                                              pady=(10, 10))

        #draw a sperator line
        ttk.Separator(self.master, orient=HORIZONTAL).grid(row=3, columnspan=5,sticky="ew")


        #create Tree to hold data from books table
        self.master.minsize(width=640, height=400)
        self.master.resizable(width=1, height=1)
        self.tree = ttk.Treeview(self.master, selectmode='browse')
        #place tree
        self.tree.place(x=10, y=100)

        #define vertical and horizontal scrollbars for the tree
        vsb = ttk.Scrollbar(self.master, orient="vertical", command=self.tree.yview)
        vsb.place(x=10 + 590, y=100, height=200 + 20)
        self.tree.configure(yscrollcommand=vsb.set)
        hsb = ttk.Scrollbar(self.master, orient="horizontal", command=self.tree.xview)
        hsb.place(x=10, y=320, width=590)
        self.tree.configure(xscrollcommand=hsb.set)

        #define the GUI tree columns
        self.tree["columns"] = ("id","title","author","year","creationTime")

        #define the headings of the tree and their width and text alignment
        self.tree['show'] = 'headings'
        self.tree.column("id", width=30, anchor='c')
        self.tree.column("title", width=200, anchor='c')
        self.tree.column("author", width=200, anchor='c')
        self.tree.column("year", width=50, anchor='c')
        self.tree.column("creationTime", width=110, anchor='c')
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("author", text="Author")
        self.tree.heading("year", text="Year")
        self.tree.heading("creationTime", text="Creation Time")

        #get all books from database
        data = db.GetAllRecords()

        #fill the tree
        self.fillTree(self.tree,data)

        #function to delete a selected book
        #show error message if no book is selected
        def DeleteSelectedRow():
            selected= self.tree.selection()
            if len(selected) > 0:
                confirmation = messagebox.askquestion('Delete Book', 'Are you sure you want to delete this book',
                                                   icon='warning')
                if confirmation == 'yes':
                    db.DeleteRow(self.tree.selection()[0])
                    self.refreshTree()
            else:
                messagebox.showwarning(title="Warning", message="You Should Select A Record First!")

        #function to update a selected book
        #show error message if no book is selected
        def UpdateSelectedRow():
            selected= self.tree.selection()
            if len(selected) > 0:
                updateWindow = AddUpdateWindow.AddUpdateWindow(self.tree.item(selected),self)
            else:
                messagebox.showwarning(title="Warning", message="You Should Select A Record First!")

        #function to add a new book
        def AddEntry():
            addWindow = AddUpdateWindow.AddUpdateWindow({},self)



        #create the delete,update and add buttons
        self.deleteButton = Button(self.master, text="Delete",command=DeleteSelectedRow)
        self.deleteButton.place(bordermode=OUTSIDE, height=20, width=100, x=10,y=350)
        self.updateButton = Button(self.master, text="Update",command=UpdateSelectedRow)
        self.updateButton.place(bordermode=OUTSIDE, height=20, width=100, x=120, y=350)
        self.addButton = Button(self.master, text="Add",command=AddEntry)
        self.addButton.place(bordermode=OUTSIDE, height=20, width=100, x=230, y=350)

        def emptyDatabase():
            db.EmptyDatabase()
            self.tree.delete(*self.tree.get_children())

        def fillDatabase():
            db.AddData()
            self.refreshTree()


        self.emptyDatabaseButton = Button(self.master, text="Empty Database", command=emptyDatabase)
        self.emptyDatabaseButton.place(bordermode=OUTSIDE, height=20, width=100, x=400, y=350)
        self.fillDatabaseButton = Button(self.master, text="Fill Database",command=fillDatabase)
        self.fillDatabaseButton.place(bordermode=OUTSIDE, height=20, width=100, x=510, y=350)

    def onExit(self):
        self.quit()

    def validateYear(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed:
            try:
                int(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return True

    #function to fill the tree with given data
    def fillTree(self,tree,data):
        for record in data:
            #insert row in the tree and set iid for the tree node to the row id from database
            tree.insert("", 'end', iid=record[0], text="L1",
                        values=(record[0] ,record[1], record[2],record[3], record[4]))

    #function to empty the tree and get all the data again from database and fill the tree again
    def refreshTree(self):
        self.tree.delete(*self.tree.get_children())
        data = db.GetAllRecords()
        self.fillTree(self.tree, data)


    #function to search the database and update the tree accordingly
    def search(self,titleE,authorE,yearFromE,yearToE):
        data = db.SearchBooks(titleE.get(),authorE.get(),yearFromE.get(),yearToE.get())
        self.tree.delete(*self.tree.get_children())
        self.fillTree(self.tree, data)

    def searchFull(self,fullInput):
        data = db.SearchBooksFull(fullInput.get())
        self.tree.delete(*self.tree.get_children())
        self.fillTree(self.tree, data)






