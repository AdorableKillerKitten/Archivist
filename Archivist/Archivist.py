from tkinter import *
from tkinter import ttk
import sqlite3

# table structure 
# name, id, company, purchase, condition, source, projects, info

#cur.execute('''CREATE TABLE collection( name text, id text, )''');


def newArchive(name):
    con = sqlite3.connect(name + ".db")
    cur = con.cursor()

    cur.execute('''CREATE TABLE collection(name text, id text, company text, purchaseDate text, condition text, source text, projects text, info text)''')
    con.commit()
    con.close()

#newArchive("myColl")
    
def loadArchive(name):
    con = sqlite3.connect(name + ".db")
    
    
    
    return con

def addData(con, name, id, company="", purchaseDate="", condition ="", source ="", projects="", info="" ):
    cursor = con.cursor()
    t = (name,id,company, purchaseDate, condition, source, projects, info)
    cursor.execute("INSERT INTO collection VALUES( ? , ?, ?,?,?,?,?,? )" , t)    
    cursor.execute("SELECT * FROM collection")
    for result in cursor.fetchall():
        print(result)

    con.commit()




# todo 
# event Listener on search_btn 
# function to parse searchbar
# searchterm seperated by blank spaces 
# iterate over string and return a list of search terms 

def focus(event):
    widget = root.focus_get()
    print(widget, " has focus")

class Item:
    def __init__(self, name, id, company, purchase,condition,source,projects,info):
        self.name = name
        self.id = id
        self.company = company
        self.purchase = purchase
        self.condition = condition
        self.source = source
        self.projects = projects
        self.info = info
       

    def printItem(self):
        print(self.name)
        print(self.id)
        print(self.company)
        print(self.purchase)
        print(self.condition)
        print(self.source)
        print(self.projects)
        print(self.info)
        


class ArchiverGUI(ttk.Frame):

    

    def __init__(self,master, editor):
        super().__init__(master)
        self.items = []
        self.master = master
        master.title("Archivist")
        self.searchTxt = ''
        self.editor = editor 
        
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
        
        self.con = loadArchive("myColl")
        self.cur = self.con.cursor()
        
        

    def parseSearch(self,searchTerms):
        return searchTerms.split()


    def searchTerm(self,term):
        
        self.cur.execute('SELECT * FROM collection')


        for result in self.cur.fetchall():
            for entry in result:
                if entry == term:
                    self.items.append(Item(result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7]))

        for item in self.items:
            item.printItem()
        self.updateList()
        #self.updateEntry()
        
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
        try:
            cursorSel = int(self.scroll_list.curselection()[0])
        except:
            return
        if( cursorSel > len(self.items)-1 or cursorSel < 0):
            return
        print(self.scroll_list.curselection())
        item = self.items[cursorSel]
        self.name_ent.delete(0,END)
        self.id_ent.delete(0,END)
        self.name_ent.insert(0,item.name)
        self.id_ent.insert(0,item.id)
        self.editor.updateEntry(updateEntries=self.items)
        self.items[cursorSel].printItem()
        pass 


class Editor(ttk.Frame):
    
    def __init__(self, master):
        self.name = ''
        self.id = ''
        self.company = ''
        self.purchase = ''
        self.condition = ''
        self.source = ''
        self.projects = ''
        self.entries = []    

        super().__init__(master)
        self.master = master 
        self.title = "Editor"
        self.grid(column=0, row=0)
        #Labels 
        self.name_lbl = ttk.Label(self, text="Name")
        self.id_lbl = ttk.Label(self, text="Label")
        self.company_lbl = ttk.Label(self,text='Company')
        self.purchase_lbl = ttk.Label(self,text='Date of Purchase')
        self.condition_lbl = ttk.Label(self,text='Current condition')
        self.source_lbl = ttk.Label(self,text='Source')
        self.projects_lbl = ttk.Label(self,text='Projects')

        # Associated Entry widgets 

        self.name_ent = ttk.Entry(self, textvariable=self.name)
        self.id_ent = ttk.Entry(self, textvariable=self.id);
        self.company_ent = ttk.Entry(self, textvariable=self.company)
        self.purchase_ent = ttk.Entry(self, textvariable=self.purchase)
        self.condition_ent = ttk.Entry(self, textvariable=self.condition)
        self.source_ent = ttk.Entry(self, textvariable=self.source)
        self.projects_ent = ttk.Entry(self, textvariable=self.projects)
        
        self.info_txt = Text(self, width = 30, height=8)

        self.entries.append(self.name_ent)
        self.entries.append(self.id_ent)
        self.entries.append(self.company_ent)
        self.entries.append(self.purchase_ent)
        self.entries.append(self.condition_ent)
        self.entries.append(self.source_ent)
        self.entries.append(self.projects_ent)
        self.entries.append(self.info_txt)
                

        self.save_btn = ttk.Button(self, text="Save", command=self.saveEntry)
        
        self.name_lbl.grid(column=0,row=0)
        self.id_lbl.grid(column=0,row=1)
        self.company_lbl.grid(column=0,row=2)
        self.purchase_lbl.grid(column=0,row=3) 
        self.condition_lbl.grid(column=0,row=4)
        self.source_lbl.grid(column=0,row=5) 
        self.projects_lbl.grid(column=0,row=6) 

        
        
        self.name_ent.grid(column=1,row=0)
        self.id_ent.grid(column=1,row=1)
        self.company_ent.grid(column=1,row=2) 
        self.purchase_ent.grid(column=1,row=3) 
        self.condition_ent.grid(column=1,row=4) 
        self.source_ent.grid(column=1,row=5) 
        self.projects_ent.grid(column=1,row=6)
        
        self.info_txt.grid(column=2, row=0)
        self.save_btn.grid(column=3,row=5);

        self.con = loadArchive("myColl")
        self.cur = self.con.cursor()

    def saveEntry(self,event=None):
            self.name = self.name_ent.get()
            self.id = self.id_ent.get();
            self.company = self.company_ent.get();
            self.purchase = self.purchase_ent.get();
            self.condition = self.condition_ent.get();
            self.source = self.source_ent.get();
            self.projects = self.projects_ent.get();
            
            addData(self.con,self.name,self.id,self.company,self.purchase,self.condition,self.source,self.projects,self.info_txt.get("1.0",END))
            
            pass

    def updateEntry(self,event=None,updateEntries=[]):
        
        for i in range(len( updateEntries)):
            self.entries[i].delete(0,END)
        self.name_ent.insert(0,updateEntries[i].name)
        self.id_ent.insert(0,updateEntries[i].id)
        self.company_ent.insert(0,updateEntries[i].company)
        self.purchase_ent.insert(0,updateEntries[i].purchase)
        self.condition_ent.insert(0,updateEntries[i].condition)
        self.source_ent.insert(0,updateEntries[i].source)
        self.projects_ent.insert(0,updateEntries[i].projects)
        self.info_txt.insert(INSERT,updateEntries[i].info)    
                
        pass 




root = Tk() 
root2 = Tk()
root.bind_all("<Button-1>", lambda e: focus(e))
edit = Editor(root2)

interface = ArchiverGUI(master=root,editor=edit)
interface.mainloop();





