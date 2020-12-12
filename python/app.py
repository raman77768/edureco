import tkinter as tk
from tkinter import ttk
import sqlite3 as sq
from extract import extract_videos
from PIL import ImageTk, Image
import webbrowser
import os
import glob
from urllib.request import urlretrieve
from ttkthemes import ThemedStyle
from tkinter import messagebox,Scrollbar

root = tk.Tk()
style = ThemedStyle(root)
style.set_theme("adapta")
root.title('EduReco')
root.geometry("1400x750+500+300")

try:
    os.mkdir('images')
except:pass
icon = tk.PhotoImage(file='icon.png')
root.iconphoto(False,icon)

conn = sq.connect('topics.db')
cur = conn.cursor()
cur.execute('create table if not exists tasks (title text)')
cur.execute('create table if not exists titles (title text)')
cur.execute('create table if not exists thumbnails (title text)')
cur.execute('create table if not exists videos (title text)')

task = []
links = []
thumbnails = []
video_names = []
buttons = []
video_labels = []

def addTask():
    word = e1.get()
    if len(word)==0:tk.messagebox.showinfo('Empty Entry', 'Enter task name')
    else:
        link,img,video_name = extract_videos(word)
        links.append(link)
        task.append(word)
        thumbnails.append(img)
        video_names.append(video_name)
        cur.execute('insert into tasks values (?)', (word,))
        cur.execute('insert into titles values (?)', (link,))
        cur.execute('insert into thumbnails values (?)', (img,))
        cur.execute('insert into videos values (?)', (video_name,))

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
            video_title = video_names[ind]
            links.pop(ind)
            thumbnails.pop(ind)
            video_names.pop(ind)
            task.remove(val)
            listUpdate()
            cur.execute('delete from tasks where title = ?', (val,))
            cur.execute('delete from titles where title = ?', (del_title,))
            cur.execute('delete from thumbnails where title = ?',(img_link,))
            cur.execute('delete from videos where title = ?',(video_title,))

    except:tk.messagebox.showinfo('Cannot Delete', 'No Task Item Selected')

def deleteAll():
    mb = messagebox.askyesno('Delete All','Are you sure?')
    if mb==True:
        task.clear()
        links.clear()
        thumbnails.clear()
        video_names.clear()

        cur.execute('delete from tasks')
        cur.execute('delete from titles')
        cur.execute('delete from thumbnails')
        cur.execute('delete from videos')

        listUpdate()

def clearList():
    t.delete(0,'end')

def bye():
    #print(video_names)
    root.destroy()

def retrieveDB():
    task.clear()
    links.clear()
    thumbnails.clear()
    video_names.clear()

    for row in cur.execute('select title from tasks'):
        task.append(row[0])
    for row in cur.execute('select title from titles'):
        links.append(row[0])
    for row in cur.execute('select title from thumbnails'):
        thumbnails.append(row[0])
    for row in cur.execute('select title from videos'):
        video_names.append(row[0])

def urlopen(url):
    webbrowser.open_new_tab(url)

def delete_but():
    for i in buttons:
        i.destroy()

def delete_video_names():
    for i in video_labels:
        i.destroy()

def images():
    delete_but()
    delete_video_names()
    folder = glob.glob('images/*')
    for f in folder:
        os.remove(f)
    i=0
    os.chdir('images')
    images=[]
    while(i<len(links)):
        urlretrieve(thumbnails[i],links[i][-11:]+'.png')
        images.append(links[i][-11:]+'.png')
        i+=1
    i=0
    count={
        1:[50,250],
        2:[50,420],
        3:[50,590],
    }
    x_count,y_count=1,1
    for img in images[:27]:
        image = Image.open(img)
        image = image.resize((120, 120), Image.ANTIALIAS)
        my_img = ImageTk.PhotoImage(image)
        url_button = ttk.Button(root,image=my_img,command=lambda url=links[i]:urlopen(url))
        url_button.image=my_img
        name_label = ttk.Label(root, text = video_names[i])
        name_label.config(width=23)
        if url_button not in buttons:
            if x_count>9:
                y_count+=1
                x_count=1
            x_val,y_val=count[y_count][0],count[y_count][1]
            url_button.place(x=x_val+(150*(x_count-1)),y=y_val)
            name_label.place(x=x_val+(150*(x_count-1)),y=y_val+140)
            buttons.append(url_button)
            video_labels.append(name_label)
            x_count+=1
        i+=1
    os.chdir("..")

l1 = ttk.Label(root, text = 'EduReco')
l2 = ttk.Label(root, text='Enter Topic Title: ')
e1 = ttk.Entry(root, width=22)

frame = tk.Frame(root)
t = tk.Listbox(frame, height=11, selectmode='SINGLE', width=50)
t.pack(side="left", fill="y")
scrollbar = Scrollbar(frame, orient="vertical")
scrollbar.config(command=t.yview)
scrollbar.pack(side="right", fill="y")
t.config(yscrollcommand=scrollbar.set)

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
frame.place(x=220, y = 60)

root.mainloop()

conn.commit()
cur.close()