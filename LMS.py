from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3


conn = sqlite3.connect('./library.db')
curs = conn.cursor()



class Main(object):  
    def __init__(self,app): 
        self.app = app

        def showBooks(self):
            count = 0
            books = curs.execute("SELECT * FROM Books").fetchall()

            self.bookList.delete(0,'end')
            for book in books:
                #print(book) Returns Tuple
                self.bookList.insert(count,str(book[0])+ " - " +book[1])
                count += 1
            
            def bookInfo(event):
                value = str(self.bookList.get(self.bookList.curselection()))
                id = value.split('-')[0]
                book = curs.execute("SELECT * FROM Books WHERE bookID=?",(id,))
                infoBook = book.fetchall()
                #print(infoBook) returns a List with a Tuple in it
                self.detaile.delete(0,'end')
                self.detaile.insert(0,"Book ID : "+str(infoBook[0][0]))
                self.detaile.insert(1,"Book Name : "+infoBook[0][1])
                self.detaile.insert(2,"Author : "+infoBook[0][2])
                self.detaile.insert(3,"Number of pages : "+str(infoBook[0][3]))
                if infoBook[0][4] == 0:
                    self.detaile.insert(4,"Status : Available")
                else:
                    self.detaile.insert(4,"Status : Not Available")


            self.bookList.bind('<<ListboxSelect>>',bookInfo)
            self.tabs.bind('<<NotebookTabChanged>>',showStatistics)
            


        def showStatistics(event):
            booksC = curs.execute("SELECT count(bookID) FROM Books").fetchall()
            membersC = curs.execute("SELECT count(MemberID) FROM Members").fetchall()
            borrowedC = curs.execute("SELECT count(status) FROM Books WHERE status=1").fetchall()
            #print(booksC) returns a Lisit with a tuple in it

            self.booknum.config(text='Number Of The Books : '+ str(booksC[0][0]))
            self.mmbrnum.config(text='Number Of The Members : '+str(membersC[0][0]))
            self.takennum.config(text='Number Of The Borrowed Books : '+str(borrowedC[0][0]))
            showBooks(self)

        #Frames
        mainFrame = Frame(self.app)
        mainFrame.pack()

        #Top Frame - Search Bar
        topFrame = LabelFrame(mainFrame,width=1000,height=65,bg='#a2d471',padx=20,relief=GROOVE,borderwidth=5,text='Search Bar')
        topFrame.pack(side=TOP,fill=X)
        self.searchLabel = Label(topFrame,text='Search :',font='arial 12 bold',bg='#a2d471',fg='black')
        self.searchLabel.grid(row=0,column=0,padx=10,pady=10)
        self.searchEntry = Entry(topFrame,width=40,bd=6)
        self.searchEntry.grid(row=0,column=1)
        self.searchBtn = Button(topFrame,text='Search',font='arial 10',bg='#356a2e',fg='white',command=self.searchBook)
        self.searchBtn.grid(row=0,column=2,padx=9,pady=3)

        #Center Frame
        centerFrame = Frame(mainFrame,width=1000,height=535,bg='#e0f0f0',relief=RIDGE)
        centerFrame.pack(side=TOP)
        
        #Center Left Frame
        centerLeftFrame = Frame(centerFrame,width=700,height=535,relief=GROOVE,borderwidth=5,bg='#e0f0f0')
        centerLeftFrame.pack(side=LEFT)

        #Center Rifgt Frame
        centerRightFrame = Frame(centerFrame,width=300,height=535,relief=GROOVE,borderwidth=5,bg='#e0f0f0')
        centerRightFrame.pack()

        #welcome
        welcome = Frame(centerRightFrame,width=300,height=50,bg='#e1eed3',relief=GROOVE)
        welcome.pack(fill=BOTH)
        self.welcomeLabel = Label(welcome,text='_Welcome to my library_',font='times 15 bold',bg='#e1eed3',fg='black')
        self.welcomeLabel.grid(row=0,column=0,padx=10,pady=10)

        #Tool Bar
        toolBar = LabelFrame(centerRightFrame,width=250,height=400,bg='#a2d471',text='Tool Bar',relief=GROOVE)
        toolBar.pack(fill=BOTH)
        #Add Book Button
        self.addBookbtn = Button(toolBar,text='Add Book',compound=CENTER,font='times 10 bold',command=self.addBook,fg='white',bg='#356a2e')
        self.addBookbtn.pack(pady=10)
        #Add Member Button
        self.addMmbrBtn = Button(toolBar,text='Add Member',font='times 10 bold',compound=CENTER,command=self.addMember,fg='white',bg='#356a2e')
        self.addMmbrBtn.pack(pady=15)
        #Lend Book Button
        self.lendBtn = Button(toolBar,text='Lend Book',compound=CENTER,font='times 10 bold',command=self.lendbook,fg='white',bg='#356a2e')
        self.lendBtn.pack(pady=17)
        #Give Book Button
        self.giveBtn = Button(toolBar,text='Return Book',compound=CENTER,font='times 10 bold',fg='white',bg='#356a2e',command=self.retrnBook)
        self.giveBtn.pack(pady=20)
        #Delete Book Button
        self.deletBbtn = Button(toolBar,text='Delete Book',font='times 10 bold',fg='white',bg='#356a2e',compound=CENTER,command=self.deletBook)
        self.deletBbtn.pack(pady=21)
        #Delete Member Button
        self.deletMbtn = Button(toolBar,text='Delete Member',font='times 10 bold',fg='white',bg='#356a2e',compound=CENTER,command=self.deletMember)
        self.deletMbtn.pack(pady=23)


        #Tabs
        self.tabs = ttk.Notebook(centerLeftFrame,width=700,height=500)
        self.tabs.pack()
        self.tab1 = ttk.Frame(self.tabs)
        self.tab2 = ttk.Frame(self.tabs)
        self.tabs.add(self.tab1,text='Books',compound=LEFT)
        self.tabs.add(self.tab2,text='Statistics',compound=LEFT)

        ### Tab 1 ###
        #List Of Books
        self.bookList = Listbox(self.tab1,width=40,height=24,bd=5,font='arial 10 bold')
        self.sb = Scrollbar(self.tab1,orient=VERTICAL)
        self.bookList.grid(row=0,column=0,padx=(0,0),pady=10,sticky=N)
        self.sb.config(command=self.bookList.yview)
        self.bookList.config(yscrollcommand=self.sb.set)
        self.sb.grid(row=0,column=0,sticky=N+S+E)
        #Details Of Books
        self.detaile = Listbox(self.tab1,width=80,height=30,bd=5,font='arail 10 bold')
        self.detaile.grid(row=0,column=1,padx=(0,0),pady=10,sticky=N)

        ### Tab 2 ###
        #statistics 
        self.booknum = Label(self.tab2,text='Number Of The Books : ',pady=20,font='verdana 10 bold')
        self.booknum.grid(row=0,sticky=W)
        self.mmbrnum = Label(self.tab2,text='Number Of The Members : ',pady=20,font='verdana 10 bold')
        self.mmbrnum.grid(row=1,sticky=W)
        self.takennum = Label(self.tab2,text='Number Of The Borrowed Books : ',pady=20,font='verdana 10 bold')
        self.takennum.grid(row=2,sticky=W)

        #Functions
        showBooks(self)
        showStatistics(self)


    def addBook(self):
        add = AddBook()

    def addMember(self):
        add = AddMember()

    def searchBook(self):
        searched = self.searchEntry.get()
        search = curs.execute("SELECT * FROM Books WHERE bookName LIKE ?",('%'+searched+'%',)).fetchall()
        # print(search) returns a List
        self.bookList.delete(0,'end')
        count = 0
        for book in search:
            self.bookList.insert(count,str(book[0])+ "-" +book[1])
            count += 1

    def lendbook(self):
        lend = LendBook()
    
    def deletBook(self):
        delete = DeletBook()

    def deletMember(self):
        delete = DeletMember()

    def retrnBook(self):
        retrn = ReturnBook()



class AddBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry('400x450+250+50')
        self.title('Add Book')
        self.resizable(False,False)
        ### Frames ###
        #Top Frame
        self.topFrame = Frame(self,height=70,bg='#e1eed3')
        self.topFrame.pack(fill=X)
        head = Label(self.topFrame,text='    Enter the information of the book you want to add to the library.',font='times 10 bold',fg='black',bg='#e1eed3')
        head.grid(row=0,column=0,padx=10,pady=10)

        #Bottom Frame
        self.bottomFrame = Frame(self,height=510,bg='#a2d471')
        self.bottomFrame.pack(fill=X)
        #Enteries
        self.nameLabel = Label(self.bottomFrame,text='Name : ',font='times 12 bold',fg='black',bg='#a2d471')
        self.nameLabel.place(x=70,y=100)
        self.nameEntery = Entry(self.bottomFrame,width=30,bd=3)
        self.nameEntery.place(x=130,y=103)

        self.authorLabel = Label(self.bottomFrame,text='Author : ',font='times 12 bold',fg='black',bg='#a2d471')
        self.authorLabel.place(x=70,y=140)
        self.authorEntery = Entry(self.bottomFrame,width=30,bd=3)
        self.authorEntery.place(x=130,y=143)

        self.pageLabel = Label(self.bottomFrame,text='pages : ',font='times 12 bold',fg='black',bg='#a2d471')
        self.pageLabel.place(x=70,y=180)
        self.pageEntery = Entry(self.bottomFrame,width=30,bd=3)
        self.pageEntery.place(x=130,y=183)

        addButton = Button(self.bottomFrame,text='Add Book',command=self.addBook,fg='white',bg='#356a2e')
        addButton.place(x=180,y=223)
    
    def addBook(self):
        name = self.nameEntery.get()
        author = self.authorEntery.get()
        pages = self.pageEntery.get()

        if name!="" and author!="" and pages!="" :
            try:
                query = "INSERT INTO 'Books' (bookName,author,numofpage) VALUES(?,?,?)"
                curs.execute(query,(name,author,pages))
                conn.commit()
                messagebox.showinfo("Success","The book successfully added to the library.",icon='info')

            except:
                messagebox.showinfo("Error","Something is wrong!",icon='warning')
        else:
            messagebox.showinfo("Error","Fields can not be empty.",icon='warning')


