import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sq
from extract import extract_videos,extract_img
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image
import webbrowser
import os
import glob
import urllib.request
from ttkthemes import ThemedStyle

root = tk.Tk()
style = ThemedStyle(root)
style.set_theme("adapta")
root.title('EduReco')
root.geometry("450x700+500+300")
try:
    os.mkdir('images')
except:pass
icon = PhotoImage(file='icon.png')
root.iconphoto(False,icon)

conn = sq.connect('topics.db')
cur = conn.cursor()
cur.execute('create table if not exists tasks (title text)')
cur.execute('create table if not exists titles (title text)')
cur.execute('create table if not exists thumbnails (title text)')
task = []
links = []
thumbnails = []

def addTask():
    word = e1.get()
    if len(word)==0:messagebox.showinfo('Empty Entry', 'Enter task name')
    else:
        link,id = extract_videos(word)
        img = extract_img(id)
        links.append(link)
        task.append(word)
        thumbnails.append(img)
        cur.execute('insert into tasks values (?)', (word,))
        cur.execute('insert into titles values (?)', (link,))
        cur.execute('insert into thumbnails values (?)', (img,))
        listUpdate()
        e1.delete(0,'end')

def listUpdate():
    clearList()
    for i in task:t.insert('end', i)
    images()

def delOne():
    try:
        val = t.get(t.curselection())
        if val in task:
            ind=task.index(val)
            del_title = links[ind]
            img_link = thumbnails[ind]
            links.pop(ind)
            thumbnails.pop(ind)
            task.remove(val)
            listUpdate()
            cur.execute('delete from tasks where title = ?', (val,))
            cur.execute('delete from titles where title = ?', (del_title,))
            cur.execute('delete from thumbnails where title = ?',(img_link,))
    except:messagebox.showinfo('Cannot Delete', 'No Task Item Selected')

def deleteAll():
    mb = messagebox.askyesno('Delete All','Are you sure?')
    if mb==True:
        while(len(task)!=0):
            task.pop()
            links.pop()
            thumbnails.pop()
        cur.execute('delete from tasks')
        cur.execute('delete from titles')
        cur.execute('delete from thumbnails')
        listUpdate()

def clearList():
    t.delete(0,'end')


def bye():
    print(task)
    root.destroy()

def retrieveDB():
    while(len(task)!=0):
        task.pop()
        links.pop()
        thumbnails.pop()
    for row in cur.execute('select title from tasks'):
        task.append(row[0])
    for row in cur.execute('select title from titles'):
        links.append(row[0])
    for row in cur.execute('select title from thumbnails'):
        thumbnails.append(row[0])

def urlopen(url):
    webbrowser.open_new_tab(url)

buttons = []
def delete_but():
    for i in buttons:
        i.destroy()

def images():
    delete_but()
    folder = glob.glob('images/*')
    for f in folder:
        os.remove(f)
    i=0
    os.chdir('images')
    images=[]
    while(i<len(links)):
        urllib.request.urlretrieve(thumbnails[i],links[i][-11:]+'.png')
        images.append(links[i][-11:]+'.png')
        i+=1
    i=0
    x_val,y_val=50,250
    count=0
    for img in images:
        image = Image.open(img)
        image = image.resize((120, 120), Image.ANTIALIAS)
        my_img = ImageTk.PhotoImage(image)
        url_button = Button(root,image=my_img,command=lambda url=links[i]:urlopen(url))
        url_button.image=my_img
        if url_button not in buttons:
            if count>0 and count%2==0:
                y_val+=150
                x_val-=150
            elif count>0 and count%2!=0:
                x_val+=150
            url_button.place(x=x_val,y=y_val)
            buttons.append(url_button)
            count+=1
        i+=1
    os.chdir("..")


l1 = ttk.Label(root, text = 'EduReco')
l2 = ttk.Label(root, text='Enter Topic Title: ')
e1 = ttk.Entry(root, width=21)
t = tk.Listbox(root, height=11, selectmode='SINGLE')
b1 = ttk.Button(root, text='Add Topic', width=20, command=addTask)
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

root.mainloop()

conn.commit()
cur.close()