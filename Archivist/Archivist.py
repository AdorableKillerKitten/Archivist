from tkinter import *
from tkinter import ttk
import sqlite3



#cur.execute('''CREATE TABLE collection( name text, id text)''');






# todo 
# event Listener on search_btn 
# function to parse searchbar
# searchterm seperated by blank spaces 
# iterate over string and return a list of search terms 

def focus(event):
    widget = root.focus_get()
    print(widget, " has focus")

class Item:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def printItem(self):
        print(self.name)
        print(self.id)


class ArchiverGUI(ttk.Frame):

    

    def __init__(self,master):
        super().__init__(master)
        self.items = []
        self.master = master
        master.title("Archivist")
        self.searchTxt = ''
         
        
        self.grid(column=0, row=0)

        self.searchbar = ttk.Entry(self, validate="key", textvariable=self.searchTxt)
        self.search_btn = ttk.Button(self, text="Search", command=self.searchFor)
        self.name_txt = ttk.Label(self, text="Name")
        self.id_txt = ttk.Label(self, text="ID")
        self.name_ent =  ttk.Entry(self)
        self.id_ent =  ttk.Entry(self)

        self.master.bind("<Return>", self.searchFor)
        #self.master.bind("<<ListboxSelect>>", self.updateEntry)

        self.scroll_list  = Listbox(self, height=5)
        self.scroll_list.bind("<<ListboxSelect>>", self.updateEntry)
        
        self.searchbar.grid(column=0,row=0, columnspan=2)
        self.search_btn.grid(column=2,row=0)

        self.name_txt.grid(column=0,row=1)
        self.id_txt.grid(column=0, row=2)
        self.name_ent.grid(column=1,row=1)
        self.id_ent.grid(column=1, row=2)
        self.scroll_list.grid(column=2, row=1, rowspan=2)

        
        

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
        cursorSel = int(self.scroll_list.curselection()[0])
        if( cursorSel > len(self.items)-1 or cursorSel < 0):
            return
        print(self.scroll_list.curselection())
        item = self.items[cursorSel]
        self.name_ent.delete(0,END)
        self.id_ent.delete(0,END)
        self.name_ent.insert(0,item.name)
        self.id_ent.insert(0,item.id)
        pass 



root = Tk() 
root.bind_all("<Button-1>", lambda e: focus(e))

interface = ArchiverGUI(master=root)
interface.mainloop();





