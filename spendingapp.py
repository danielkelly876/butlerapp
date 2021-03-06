# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 08:11:34 2021

@author: kingpc
"""
import random
from tkinter import *
import tkinter as tk
import tkinter.messagebox as tkBox
from tkinter import messagebox, ttk
import numpy as np
from tkcalendar import *
import time
import sqlite3
import os
from PIL import Image, ImageTk
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from itertools import cycle, islice
from datetime import date, datetime, timedelta
import csv

#Importing Libraries ends here

#Global Variable Declaration
background_color = "#0A2455"
password = ["1234", "daniel", "asd"]
savingsButtonState = 0
locMonth="Jan-2021"
update_row_id=""
startDate=(date.today()-timedelta(days=2)).strftime("%m/%d/%Y")
endDate=date.today().strftime("%m/%d/%Y")
loginVerifier=False

#Sign In Method
def sign_in():
    global  loginVerifier
    enter_password = (txtfld.get())
    if enter_password in password:
        loginVerifier = True
        password_Index = (password.index(txtfld.get()))
        # print(password_Index)
        # print(enter_password)
        # print(password[password_Index])
        if enter_password == (password[password_Index]):

            window.destroy()
        else:
            tkBox.showinfo('error', "Please Try Again")     #Opens a warning box
    else:
        tkBox.showinfo('wrong passcode', "Please Try Again")    #Opens a warning box

#Declaring login Window and setting its properties
window = Tk()
img = Image.open("Loginbackground.png")
img = img.resize((350, 460), Image.ANTIALIAS)
img_set = ImageTk.PhotoImage(img)
window.configure(background=background_color)
window.geometry("800x500")
window.title("Spending App 2021")


background_label = Label(window, image=img_set)
mycal = Calendar(window, setmode='day', date_pattern='d/m/yy', font="Arial 8")
lbl1 = Label(window, text="Login Here !", fg='white', bg=background_color, font=("Lilita One", 18))
lbl = Label(window, text="Type Your password", fg='white', bg=background_color, font=("Lilita One", 10))
txtfld = Entry(window, show='*', fg='black', width=28)
btn = Button(window, text="Login", fg='white', bg="#008CFF", width=20, height=2, command=sign_in,
             font=("Lilita One", 12))
background_label.place(x=5, y=15)
my_label = Label(window, text="", font=("Lilita One", 26), fg="white", bg=background_color)




# login page
def login_view():
    mycal.place(x=65, y=180)
    lbl1.place(x=500, y=105)
    lbl.place(x=495, y=150)
    txtfld.place(x=470, y=175, height=25)
    btn.place(x=460, y=210)
    clock() #Running the Clock
    my_menu = Menu(window)
    window.config(menu=my_menu)
    file_menu = Menu(my_menu)
    my_menu.add_cascade(label="File", menu=file_menu)
    my_menu.add_cascade(label="Edit", menu=file_menu)
    my_menu.add_cascade(label="Options", menu=file_menu)
    my_menu.add_cascade(label="Tools", menu=file_menu)
    my_menu.add_cascade(label="Window", menu=file_menu)
    my_menu.add_cascade(label="Help", menu=file_menu)
    my_label.place(x=115, y=120)
    window.mainloop()

#Clock Method
def clock():
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")
    my_label.config(text=hour + ":" + minute + ":" + second)
    my_label.after(1000, clock)


def update():
    my_label.config(text="new text")




# MAIN WINDOW
class App:
    def __init__(self, root):

        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute("SELECT rowid, saving, spending, budget FROM target")
        records = c.fetchall()
        # print_records = "0.00"
        # try:
        #     print_records = str(records[0][0] - records[1][0])
        # except:
        #     for record in records:
        #         print_records = str(record[0])
        id_array = []
        saving_array = []
        spending_array = []
        budget_array = []
        #Fetching the records and placing them in arrays to show data in chart
        for record in records:
            id_array.append(record[0])
            saving_array.append(record[1])
            spending_array.append(record[2])
            budget_array.append(record[3])

        conn.commit()
        conn.close()

        #declaring variables for Line Chart

        data2 = {'id': id_array,
                 'saving': saving_array,
                 'spending': spending_array,
                 'budget': budget_array
                 }
        df2 = DataFrame(data2, columns=['id', 'saving', 'spending', 'budget'])

        figure2 = plt.Figure(figsize=(5, 4), dpi=100)
        ax2 = figure2.add_subplot(111)
        line2 = FigureCanvasTkAgg(figure2, root)
        line2.get_tk_widget().place(x=5, y=100)
        df2 = df2[['id', 'saving', 'spending', 'budget']].groupby('id').sum()
        df2.plot(kind='line', legend=True, ax=ax2, color=list(islice(cycle(['r', 'g', 'b']), None, len(df2))),
                 marker='o', fontsize=10)   #Line Chart Plots Here
        ax2.set_title('Targets')

        # setting title
        root.title("EXPENSE TRACKER 2021 ~ Developed by Daniel | MainScreen")
        # setting window size
        width = 800
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        # self.mycal = Calendar(root, setmode='day', date_pattern='d/m/yy')
        # self.mycal.place(x=5, y=311)

        my_menu = Menu(root)
        root.config(menu=my_menu)

        file_menu = Menu(my_menu)
        file_menu.add_command(label="Item")
        file_menu.add_command(label="Exit", command=root.destroy)
        my_menu.add_cascade(label="File", menu=file_menu)

        edit_menu = Menu(my_menu)
        edit_menu.add_command(label="Edit")
        my_menu.add_cascade(label="Edit", menu=edit_menu)

        my_menu.add_cascade(label="Options", menu=file_menu)
        my_menu.add_cascade(label="Tools", menu=file_menu)
        my_menu.add_cascade(label="Window", menu=file_menu)
        my_menu.add_cascade(label="Help", menu=file_menu)

        self.btn_img = Image.open("assets/LogOutButton.png")
        self.btn_img = self.btn_img.resize((55, 35), Image.ANTIALIAS)
        self.btn_imgSet = ImageTk.PhotoImage(self.btn_img)

        self.logout_btn = Button(root, command=root.destroy, fg="white", bg="#25BCAF", activebackground="#25BCAF",
                                 image=self.btn_imgSet, text="LogOut", compound="right", font=("Lilita One", 16))
        self.logout_btn.place(x=671, y=50)
        self.addtrans_btn = Button(root, command=lambda: self.addtrans(), fg="white", bg="#25BCAF",
                                   activebackground="#25BCAF", image=self.btn_imgSet, text="Add Transaction",
                                   compound="right", font=("Lilita One", 16))
        self.addtrans_btn.place(x=588, y=100)
        self.eacc_btn = Button(root, fg="white", bg="#25BCAF", activebackground="#25BCAF", image=self.btn_imgSet,
                               text="Edit Account", compound="right", font=("Lilita One", 16), command=self.edit_account)
        self.eacc_btn.place(x=623, y=150)
        self.set_bttn = Button(root, command=lambda: self.setup(), fg="white", bg="#25BCAF", activebackground="#25BCAF",
                               image=self.btn_imgSet, text="Setup", compound="right", font=("Lilita One", 16))
        self.set_bttn.place(x=684, y=200)
        self.query()
        self.dashboardLabel = Label(root, text="MainScreen ", font=("Lilita One", 14, "underline"), fg="black")
        self.dashboardLabel.place(x=350, y=5)
        self.balancefigure = Label(root, text="Euros in bank : ", font=("Lilita One", 16), fg="#25BCAF")
        self.balancefigure.place(x=210, y=50)
        self.acc_sumbtn = Button(root, command=lambda: self.account_summary(), fg="white", bg="#25BCAF",
                                 activebackground="#25BCAF", image=self.btn_imgSet, text="Account Summary",
                                 compound="right", font=("Lilita One", 16))
        self.acc_sumbtn.place(x=572, y=250)
        self.supalotto = Button(root, fg="white", bg="#25BCAF", activebackground="#25BCAF", image=self.btn_imgSet,
                                text="Play Lotto", compound="right", font=("Lilita One", 16), command= self.play_lotto)
        self.supalotto.place(x=645, y=300)

        # connect to the database

    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    # c.execute(""" CREATE TABLE MoneySpent (
    # EUROS real,
    # CATEGORY text,
    # PLACE text
    # )""")

    conn.close()

    #QUERY function
    def query(self):
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute("SELECT SUM(EUROS) FROM MoneySpent GROUP BY STATUS")
        records = c.fetchall()
        print_records = "0.00"
        try:
            print_records = str(records[0][0] - records[1][0])
        except:
            for record in records:
                print_records = str(record[0])
        query_label = Label(root, text=print_records, font=("Lilita One", 16), fg='#f06292')
        query_label.place(x=350, y=50)

        conn.commit()
        conn.close()

    #Fetch Category OptionBox Data
    def get_category_value(self, *args):
        return self.cat_var.get()

    # Fetch Month OptionBox Data
    def get_month_value(self, *args):
        return self.month_var.get()

    #Set Month
    def setMonth(self, open_scene):
        global locMonth
        locMonth = self.get_month_value()
        # print(locMonth)
        open_scene.destroy()
        self.account_summary()


    #SUBMIT FUNCTION
    def submit(self):

        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        locCheckState = "spending"
        locDateTime = self.txtfld2.get().split("/")
        monthList =['Jan-2021', 'Feb-2021', 'Mar-2021', 'Apr-2021', 'May-2021', 'Jun-2021', 'Jul-2021',
                              'Aug-2021', 'Sep-2021', 'Oct-2021', 'Nov-2021', 'Dec-2021']
        # print(locDateTime[0])
        if savingsButtonState == 1:
            locCheckState = "saving"

        c.execute("INSERT INTO MoneySpent VALUES(:EUROS, :CATEGORY, :PLACE, :STATUS, :DATE, :MONTH)",
                  {
                      'EUROS': self.euros.get(),
                      'CATEGORY': self.get_category_value(),
                      'PLACE': self.purposeValue.get(),
                      "STATUS": locCheckState,
                      "DATE": self.txtfld2.get(),
                      "MONTH": monthList[int(locDateTime[0])-1]

                  })

        messagebox.showinfo("Confirmation", "Transaction Added")

        conn.commit()
        conn.close()

        self.euros.delete(0, END)
        self.txtfld2.delete(0, END)
        self.purposeValue.delete(0, END)

    #Return To menu function
    def open_mainMenu(self, open_scene):
        open_scene.destroy()
        self.__init__(root)

    #Check the MoneyIn Button State
    def savingsButtonState(self):
        global savingsButtonState
        if savingsButtonState == 0:
            savingsButtonState = 1
        elif savingsButtonState == 1:
            savingsButtonState = 0

    #Add Transaction view Method
    def addtrans(self):

        self.newWin = Toplevel(root)
        self.newWin.title("EXPENSE TRACKER 2021 ~ Developed by Daniel | Add Transaction")
        width = 800
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        self.newWin.geometry(alignstr)
        self.newWin.resizable(width=False, height=False)
        self.lbl1 = Label(self.newWin, text="Amount:", fg='#25BCAF', font=("Lilita One", 14))
        self.lbl1.place(x=210, y=85)
        self.euros = Entry(self.newWin, width=20, font=("Lilita One", 14))
        self.euros.place(x=300, y=85, height=30, width=150)
        self.lbl2 = Label(self.newWin, text="Category:", fg='#25BCAF', font=("Lilita One", 14))
        self.lbl2.place(x=200, y=50)

        self.cat_var = StringVar(self.newWin)
        self.cat_choices = ['Rent', 'Travel', 'Groceries', 'Subscription', 'Guilty Pleasures']
        self.cat_var.set('Rent')
        self.cat_entry = OptionMenu(self.newWin, self.cat_var, *self.cat_choices, command=self.get_category_value)

        # self.cat_var = tk.StringVar()
        # self.cat_choices = ttk.Combobox(self.newWin, width=27, textvariable=self.cat_var)
        # self.cat_choices['values'] = ('Rent', 'Travel', 'Groceries', 'Subscription', 'Guilty Pleasures')
        # self.cat_choices.grid(column=1, row=5)
        # self.cat_entry = self.cat_choices.current()
        self.cat_entry.place(x=299, y=45, height=35, width=150)

        # self.cat_entry.pack()
        self.place_purpose = Label(self.newWin, text="Purpose: ", fg="#25BCAF", font=("Lilita One", 14))
        self.place_purpose.place(x=205, y=117)
        self.purposeValue = Entry(self.newWin, width=20, font=("Lilita One", 14))
        self.purposeValue.place(x=299, y=120, height=30, width=150)

        self.place_entry = Label(self.newWin, text="Date: ", fg="#25BCAF", font=("Lilita One", 14))
        self.place_entry.place(x=235, y=157)
        self.txtfld2 = Entry(self.newWin, width=20, font=("Lilita One", 14))
        self.txtfld2.insert(END, date.today().strftime("%m/%d/%Y"))
        self.txtfld2.place(x=299, y=160, height=30, width=150)

        self.savingsButton = Checkbutton(self.newWin, text="Money Into Bank?", fg="#25BCAF",
                                         command=self.savingsButtonState, font=("Lilita One", 14))
        self.savingsButton.place(x=250, y=200)
        self.submit_btn = Button(self.newWin, text="Submit Record", command=lambda: self.submit(), fg="white",
                                 bg="#008CFF", font=("Lilita One", 14))
        self.submit_btn.place(x=250, y=240)

        self.lout_btn = Button(self.newWin, command=root.destroy, fg="white", bg="#25BCAF", activebackground="#25BCAF",
                               image=self.btn_imgSet, text="LogOut", compound="right", font=("Lilita One", 16))
        self.lout_btn.place(x=671, y=50)
        self.rtm = Button(self.newWin, command=lambda: self.open_mainMenu(self.newWin), fg="white", bg="#25BCAF",
                          activebackground="#25BCAF", image=self.btn_imgSet, text="Return To Menu", compound="right",
                          font=("Lilita One", 16))
        self.rtm.place(x=593, y=100)

    #Fetch Category on Setup page
    def get_setup_category_value(self, *args):
        return self.cat_var_setup.get()

    #Submit The values from Setup page
    def submit_setup(self):
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()

        c.execute("INSERT INTO target VALUES(:saving, :spending, :budget, :category)",
                  {
                      'saving': self.savingsTarget_amount.get(),
                      'spending': self.spendingTarget_amount.get(),
                      'budget': self.estimatedBudget_amount.get(),
                      'category': self.get_setup_category_value()

                  })

        messagebox.showinfo("Confirmation", "Target Added")

        conn.commit()
        conn.close()

    #Setup Page View
    def setup(self):
        self.newWin = Toplevel(root)
        self.newWin.title("EXPENSE TRACKER 2021 ~ Developed by Daniel | Setup")
        width = 800
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        self.newWin.geometry(alignstr)
        self.newWin.resizable(width=False, height=False)

        self.spendingTarget = Label(self.newWin, text="Spending Target:", fg='#25BCAF', font=("Lilita One", 14))
        self.spendingTarget.place(x=150, y=85)
        self.spendingTarget_amount = Entry(self.newWin, width=20, font=("Lilita One", 14))
        self.spendingTarget_amount.place(x=300, y=85, height=30, width=150)

        self.savingsTarget = Label(self.newWin, text="Saving Target:", fg='#25BCAF', font=("Lilita One", 14))
        self.savingsTarget.place(x=171, y=50)
        self.savingsTarget_amount = Entry(self.newWin, width=20, font=("Lilita One", 14))
        self.savingsTarget_amount.place(x=299, y=45, height=30, width=150)

        self.estimatedBudget = Label(self.newWin, text="Estimated Budget: ", fg="#25BCAF", font=("Lilita One", 14))
        self.estimatedBudget.place(x=140, y=117)
        self.estimatedBudget_amount = Entry(self.newWin, width=20, font=("Lilita One", 14))
        self.estimatedBudget_amount.place(x=299, y=120, height=30, width=150)

        self.categoryLabel = Label(self.newWin, text="Category: ", fg="#25BCAF", font=("Lilita One", 14))
        self.categoryLabel.place(x=210, y=160)
        self.cat_var_setup = StringVar(self.newWin)
        self.cat_choices_setup = ['Rent', 'Travel', 'Groceries', 'Subscription', 'Guilty Pleasures']
        self.cat_var_setup.set('Rent')
        self.cat_entry_setup = OptionMenu(self.newWin, self.cat_var_setup, *self.cat_choices_setup,
                                          command=self.get_setup_category_value)
        self.cat_entry_setup.place(x=299, y=160, height=35, width=150)

        self.submit_btn = Button(self.newWin, command=self.submit_setup, text="Submit Record", fg="white",
                                 bg="#008CFF", font=("Lilita One", 14))
        self.submit_btn.place(x=250, y=210)

        self.lout_btn = Button(self.newWin, command=root.destroy, fg="white", bg="#25BCAF", activebackground="#25BCAF",
                               image=self.btn_imgSet, text="LogOut", compound="right", font=("Lilita One", 16))
        self.lout_btn.place(x=671, y=50)
        self.rtm = Button(self.newWin, command=lambda: self.open_mainMenu(self.newWin), fg="white",
                          bg="#25BCAF", activebackground="#25BCAF", image=self.btn_imgSet,
                          text="Return To Menu", compound="right", font=("Lilita One", 16))
        self.rtm.place(x=593, y=100)
    #Account Summary Function
    def account_summary(self):
        global locMonth
        # print("Local Month"+ locMonth)

        self.newWin = Toplevel(root)
        self.newWin.title("EXPENSE TRACKER 2021 ~ Developed by Daniel | Account Summary")
        width = 800
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        self.newWin.geometry(alignstr)
        self.newWin.resizable(width=False, height=False)


        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute("SELECT SUM(EUROS), category  FROM MoneySpent WHERE STATUS='spending' AND MONTH='"+locMonth+"' GROUP BY CATEGORY")
        records = c.fetchall()
        # print_records = "0.00"
        # try:
        #     print_records = str(records[0][0] - records[1][0])
        # except:
        #     for record in records:
        #         print_records = str(record[0])

        # id_array = []
        # saving_array = []
        category_array = []
        amount_array = []
        #Placing records in arrays
        for record in records:
            category_array.append(record[1])
            amount_array.append(record[0])
        # print(amount_array)
        # print(category_array)
        newAmArray = []
        for amount in amount_array:
            newAmArray.append(float(amount))

        conn.commit()
        conn.close()
        try:

            data1 = {'Category': category_array,
                     'Amount': newAmArray
                     }
            df1 = DataFrame(data1, columns=['Category', 'Amount'])
            figure1 = plt.Figure(figsize=(6, 5), dpi=80)
            ax1 = figure1.add_subplot(111)
            bar1 = FigureCanvasTkAgg(figure1, self.newWin)
            bar1.get_tk_widget().place(x=5, y=100)
            df1 = df1[['Category', 'Amount']].groupby('Category').sum()
            df1.plot(kind='bar', legend=True, ax=ax1)   #Plotting bar Chart
            ax1.set_title('Category Vs. Spending')
        except:
            print("Failed")


        self.month_label = Label(self.newWin, text="Month:", fg='#25BCAF', font=("Lilita One", 14))
        self.month_label.place(x=130, y=48)

        self.month_var = StringVar(self.newWin)
        self.month_choices = ['Jan-2021', 'Feb-2021', 'Mar-2021', 'Apr-2021', 'May-2021', 'Jun-2021', 'Jul-2021',
                              'Aug-2021', 'Sep-2021', 'Oct-2021', 'Nov-2021', 'Dec-2021']
        self.month_var.set(locMonth)
        self.month_entry = OptionMenu(self.newWin, self.month_var, *self.month_choices, command=self.get_month_value)
        self.month_entry.place(x=200, y=45, height=35, width=150)

        self.submit_btn = Button(self.newWin, text="Filter", fg="white",
                                 bg="#008CFF", font=("Lilita One", 14), command=lambda: self.setMonth(self.newWin))
        self.submit_btn.place(x=370, y=45, height=30)

        self.moneyIn = Label(self.newWin, text="Money In:", fg='#25BCAF', font=("Lilita One", 14))
        self.moneyIn.place(x=532, y=372)

        self.spending = Label(self.newWin, text="Spending: ", fg='#25BCAF', font=("Lilita One", 14))
        self.spending.place(x=535, y=412)

        self.savings = Label(self.newWin, text="Savings:", fg="#25BCAF", font=("Lilita One", 14))
        self.savings.place(x=550, y=452)

        # %%
        self.lout_btn = Button(self.newWin, command=root.destroy, fg="white", bg="#25BCAF", activebackground="#25BCAF",
                               image=self.btn_imgSet, text="LogOut", compound="right", font=("Lilita One", 16))
        self.lout_btn.place(x=671, y=50)
        self.rtm = Button(self.newWin, command=lambda: self.open_mainMenu(self.newWin), fg="white",
                          bg="#25BCAF", activebackground="#25BCAF", image=self.btn_imgSet,
                          text="Return To Menu", compound="right", font=("Lilita One", 16))
        self.rtm.place(x=593, y=100)

        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute("SELECT SUM(EUROS) FROM MoneySpent GROUP BY STATUS")
        records = c.fetchall()
        moneyIn_value = "0"
        spending_value = "0"
        savings_value = "0"
        try:
            savings_value = str(records[0][0] - records[1][0])
            moneyIn_value = str(records[0][0])
            spending_value = str(records[1][0])
        except:
            for record in records:
                print_records = str(record[0])

                moneyIn_value = str(record[0])
                savings_value = moneyIn_value
                spending_value = "0"

        self.moneyIn_amount = Label(self.newWin, text=moneyIn_value, font=("Lilita One", 14), fg='#f06292')
        self.moneyIn_amount.place(x=630, y=370, height=30, width=150)

        self.spending_amount = Label(self.newWin, text=spending_value, font=("Lilita One", 14), fg='#f06292')
        self.spending_amount.place(x=630, y=410, height=30, width=150)

        self.savings_amount = Label(self.newWin, text=savings_value, font=("Lilita One", 14), fg='#f06292')
        self.savings_amount.place(x=630, y=450, height=30, width=150)

        conn.commit()
        conn.close()
    #Playing Lotto Function | Randomized Output | Cuts 2.5 Euros in every try
    def play_lotto(self):
        value = random.randint(0, 100)
        monthList = ['Jan-2021', 'Feb-2021', 'Mar-2021', 'Apr-2021', 'May-2021', 'Jun-2021', 'Jul-2021',
                     'Aug-2021', 'Sep-2021', 'Oct-2021', 'Nov-2021', 'Dec-2021']
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute("INSERT INTO MoneySpent VALUES(:EUROS, :CATEGORY, :PLACE, :STATUS, :DATE, :MONTH)",
                  {
                      'EUROS': 2.50,
                      'CATEGORY': "Guilty Pleasures",
                      'PLACE': "Home",
                      "STATUS": "spending",
                      "DATE": date.today().strftime("%m/%d/%Y"),
                      "MONTH": monthList[int(datetime.now().month)-1]

                  })

        conn.commit()
        conn.close()
        if(value>60):
            conn = sqlite3.connect('expenses.db')
            c = conn.cursor()
            money_earned=random.randint(5, 10)
            c.execute("INSERT INTO MoneySpent VALUES(:EUROS, :CATEGORY, :PLACE, :STATUS, :DATE, :MONTH)",
                      {
                          'EUROS': money_earned,
                          'CATEGORY': "Guilty Pleasures",
                          'PLACE': "Home",
                          "STATUS": "saving",
                          "DATE": date.today().strftime("%m/%d/%Y"),
                          "MONTH": monthList[int(datetime.now().month)-1]

                      })

            conn.commit()
            conn.close()
            tkBox.showinfo("Lotto Message", "You Won "+str(money_earned)+" Euros")
        else:
            tkBox.showinfo("Lotto Message", "Gambling is stupid. You Have Won Nothing")

        self.__init__(root)

    #Select the record for Edit Account page
    def select_record(self):
        global update_row_id
        self.amount_box.delete(0, END)
        self.date_box.delete(0, END)
        self.category_box.delete(0, END)
        try:
            selected = self.my_tree.focus()
            values = self.my_tree.item(selected, 'values')
            self.amount_box.insert(0, values[2])
            self.date_box.insert(0, values[1])
            self.category_box.insert(0, values[3])
            update_row_id=values[0]
        except:
            print("No Rows Selected")

    #Update the record for the selected row from Edit Account page
    def update_record(self):
        # print(self.amount_box.get())
        # print(self.date_box.get())
        # print(self.category_box.get())
        # print(update_row_id)

        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute("UPDATE MoneySpent SET EUROS='"+str(self.amount_box.get())+"', DATE='"+str(self.date_box.get())+"', CATEGORY='"+str(self.category_box.get())+"' WHERE rowid='"+str(update_row_id)+"'")

        conn.commit()
        conn.close()
        self.newWin.destroy()
        self.edit_account()

    #Set the filter dates for Edit Account page
    def filter_record(self):
        global startDate, endDate
        startDate=self.date_first.get()
        endDate=self.date_last.get()
        self.newWin.destroy()
        self.edit_account()

    #Export CSV for the filtered result
    def export_csv(self):
        with open('MoneySpent.csv', 'w', newline='') as file:
            writer=csv.writer(file)
            writer.writerow(["id", "date", "amount", "category", "place", "status"])
            conn = sqlite3.connect('expenses.db')
            c = conn.cursor()
            c.execute("SELECT rowid, DATE, EUROS, CATEGORY, PLACE, STATUS FROM MoneySpent")
            records = c.fetchall()
            for record in records:
                writer.writerow([str(record[0]), str(record[1]), str(record[2]),str(record[3]),str(record[4]),str(record[5]),])

            conn.commit()
            conn.close()

    #Edit Account View
    def edit_account(self):
        self.newWin = Toplevel(root)
        self.newWin.title("EXPENSE TRACKER 2021 ~ Developed by Daniel | Edit Account")
        width = 800
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        self.newWin.geometry(alignstr)
        self.newWin.resizable(width=False, height=False)
        self.lout_btn = Button(self.newWin, command=root.destroy, fg="white", bg="#25BCAF", activebackground="#25BCAF",
                               image=self.btn_imgSet, text="LogOut", compound="right", font=("Lilita One", 16))
        self.lout_btn.place(x=671, y=50)
        self.rtm = Button(self.newWin, command=lambda: self.open_mainMenu(self.newWin), fg="white",
                          bg="#25BCAF", activebackground="#25BCAF", image=self.btn_imgSet,
                          text="Return To Menu", compound="right", font=("Lilita One", 16))
        self.rtm.place(x=593, y=100)

        self.date_first = Entry(self.newWin, width=20, font=("Lilita One", 14))
        self.date_first.insert(END, startDate)
        self.date_first.place(x=70, y=30, height=30, width=150)
        Label(self.newWin,text="Start Range (m/d/y)",font=("Lilita One", 10)).place(x=80, y=70)

        self.date_last = Entry(self.newWin, width=20, font=("Lilita One", 14))
        self.date_last.insert(END, endDate)
        self.date_last.place(x=270, y=30, height=30, width=150)
        Label(self.newWin, text="End Range (m/d/y)", font=("Lilita One", 10)).place(x=280, y=70)

        self.filter_btn = Button(self.newWin, text="Filter", fg="white",
                                bg="#008CFF", font=("Lilita One", 14), command=self.filter_record)
        self.filter_btn.place(x=450, y=30)

        self.my_tree = ttk.Treeview(self.newWin)
        self.my_tree['columns'] = ("id", "date", "amount", "category")
        self.my_tree.column("#0", width=80, minwidth=25)
        self.my_tree.column("id", width=50, minwidth=25)
        self.my_tree.column("date", anchor=W, width=80, minwidth=25)
        self.my_tree.column("amount", anchor=CENTER, width=90, minwidth=25)
        self.my_tree.column("category", anchor=W, width=120, minwidth=25)

        self.my_tree.heading("id", text="id", anchor=W)
        self.my_tree.heading("date", text="date", anchor=W)
        self.my_tree.heading("amount", text="amount", anchor=CENTER)
        self.my_tree.heading("category", text="category", anchor=W)

        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        print(startDate)
        print(endDate)
        c.execute("SELECT rowid, DATE, EUROS, CATEGORY FROM MoneySpent WHERE DATE BETWEEN '"+startDate+"' AND '"+endDate+"'")
        records = c.fetchall()
        for record in records:

            self.my_tree.insert(parent="", index="end", iid=record[0], text="Parent", values=( record[0],record[1], record[2], record[3]))


        conn.commit()
        conn.close()



        self.my_tree.place(x=120, y=120)

        add_frame = Frame(self.newWin)
        add_frame.place(x=140, y=350)

        nl = Label(add_frame, text="Amount")
        nl.grid(row=0, column=0)

        il=Label(add_frame, text="Category")
        il.grid(row=0, column=1)

        tl = Label(add_frame, text="Date")
        tl.grid(row=0, column=2)

        self.amount_box = Entry(add_frame)
        self.amount_box.grid(row=1, column=0)

        self.category_box = Entry(add_frame)
        self.category_box.grid(row=1, column=1)

        self.date_box = Entry(add_frame)
        self.date_box.grid(row=1, column=2)

        self.refresh_btn = Button(self.newWin, text="Refresh", fg="white",
                                 bg="#008CFF", font=("Lilita One", 14), command=self.select_record)
        self.refresh_btn.place(x=140, y=410)

        self.update_btn = Button(self.newWin, text="Update", fg="white",
                                  bg="#008CFF", font=("Lilita One", 14), command=self.update_record)
        self.update_btn.place(x=280, y=410)

        self.export_btn = Button(self.newWin, text="Export CSV", fg="white",
                                  bg="#008CFF", font=("Lilita One", 14), command=self.export_csv())
        self.export_btn.place(x=400, y=410)


if __name__ == "__main__":
    login_view()
    root = tk.Tk()
    if loginVerifier:
        app = App(root)
        root.mainloop()
    else:
        print("Did Not Login")

