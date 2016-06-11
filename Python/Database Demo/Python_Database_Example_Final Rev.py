#!/usr/bin/python 2
# -*- coding: utf-8 -*-

# Author:       Daniel A. Christie 2015
# App Name:     Database Demo - with a Tkinter GUI
#
# Purpose:      To demonstrate how an application accesses a database
#               to query, add, update, edit, and delete information,
#               supported by a Tkinte GUI.
#
#               I also required for my GUI to have a listbox, textbox,
#               and entry field to demonstrate how to present the data
#               to the user.

from Tkinter import *
import tkMessageBox
#from Tkinter import tkMessageBox
import sqlite3

#=========================================================
def dbConnect():
    # Connect to database
    conn = sqlite3.connect('dbWebPages.db')

    # Create table named webpages
    conn.execute("CREATE TABLE if not exists tblWebContent( \
        ID INTEGER PRIMARY KEY AUTOINCREMENT, \
        colName TEXT, \
        colBody TEXT \
        );")

    # Save changes & close the database connection
    conn.commit()
    conn.close()


#Select item in ListBox
def onSelect(event):
    varList = event.widget #ListBox widget
##    varSel = varList.curselection()
##    for a in varSel:
##        print("The listbox's selected index is: {}".format(a)) #Index of list selection
    select = varList.curselection()[0]
##    print("varList.cursorselection is: {}".format(select)) #Index of list selection
    value = varList.get(select)
##    print("The value of the selected item is: {}".format(value)) #Listbox's selected value
    txtName.delete(0, END)
    txtName.insert(0, value)
    conn = sqlite3.connect('dbWebPages.db')
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT colBody FROM tblWebContent where colName = (?)", [value])
        varBody = cursor.fetchall()[0]
        for b in varBody:
##            print("The content of cursor.fetchall[select] is: {}".format(b))
            txtBody.delete(1.0, END)
            txtBody.insert(1.0, b)

def addToList():
    varBody = txtBody.get(1.0, END)
    varName = txtName.get()
    #Normalize the data
    varName = varName.strip()
    varName = varName.upper()
    if (len(varBody) > 1) and (len(varName) > 0):
        conn = sqlite3.connect('dbWebPages.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM tblWebContent WHERE colName = '"+varName+"'")
            count = cursor.fetchone()[0]
            chkName = count
            if chkName == 0:
                cursor.execute("INSERT INTO tblWebContent (colName, colBody) VALUES ('"+varName+"', '"+varBody+"')")
                lstList1.insert(END, varName)
                txtName.delete(0, END)
                txtBody.delete(1.0, END)
            else:
                tkMessageBox.showerror("Name Error","'{}' already exists in the database! Please choose a different name.".format(varName))
        conn.commit()
        conn.close()
    else:
        tkMessageBox.showerror("Missing Text Error","Please ensure that there is information in the Name and Body fields.")
        

def onDelete():
    varSel = lstList1.get(lstList1.curselection()) #Listbox's selected value
    confirm = tkMessageBox.askokcancel("Delete Confirmation", "'{}' will be permenantly deleted, are you sure?".format(varSel))
    if confirm:
        conn = sqlite3.connect('dbWebPages.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tblWebContent WHERE colName = '"+varSel+"'")
        onClear()
        onRefresh
        conn.commit()
    else:
        pass
    conn.close()


def onClear():
    #Delete the selected item in the index and clear all text boxes
    txtName.delete(0,END)
    txtBody.delete(1.0,END)
    try:
        index = lstList1.curselection()[0]
        lstList1.delete(index)
    except IndexError:
        pass
    onRefresh()
    

def onRefresh():
    #Populate the listbox, coinciding with the database
    lstList1.delete(0,END)
    conn = sqlite3.connect('dbWebPages.db')
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tblWebContent")
        count = cursor.fetchone()[0]
        i = 0
        while i < count:
                cursor.execute("SELECT colName FROM tblWebContent")
                varList = cursor.fetchall()[i]
                for item in varList:
                    lstList1.insert(0, str(item))
                    i = i + 1
    conn.close()


def onEdit():
    varBody = txtBody.get(1.0, END)
    varSelect = lstList1.curselection()[0] #Index of list selection
    lstValue = lstList1.get(varSelect) #List selection text value
    if (len(varBody) > 1) and (len(lstValue) > 0):
        pass
        conn = sqlite3.connect('dbWebPages.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE tblWebContent SET colName = '"+lstValue+"', colBody = '"+varBody+"' WHERE colNAME='"+lstValue+"'")
            txtName.delete(0, END)
            txtBody.delete(1.0, END)
            onRefresh()
        conn.commit()
        conn.close()
    else:
        tkMessageBox.showerror("Missing Text Error","Please select a record to edit and ensure that there is information in the Body field.")


def onClose():
    root.destroy()


def centerScreen():
    #Get the app's dimensions
    width = root.winfo_width()
    height = root.winfo_height()
    #Get user's screen dimensions and calculate from the app's dimensions
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    #Assign the return to the geometry manager
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))


#============================Paint the GUI=========================================
root = Tk()
root.title("Database Demo")
root.minsize(width = 635, height = 440)
#root.maxsize(width = 800, height = 800)

centerScreen()
dbConnect()
    
    
#Adding Labels to the GUI
lblName = Label(root, text = "Name:").grid(row = 0, column = 0, padx = 15, pady = 0, sticky = W)
lblBody = Label(root, text = "Body text:").grid(row = 0, column = 3, padx = 10, pady = 0, sticky = W)

#Define the text boxes & Paint them
txtName = Entry(root)
txtName.grid(row = 1, column = 0, columnspan = 2, padx = 15, pady = 5, sticky = N+W+E)
txtBody = Text(root, height = 22, width = 50)
txtBody.grid(row = 1, column = 3, rowspan = 2, columnspan = 2, padx = 10, pady = 5, sticky = N+S)


#Define the listbox with a scrollbar and paint them
scrollbar1 = Scrollbar(root, orient=VERTICAL)
scrollbar2 = Scrollbar(root, orient=VERTICAL)
lstList1 = Listbox(root, exportselection=0, yscrollcommand = scrollbar1.set, height = 20, width = 20)
lstList1.bind('<<ListboxSelect>>', onSelect)
scrollbar1.config(command = lstList1.yview)
scrollbar2.config(command = txtBody.yview)
scrollbar1.grid(row = 2, column = 1, rowspan = 1, columnspan = 2, padx = 0, pady = 0, sticky = N+S+E)
lstList1.grid(row = 2, column = 0, rowspan = 1, columnspan = 2, padx = 15, pady = 0, sticky = N+E+W)
scrollbar2.grid(row = 1, column = 4, rowspan = 2, columnspan = 2, padx = 5, pady = 0, sticky = N+S+E)

#Define buttons & paint them
btnEdit = Button(root, text = "Edit Record", command = onEdit)
btnEdit.grid(row = 4, column = 0, padx = 15, pady = 10, sticky = W)
btnAdd = Button(root, text = "Add Record", command = addToList)
btnAdd.grid(row = 4, column = 1, padx = 15, pady = 10, sticky = W)
btnDel = Button(root, text = "Delete Record", command = onDelete)
btnDel.grid(row = 4, column = 3, padx = 10, pady = 10, sticky = W)
btnClose = Button(root, text = "       Close       ", command = onClose)
btnClose.grid(row = 4, column = 4, padx = 10, pady = 10, sticky = E)


onRefresh()

root.mainloop()
