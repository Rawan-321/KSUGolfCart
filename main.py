#you need to import the class so you can use the methods
import logging
logging.basicConfig(filename='ReservationLog.log',
                  filemode='a',
                  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                  level=logging.DEBUG)

from db import (insert_user,get_user_by_id,get_userClass_by_id,get_admin_by_id,get_reservation_by_userID,
                get_reservation_by_plateNumber,insertGolfCart,insert_golf_cart,get_golf_cart_by_id,
                get_available_golf_carts,get_all_golf_Carts,insert_reservation,create_connection)

from User import User
from Reservation import Reservation
import tkinter as tk
from tkinter import ttk
import tkinter
from tkinter import messagebox
import hashlib
from datetime import datetime,timedelta,date
import re
from Golf_Cart import Golf_Cart
import csv
conn=create_connection("app.db")
c=conn.cursor()

class MyGUI:
    def __init__(self):
        self.main_window = tkinter.Tk()
        self.main_window.title('KSU Golf Cart')
        self.main_window.geometry('440x500')
        self.main_window.configure(bg='white')
        Font = ('Times', 15)

        self.labelframe = tkinter.LabelFrame(self.main_window, text='Sign up window ')
        self.labelframe.config()


        # labels
        self.welcome_label = tkinter.Label(self.labelframe, text="welcome to KSU golf cart system ", font=Font)
        self.sign_up_lable=tkinter.Label(self.labelframe,text="",font=Font,foreground="blue")
        self.ID_label = tkinter.Label(self.labelframe, text='ID:', font=Font)
        self.ID_validate_label = tkinter.Label(self.labelframe, fg="red")
        self.first_name_label = tkinter.Label(self.labelframe, text='First Name:', font=Font)
        self.first_validate_label = tkinter.Label(self.labelframe,foreground="red")
        self.last_name_label = tkinter.Label(self.labelframe, text='Last Name:', font=Font)
        self.last_validate_label = tkinter.Label(self.labelframe,fg="red")
        self.user_class_label = tkinter.Label(self.labelframe, text="User Class:", font=Font)
        self.email_label = tkinter.Label(self.labelframe, text='Email Address:', font=Font)
        self.email_validate_label=tkinter.Label(self.labelframe, foreground="red")
        self.phone_number_label = tkinter.Label(self.labelframe, text='Phone Number:', font=Font)
        self.phone_validate_label=tkinter.Label(self.labelframe,fg="red")
        self.password_label = tkinter.Label(self.labelframe, text='Password:', font=Font)
        self.password_validate_label = tkinter.Label(self.labelframe, fg="red")

        # user class menu
        self.classOption = tkinter.StringVar()
        self.classOption.set("Student")  # Default value
        self.class_options = ["Student", "Faculty", "Employee"]
        self.class_dropdown = tkinter.OptionMenu(self.labelframe, self.classOption, *self.class_options)
        self.class_dropdown.config(font=Font, bg='white')

        # entries
        self.IDEntry = tkinter.Entry(self.labelframe, font=Font,validatecommand=self.is_ID_valid,validate="focusout")
        self.firstNameEntry = tkinter.Entry(self.labelframe, font=Font, validatecommand=self.is_first_valid,
                                            validate="focusout")
        self.lastNameEntry = tkinter.Entry(self.labelframe, font=Font, validatecommand=self.is_last_valid,
                                           validate="focusout")
        self.emailEntry = tkinter.Entry(self.labelframe, font=Font,validatecommand=self.is_email_valid,
                                        validate="focusout")
        self.phoneEntry = tkinter.Entry(self.labelframe, font=Font,validatecommand=self.is_phone_valid,
                                        validate="focusout")
        self.passEntry = tkinter.Entry(self.labelframe, font=Font, show="*",validatecommand=self.is_password_valid,
                                       validate="focusout")

        # buttons
        self.submit = tkinter.Button(self.labelframe, text="Submit", command=self.submit, font=Font, bg='white')
        self.login = tkinter.Button(self.labelframe, text="Login", font=Font, bg='white',
                                    command=self.destroy_main_window)

        # pack
        self.welcome_label.grid(row=0, column=0, sticky="new", columnspan=2)
        self.sign_up_lable.grid(row=1, column=0,sticky="news",columnspan=2)
        self.user_class_label.grid(row=2, column=0, sticky="e", pady=30)
        self.ID_label.grid(row=3, column=0, sticky='e')
        self.ID_validate_label.grid(row=4,column=1)
        self.first_name_label.grid(row=5, column=0, sticky='e')
        self.first_validate_label.grid(row=6,column=1)
        self.last_name_label.grid(row=7, column=0, sticky='e')
        self.last_validate_label.grid(row=8, column=1)
        self.email_label.grid(row=9, column=0, sticky='e')
        self.email_validate_label.grid(row=10,column=1)
        self.phone_number_label.grid(row=11, column=0, sticky='e')
        self.phone_validate_label.grid(row=12,column=1)
        self.password_label.grid(row=13, column=0, sticky='e')
        self.password_validate_label.grid(row=14,column=1)

        self.class_dropdown.grid(row=2, column=1, sticky='w')

        self.IDEntry.grid(row=3, column=1, sticky='w')
        self.firstNameEntry.grid(row=5, column=1, sticky='w')
        self.lastNameEntry.grid(row=7, column=1, sticky='w')
        self.emailEntry.grid(row=9, column=1, sticky='w')
        self.phoneEntry.grid(row=11, column=1, sticky='w')
        self.passEntry.grid(row=13, column=1, sticky='w')

        self.submit.grid(row=15, column=1, sticky='w')
        self.login.grid(row=15, column=0, sticky='e')

        self.labelframe.pack()


        tkinter.mainloop()

    def check_ID_accuracy(self,classOption,ID):
        if ( classOption == "Employee") and (len(ID) == 6):
            return True
        if ( classOption == "Faculty") and (len(ID) == 6):
            return True
        if(classOption == "Student" and len(ID) == 10):
            return True
        else:
            return False
    def check_ID_not_exists(self,ID):
        value = get_user_by_id(ID)
        if len(value) ==0:
            return True
        else:
            return False
    def display_error_massage(self,ID):
        if (self.classOption.get() == "Employee") and (len(ID) != 6):
            self.ID_validate_label.configure(text="Employee ID should be 6 digits\n"
                                                  "Please enter a valid ID")
        elif (self.classOption.get() == "Faculty") and (len(ID) != 6):
            self.ID_validate_label.configure(text="Faculty ID should be 6 digits\n"
                                                  "Please enter a valid ID")
        elif len(ID) != 10 and self.classOption.get() == "Student":
            self.ID_validate_label.configure(text="Student ID should be 10 digits\n"
                                                  "Please enter a valid ID")
        else:
            self.ID_validate_label.configure(text="something wrong")

    def submit(self):
        ID=self.IDEntry.get()
        first=self.firstNameEntry.get()
        last=self.lastNameEntry.get()
        password=hashlib.sha256(self.passEntry.get().encode()).hexdigest()
        email=self.emailEntry.get()
        phone=self.phoneEntry.get()
        userClass=self.classOption.get()
        classOption=self.classOption.get()
        value = get_user_by_id(ID)
        if not self.check_ID_not_exists(ID):
            tkinter.messagebox.showinfo("Error", "The ID already exists\n "
                                                 "try signing in")
        elif not self.is_ID_valid():
            self.is_ID_valid()
        elif not self.is_password_valid():
            self.is_password_valid()
        elif not self.is_email_valid():
            self.is_email_valid()
        elif not self.is_phone_valid():
            self.is_phone_valid()
        elif not self.is_first_valid():
            self.is_first_valid()
        elif not self.is_last_valid():
            self.is_last_valid()
        else:
            user=User(ID,first,last,password,email,phone,userClass)
            insert_user(user)
            self.sign_up_lable.configure(text="you have signed up successfully")


    def destroy_main_window(self):
       self.main_window.destroy()
       login()

    def is_first_valid(self):
        entry=self.firstNameEntry.get()

        if len(entry)==0:
            self.first_validate_label.configure(text="Please enter your first name")
            return False
        elif entry.isdigit():
            self.first_validate_label.configure(text="Please enter only characters")
            return False
        elif (len(entry)>0) and (entry.isalpha()):
            self.first_validate_label.configure(text="")
            return True

    def is_last_valid(self):
        entry=self.lastNameEntry.get()

        if len(entry)==0:
            self.last_validate_label.configure(text="Please enter your first name")
            return False
        elif entry.isdigit():
            self.last_validate_label.configure(text="Please enter only characters")
            return False
        elif (len(entry)>0) and (entry.isalpha()):
            self.last_validate_label.configure(text="")
            return True

    def is_password_valid(self):
        entry=self.passEntry.get()

        if len(entry)==0:
            self.password_validate_label.configure(text="Please enter password")
            return False
        elif  len(entry) >= 6:
            self.password_validate_label.configure(text="")
            return True
        elif  len(entry) < 6:
            self.password_validate_label.configure(text="Enter at least 6 digits or characters")
            return False

    def is_ID_valid(self):
        entry=self.IDEntry.get()
        if self.classOption.get()=="Student":
            if len(entry)==0:
                self.ID_validate_label.configure(text="Please inter ID")
                return False
            elif entry.isdigit() and len(entry) == 10:
                self.ID_validate_label.configure(text="")
                return True
            # elif entry.isalpha() :
            #     self.ID_validate_label.configure(text="please enter only integers")
            #     return False
            elif len(entry) !=10:
                self.ID_validate_label.configure(text="Please enter 10 digits")
                return False
            else:
                self.ID_validate_label.configure(text="Please enter only integers")
                return False

        else:
            if len(entry) == 0:
                self.ID_validate_label.configure(text="please inter ID")
                return False
            elif entry.isdigit() and len(entry) == 6:
                self.ID_validate_label.configure(text="")
                return True
            elif entry.isalpha() and entry.isdigit():
                self.ID_validate_label.configure(text="please enter only integers")
                return False
            elif len(entry) != 6:
                self.ID_validate_label.configure(text="please enter 6 digits")
                return False

    def is_email_valid(self):
        reg = "^([a-zA-Z0-9]){8}(@ksu\.edu\.sa)$"
        pat = re.compile(reg)
        email=self.emailEntry.get()
        x=re.search(pat,email)
        if x:
            self.email_validate_label.configure(text="")
            return True
        else:
            self.email_validate_label.configure(text="the email format is  XXXXXXXX@ksu.edu.sa)")
            return False

    def is_phone_valid(self):
        entry=self.phoneEntry.get()
        reg = "^(05)([0-9]){8}$"
        pat = re.compile(reg)
        x=re.search(pat,entry)
        if x:
            self.phone_validate_label.configure(text="")
            return True
        else:
            self.phone_validate_label.configure(text="the phone format is 05XXXXXXXX")
            return False

