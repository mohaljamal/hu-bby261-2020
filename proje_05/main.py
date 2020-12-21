import tkinter as tk
import MainWindow
import db
def main():

    root = tk.Tk()    #intialize GUI root
    db.createTable()
    app = MainWindow.MainWindow() #create main window
    root.mainloop()


#program starts here ----->
if __name__ == '__main__':
    main()
