from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from functools import partial
import db
class AddUpdateWindow():

    def __init__(self,data,parent):
        super().__init__()
        #intialize the input data and parent window
        self.data = data
        self.parent = parent
        self.initUI()



    def initUI(self):
        self.master = Toplevel()
        self.master.geometry("500x120")
        vcmd = (self.master.register(self.validateYear),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        #to check if operation is add or update
        self.OperationAdd = True
        self.ButtonText = "Add"
        self.RecordId = ""
        self.master.title("Add")
        if 'values' in self.data.keys(): #if there are values in passed data then its an update operation
            self.OperationAdd = False
            self.RecordId = self.data["values"][0]
            self.ButtonText = "Update"
            self.master.title("Update")

        #define variable to store input
        self.Title = StringVar()
        self.Author = StringVar()
        self.Year = StringVar()

        #define labels and inputs for add or update operation
        a = Label(self.master, text="Book Title").grid(row=0, column=0)
        self.TitleInput = Entry(self.master, textvariable=self.Title,width=50).grid(row=0, column=1)
        b = Label(self.master, text="Author").grid(row=1, column=0)
        self.AuthorInput = Entry(self.master, textvariable=self.Author,width=50).grid(row=1, column=1)
        c = Label(self.master, text="Year").grid(row=2, column=0)
        self.YearInput = Entry(self.master, validate='key', validatecommand=vcmd,
                                    textvariable=self.Year,width=10).grid(sticky="w",row=2, column=1)


        addUpdateCommand = partial(self.AddUpdate, self.Title, self.Author, self.Year,self.RecordId)
        addUpdateButton = ttk.Button(self.master, text=self.ButtonText, command=addUpdateCommand).grid(row=3, column=0, padx=(20, 10),pady=(10, 10))

        #if it is and update operation fill the input with the passed data
        if self.OperationAdd == False:
            self.Title.set(self.data["values"][1])
            self.Author.set(self.data["values"][2])
            self.Year.set(self.data["values"][3])

    def validateYear(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed:
            try:
                int(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return True

    #function to add or update depending on the passed parameter
    def AddUpdate(self,title,author,year,id):
        titleInput = title.get().strip()
        authorInput = author.get().strip()
        yearInput = year.get().strip()

        emptyFields =""
        if titleInput == "":
            emptyFields = emptyFields + "(Title) "
        if authorInput == "":
            emptyFields = emptyFields + "(Author) "
        if yearInput == "":
            emptyFields = emptyFields + "(Year)"

        if emptyFields != "":
            message = "Please fill the missing parameters:\n" + emptyFields
            messagebox.showwarning(title="Warning", message=message)
            return 0

        if id != "":
            db.UpdateBook(titleInput,authorInput,yearInput, id)
        else:
            db.AddBook(titleInput,authorInput,yearInput)

        #refresh tree
        self.parent.tree.delete(*self.parent.tree.get_children())
        self.parent.refreshTree()
        #close add update window
        self.master.destroy()