class login():
    # global_ID = None
    def __init__(self):
     self.login_window=tkinter.Tk()
     self.login_window.title("Login form")
   #  self.login_window.configure(background="white")
     self.login_window.geometry("440x500")
     Font = ('Times', 15)


#widgets
     self.frame=tkinter.Frame(self.login_window)
     self.button_frame=tkinter.Frame(self.frame)

     self.login_label=tkinter.Label(self.frame, text="Login", fg="black",font =('Times', 20))
     self.ID_label=tkinter.Label(self.frame, text="ID", fg="black", font=Font )
     self.password_label=tkinter.Label(self.frame, text="Password", fg="black",
                                       font=Font)
     self.ID_entry=tkinter.Entry(self.frame,validatecommand=self.is_ID_valid,validate="focusout")
     self.ID_validate_label=tkinter.Label(self.frame, fg="red")
     # self.ID_entry.bind("<FocusIn>", self.temp_text)
     # self.ID_entry.insert(0,"6 or 10 digits")
     self.password_entry=tkinter.Entry(self.frame,show="*",validatecommand=self.is_password_valid,validate="focusout")
     self.password_validate_label = tkinter.Label(self.frame, fg="red")
     self.login_button=tkinter.Button(self.button_frame,text="Login",fg="black",font=Font,
                                      command=self.check_credentials)
     self.sign_up_button=tkinter.Button(self.button_frame,text="sign up",fg="black",
                                        command=self.back_to_sign_up,font=Font)

