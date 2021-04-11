from tkinter import *
from tkinter import ttk
import sqlite3



#cur.execute('''CREATE TABLE collection( name text, id text)''');






# todo 
# event Listener on search_btn 
# function to parse searchbar
# searchterm seperated by blank spaces 
# iterate over string and return a list of search terms 
class Item:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def printItem(self):
        print(self.name)
        print(self.id)


class ArchiverGUI:

    

    def __init__(self,master):
        self.items = []
        self.master = master
        master.title("Archivist")
        self.searchTxt = ''
        self.mainFrame = Frame(root); 
        
        self.mainFrame.grid(column=0, row=0)

        self.searchbar = ttk.Entry(self.mainFrame, validate="key", textvariable=self.searchTxt)
        self.search_btn = ttk.Button(self.mainFrame, text="Search", command=self.searchFor)
        self.name_txt = ttk.Label(self.mainFrame, text="Name")
        self.id_txt = ttk.Label(self.mainFrame, text="ID")
        self.name_ent =  ttk.Entry(self.mainFrame)
        self.id_ent =  ttk.Entry(self.mainFrame)

        #self.master.bind("<Return>", self.searchFor)
        self.master.bind("<Return>", self.updateEntry)

        self.scroll_list  = Listbox(self.mainFrame, height=5)
        self.scroll_list.bind("<<ListBoxSelect>>", self.updateEntry)
        self.searchbar.grid(column=0,row=0, columnspan=2)
        self.search_btn.grid(column=2,row=0)

        self.name_txt.grid(column=0,row=1)
        self.id_txt.grid(column=0, row=2)
        self.name_ent.grid(column=1,row=1)
        self.id_ent.grid(column=1, row=2)
        self.scroll_list.grid(column=2, row=1, rowspan=2)

        self.mainFrame.focus_set()
        

    def parseSearch(self,searchTerms):
        return searchTerms.split()


    def searchTerm(self,term):
        database = sqlite3.connect('test.db')
        cur = database.cursor()
        cur.execute('SELECT * FROM collection')


        for result in cur.fetchall():
            for entry in result:
                if entry == term:
                    self.items.append(Item(result[0],result[1]))

        for item in self.items:
            item.printItem()
        self.updateList()
        #self.updateEntry()
        database.close()

    def searchFor(self, event=None):
    
    
       
    
        self.searchTxt = self.searchbar.get()
        terms = self.parseSearch(self.searchTxt)

        for term in terms:
            self.searchTerm(term)

    def updateList(self):
        index = 0
        for item in self.items:
            self.scroll_list.insert("end",item.name)
            index +=1

    def updateEntry(self,event=None):
        print(self.scroll_list.curselection())
        item = self.items[int(self.scroll_list.curselection()[0])]
        self.name_ent.delete(0,END)
        self.id_ent.delete(0,END)
        self.name_ent.insert(0,item.name)
        self.id_ent.insert(0,item.id)
        pass 



root = Tk() 

interface = ArchiverGUI(root)




root.mainloop();

