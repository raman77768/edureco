import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sq
from tkinter import Scrollbar
from extract import extract_videos

root = tk.Tk()
root.title('To-Do List')
root.geometry("600x250+500+300")

conn = sq.connect('todo.db')
cur = conn.cursor()
cur.execute('create table if not exists tasks (title text)')
cur.execute('create table if not exists titles (title text)')
task = []
links = []

def addTask():
    word = e1.get()
    if len(word)==0:messagebox.showinfo('Empty Entry', 'Enter task name')
    else:
        link = extract_videos(word)
        links.append(link)
        task.append(word)
        cur.execute('insert into tasks values (?)', (word,))
        cur.execute('insert into titles values (?)', (link,))
        listUpdate()
        e1.delete(0,'end')

def listUpdate():
    clearList()
    for i in task:t.insert('end', i)
    for j in links:t2.insert('end',j)

def delOne():
    try:
        val = t.get(t.curselection())
        if val in task:
            del_title = links[task.index(val)]
            links.pop(task.index(val))
            task.remove(val)
            listUpdate()
            cur.execute('delete from tasks where title = ?', (val,))
            cur.execute('delete from titles where title = ?', (del_title,))
    except:messagebox.showinfo('Cannot Delete', 'No Task Item Selected')

def deleteAll():
    mb = messagebox.askyesno('Delete All','Are you sure?')
    if mb==True:
        while(len(task)!=0):
            task.pop()
            links.pop()
        cur.execute('delete from tasks')
        cur.execute('delete from titles')
        listUpdate()

def clearList():
    t.delete(0,'end')
    t2.delete(0,'end')

def bye():
    print(task)
    root.destroy()

def retrieveDB():
    while(len(task)!=0):
        task.pop()
        links.pop()
    for row in cur.execute('select title from tasks'):
        task.append(row[0])
    for row in cur.execute('select title from titles'):
        links.append(row[0])


l1 = ttk.Label(root, text = 'To-Do List')
l2 = ttk.Label(root, text='Enter task title: ')
e1 = ttk.Entry(root, width=21)
t = tk.Listbox(root, height=11, selectmode='SINGLE')
t2 = tk.Listbox(root, height=11, selectmode='SINGLE')
b1 = ttk.Button(root, text='Add task', width=20, command=addTask)
b2 = ttk.Button(root, text='Delete', width=20, command=delOne)
b3 = ttk.Button(root, text='Delete all', width=20, command=deleteAll)
b4 = ttk.Button(root, text='Exit', width=20, command=bye)

retrieveDB()
listUpdate()


l2.place(x=50, y=50)
e1.place(x=50, y=80)
b1.place(x=50, y=110)
b2.place(x=50, y=140)
b3.place(x=50, y=170)
b4.place(x=50, y =200)
l1.place(x=50, y=10)
t.place(x=220, y = 50)
t2.place(x=400,y=50)
root.mainloop()

conn.commit()
cur.close()