#pack
     self.login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=15)
     self.ID_label.grid(row=1, column=0)
     self.password_label.grid(row=3, column=0)
     self.ID_entry.grid(row=1,column=1)
     self.ID_validate_label.grid(row=2, column=1)
     self.password_entry.grid(row=3,column=1)
     self.password_validate_label.grid(row=4, column=1)
     self.login_button.grid(row=5,column=1,sticky="news")     #pady=20
     self.sign_up_button.grid(row=5,column=0,sticky="news")

     self.button_frame.grid(row=5,column=0,columnspan=2)
     self.frame.pack()
     self.login_window.mainloop()

    def back_to_sign_up(self):
        self.login_window.destroy()
        MyGUI()

    def is_ID_valid(self):
        entry=self.ID_entry.get()
        if len(entry)==0:
            self.ID_validate_label.configure(text="please inter ID")
            return True
        elif entry.isdigit() and len(entry) == 6:
            self.ID_validate_label.configure(text="")
            return True
        elif entry.isalpha():
            self.ID_validate_label.configure(text="please enter only integers")
            return False
        elif entry.isdigit() and len(entry) == 10:
            self.ID_validate_label.configure(text="")
            return True
        elif len(entry)!=6 or len(entry) !=10:
            self.ID_validate_label.configure(text="please enter 6 or 10 digits")
            return False


    def is_password_valid(self):
        entry=self.password_entry.get()

        if len(entry)==0:
            self.password_validate_label.configure(text="please enter password")
            return True
        elif  len(entry) >= 6:
            self.password_validate_label.configure(text="")
            return True
        elif  len(entry) < 6:
            self.password_validate_label.configure(text="the password is at least 6 digits or characters")
            return False

    def check_ID_exists(self,ID):
        value = get_user_by_id(ID)
        if len(value) !=0:
            return True
        ad=get_admin_by_id(ID)
        if len(ad) != 0:
            return True
        else:
            return False

    def check_pass_accuracy(self,password,id):
            user = get_user_by_id(id)
            if len(user)== 0:
                return False
            userpass = user[0][3]
            inpass = hashlib.sha256(password.encode()).hexdigest()
            if userpass == inpass:
                return True
            else:
                return False

    def get_login_ID(self):
        global_ID = self.ID_entry.get()
        return global_ID

    def check_admin_or_not(self,ID,password):
        ad = get_admin_by_id(ID)
        if len(ad)==0:
            return False
        else:
            admin_pass=ad[0][1]
            checkpass = hashlib.sha256(password.encode()).hexdigest()
            if admin_pass == checkpass:
                return True
            else:
                return False

    def check_credentials(self):
        # global global_ID
        global_ID=self.ID_entry.get()
        password=self.password_entry.get()
        if self.check_admin_or_not(global_ID,password):
            self.login_window.destroy()
            AdminWindow()
        if not self.is_ID_valid():
            self.is_ID_valid()
        elif not self.is_password_valid():
            self.is_password_valid()
        elif not self.check_ID_exists(global_ID):
            self.ID_validate_label.configure(text="please enter 6 or 10 digits")
        elif not self.check_pass_accuracy(password, global_ID):
            self.password_validate_label.configure(text="the password is not correct\ntry again")
        else:
                self.login_window.destroy()
                GolfCartReservationApp(global_ID)

