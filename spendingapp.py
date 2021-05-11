# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 08:11:34 2021

@author: kingpc
"""
from tkinter import*
import tkinter as tk
import tkinter.messagebox as tkBox
import numpy as np 
from tkcalendar import*
import time 
import sqlite3 
import os
from PIL import Image, ImageTk
os.system('clear')

background_color="#0A2455"


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
img=Image.open("Loginbackground.png")
img = img.resize((350, 460), Image.ANTIALIAS)
img_set=ImageTk.PhotoImage(img)
window.configure(background=background_color)
window.geometry("800x500")
window.title("Spending App 2021")

background_label=Label(window, image=img_set)
background_label.place(x=5, y=15)


mycal = Calendar(window, setmode='day', date_pattern='d/m/yy', font="Arial 8")
mycal.place(x=65, y=180)


lbl1=Label(window, text="Login Here !", fg='white', bg=background_color, font=("Lilita One", 18))
lbl1.place(x=500, y=105)

lbl=Label(window, text = "Type Your password", fg='white', bg=background_color, font=("Lilita One", 10))
lbl.place(x=495, y=150)

txtfld=Entry(window, show='*', fg='black', width=28)
txtfld.place(x=470, y=175, height=25)

btn=Button(window, text="Login", fg='white', bg="#008CFF", width=20, height=2, command=sign_in, font=("Lilita One", 12))
btn.place(x=460, y=210)




def clock(): 
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")
    my_label.config(text=hour + ":" + minute + ":" + second)
    my_label.after(1000, clock)
def update(): 
    my_label.config(text="new text")
        
my_label = Label(window, text="", font=("Lilita One", 26), fg="white", bg=background_color)
my_label.place(x=115, y=120)

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
        width = 800
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False) 
        self.mycal = Calendar(root, setmode='day', date_pattern='d/m/yy')
        self.mycal.place(x=450, y=411)
        
        self.logout_btn=Button(root, text="  LOGOUT  ", fg="red", command=root.destroy)
        self.logout_btn.place(x=600, y=50)
        self.addtrans_btn=Button(root, text="ADD TRANSACTION", command=lambda: self.addtrans())
        self.addtrans_btn.place(x=550, y=100)
        self.eacc_btn=Button(root, text=" EDIT ACC.")
        self.eacc_btn.place(x=600, y= 140)
        self.set_bttn=Button(root, text="   SETUP    ")
        self.set_bttn.place(x=603, y=190) 
        self.query() 
        self.balancefigure = Label(root, text=" EUROS IN BANK : ",font=("Helvetica", 11), fg="green")
        self.balancefigure.place(x=160, y=50)
        self.acc_sumbtn=Button(root, text=" ACC. SUMMARY ")
        self.acc_sumbtn.place(x=564, y=240)
        self.supalotto=Button(root, text="    LOTTO     ")
        self.supalotto.place(x=590, y=280)
       
        #connect to the database
     
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor() 
    #c.execute(""" CREATE TABLE MoneySpent (
                # EUROS real, 
                 #CATEGORY text, 
                 #PLACE text
                 #)""")
        
    conn.close()
    
    #%% QUERY function
    def query(self): 
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor() 
        c.execute("SELECT SUM(EUROS) FROM MoneySpent WHERE EUROS > 0")
        records =  c.fetchall()
       # print(records) 
        
        print_records = ''
        for record in records: 
            print_records += str(record[0]) + "\n"
        query_label = Label(root, text=print_records, font=("Helvetica", 11), fg='red')
        query_label.place(x=300, y=50)
            
        
        conn.commit() 
        conn.close() 
     #%%   
#%% SUBMIT FUNCTION
    def submit(self): 
            conn = sqlite3.connect('expenses.db') 
            c = conn.cursor() 
            c.execute("INSERT INTO MoneySpent VALUES(:EUROS, :CATEGORY, :PLACE)", 
                      {
                          'EUROS': self.euros.get(),
                          'CATEGORY': self.cat_entry.get(), 
                          'PLACE': self.txtfld2.get()
            
                      }) 
                
            conn.commit() 
            conn.close() 
    
            self.euros.delete(0, END)  
            self.cat_entry.delete(0,END) 
            self.txtfld2.delete(0, END)
           
        
        
    #%% add transaction function   
    def addtrans(self): 
            
        self.newWin = Toplevel(root) 
        width = 600
        height = 400 
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        self.newWin.geometry(alignstr)
        self.newWin.resizable(width=False, height=False)   
        self.lbl1 = Label(self.newWin, text="Enter amount in Euros :", fg='red')
        self.lbl1.place(x=150 , y=50)
        self.euros = Entry(self.newWin, width=20)
        self.euros.place(x=300, y=50)
        self.lbl2 = Label(self.newWin, text="CATEGORY :", fg='green') 
        self.lbl2.place(x=150 , y=80)
        self.cat_entry = Entry(self.newWin, width=20)
        self.cat_entry.place(x=299, y=80)
        self.place_entry = Label(self.newWin, text=" ENTER NAME OF PLACE :")
        self.place_entry.place(x=140, y=120)
        self.txtfld2 = Entry(self.newWin, width=20)
        self.txtfld2.place(x=299, y=120)
        self.submit_btn=Button(self.newWin, text="SUBMIT RECORD TO DATABASE", command=lambda: self.submit())
        self.submit_btn.place(x=280, y=160) 
        self.chkbttn=Checkbutton(self.newWin, text="Money Into Bank?")
        self.chkbttn.place(x=280, y=200)
        
            
    #%% add trans function       
       
    #%%
        self.logout_btn=Button(root, text="  LOGOUT  ", fg="red", command=root.destroy)
        self.logout_btn.place(x=600, y=50)
        self.addtrans_btn=Button(root, text="ADD TRANSACTION", command=lambda: addtrans(root))
        self.addtrans_btn.place(x=550, y=100)
        self.eacc_btn=Button(root, text=" EDIT ACC.")
        self.eacc_btn.place(x=600, y= 140)
        self.set_bttn=Button(root, text="   SETUP    ")
        self.set_bttn.place(x=603, y=190)
        self.acc_sumbtn=Button(root, text=" ACC. SUMMARY ")
        self.acc_sumbtn.place(x=603, y=180)
        
        
    
        

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
#%%
 