class AddMember(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry('400x450+250+50')
        self.title('Add Member')
        self.resizable(False,False)

        ### Frames ###
        #Top Frame
        self.topFrame = Frame(self,height=70,bg='#e1eed3')
        self.topFrame.pack(fill=X)
        head = Label(self.topFrame,text='Enter information of the member.',font='times 10 bold',fg='black',bg='#e1eed3')
        head.grid(row=0,column=0,padx=10,pady=10)

        #Bottom Frame
        self.bottomFrame = Frame(self,height=510,bg='#a2d471')
        self.bottomFrame.pack(fill=X)
        #Enteries
        self.nameLabel = Label(self.bottomFrame,text='Name : ',font='times 12 bold',fg='black',bg='#a2d471')
        self.nameLabel.place(x=70,y=100)
        self.nameEntery = Entry(self.bottomFrame,width=30,bd=3)
        self.nameEntery.place(x=130,y=103)

        self.emailLabel = Label(self.bottomFrame,text='E-mail : ',font='times 12 bold',fg='black',bg='#a2d471')
        self.emailLabel.place(x=70,y=140)
        self.emailEntery = Entry(self.bottomFrame,width=30,bd=3)
        self.emailEntery.place(x=130,y=143)

        addButton = Button(self.bottomFrame,text='Add Member',command=self.addMember,fg='white',bg='#356a2e')
        addButton.place(x=170,y=183)

    def addMember(self):
        name = self.nameEntery.get()
        email = self.emailEntery.get()

        if name!="" and email!="":
            try:
                query = "INSERT INTO 'Members' (memberName , memberEmail) VALUES(?,?)"
                curs.execute(query,(name,email))
                conn.commit()
                messagebox.showinfo("Success","Member Successfully joind to the library.",icon='info')

            except:
                messagebox.showinfo("Error","Something is wrong!",icon='warning')

        else:
            messagebox.showinfo("Error","Fields can not be empty.",icon='warning')



class LendBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry('400x450+250+50')
        self.title('Lend Book')
        self.resizable(False,False)
        
        query = "SELECT * FROM Books WHERE status=0"
        Books = curs.execute(query).fetchall()
        bookList = []
        for book in Books:
            bookList.append(str(book[0])+" - "+book[1])

        quuery = "SELECT * FROM Members"
        Memebers = curs.execute(quuery).fetchall()
        mmbrList = []
        for member in Memebers:
            mmbrList.append(str(member[0])+" - "+member[1])

         ### Frames ###
        #Top Frame
        self.topFrame = Frame(self,height=70,bg='#e1eed3')
        self.topFrame.pack(fill=X)
        head = Label(self.topFrame,text='Fill the following fields.',font='times 10 bold',fg='black',bg='#e1eed3')
        head.grid(row=0,column=0,padx=10,pady=10)
         #Bottom Frame
        self.bottomFrame = Frame(self,height=510,bg='#a2d471')
        self.bottomFrame.pack(fill=X)

        ### Combo Box ###
        #Book Name
        self.bookName = StringVar()
        self.bookNameL = Label(self.bottomFrame,text='Book : ',font='times 12 bold',fg='black',bg='#a2d471')
        self.bookNameL.place(x=70,y=100)
        self.bookNameC = ttk.Combobox(self.bottomFrame,textvariable=self.bookName)
        self.bookNameC['values'] = bookList
        self.bookNameC.place(x=130,y=103)

        #Member Name
        self.memberName = StringVar()
        self.memberNameL = Label(self.bottomFrame,text='Member : ',font='times 10 bold',fg='black',bg='#a2d471')
        self.memberNameL.place(x=70,y=140)
        self.memberNameC = ttk.Combobox(self.bottomFrame,textvariable=self.memberName)
        self.memberNameC['values'] = mmbrList
        self.memberNameC.place(x=130,y=143)

        #Lend Button
        lendButton = Button(self.bottomFrame,text='Lend',command=self.lendBook,fg='white',bg='#356a2e')
        lendButton.place(x=180,y=183)

    def lendBook(self):
        bookName = self.bookName.get()
        self.bookID = bookName.split(' - ')[0]
        memberName = self.memberName.get()

        if bookName != "" and memberName != "":
            try:
                query = "INSERT INTO 'Borrow' (borrowedbID,borrowermID) VALUES(?,?)"
                curs.execute(query,(bookName,memberName))
                conn.commit()
                messagebox.showinfo("Success","Successfully Lended.",icon='info')
                curs.execute("UPDATE Books SET status =? WHERE bookID=?",(1,self.bookID))
                conn.commit()

            except:
                messagebox.showinfo("Error","Something is wrong!",icon='warning')

        else:
            messagebox.showinfo("Error","Fields can not be empty.",icon='warning')

class DeletBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry('400x450+250+50')
        self.title('Delete Book')
        self.resizable(False,False)

        ### Frames ###
        #Top Frame
        self.topFrame = Frame(self,height=70,bg='#e1eed3')
        self.topFrame.pack(fill=X)
        head = Label(self.topFrame,text='Choose the book you want to delete.',font='times 10 bold',fg='black',bg='#e1eed3')
        head.grid(row=0,column=0,padx=10,pady=10)
         #Bottom Frame
        self.bottomFrame = Frame(self,height=510,bg='#a2d471')
        self.bottomFrame.pack(fill=X)

        query = "SELECT * FROM Books WHERE status=0"
        Books = curs.execute(query).fetchall()
        bookList = []
        for book in Books:
            bookList.append(book[1])
        
        #Label and Combobox
        self.name = StringVar()
        self.nameL = Label(self.bottomFrame,text='Book : ',font='times 12 bold',fg='black',bg='#a2d471')
        self.nameL.place(x=70,y=140)
        self.nameC = ttk.Combobox(self.bottomFrame,textvariable=self.name)
        self.nameC['values'] = bookList
        self.nameC.place(x=130,y=143)

        #Delete Button
        deletButton = Button(self.bottomFrame,text='Delete',fg='white',bg='#356a2e',command=self.deleteBook)
        deletButton.place(x=180,y=183)

    def deleteBook(self):
        name = self.name.get()

        if name != "":
            try:
                curs.execute("DELETE FROM Books WHERE bookName=?",[name])
                conn.commit()
                messagebox.showinfo("Success","Book deleted..",icon='info')

            except:
                messagebox.showinfo("Error","Something is wrong!",icon='warning')
            
        else:
            messagebox.showinfo("Error","Fields can not be empty.",icon='warning')

class DeletMember(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry('400x450+250+50')
        self.title('Delete Member')
        self.resizable(False,False)
        ### Frames ###
        #Top Frame
        self.topFrame = Frame(self,height=70,bg='#e1eed3')
        self.topFrame.pack(fill=X)
        head = Label(self.topFrame,text='Choose the member you want to delete.',font='times 10 bold',fg='black',bg='#e1eed3')
        head.grid(row=0,column=0,padx=10,pady=10)
         #Bottom Frame
        self.bottomFrame = Frame(self,height=510,bg='#a2d471')
        self.bottomFrame.pack(fill=X)

        query = "SELECT * FROM Members"
        Members = curs.execute(query).fetchall()
        memberList = []
        for member in Members:
            memberList.append(member[1])

            #Label and Combobox
        self.member = StringVar()
        self.memberL = Label(self.bottomFrame,text='Member : ',font='times 10 bold',fg='black',bg='#a2d471')
        self.memberL.place(x=70,y=140)
        self.memberC = ttk.Combobox(self.bottomFrame,textvariable=self.member)
        self.memberC['values'] = memberList
        self.memberC.place(x=130,y=143)

        #Delete Button
        deletButton = Button(self.bottomFrame,text='Delete',fg='white',bg='#356a2e',command=self.deleteMember)
        deletButton.place(x=180,y=183)

    def deleteMember(self):
        member = self.member.get()

        if member != "":
            try:
                curs.execute("DELETE FROM Members WHERE memberName=?",[member])
                conn.commit()
                messagebox.showinfo("Success","Member deleted..",icon='info')

            except:
                messagebox.showinfo("Error","Something is wrong!",icon='warning')
            
        else:
            messagebox.showinfo("Error","Fields can not be empty.",icon='warning')


class ReturnBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry('400x450+250+50')
        self.title('Return Book')
        self.resizable(False,False)

        ### Frames ###
        #Top Frame
        self.topFrame = Frame(self,height=70,bg='#e1eed3')
        self.topFrame.pack(fill=X)
        head = Label(self.topFrame,text='Choose the book you want to return.',font='times 10 bold',fg='black',bg='#e1eed3')
        head.grid(row=0,column=0,padx=10,pady=10)
         #Bottom Frame
        self.bottomFrame = Frame(self,height=510,bg='#a2d471')
        self.bottomFrame.pack(fill=X)


        query = "SELECT * FROM Books WHERE status=1"
        borrowed = curs.execute(query).fetchall()
        borrowedList = []
        for book in borrowed:
            borrowedList.append(str(book[0])+" - "+book[1])
        
        #Label and Combobox
        self.name = StringVar()
        self.nameL = Label(self.bottomFrame,text='Book : ',font='times 12 bold',fg='black',bg='#a2d471')
        self.nameL.place(x=70,y=140)
        self.nameC = ttk.Combobox(self.bottomFrame,textvariable=self.name)
        self.nameC['values'] = borrowedList
        self.nameC.place(x=130,y=143)
        #Delete Button
        retrnButton = Button(self.bottomFrame,text='Return',fg='white',bg='#356a2e',command=self.retBook)
        retrnButton.place(x=180,y=183)

    def retBook(self):
        name = self.name.get()
        self.bookID = name.split(' - ')[0]

        if name != "":
            try:
                curs.execute("DELETE FROM Borrow WHERE borrowedbID =?",[self.bookID])
                conn.commit()
                messagebox.showinfo("Success","Successfully returned to the library.",icon='info')
                curs.execute("UPDATE Books SET status =? WHERE bookID=?",(0,self.bookID))
                conn.commit()

            except:
                messagebox.showinfo("Error","Something is wrong!",icon='warning')

        else:
            messagebox.showinfo("Error","Fields can not be empty.",icon='warning')


  
                


def main():
    root = Tk()
    lms_app = Main(root)
    root.title("Library Management System")
    root.geometry("1000x525+100+30")
    root.resizable(False,False)
    root.mainloop()


if __name__ == '__main__':
    main()
