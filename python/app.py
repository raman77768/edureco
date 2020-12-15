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
from collections import OrderedDict
from trends.fetch import Trends

trends = Trends()

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

titles = OrderedDict()
buttons = []
video_labels = []

def addTask():
    word = e1.get()
    if len(word)==0:tk.messagebox.showinfo('Empty Entry', 'Enter task name')
    else:
        link,img,video_name = extract_videos(word)
        titles[word] = {'links':link,'thumbnails':img,'names':video_name}
        cur.execute('insert into tasks values (?)', (word,))
        cur.execute('insert into titles values (?)', (link,))
        cur.execute('insert into thumbnails values (?)', (img,))
        cur.execute('insert into videos values (?)', (video_name,))

        listUpdate()
        e1.delete(0,'end')

def get_recommended():
    recommended_list = []
    for i in titles:
        res = trends.get_results(i)
        recommended_list += res
    return recommended_list

def listUpdate():
    clearList()
    for i in titles:
        t.insert('end', i)
    for i in set(get_recommended()):
        t2.insert('end', i)
    images()

def delOne():
    try:
        val = t.get(t.curselection())
        if val in titles.keys():
            del_title = titles[val]['links']
            img_link = titles[val]['thumbnails']
            video_title = titles[val]['names']
            del titles[val]
            listUpdate()
            cur.execute('delete from tasks where title = ?', (val,))
            cur.execute('delete from titles where title = ?', (del_title,))
            cur.execute('delete from thumbnails where title = ?',(img_link,))
            cur.execute('delete from videos where title = ?',(video_title,))

    except:tk.messagebox.showinfo('Cannot Delete', 'No Task Item Selected')

def deleteAll():
    mb = messagebox.askyesno('Delete All','Are you sure?')
    if mb==True:
        titles.clear()

        cur.execute('delete from tasks')
        cur.execute('delete from titles')
        cur.execute('delete from thumbnails')
        cur.execute('delete from videos')

        listUpdate()

def clearList():
    t.delete(0,'end')
    t2.delete(0,'end')

def bye():
    #print(video_names)
    root.destroy()

def retrieveDB():
    titles.clear()
    for (r1,r2,r3,r4) in zip(list(cur.execute('select title from tasks')),list(cur.execute('select title from titles')),\
        list(cur.execute('select title from thumbnails')),list(cur.execute('select title from videos'))):
        titles[r1[0]]={'links':r2[0],
        'thumbnails':r3[0],
        'names':r4[0]}

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

    os.chdir('images')

    count={
        1:[50,250],
        2:[50,420],
        3:[50,590],
    }
    x_count,y_count=1,1
    for i in titles:
        urlretrieve(titles[i]['thumbnails'],titles[i]['links'][-11:]+'.png')
        img = titles[i]['links'][-11:]+'.png'
        image = Image.open(img)
        image = image.resize((120, 120), Image.ANTIALIAS)
        my_img = ImageTk.PhotoImage(image)
        url_button = ttk.Button(root,image=my_img,command=lambda url=titles[i]['links']:urlopen(url))
        url_button.image=my_img
        name_label = ttk.Label(root, text = titles[i]['names'])
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
    os.chdir("..")

l1 = ttk.Label(root, text = 'EduReco')
l2 = ttk.Label(root, text='Enter Topic Title: ')
l3 = ttk.Label(root, text='Added Topics')
l4 = ttk.Label(root, text='Recommended Topics')
e1 = ttk.Entry(root, width=22)

frame = tk.Frame(root)
t = tk.Listbox(frame, height=11, selectmode='SINGLE', width=50)
t.pack(side="left", fill="y")
scrollbar = Scrollbar(frame, orient="vertical")
scrollbar.config(command=t.yview)
scrollbar.pack(side="right", fill="y")
t.config(yscrollcommand=scrollbar.set)

frame2 = tk.Frame(root)
t2 = tk.Listbox(frame2, height=11, selectmode='SINGLE', width=50)
t2.pack(side="left", fill="y")
scrollbar2 = Scrollbar(frame2, orient="vertical")
scrollbar2.config(command=t2.yview)
scrollbar2.pack(side="right", fill="y")
t2.config(yscrollcommand=scrollbar2.set)

b1 = ttk.Button(root, text='Add Topic', width=20, command=addTask)
b2 = ttk.Button(root, text='Delete', width=20, command=delOne)
b3 = ttk.Button(root, text='Delete all', width=20, command=deleteAll)
b4 = ttk.Button(root, text='Exit', width=20, command=bye)


retrieveDB()
listUpdate()


l2.place(x=50, y=50)
l3.place(x=330,y=45)
l4.place(x=695,y=45)
e1.place(x=50, y=80)
b1.place(x=50, y=110)
b2.place(x=50, y=140)
b3.place(x=50, y=170)
b4.place(x=50, y =200)
l1.place(x=50, y=10)
frame.place(x=220, y = 60)
frame2.place(x=600, y=60)

root.mainloop()

conn.commit()
cur.close()