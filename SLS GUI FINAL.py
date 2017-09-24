from tkinter import *
import pymysql
import os
import time
import datetime
import tkinter.ttk as ttk
from tkinter import messagebox

class SLSGUI:

    def __init__(self, win):
        self.win = win
        self.loginWin()
        self.cityStates()
        
    def connect(self):
        hostname = "academic-mysql.cc.gatech.edu" 
        password = "MdInm4Dl"
        username = "cs4400_67"
        dbname = "cs4400_67"
        db = pymysql.connect(host = hostname, passwd = password, user = username, db=dbname)
        return db

    def close(self, cursor, db):
        cursor.close()
        db.commit()
        db.close()
        return

    def cityStates(self):
        db = self.connect()
        cursor = db.cursor()
        sql = "SELECT DISTINCT city FROM cityState"
        cursor.execute(sql)
        self.cityList = list(cursor)
        sql = "SELECT DISTINCT state FROM cityState"
        cursor.execute(sql)
        self.stateList = list(cursor)

    def loginWin(self):
        self.win.title("Log In")
        f = Frame(self.win, background = "azure")
        f.grid()
        Label(f, text = "Welcome! Please login to begin.", background = "gold").grid(row=0,column = 0, sticky =W+E)
        f1 = Frame(f, background = "azure")
        f1.grid(row = 1, column=0, sticky = E+W)
        self.photo = PhotoImage(file = "5GjN8X2.gif")
        l = Label(image = self.photo)
        l.image = self.photo
        Label(f1, text = "Username:", background = "azure", width =27).grid(row=0, column=0, sticky =W)
        Label(f1, text = "Password:", background = "azure", width =27).grid(row=1, column=0, sticky = W)
        self.username = StringVar()
        Entry(f1, textvariable = self.username, width=27).grid(row=0, column=1, sticky = E)
        self.password = StringVar()
        Entry(f1, textvariable = self.password, width=27).grid(row=1, column=1, sticky = E)
        Button(f1, text= "Log In", width = 10, command = self.loginCheck).grid(row=2, column=0)
        Button(f1, text = "Register", width=10, command = self.registerWin).grid(row=2, column=1)
        l.grid(row=2, column=0)

    def registerWin(self):       
        self.registerWin = Toplevel()
        self.win.withdraw()
        self.registerWin.title("New User Registration")
        f = Frame(self.registerWin, background = "azure")
        f.grid()
        Label(f, text = "Please register below.", background = "gold").grid(row=0, column=0, sticky =W+E)
        f1 = Frame(f, background = "azure")
        f1.grid(row=1, column = 0, sticky=E+W)
        Label(f1, text = "Username:", background = "azure").grid(row = 0, column = 0, sticky = E, pady = 5, padx = 5)
        Label(f1, text = "Email Address:", background = "azure").grid(row = 1, column = 0, sticky = E, pady = 5, padx = 5)
        Label(f1, text = "Password:", background = "azure").grid(row =2, column = 0, sticky = E, pady = 5, padx = 5)
        Label(f1, text = "Confirm Password:", background = "azure").grid(row = 3, column = 0, sticky = E, pady = 5, padx = 5)
        Label(f1, text = "User Type:", background = "azure").grid(row = 4, column =0, sticky = E, pady = 5, padx=5)
        self.Rusername = StringVar(self.registerWin)
        Entry(f1, textvariable = self.Rusername, width = 30).grid(row = 0, column = 1, sticky = W)
        self.Remail = StringVar(self.registerWin)
        Entry(f1, textvariable = self.Remail, width = 30).grid(row = 1, column = 1, sticky = W)
        self.Rpassword = StringVar(self.registerWin)
        Entry(f1, textvariable = self.Rpassword, width = 30).grid(row = 2, column = 1, sticky = W)
        self.RpasswordCheck = StringVar(self.registerWin)
        Entry(f1, textvariable = self.RpasswordCheck, width = 30).grid(row = 3, column = 1, sticky = W)
        self.type = StringVar(self.registerWin)
        m = OptionMenu(f1, self.type, "city official", "city scientist")
        m.grid(row = 4, column = 1, sticky = W)
        m.config(width=30)
        l = Label(f, text ="Please fill out the data below if you choose city official:", background = "gold")
        l.grid(row=2, column =0, sticky = E+W)
        f2 = Frame(f, background = "azure")
        f2.grid(row=3, column =0, sticky=E+W)
        Label(f2, text = "City:", background = "azure").grid(row = 0, column = 0, sticky = E)
        Label(f2, text = "State:", background = "azure").grid(row = 1, column = 0, sticky = E)
        self.cityvar = StringVar(self.registerWin)
        city = OptionMenu(f2, self.cityvar, *self.cityList)
        city.grid(row = 0, column = 1, sticky =E)
        city.config(width = 20)
        self.statevar = StringVar(self.registerWin)
        state = OptionMenu(f2, self.statevar, *self.stateList)
        state.grid(row = 1, column = 1, sticky = E)
        state.config(width = 20)
        Label(f2, text = "Title:", background = "azure").grid(row=2, column=0, sticky = E)
        self.title = StringVar(self.registerWin)
        Entry(f2, textvariable = self.title, width = 20).grid(row=2, column=1, sticky= E)
        Button(f, text = "Create", width = 10, command = self.registerCheck).grid(row=4, column = 0)

    def registerCheck(self):
        db = self.connect()
        cursor = db.cursor()
        password = self.Rpassword.get()
        passwordCheck = self.RpasswordCheck.get()
        username = self.Rusername.get()
        email = self.Remail.get()
        type1 = self.type.get()
        cursor.execute("SELECT username FROM user WHERE username = '"+username+"'")
        usernames = list(cursor)
        cursor.execute("SELECT emailAddress FROM user WHERE emailAddress = '"+email+"'")
        emails = list(cursor)
        if len(usernames) != 0 or username.strip() == "":
            messagebox.showerror("ERROR", "Username is already taken or was left blank!")
            return
        if len(emails) != 0 or email.strip() == "":
            messagebox.showerror("ERROR", "Email is already registered or was left blank!")
            return
        if password != passwordCheck or password.strip() == "":
            messagebox.showerror("ERROR", "Passwords don't match or field was left empty!")
            return
        if type1 == "":
            messagebox.showerror("ERROR", "Please pick user type!")
            return
        if type1 == "city scientist":
            sql = "INSERT INTO user (username, emailAddress, pass, userType) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (username, email, password, type1))
            self.close(cursor, db)
            messagebox.showinfo("Success!", "Registration was successful.")
            self.registerWin.destroy()
            self.win.deiconify()
        if type1 == "city official":
            city = self.cityvar.get()
            state = self.statevar.get()
            title = self.title.get()
            sql = "SELECT city, state FROM cityState WHERE city='"+city[2:-3]+"' AND state='"+state[2:-3]+"'"
            num = cursor.execute(sql)
            if num == 0:
                messagebox.showerror("ERROR", "City and State combination is invalid.")
                return
            sql = "INSERT INTO user VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (username, email, password, type1))
            if title.strip() == "":
                sql1 = "INSERT INTO cityOfficial (username, city, state) VALUES (%s, %s, %s)"
                cursor.execute(sql1, (username, city[2:-3], state[2:-3]))
            else:
                sql2 = "INSERT INTO cityOfficial (username, title, city, state) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql2, (username, title, city[2:-3], state[2:-3]))
            self.close(cursor, db)
            messagebox.showinfo("Success!", "Registration was successful.")
            self.registerWin.destroy()
            self.win.deiconify()           

    def loginCheck(self):
        db = self.connect()
        cursor = db.cursor()
        Lusername = self.username.get()
        Lpassword = self.password.get()
        sql = "SELECT * FROM user WHERE username  = '" +Lusername+ "' AND pass = '" +Lpassword+"'"
        num = cursor.execute(sql)
        if num != 1:
            messagebox.showerror("ERROR", "Password or username invalid.")
            return
        for data in cursor:
            self.userType = data[3]
        sql1 = "SELECT username, approved FROM cityOfficial WHERE username ='"+Lusername+"' AND approved is NULL"
        num1 = cursor.execute(sql1)
        if num1 != 0:
            messagebox.showerror("ERROR", "You have not been approved yet!")
            return
        sql2 = "SELECT username, approved FROM cityOfficial WHERE username ='"+Lusername+"' AND approved = FALSE"
        num2 = cursor.execute(sql2)
        if num2 != 0:
            messagebox.showerror("ERROR", "Your account has been rejected!")
            return
        messagebox.showinfo("Welcome!", "Login successful.")
        cursor.execute("SELECT userType FROM user WHERE username = '"+Lusername+"'")
        vals = list(cursor)
        val = vals[0]
        if 'admin' in val:
            self.adminFunc()
        elif 'city official' in val:
            self.officialFunc()
        elif 'city scientist' in val:
            self.newDataPoint()
        self.close(cursor, db)
        self.win.withdraw()
        
    def helper3(self):
        self.adminFuncWin.destroy()
        self.win.deiconify()

    def adminFunc(self):
        self.adminFuncWin = Toplevel()
        self.adminFuncWin.title('Admin Options')
        f = Frame(self.adminFuncWin, background = "azure")
        f.grid()
        Label(f, text = "Choose Functionality", background = "gold").grid(column=0,row=0, sticky = E+W, pady =10)
        Button(f, text = "Pending Data Points", width=20, command = self.pendingData).grid(column=0,row=1, pady = 10, padx = 5)
        Button(f, text = "Pending City Official Accounts", width =20, command = self.cityOfficials).grid(column=0,row=2, pady =10, padx=5)
        Button(f, text = "Logout", width = 20, command = self.helper3).grid(column=0,row=3, pady =10, padx =5)
        self.original = "POI"

    def pendingData(self):
        db = self.connect()
        cursor = db.cursor()
        self.adminFuncWin.withdraw()
        self.pendingDataPage = Toplevel()
        self.pendingDataPage.title('Admin: Data Points')
        f = Frame(self.pendingDataPage, bg = "azure")
        f.grid()
        Label(f, text = "Pending Data Points", bg = "gold").grid(columnspan = 2,row = 0, sticky=E+W)
        Label(f, text = "Sort By:", width = 15, background = "azure").grid(row = 1, column = 0, sticky = E)
        sortOptions = ["POI", "Data Type", "Data Value", "Time & Date"]
        menu = StringVar(self.pendingDataPage)
        menu.set(self.original)
        drop = OptionMenu(f, menu, *sortOptions, command = self.dropDownMenu)
        drop.grid(row = 1, column = 1, sticky = W)
        drop.config(width = 15)
        f1 = Frame(f, background = "azure")
        f1.grid(row = 2, columnspan = 2)
        Label(f1, text="Select", bg = "gold", width=15).grid(column=0,row=0)
        Label(f1,text="POI", bg= "gold", width=15).grid(column=1,row=0)
        Label(f1, text="Data Type", bg= "gold", width=15).grid(column=2,row=0)
        Label(f1, text="Data Value", bg = "gold", width=15).grid(column=3,row=0)
        Label(f1, text="Time & Date", bg = "gold", width=15).grid(column=4,row=0)
        menuOption = menu.get()
        if menuOption == "POI":
            sql = "SELECT locationName, type, dataValue, datetime FROM dataPoint WHERE accepted IS NULL ORDER BY locationName"
        if menuOption == "Data Type":
            sql = "SELECT locationName, type, dataValue, datetime FROM dataPoint WHERE accepted IS NULL ORDER BY type"
        if menuOption == "Data Value":
            sql = "SELECT locationName, type, dataValue, datetime FROM dataPoint WHERE accepted IS NULL ORDER BY dataValue"
        if menuOption == "Time & Date":
            sql = "SELECT locationName, type, dataValue, datetime  FROM dataPoint WHERE accepted IS NULL ORDER BY datetime"
        cursor.execute(sql)
        n=0
        self.checklist=[]
        self.pointlist=[]
        for record in cursor:
            n += 1
            poi = record[0]
            Type = record[1]
            value = record[2]
            time = str(record[3])
            self.pointlist.append([poi,Type,value,time])
            v = IntVar(self.pendingDataPage)
            self.checklist.append(v)
            c = Checkbutton(f1, variable = v, offvalue = 0, onvalue = 1)
            c.grid(column=0,row=n)
            Label(f1,text=poi).grid(column=1,row=n)
            Label(f1,text=Type).grid(column=2,row=n)
            Label(f1,text=value).grid(column=3,row=n)
            Label(f1,text=time).grid(column=4,row=n)                
        frame2 = Frame(self.pendingDataPage)
        frame2.grid(columnspan = 2,row = 3)
        Button(frame2,text="Back",command=self.backButton1).grid(column=0,row=0)
        Button(frame2,text="Reject", command=self.reject1).grid(column=1,row=0)
        Button(frame2,text="Accept", command=self.accept1).grid(column=3,row=0)
        self.close(cursor, db)

    def dropDownMenu(self, menuOption):
        if menuOption == self.original:
            return
        self.original = menuOption
        self.pendingDataPage.destroy()
        self.pendingData()
        
    def reject1(self):
        count = 0
        db = self.connect()
        cursor = db.cursor()
        for x in range(len(self.checklist)):
            num = self.checklist[x].get()
            if num == 1:
                sql = "UPDATE dataPoint SET accepted = 0 WHERE datetime = '"+self.pointlist[x][3]+"' AND locationName = '"+self.pointlist[x][0]+"'"
                cursor.execute(sql)
            else:
                count += 1
        self.close(cursor, db)
        if count == len(self.checklist):
            messagebox.showerror("ERROR", "No data points selected!")
        else:
            messagebox.showinfo("Success", "Data points rejected.")
            self.pendingDataPage.destroy()
            self.adminFuncWin.deiconify()                
 
    def accept1(self):
        count = 0
        db = self.connect()
        cursor = db.cursor()
        for x in range(len(self.checklist)):
            num = self.checklist[x].get()
            if num == 1:
                sql = "UPDATE dataPoint SET accepted = 1 WHERE datetime = '"+self.pointlist[x][3]+"' AND locationName = '"+self.pointlist[x][0]+"'"
                cursor.execute(sql)
            else:
                count += 1
        self.close(cursor, db)
        if count == len(self.checklist):
            messagebox.showerror("ERROR", "No Data Points Selected!")
        else:
            messagebox.showinfo("Success", "Data Points Accepted")
            self.pendingDataPage.destroy()
            self.adminFuncWin.deiconify()               
        
    def backButton1(self):
        self.pendingDataPage.destroy()
        self.adminFuncWin.deiconify()

    def cityOfficials(self):
        self.adminFuncWin.withdraw()
        self.cityOfficialsPage = Toplevel()
        self.cityOfficialsPage.title('Admin: City Officials')
        Label(self.cityOfficialsPage, text = "Pending City Official Accounts", background="gold").grid(column=0,row=0, sticky = E+W, pady = 5)
        frame = Frame(self.cityOfficialsPage, background="azure")
        frame.grid(column=0,row=1)
        Label(frame, text="Select", bg = "gold").grid(column=0,row=0)
        Label(frame, text="Username", bg = "gold").grid(column=1,row=0)
        Label(frame, text="Email", bg = "gold").grid(column=2,row=0)
        Label(frame, text="City", bg = "gold").grid(column=3,row=0)
        Label(frame, text="State", bg = "gold").grid(column=4,row=0)
        Label(frame, text="Title", bg = "gold").grid(column=5, row=0)
        self.checklist2=[]
        self.officiallist=[]
        sql= "SELECT username, city, state, title FROM cityOfficial WHERE approved IS NULL"
        db = self.connect()
        cursor = db.cursor()
        cursor.execute(sql)
        records = list(cursor)
        n = 0
        for record in records:
            n += 1
            username = record[0]
            city = str(record[1])
            state = str(record[2])
            title = str(record[3])
            sql2 = "SELECT emailAddress FROM user WHERE username = '"+username+"'"
            cursor.execute(sql2)
            emails = list(cursor)
            for entry in emails:
                email = entry[0]
            self.officiallist.append([username, email, city, state, title])
            v = IntVar(self.cityOfficialsPage)
            self.checklist2.append(v)
            c = Checkbutton(frame, variable=v, offvalue=0, onvalue=1, bg = "azure")
            c.grid(column=0,row=n)
            Label(frame,text=username, bg = "azure").grid(column=1,row=n, padx = 5)
            Label(frame,text=email, bg = "azure").grid(column=2,row=n, padx = 5)
            Label(frame,text=city, bg = "azure").grid(column=3,row=n, padx = 5)
            Label(frame,text=state, bg = "azure").grid(column=4,row=n, padx = 5)
            Label(frame, text=title, bg = "azure").grid(column=5, row=n, padx = 5)
        frame2 = Frame(self.cityOfficialsPage)
        frame2.grid(column=0,row=2)
        Button(frame2,text="Back",command=self.backButton2).grid(column=0,row=0)
        Button(frame2,text="Reject", command=self.reject2).grid(column=1,row=0)
        Button(frame2,text="Accept", command=self.accept2).grid(column=3,row=0)
        
    def backButton2(self):
        self.cityOfficialsPage.withdraw()
        self.adminFuncWin.deiconify()

    def accept2(self):
        count = 0
        db = self.connect()
        cursor = db.cursor()
        for x in range(len(self.checklist2)):
            num = self.checklist2[x].get()
            if num == 1:
                sql = "UPDATE cityOfficial SET approved = 1 WHERE username = '"+self.officiallist[x][0]+"'"
                cursor.execute(sql)
            else:
                count += 1
        self.close(cursor, db)
        if count == len(self.checklist2):
            messagebox.showerror("ERROR", "No City Officials Selected!")
        else:
            messagebox.showinfo("Success", "City Officials Accepted")
            self.cityOfficialsPage.destroy()
            self.adminFuncWin.deiconify()                 

    def reject2(self):
        count = 0
        db = self.connect()
        cursor = db.cursor()
        for x in range(len(self.checklist2)):
            num = self.checklist2[x].get()
            if num == 1:
                sql = "UPDATE cityOfficial SET approved = 0 WHERE username = '"+self.officiallist[x][0]+"'"
                cursor.execute(sql)
            else:
                count += 1
        self.close(cursor, db)
        if count == len(self.checklist2):
            messagebox.showerror("ERROR", "No City Officials Selected!")
        else:
            messagebox.showinfo("Success", "City Officials Rejected.")
            self.cityOfficialsPage.destroy()
            self.adminFuncWin.deiconify()

    def helper1(self):
            self.win.deiconify()
            self.newDataPointWin.destroy()

    def newDataPoint(self):
        self.newDataPointWin = Toplevel()
        self.newDataPointWin.title('New Data Point')
        f1 = Frame(self.newDataPointWin, background = "azure", borderwidth = 5)
        f1.grid(row=0, column = 0, sticky=E+W)
        sql='SELECT DISTINCT locationName FROM poi'
        db = self.connect()
        cursor = db.cursor()
        cursor.execute(sql)
        locations = list(cursor)
        self.location_choices = StringVar(self.newDataPointWin)
        title_label = Label(f1, text="Add a new data point below.", bg='gold')
        title_label.grid(column=1, row=1, sticky=E,padx=5, pady=5)
        drop_down=OptionMenu(f1, self.location_choices, *locations)
        drop_down.config(width=20)
        drop_down.grid(row=2, column=1, sticky = W)
        Button(f1, text="Add a new location.", command = self.add_new_location, width=20).grid(row=2, column=2)
        Label(f1, text="Location Name:", bg='azure').grid(column=0, row=2, sticky=E,padx=5, pady=5)
        Label(f1, text="Date and time of data reading: ", bg='azure').grid(column=0, row=3, sticky=E,padx=5, pady=5)
        self.date_time = StringVar(self.newDataPointWin)
        Entry(f1, textvariable = self.date_time, width = 20).grid(row = 3, column = 1, sticky = W)
        date_time_explanation = Label(f1, text="**date and time should be in form YYYY-MM-DD HH:MM:SS**", bg = "gold")
        date_time_explanation.grid(columnspan=2, row=4)
        sql2 = 'SELECT DISTINCT type FROM dataType'
        cursor.execute(sql2)
        typeList = list(cursor)
        self.data_choices = StringVar(self.newDataPointWin)
        drop_down2=OptionMenu(f1, self.data_choices, *typeList)
        drop_down2.config(width=20)
        drop_down2.grid(row=5, column=1, sticky = W)
        Label(f1, text="Data Type: ", foreground='black', bg='azure').grid(column=0, row=5, sticky=E,padx=5, pady=5)
        Label(f1, text="Data value: ", foreground='black', bg='azure').grid(row=6, column=0, sticky=E,padx=5, pady=5)
        self.value = StringVar(self.newDataPointWin)
        Entry(f1, textvariable = self.value, width = 20).grid(row = 6, column = 1, sticky = W)
        Button(f1, text="Back", width = 10, command = self.helper1).grid(row=7, column=0)
        Button(f1, text="Submit", width = 10, command=self.data_point_check).grid(row=7, column=1)
        self.close(cursor, db)

    def helper2(self):
        self.newDataPointWin.deiconify()
        self.add_new_locationWin.destroy()

    def add_new_location(self):
        self.add_new_locationWin = Toplevel()
        self.newDataPointWin.withdraw()
        self.add_new_locationWin.title("New Location")
        f1 = Frame(self.add_new_locationWin, background = "azure")
        f1.grid(row=0, column = 0, sticky=E+W)
        Label(f1, text="Add A New Location ", bg='gold').grid(columnspan=2, row=0, sticky=E,padx=5, pady=5)
        Label(f1, text="POI Location Name:", bg='gold').grid(column=0, row=2, sticky=E,padx=5, pady=5)
        self.poi_location_name = StringVar(self.add_new_locationWin)
        Entry(f1, textvariable = self.poi_location_name, width = 20).grid(row =2, column = 1, sticky = W)
        self.city_choices = StringVar(self.add_new_locationWin)
        drop_down=OptionMenu(f1, self.city_choices, *self.cityList)
        drop_down.config(width=20)
        drop_down.grid(row=3, column=1, sticky = W)
        Label(f1, text="City:", bg='gold').grid(column=0, row=3, sticky=E,padx=5, pady=5)
        self.state_choices = StringVar(self.add_new_locationWin)
        drop_down2=OptionMenu(f1, self.state_choices, *self.stateList)
        drop_down2.config(width=20)
        drop_down2.grid(row=4, column=1, sticky = W)
        Label(f1, text="State:", bg='gold').grid(column=0, row=4, sticky=E,padx=5, pady=5)
        Label(f1, text="Zip Code:", bg='gold').grid(row=5, column=0, sticky = E, padx = 5, pady=5)
        self.zip_code = StringVar(self.add_new_locationWin)
        Entry(f1, textvariable = self.zip_code, width = 10).grid(row =5, column =1, sticky = W)
        Button(f1, text="Back", width=10, command = self.helper2).grid(row=6, column=0)
        Button(f1, text="Submit", width=10, command=self.new_location_check).grid(row=6, column=1)

    def new_location_check(self):
        db = self.connect()
        cursor = db.cursor()
        poi_location_name = self.poi_location_name.get()
        cursor.execute("SELECT locationName FROM poi WHERE locationName = '"+poi_location_name+"'")
        names = list(cursor)
        if len(names) != 0 or poi_location_name.strip() == "":
            messagebox.showerror("ERROR", "Location name is already registered or was left blank!")
            return
        city = self.city_choices.get()
        if city == "":
            messagebox.showerror("ERROR", "Please pick a city!")
            return
        state = self.state_choices.get()
        if state == "":
            messagebox.showerror("ERROR", "Please pick a state!")
            return
        sql = "SELECT city, state FROM cityState WHERE city='"+city[2:-3]+"' AND state='"+state[2:-3]+"'"
        num = cursor.execute(sql)
        if num == 0:
            messagebox.showerror("ERROR", "City and State combination is invalid.")
            return
        zipcode = self.zip_code.get()
        if zipcode.strip() == "":
            sql = "INSERT INTO poi (locationName, city, state) VALUES (%s, %s, %s)"
            cursor.execute(sql, (poi_location_name, city[2:-3], state[2:-3]))
        else:
            try:
                zipcode = int(zipcode)
                if zipcode<10000 or zipcode>99999:
                    messagebox.showerror("ERROR", "Please choose a 5-digit integer for the zipcode!")
                    return
            except:
                messagebox.showerror("ERROR", "Please choose a 5-digit integer for the zipcode!")
                return
            sql = "INSERT INTO poi (locationName, zipcode, city, state) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (poi_location_name, zipcode, city[2:-3], state[2:-3]))
        self.close(cursor, db)
        messagebox.showinfo("Success!", "Location was added.")
        self.newDataPointWin.deiconify()
        self.add_new_locationWin.destroy()

    def data_point_check(self):
        db = self.connect()
        cursor = db.cursor()
        location = self.location_choices.get()
        if location == "":
            messagebox.showerror("ERROR", "Please pick a location!")
            return
        date_time = self.date_time.get().strip()
        try:
            dateFormat = time.strptime(date_time, "%Y-%m-%d %H:%M:%S")
        except:
            messagebox.showerror("ERROR", "Date/time format is incorrect or date/time not provided!")
            return
        data = self.data_choices.get()
        if data == "":
            messagebox.showerror("ERROR", "Please pick a data type!")
            return
        value = self.value.get()
        if value.strip() =="":
            messagebox.showerror("ERROR", "Please enter a data value!")
            return
        try:
            value = int(value)
        except:
            messagebox.showerror("ERROR", "Please enter an integer for the value!")
            return
        sql= "SELECT locationName, datetime FROM dataPoint WHERE locationName = '"+location[2:-3]+"' AND datetime = '"+date_time+"'"
        cursor.execute(sql)
        keys = list(cursor)
        if len(keys) != 0:
            messagebox.showerror("ERROR", "There is already a data value for this time & location!")
            return
        sql = "INSERT INTO dataPoint (datetime, locationName, dataValue, type) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (date_time, location[2:-3], value, data[2:-3]))
        self.close(cursor, db)
        messagebox.showinfo("Success!", "Data point was added.")

    def helper8(self):
        self.officialFuncWin.destroy()
        self.win.deiconify()

    def officialFunc(self):
        self.officialFuncWin = Tk()
        self.officialFuncWin.title('City Official Options')
        f = Frame(self.officialFuncWin, background = "azure")
        f.grid()
        Label(f, text = "Choose Functionality", background = "gold").grid(column=0,row=0, sticky = E+W, pady =10)
        Button(f, text = "Filter or Search POIs", width=20, command = self.helper9).grid(column=0,row=1, pady = 10, padx = 5)
        Button(f, text = "POI Report", width =20, command = self.helper11).grid(column=0,row=2, pady =10, padx=5)
        Button(f, text = "Logout", width = 20, command = self.helper8).grid(column=0,row=3, pady =10, padx =5)
        self.original1 = "Flagged?"

    def helper9(self):
        self.officialFuncWin.destroy()
        self.Poi()

    def Poi(self):
        db = self.connect()
        cursor = db.cursor()
        self.viewPoiWin = Toplevel()
        self.viewPoiWin.title("View POIs")
        self.f = Frame(self.viewPoiWin, background="azure", width=500, height=500)
        self.f.grid()
        f1 = Frame(self.f, background="azure", width=500, height=500)
        f1.grid(row=0, columnspan=2) 
        Label(f1, text="View POI", font=("Comic Sans MS", 20, "bold"),bg="sky blue", relief="groove").grid(row=0, columnspan=4, sticky=EW)
        Label(f1, text="POI location Name:", bg="azure").grid(row=1, column=0, sticky=W)
        Label(f1, text="City:", bg="azure").grid(row=2,column=0, sticky=W)
        Label(f1, text="State:", bg="azure").grid(row=3, column=0, sticky=W)
        Label(f1, text="Zip Code:", bg="azure").grid(row=4, column=0, sticky=W)
        Label(f1, text="Flagged?:", bg="azure").grid(row=5, column=0, sticky=W)
        Label(f1, text="Date Flagged:", bg="azure").grid(row=6, column=0, sticky=W)
        self.loc= StringVar(self.viewPoiWin)
        sql= """SELECT locationName FROM poi"""
        cursor.execute(sql)
        l=list(cursor)
        if len(l) == 0:
            l.append("No locations to choose from!")
        locoptions = OptionMenu(f1, self.loc, *l)
        locoptions.grid(row=1, column=1, sticky=E)
        locoptions.config(width=15)
        self.loc.set("-Select-")
        self.city= StringVar(self.viewPoiWin)
        cities=OptionMenu(f1, self.city, *self.cityList)
        cities.grid(row=2,column=1, sticky=W)
        cities.config(width=15)
        self.city.set("-Select-")
        self.state= StringVar(self.viewPoiWin)
        states=OptionMenu(f1, self.state, *self.stateList)
        states.grid(row=3,column=1, sticky=W)
        states.config(width=15)
        self.state.set("-Select-")
        self.zip= StringVar(self.viewPoiWin)
        self.zip.set("0")
        Entry(f1, textvariable=self.zip, width=5).grid(row=4,column=1, sticky=W)           
        self.flag= IntVar(self.viewPoiWin)
        cb = Checkbutton(f1, variable=self.flag)
        cb.grid(row=5,column=1, sticky=W)
        self.date1= StringVar(self.viewPoiWin)
        self.date2= StringVar(self.viewPoiWin)
        Entry(f1, textvariable=self.date1,width=10).grid(row=6,column=1,sticky=W)
        Label(f1, text="MM/DD/YYYY", background="azure").grid(row=7,column=1, sticky=W)
        Label(f1,text="to",background="azure", font="bold").grid(row=6, column=2, sticky=EW)  
        Entry(f1, textvariable=self.date2,width=10).grid(row=6,column=3,sticky=W)
        Label(f1, text="MM/DD/YYYY", background="azure").grid(row=7,column=3, sticky=W)
        f2 = Frame(self.f, background="azure")
        f2.grid(row=1, columnspan=2)
        Button(f2, text="Apply Filter", background="sky blue", width=20,command= self.Results).grid(row=0,column=1, sticky=W, pady=10)
        Button(f2, text="Reset Filter", background="sky blue", width=20,command=self.ResetFilter).grid(row=0, column=2, sticky=W,pady=10)
        self.close(cursor, db)

    def ResetFilter(self):
        self.loc.set("-Select-")
        self.city.set("-Select-")
        self.state.set("-Select-")
        self.date1.set("")
        self.date2.set("")
        self.zip.set("0")
        self.flag.set(0)
        self.f3.grid_forget()
        self.f4.grid_forget()

    def Results(self):
        db = self.connect()
        cursor = db.cursor()
        Loc = self.loc.get()[2:-3]
        City =self.city.get()[2:-3]
        State =self.state.get()[2:-3]
        Zip = self.zip.get()
        date1 = self.date1.get()
        date2 = self.date2.get()
        dateFormat= "%Y-%m-%d"
        flag = self.flag.get()
        try:
            d1=time.strptime(date1,dateFormat)
            d2=time.strptime(date2,dateFormat)
            date1bool = "TRUE"
            date2bool = "TRUE"
        except:
            date1bool = "FALSE"
            date2bool = "FALSE"
        if Loc != "ele":
            locbool = "TRUE"
        else:
            locbool = "FALSE"
        if City != "ele":
            citybool = "TRUE"
        else:
            citybool = "FALSE"
        if State!= "ele":
            statebool = "TRUE"
        else:
            statebool = "FALSE"
        if Zip.strip() == "" or Zip == "0":
            zipbool = "FALSE"
        else:
            try:
                Zipint = int(Zip)
                if Zipint<10000 or Zipint>99999:
                    messagebox.showerror("ERROR", "Please choose a 5-digit integer for the zipcode!")
                    return
                else: zipbool = "TRUE"
            except:
                messagebox.showerror("ERROR", "Please choose a 5-digit integer for the zipcode!")
                return
        if flag == 1:  
            sql= """SELECT * FROM poi
                 WHERE locationName = CASE WHEN """+locbool+""" THEN '"""+Loc+"""' ELSE locationName END
                 AND zipcode = CASE WHEN """+zipbool+""" THEN """+Zip+""" ELSE zipcode END
                 AND city = CASE WHEN """+citybool+""" THEN '"""+City+"""' ELSE city END
                 AND state = CASE WHEN """+statebool+""" THEN '"""+State+"""' ELSE state END
                 AND dateFlagged >= CASE WHEN """+date1bool+""" THEN '"""+date1+"""' ELSE dateFlagged END
                 AND dateFlagged <= CASE WHEN """+date2bool+""" THEN '"""+date2+"""' ELSE dateFlagged END
                 AND flag = 1"""
        if flag == 0:
            sql= """SELECT * FROM poi
                 WHERE locationName = CASE WHEN """+locbool+""" THEN '"""+Loc+"""' ELSE locationName END
                 AND zipcode = CASE WHEN """+zipbool+""" THEN """+Zip+""" ELSE zipcode END
                 AND city = CASE WHEN """+citybool+""" THEN '"""+City+"""' ELSE city END
                 AND state = CASE WHEN """+statebool+""" THEN '"""+State+"""' ELSE state END
                 AND flag = 0"""
        cursor.execute(sql)
        values = cursor
        self.f3 = Frame(self.f, background="azure")
        self.f3.grid(row=3, columnspan=3)
        self.f3.config(relief=RAISED)
        headings=["Location Name", "Flagged?", "Zip Code","Date Flagged","City","State"]
        self.tree1 = ttk.Treeview(self.f3, columns=headings, show="headings")
        self.tree1.grid(columnspan=6)
        for c in headings:
            self.tree1.heading(c, text=c.title())
            self.tree1.column(c, width=100)
        for i in values:
            self.tree1.insert("", "end", values=i)
        self.tree1.bind("<Double-1>", self.OnDoubleClick)
        self.f4 = Frame(self.f, background="azure")
        self.f4.grid(row=4, columnspan=3)
        Button(self.f4, text="Back", background="turquoise", width=10,command=self.Return).grid(row=4,column=3)
        self.close(cursor, db)

    def OnDoubleClick(self, event):
        db = self.connect()
        cursor = db.cursor()
        item = self.tree1.identify('item',event.x,event.y)
        ting=self.tree1.focus()
        tings=self.tree1.item(ting)
        self.l=tings["values"][0]
        self.viewPoiWin.withdraw()
        self.poiDetail=Toplevel()
        self.poiDetail.title("POI Location: " + self.l)
        self.fr=Frame(self.poiDetail, background="azure", width=500, height=500)
        self.fr.grid()
        f1 = Frame(self.fr, background="azure", width=500, height=500)
        f1.grid(row=0, columnspan=2) 
        Label(f1, text="POI Detail", font=("Comic Sans MS", 20, "bold"),bg="sky blue", relief="groove").grid(row=0, columnspan=8, sticky=EW)
        Label(f1, text="Type:", bg="azure").grid(row=1, column=0, sticky=W)
        Label(f1, text="Data Value:", bg="azure").grid(row=2,column=0, sticky=W)
        Label(f1, text="Time & Date:", bg="azure").grid(row=3, column=0, sticky=W)
        self.type= StringVar(self.poiDetail)
        sql= """SELECT type FROM dataType"""
        cursor.execute(sql)
        t=cursor
        datatype = OptionMenu(f1, self.type, *t)
        datatype.grid(row=1, column=1, sticky=W)
        datatype.config(width=10)
        self.dValue1= StringVar(self.poiDetail)
        Entry(f1, textvariable=self.dValue1, width=4).grid(row=2,column=1, sticky=W)
        Label(f1,text="to",background="azure", font="bold").grid(row=2, column=2, sticky=W)  
        self.dValue2= StringVar()
        Entry(f1, textvariable=self.dValue2, width=4).grid(row=2,column=3, sticky=W)
        sql1= """SELECT dataValue FROM dataPoint WHERE locationName=%s"""
        cursor.execute(sql1,(self.l))
        dv=list(cursor)
        self.timedate1= StringVar(self.poiDetail)
        self.timedate2= StringVar(self.poiDetail)
        Entry(f1, textvariable=self.timedate1,width=15).grid(row=3,column=1,sticky=W)
        Label(f1, text="YYYY-MM-DD HH:MM:SS", background="azure").grid(row=4,column=1, sticky=W)
        Label(f1,text="to",background="azure", font="bold").grid(row=3, column=2, sticky=EW)  
        Entry(f1, textvariable=self.timedate2,width=15).grid(row=3,column=3,sticky=W)
        Label(f1, text="YYYY-MM-DD HH:MM:SS", background="azure").grid(row=4,column=3, sticky=W)
        f2 = Frame(self.fr, background="azure")
        f2.grid(row=1, columnspan=4)
        Button(f2, text="Apply Filter", background="sky blue", width=20,command= self.Deets).grid(row=0,column=1, sticky=W, pady=10)
        Button(f2, text="Reset Filter", background="sky blue", width=20,command=self.Reset).grid(row=0, column=2, sticky=W,pady=10)
        Button(f2, text="Back", background="turquoise", width=10,command=self.helper10).grid(row=0,column=3)
        Button(f2, text="Flag/UnFlag", background="turquoise", width=10,command=self.Flag).grid(row=0,column=4)
        self.close(cursor, db)
        
    def helper10(self):
        self.viewPoiWin.deiconify()
        self.poiDetail.destroy()
        
    def Return(self):
        self.viewPoiWin.destroy()
        self.officialFunc()
        
    def Deets(self):
        db = self.connect()
        cursor = db.cursor()
        dv1=self.dValue1.get()
        dv2=self.dValue2.get()
        td1=self.timedate1.get()
        td2=self.timedate2.get()
        dateFormat= "%Y-%m-%d %H:%M:%S"
        t=self.type.get()[2:-3]
        try:
            dateFormat = time.strptime(td1, "%Y-%m-%d %H:%M:%S")
            td1bool = "TRUE"
        except:
            td1bool = "FALSE"
        try:
            dateFormat = time.strptime(td2, "%Y-%m-%d %H:%M:%S")
            td2bool = "TRUE"
        except:
            td2bool = "FALSE"
        if dv1.strip() == "":
            dv1bool = "FALSE"
        else:
            try:
                dv1 = int(dv1)
                dv1bool = "TRUE"
            except:
                messagebox.showerror("ERROR", "Please enter integer for data value!")
                return
        if dv2.strip() == "":
            dv2bool = "FALSE"
        else:
            try:
                dv2 = int(dv2)
                dv2bool = "TRUE"
            except:
                messagebox.showerror("ERROR", "Please enter integer for data value!")
                return
        if t=="mold" or t=="air quality":
            tbool = "TRUE"
        else:
            tbool = "FALSE"
        sql="""SELECT type, dataValue, dateTime FROM dataPoint 
                    WHERE locationName =%s AND accepted=1
                    AND type = CASE WHEN """+tbool+""" THEN '"""+t+"""' ELSE type END
                    AND dateTime >= CASE WHEN """+td1bool+""" THEN '"""+td1+"""' ELSE dateTime END
                    AND dateTime <= CASE WHEN """+td2bool+""" THEN '"""+td2+"""' ELSE dateTime END
                    AND dataValue >= CASE WHEN """+dv1bool+""" THEN '"""+str(dv1)+"""' ELSE dataValue END
                    AND dataValue <= CASE WHEN """+dv2bool+""" THEN '"""+str(dv2)+"""' ELSE  dataValue END"""
        cursor.execute(sql, self.l)
        values=cursor
        self.fr3 = Frame(self.fr, background="azure")
        self.fr3.grid(row=2, columnspan=4)
        self.fr3.config(relief=RAISED)       
        headings=["Data Type","Data Value","Time & Date of Reading"]
        self.tree2 = ttk.Treeview(self.fr3, columns=headings, show="headings")
        self.tree2.grid(columnspan=3,)
        for c in headings:
            self.tree2.heading(c, text=c.title())
            self.tree2.column(c, width=120)
        for i in values:
            self.tree2.insert("", "end", values=i)
        self.fr4 = Frame(self.fr, background="azure")
        self.fr4.grid(row=3, columnspan=4)
        self.close(cursor, db)

    def Flag(self):
        db = self.connect()
        cursor = db.cursor()
        date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        seql= """SELECT flag from poi WHERE locationName=%s"""
        cursor.execute(seql,(self.l))
        theflag=list(cursor)
        flag= theflag[0][0]
        
        if flag==0:
            sql="""UPDATE poi SET flag=1, dateFlagged=%s WHERE locationName =%s"""
            cursor.execute(sql,(date,self.l))
            messagebox.showerror("Bless Up!", "POI location Flagged")
        elif flag==1:
            sql="""UPDATE poi SET flag=0, dateFlagged=NULL WHERE locationName =%s"""
            cursor.execute(sql,(self.l))
            messagebox.showerror("Okie!", "POI location Un-Flagged")
        self.close(cursor, db)
        

    def Reset(self):
        self.dValue1.set("")
        self.dValue2.set("")
        self.timedate1.set("")
        self.timedate2.set("")
        self.type.set("")
        try:
            self.fr3.grid_forget()
            self.fr4.grid_forget()
        except:
            pass
        
    def helper11(self):
        self.officialFuncWin.destroy()
        self.report()

    def report(self):
        db = self.connect()
        cursor = db.cursor()
        self.poiReport = Toplevel()
        self.poiReport.title("City Official Report")
        f=Frame(self.poiReport, background="azure", width=500, height=500)
        f.grid()
        f5 = Frame(f, background="azure")
        f5.grid()
        Label(f5, text="POI Report", font=("Comic Sans MS", 20, "bold"),bg="sky blue", relief="groove").grid(row=0, columnspan=2, sticky=EW)
        sortOptions = ["Flagged?","Mold Min", "Mold Avg", "Mold Max", "AQ Min", "AQ Avg","AQ Max", "# Of Data Points"]
        menu = StringVar(self.poiReport)
        menu.set(self.original1)
        drop = OptionMenu(f5, menu, *sortOptions, command = self.dropDownMenu1)
        drop.grid(row = 1, column = 1, sticky = W)
        drop.config(width = 15)
        Label(f5, text = "Sort By:", width = 15, bg = "gold").grid(row =1, column = 0)
        headings=["POI Location", "City", "State", "Flagged?", "AQ Min","AQ Avg", "AQ Max", "Mold Min", "Mold Avg","Mold Max", "# Of Data Points"]
        sql= """SELECT T1.locationName, T1.city, T1.state, T1.flag, T2.aqMin, T2.aqAvg, T2.aqMax, T3.moldMin, T3.moldAvg, T3.moldMax, T4.count
             FROM (select locationName, city, state, flag from poi) T1
             LEFT JOIN (select locationName, MIN(dataValue) as aqMin, AVG(dataValue) AS aqAvg, MAX(dataValue) as aqMax FROM dataPoint
             WHERE type = 'air quality' and accepted = 1 GROUP BY locationName) T2
             ON T1.locationName = T2.locationName
             LEFT JOIN (select locationName, MIN(dataValue) as moldMin, AVG(dataValue) AS moldAvg, MAX(dataValue) as moldMax FROM dataPoint
             WHERE type = 'mold' and accepted = 1 GROUP BY locationName) T3
             ON T1.locationName = T3.locationName
             LEFT JOIN (select locationName, COUNT(dataValue) as count FROM dataPoint WHERE accepted = 1 GROUP BY locationName) T4
             ON T1.locationName = T4.locationName """
        menuOption = menu.get()
        if menuOption == "Flagged?":
            sql1 = "ORDER BY T1.flag"
        if menuOption == "Mold Min":
            sql1 = "ORDER BY T3.moldMin"
        if menuOption == "Mold Avg":
            sql1 = "ORDER BY T3.moldAvg"
        if menuOption == "Mold Max":
            sql1 = "ORDER BY T3.moldMax"
        if menuOption == "AQ Min":
            sql1 = "ORDER BY T2.AQMin"
        if menuOption == "AQ Avg":
            sql1 = "ORDER BY T2.AQAvg"
        if menuOption == "AQ Max":
            sql1 = "ORDER BY T2.AQMax"
        if menuOption == "# Of Data Points":
            sql1 = "ORDER BY T4.count"
        cursor.execute(sql+sql1)
        values=list(cursor)
        f1 = Frame(f5, bg = "azure")
        f1.grid(columnspan = 2, row = 2)
        n = 0
        for header in headings:
            Label(f1, text = header, bg = "gold").grid(row =0, column = n, padx = 5)
            n += 1
        m = 1
        for record in values:
            s = 0
            for value in record:
                if value == None:
                    Label(f1, text = "NULL", bg = "azure").grid(row = m, column = s, padx = 5)
                else:
                    Label(f1, text = value, bg = "azure").grid(row = m, column = s, padx = 5)
                s += 1
            m+=1
        Button(f,text = "Back", width = 10, command = self.helper12).grid(row=1, column = 0)
        self.close(cursor, db)

    def helper12(self):
        self.poiReport.destroy()
        self.officialFunc()
            
    def dropDownMenu1(self, menuOption):
        if menuOption == self.original1:
            return
        self.original1 = menuOption
        self.poiReport.destroy()
        self.report()

win = Tk()
app = SLSGUI(win)
win.mainloop()