class GolfCartReservationApp:
    def __init__(self,global_ID):
        self.root = tk.Tk()
        Font = ('Times', 15)
        self.root.title("KSU Golf Cart Reservation ")
        #self.root.geometry("380x480")
        self.notebook = ttk.Notebook(self.root)
        self.reserve_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.reserve_tab, text="Reserve a Cart")
        # self.create_reserve_tab()
        self.secondFrame = tk.LabelFrame(self.reserve_tab, text='reserve a cart', font=Font)
        self.ID=global_ID

        #comboBox
        self.Option = tk.StringVar()
        self.available_carts = get_all_golf_Carts()
        self.cb=ttk.Combobox(self.secondFrame,textvariable=self.Option)
        self.cb['values']=self.available_carts
        self.cb.config(font=Font)
        self.cb.grid(row=1, column=1, sticky='e')
        self.cb.current(0)

        # labels
        self.golfListLabel = tk.Label(self.secondFrame, text='choose a golf cart', font=Font).grid(row=1, column=0, sticky='w')
        self.dateLabel = tk.Label(self.secondFrame, text='Enter date of reservation', font=Font).grid(row=2, column=0,sticky='w')
        self.startLabel = tk.Label(self.secondFrame, text='Enter starting time of reservation', font=Font).grid(row=4,column=0,sticky='w')
        self.endLabel = tk.Label(self.secondFrame, text='Enter ending time of reservation', font=Font).grid(row=6, column=0,sticky='w')

        # validation labels
        self.start_time_validate_lable = tk.Label(self.secondFrame, bg="white", fg="red")
        self.end_time_validate_lable = tk.Label(self.secondFrame, bg="white", fg="red")
        self.date_validate_lable = tk.Label(self.secondFrame, bg="white", fg="red")
        self.reservation_period_valid_lable=tk.Label(self.secondFrame,bg="white", fg="red")
        self.check_reservation_conflict_lable = tk.Label(self.secondFrame, bg="white", fg="red")

        #entries
        self.dateEntry = tk.Entry(self.secondFrame, validatecommand=self.is_date_valid, validate="focusout")
        self.startEntry = tk.Entry(self.secondFrame, validatecommand=self.is_start_time_valid, validate="focusout")
        self.endEntry = tk.Entry(self.secondFrame, validatecommand=self.is_end_time_valid, validate="focusout")

        #buttons
        self.confirmRes = tk.Button(self.secondFrame, text='reserve', font=Font, command=self.confirm)
        self.confirmRes.grid(row=10, column=0, sticky='')
        self.logOut = tk.Button(self.secondFrame, text='log out', font=Font, command=self.logout)
        self.logOut.grid(row=10, column=0, sticky='e')


        self.view_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.view_tab, text="View My Reservations")
        self.create_view_tab()


        # packs
        self.dateEntry.grid(row=2, column=1, sticky='e')
        self.date_validate_lable.grid(row=3, column=1, sticky='e')
        self.startEntry.grid(row=4, column=1, sticky='e')
        self.start_time_validate_lable.grid(row=5, column=1, sticky='e')
        self.endEntry.grid(row=6, column=1, sticky='e')
        self.end_time_validate_lable.grid(row=7, column=1, sticky='e')
        self.reservation_period_valid_lable.grid(row=8, column=0, sticky='e')
        self.check_reservation_conflict_lable.grid(row=9,column=0, sticky='e')

        self.notebook.pack()
        self.secondFrame.pack()

        self.root.mainloop()

    def create_view_tab(self):

        label = tk.Label(self.view_tab, text="Your Reservations:")
        label.pack(pady=10)

        self.reservation_listbox = tk.Listbox(self.view_tab, selectmode=tk.SINGLE, width=50, height=10)
        self.reservation_listbox.pack(pady=10)

        show_button = tk.Button(self.view_tab, text="Show Active Reservations", command=self.show_all_reservations)
        show_button.pack(pady=10)

        logout_button = tk.Button(self.view_tab, text="Logout", command=self.back_to_sign_up)

        logout_button.pack(pady=10)

    def show_all_reservations(self):
        # Connect to the SQLite database
        conn = create_connection("app.db")
        c = conn.cursor()
        c.execute("SELECT * FROM reservation WHERE user_ID = ?",
                  (self.ID,))
        reservations_data = c.fetchall()

        # Clear the listbox
        self.reservation_listbox.delete(0, tk.END)
        try:
            if len(reservations_data) !=0:
                for reservation in reservations_data:
                    dateTime1 = datetime.strptime(reservation[2], "%d/%m/%Y")
                   # if dateTime1 >= datetime.today():
                    display_text = f"Start Time: {reservation[0]} | End Time: {reservation[1]} | " \
                                   f"Date: {reservation[2]} | user ID: {reservation[3]} | "\
                                   f"Plate Number:{reservation[4]}"
                    self.reservation_listbox.insert(tk.END, display_text)
            else:
                display=f"There is no active reservations"
                self.reservation_listbox.insert(tk.END,display)
        except ValueError as e:
            print(e)
        conn.close()

    def back_to_sign_up(self):
        self.root.destroy()
        MyGUI()

    def is_start_time_valid(self):
        entry = self.startEntry.get()
        Format = r"^(2[0-3]|[01]?[0-9]):([0-5]?[0-9])$"
        match = re.match(Format, entry)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2))
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                self.start_time_validate_lable.configure(text="")
                return True
        self.start_time_validate_lable.configure(text="please enter time in 24-hour-format (HH:MM)")
        return False

    def is_end_time_valid(self):
        entry = self.endEntry.get()
        Format = r"^(2[0-3]|[01]?[0-9]):([0-5]?[0-9])$"
        match = re.match(Format, entry)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2))
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                self.end_time_validate_lable.configure(text="")
                return True
        self.end_time_validate_lable.configure(text="please enter time in 24-hour-format (HH:MM)")
        return False

    def is_date_valid(self):
        entry = self.dateEntry.get()
        if len(entry) != 10:
            self.date_validate_lable.configure(text="please enter date in DD/MM/YYYY format")
            return False
        day, month, year = entry.split("/")
        if len(day) != 2 or len(month) != 2 or len(year) != 4:
            self.date_validate_lable.configure(text="please enter date in DD/MM/YYYY format")
            return False
        try:
            dateObj = datetime.strptime(entry, "%d/%m/%Y")
            if dateObj.year >= 2023:
                self.date_validate_lable.configure(text="")
                return True
            else:
                self.date_validate_lable.configure(text="The year should be 2023 or greater")
                return False
        except ValueError:
            self.date_validate_lable.configure(text="please enter date in DD/MM/YYYY format")
            return False

    def is_reservation_period_valid(self, startEntry, endEntry, user_type):
        # calculate time period
        selected_cart = self.Option.get()
        s1 = startEntry
        s2 = endEntry  
        FMT = '%H:%M'
        tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)

        if tdelta.days < 0:
            self.reservation_period_valid_lable.configure(text="the start time is greater than end time\ntry again")
            logging.info(
                f'A reservation have been declined due to entering invalid time made by user with ID:{self.ID} '
                f'for the cart with Plate number:'
                f'{selected_cart[0:4]} and Location {selected_cart[5:]}'
                f'and Start time={startEntry} and End time={endEntry} and Date={self.dateEntry.get()}')
            return False
        # validate time based on user type
        if user_type == "Student":
            student_time = timedelta(hours=00, minutes=30, seconds=00)
            if tdelta > student_time or tdelta.days<0:
                self.reservation_period_valid_lable.configure(
                    text="Student can not reserve golf cart more than 30 mins")
                logging.info(
                    f'A reservation have been declined due to time exceeding the time limit made by user with ID:{self.ID} '
                    f'for the cart with Plate number:'
                    f'{selected_cart[0:4]} and Location {selected_cart[5:]}'
                    f'and Start time={startEntry} and End time={endEntry} and Date={self.dateEntry.get()}')
                return False
            else:
                self.reservation_period_valid_lable.configure(
                    text="")
                return True
        if user_type == "Employee":
            Employee_time = timedelta(hours=1, minutes=00, seconds=00)
            if tdelta > Employee_time or tdelta.days<0:
                self.reservation_period_valid_lable.configure(
                    text="employee can not reserve golf cart more than one Hour")
                logging.info(
                    f'A reservation have been declined due to time exceeding the time limit made by user with ID:{self.ID} '
                    f'for the cart with Plate number:'
                    f'{selected_cart[0:4]} and Location {selected_cart[5:]}'
                    f'{selected_cart[0:4]} and Location {selected_cart[5:]}'
                    f'and Start time={startEntry} and End time={endEntry} and Date={self.dateEntry.get()}')
                return False
            else:
                self.reservation_period_valid_lable.configure(
                    text="")
                return True
        if user_type == "Faculty":
            faculty_time= timedelta(hours=1, minutes=30, seconds=00)
            if tdelta > faculty_time or tdelta.days<0:
                self.reservation_period_valid_lable.configure(
                    text="Faculty can not reserve golf cart more than one 1:30 Hour")
                logging.info(
                    f'A reservation have been declined due to time exceeding the time limit made by user with ID:{self.ID} '
                    f'for the cart with Plate number:'
                    f'{selected_cart[0:4]} and Location {selected_cart[5:]}'
                    f'{selected_cart[0:4]} and Location {selected_cart[5:]}'
                    f'and Start time={startEntry} and End time={endEntry} and Date={self.dateEntry.get()}')
                return False
            else:
                self.reservation_period_valid_lable.configure(
                    text="")
                return True

    def check_reservation_conflict(self):
        start_time = self.startEntry.get()
        end_time = self.endEntry.get()
        selected_date = self.dateEntry.get()
        selected_cart = self.Option.get()
        selected_cart_plate_number = selected_cart[0:4]
        cart=get_golf_cart_by_id(selected_cart_plate_number)
        all_reservation = get_reservation_by_plateNumber(selected_cart_plate_number)

        for reservation in all_reservation:
            if (reservation[0] == start_time and reservation[2] == selected_date) or \
                    (reservation[1] == end_time and reservation[2] == selected_date) or \
                    (reservation[0] <= start_time < reservation[1] and reservation[2] == selected_date) or \
                    (reservation[0] < end_time <= reservation[1] and reservation[2] == selected_date):
                self.check_reservation_conflict_lable.configure(text="This golf cart is reserved, choose another one")
                return False
        self.check_reservation_conflict_lable.configure(text="")
        return True
    def logout(self):
        self.root.destroy()
        MyGUI()

    def confirm(self):
        user = get_user_by_id(self.ID)
        user_type = user[0][6]
        start_time = self.startEntry.get()
        end_time = self.endEntry.get()
        selected_date=self.dateEntry.get()

        if not self.is_date_valid():
            logging.info(
                f'have been declined due to not entering the right format for date made by user with ID:{self.ID} '
                f'for the cart with Plate number:'
                f'{self.Option.get()[0:4]} and Location {self.Option.get()[5:]}'
                f'and Start time={self.startEntry.get()} and End time={self.endEntry.get()} and Date={self.dateEntry.get()}')
            self.is_date_valid()
        elif not self.is_start_time_valid():
            logging.info(
                f'A reservation have been declined due to not entering the right format for time made by user with ID:{self.ID} '
                f'for the cart with Plate number:'
                f'{self.Option.get()[0:4]} and Location {self.Option.get()[5:]}'
                f'and Start time={self.startEntry.get()} and End time={self.endEntry.get()} and Date={self.dateEntry.get()}')
            self.is_start_time_valid()
        elif not self.is_end_time_valid():
            logging.info(
                f'A reservation have been declined due to not entering the right format for time made by user with ID:{self.ID} '
                f'for the cart with Plate number:'
                f'{self.Option.get()[0:4]} and Location {self.Option.get()[5:]}'
                f'and Start time={self.startEntry.get()} and End time={self.endEntry.get()} and Date={self.dateEntry.get()}')
            self.is_end_time_valid()
        elif not self.is_reservation_period_valid(start_time, end_time, user_type):
            self.is_reservation_period_valid(start_time, end_time, user_type)
        elif not self.check_reservation_conflict():
            logging.info(
                f'A reservation have been declined due to conflict in time made by user with ID:{self.ID} '
                f'for the cart with Plate number:'
                f'{self.Option.get()[0:4]} and Location {self.Option.get()[5:]}'
                f'and Start time={start_time} and End time={end_time} and Date={selected_date}')
            self.check_reservation_conflict()
        else :
            res = Reservation(start_time, end_time, selected_date)
            all_re=get_reservation_by_plateNumber(self.Option.get()[0][0])
            if res in all_re:
                self.check_reservation_conflict_lable.configure(text="The reservation already exists")
            insert_reservation(res, self.ID, self.Option.get()[0:4])
            self.check_reservation_conflict_lable.configure(text="Your reservation is complete successfully")

