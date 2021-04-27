# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 08:11:34 2021

@author: kingpc
"""
from tkinter import* 
import tkinter.messagebox as tkBox
import numpy as np 


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
        

window=Tk() 
window.geometry("400x300") 
window.title("Spending App 2021")
btn=Button(window, text="Login", fg='red', width=10 , command=sign_in)

lbl1=Label(window, text=" ENTER PASSWORD BELOW FOR ACCESS", fg='green', font=("Helvetica", 10))
lbl1.place(x=80, y=45)

btn.place(x=175, y=170)
lbl=Label(window, text = "PASSWORD :")

lbl.place(x=100, y=100)
txtfld=Entry(window, show='*', fg='blue')
txtfld.place(x=175, y=101)

password = ["engineer", "daniel"]  








    
    
    
     
    

window.mainloop() 

  







