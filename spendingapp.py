# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 08:11:34 2021

@author: kingpc
"""
from tkinter import * 
import tkinter as tk
import tkinter.messagebox as tkBox
import numpy as np 
from tkcalendar import* 
import time 
import sqlite3 
import os 
os.system('clear')

#%% sign in function
def sign_in(): 
    enter_password = (txtfld.get())
    if enter_password in password: 
        password_Index = (password.index(txtfld.get()))
        print(password_Index)
        print(enter_password)
        print(password[password_Index])
        if enter_password == (password[password_Index]):
            window.destroy()
        else: 
            tkBox.showinfo('error')
    else:
        tkBox.showinfo('wrong passcode')

#%% login page
window=Tk() 
window.geometry("600x500") 
window.title("Spending App 2021")
btn=Button(window, text="Login", fg='red', width=10 , command=sign_in) 

mycal = Calendar(window, setmode='day', date_pattern='d/m/yy')
mycal.place(x=1, y=300)


lbl1=Label(window, text=" ENTER PASSWORD BELOW FOR ACCESS", fg='green', font=("Helvetica", 10))
lbl1.place(x=150, y=45)

btn.place(x=250, y=170)
lbl=Label(window, text = "PASSWORD :")

lbl.place(x=145, y=100)
txtfld=Entry(window, show='*', fg='blue')
txtfld.place(x=220, y=101)  

def clock(): 
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")
    my_label.config(text=hour + ":" + minute + ":" + second)
    my_label.after(1000, clock)
def update(): 
    my_label.config(text="new text")
        
my_label = Label(window, text="", font=("Helvetica", 26), fg="red", bg="black")
my_label.place(x=400, y=300) 

clock() 
        
#my_label.after(3000, update)

my_menu = Menu(window) 
window.config(menu=my_menu) 
file_menu = Menu(my_menu)
my_menu.add_cascade(label="File", menu=file_menu)
my_menu.add_cascade(label="Edit", menu=file_menu) 
my_menu.add_cascade(label="Options", menu=file_menu)
my_menu.add_cascade(label="Tools", menu=file_menu)
my_menu.add_cascade(label="Window", menu=file_menu)
my_menu.add_cascade(label="Help", menu=file_menu)

password = ["1234", "daniel"]  
window.mainloop() 

#%% MAIN WINDOW
class App:
    def __init__(self, root):
        # setting title
        root.title("EXPENSE TRACKER 2021 ~ Developed by Daniel")
        # setting window size
        width = 700
        height = 600
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False) 
    #%% add transaction function   
        def addtrans(): 
            newWin = Toplevel(root) 
            width = 600
            height = 400 
            screenwidth = root.winfo_screenwidth()
            screenheight = root.winfo_screenheight()
            alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
            newWin.geometry(alignstr)
            newWin.resizable(width=False, height=False)   
            lbl1 = Label(newWin, text="Enter amount in Euros :")
            lbl1.place(x=180 , y=50)
            
    #%% add trans function ^        
       
    #%%
        self.logout_btn=Button(root, text="  LOGOUT  ", fg="red", command=root.destroy)
        self.logout_btn.place(x=600, y=50)
        self.addtrans_btn=Button(root, text="ADD TRANSACTION", command=addtrans)
        self.addtrans_btn.place(x=550, y=100)
        self.eacc_btn=Button(root, text=" EDIT ACC.")
        self.eacc_btn.place(x=600, y= 140)
        
        #connect to the database
        '''
        conn = sqlite3.connect('transaction.db')
        c = conn.cursor() 
        c.execute(""" CREATE TABLE transactions (
                  rent real,
                  travel real,
                  groceries real,
                  subscriptions real,
                  cigarettes real,
                  )""")
        
        conn.close()
        '''
       
        
      
        

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
#%%
 