class AdminWindow:
    def __init__(self):
        self.admin_window = tk.Tk()
        self.admin_window.title('Admin Window')
        self.admin_window.geometry('400x300')
        self.admin_window.configure(bg='white')

        Font = ('Times', 15)

        self.labelframe = tk.LabelFrame(self.admin_window, text='Admin Panel')
        self.labelframe.config()

        # labels and entries
        self.plate_number_label = tk.Label(self.labelframe, text='Plate Number:', font=Font)
        self.plate_number_entry = tk.Entry(self.labelframe,font=Font)

        self.college_label = tk.Label(self.labelframe, text='College:', font=Font)
        self.college_entry = tk.Entry(self.labelframe, font=Font)

        # buttons
        self.create_button = tk.Button(self.labelframe, text='Create', command=self.create_golf_cart, font=Font,
                                       bg='white')
        self.logout_button = tk.Button(self.labelframe, text='Logout', command=self.logout, font=Font, bg='white')
        self.backup_button = tk.Button(self.labelframe, text='Backup', command=self.backup_database, font=Font,
                                       bg='white')

        # labels for error messages
        self.plate_error_label = tk.Label(self.labelframe, text='', font=('Arial', 12), fg='red')
        self.college_error_label = tk.Label(self.labelframe, text='', font=('Arial', 12), fg='red')

        # pack
        self.plate_number_label.grid(row=0, column=0, sticky='e')
        self.plate_number_entry.grid(row=0, column=1, sticky='w')
        self.plate_error_label.grid(row=1, column=0, columnspan=2, pady=5)

        self.college_label.grid(row=2, column=0, sticky='e')
        self.college_entry.grid(row=2, column=1, sticky='w')
        self.college_error_label.grid(row=3, column=0, columnspan=2, pady=5)

        self.create_button.grid(row=4, column=0, columnspan=2, pady=10)
        self.logout_button.grid(row=5, column=0,columnspan=1, pady=10)
        self.backup_button.grid(row=5, column=1, columnspan=2, pady=10)

        self.labelframe.pack(pady=20)

        self.admin_window.mainloop()

    def create_golf_cart(self):
        if self.is_plate_number_valid() and self.is_college_valid():
            plate_number = self.plate_number_entry.get()
            college = self.college_entry.get()
            golfCartOBJ = Golf_Cart(plate_number, college)
            if len(get_golf_cart_by_id(plate_number))==0:
                insert_golf_cart(golfCartOBJ)
                self.show_info_message("Golf cart added successfully!")
            else:
                self.show_info_message("there is already a cart with the same plate number")

    def is_plate_number_valid(self):
        plate_number = self.plate_number_entry.get()
        if not plate_number.isdigit():
            self.plate_error_label.config(text="Please enter a valid plate number; letters are not accepted.")
            return False
        elif len(plate_number)!=4:
            self.plate_error_label.config(text="the Plate Number should consist of only 4 integers")
        elif plate_number.isdigit() and len(plate_number)==4:
            self.plate_error_label.config(text="")
            return True

    def is_college_valid(self):
        college = self.college_entry.get()
        if college.isdigit():
            self.college_error_label.config(text="Please enter a valid college name; numbers are not accepted.")
            return False
        else:
            self.college_error_label.config(text="")
            return True

    def logout(self):
        self.admin_window.destroy()
        MyGUI()

    def backup_database(self):
        try:
            conn = create_connection("app.db")
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                csv_file_path = "db_backup.csv"
                with open(csv_file_path, 'a', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow([description[0] for description in cursor.description])
                    csv_writer.writerows(rows)
                    csv_file.close()
            conn.close()
            messagebox.showinfo("Backup", "Database backed up successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Error during backup: {str(e)}")

    def show_info_message(self, message):
        tk.messagebox.showinfo("Info", message)


MyGUI()
