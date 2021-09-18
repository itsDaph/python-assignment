from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pickle
import datetime

staffList = [] #staffList = email, password, name
patientList = [] #patientList = email, password, name, ic, gender, phone number, address
appointmentList = [] #appointmentList = userID, dentist, typeOfTreatment, date, time, remark, status
recordsList = [] #recordsList = searchType, searchQuery, datetime, appointmentID[]
userID = None
userType = None
treatmentTypes = ["Extractions", "Fillings & Repairs", "Teeth Cleaning", "Dentures"]

class Initiate():
    def __init__(self):
        global staffList
        global patientList
        global appointmentList
        global recordsList
        
        try:
            staffList = pickle.load(open("staff", "rb"))
        except (OSError, IOError) as e:
            staffList = [["a", "a", "Dr.Stanley"], ["b", "b", "Dr.Ong"], ["n", "n", "Nurse"]]
            pickle.dump(staffList, open("staff", "wb"))
        
        try:
            patientList = pickle.load(open("patient", "rb"))
        except (OSError, IOError) as e:
            patientList = []
            pickle.dump(patientList, open("patient", "wb"))

        try: 
            appointmentList = pickle.load(open("appointment", "rb"))
        except (OSError, IOError) as e:
            appointmentList = []
            pickle.dump(appointmentList, open("appointment", "wb"))

        try: 
            recordsList = pickle.load(open("records", "rb"))
        except (OSError, IOError) as e:
            recordsList = []
            pickle.dump(recordsList, open("records", "wb"))

        Login(window)

class Login(Frame):
    def showRegister(self):
        self.grid_forget()
        self.content.grid_forget()
        self.app = Register(self.master)

    def showDashboard(self):
        self.grid_forget()
        self.content.grid_forget()
        self.app = Dashboard(self.master)

    def validateLogin(self):
        global userID
        global userType
        for staff in staffList:
            if self.email.get() == staff[0] and self.password.get() == staff[1]:
                userID = staffList.index(staff)
                if staff[2] == "Nurse":
                    userType = "Nurse"
                else:
                    userType = "Dentist"
                self.showDashboard()
                print("Staff found")
                return
        
        for patient in patientList:
            if self.email.get() == patient[0] and self.password.get() == patient[1]:
                userID = patientList.index(patient)
                userType = "Patient"
                self.showDashboard()
                print("Patient found")
                return
        
        self.status.config(text="Incorrect email or password")

    def __init__(self, master):
      Frame.__init__(self, master)
      self.master = master
      self.content = Frame(window)

      self.grid(row=0, column=0, sticky=NSEW)
      self.content.grid(row=1, column=0, sticky=NSEW)

      self.grid_rowconfigure(0, weight=1)
      self.content.grid_rowconfigure(1, weight=5)

      loginLabel = Label(self, text="Log In as Customer", fg="salmon", font=("Arial",15))
      loginLabel.grid(row=0, column=0, sticky=W)

      self.emailLabel = Label(self.content, text="Email", fg="salmon", font=(None, 11))
      self.emailLabel.grid(row=1, column=0, sticky=W)
      self.email = StringVar()
      self.emailEntered = Entry(self.content, textvariable=self.email, width=69)
      self.emailEntered.grid(row=1, column=1)

      self.passLabel = Label(self.content, text="Password", fg="salmon", font=(None, 11))
      self.passLabel.grid(row=2, column=0, sticky=W)
      self.password = StringVar()
      self.passEntered = Entry(self.content, textvariable=self.password, width=69)
      self.passEntered.grid(row=2, column=1)

      login = Button(self.content, text="Log In", bg="salmon", fg="white", command=lambda:self.validateLogin())
      login.grid(row=3, column=1, sticky=E)

      register = Button(self.content, text="Register", bg="salmon", fg="white", command=lambda:self.showRegister())
      register.grid(row=4, column=1, sticky=E)

      self.status = Label(self.content, "", fg="salmon")
      self.status.grid(row=5, column=1, sticky=W)

class Register(Frame):
    def showLogin(self):
        self.grid_forget()
        self.app = Login(self.master)
    
    def validateRegister(self):
        global patientList
        for patient in patientList:
            if self.email.get() == patient[0] or self.ICNumber.get() == patient[3]:
                self.status.config(text="This user has been registered")
                return
        
        patientList.append([self.email.get(), self.password.get(), self.fullName.get(), self.ICNumber.get(), self.gender.get(), self.contactNumber.get(), self.address.get()])
        pickle.dump(patientList, open("patient", "wb"))
        self.showLogin()
        print("Done")
    
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.content = Frame(window)
        
        self.grid(sticky=NSEW)

        newUserLabel = Label(self, text="New User?", fg="salmon", font=("Arial", 15))
        newUserLabel.grid(row=0, column=0, sticky=W)

        self.emailLabel = Label(self, text="Email", fg="salmon", font=(None, 11))
        self.emailLabel.grid(row=1, column=0, sticky=W)
        self.email = StringVar()
        self.emailEntered = Entry(self, textvariable=self.email, width=62)
        self.emailEntered.grid(row=1, column=1)

        self.passLabel = Label(self, text="Password", fg="salmon", font=(None, 11))
        self.passLabel.grid(row=2, column=0, sticky=W)
        self.password = StringVar()
        self.passEntered = Entry(self, textvariable=self.password, width=62)
        self.passEntered.grid(row=2, column=1)

        self.fNameLabel = Label(self, text="Full Name", fg="salmon", font=(None, 11))
        self.fNameLabel.grid(row=3, column=0, sticky=W)
        self.fullName = StringVar()
        self.fNameEntered = Entry(self, textvariable=self.fullName, width=62)
        self.fNameEntered.grid(row=3, column=1)

        self.ICNumLabel = Label(self, text="IC Number", fg="salmon", font=(None, 11))
        self.ICNumLabel.grid(row=4, column=0, sticky=W)
        self.ICNumber = StringVar()
        self.ICNumEntered = Entry(self, textvariable=self.ICNumber, width=62)
        self.ICNumEntered.grid(row=4, column=1)

        self.genderLabel = Label(self, text="Gender", fg="salmon", font=(None, 11))
        self.genderLabel.grid(row=5, column=0, sticky=W)
        self.gender = IntVar()
        self.male = Radiobutton(self, text="Male", variable=self.gender, value=1, fg="salmon")
        self.male.grid(row=5, column=1, sticky=W)
        self.female = Radiobutton(self, text="Female", variable=self.gender, value=2, fg="salmon")
        self.female.grid(row=5, column=1)

        self.conNumLabel = Label(self, text="Contact Number", fg="salmon", font=(None, 11))
        self.conNumLabel.grid(row=6, column=0, sticky=W)
        self.contactNumber = StringVar()
        self.conNumEntered = Entry(self, textvariable=self.contactNumber, width=62)
        self.conNumEntered.grid(row=6, column=1)

        self.addressLabel = Label(self, text="Address", fg="salmon", font=(None, 11))
        self.addressLabel.grid(row=7, column=0, sticky=W)
        self.address = StringVar()
        self.addressEntered = Entry(self, textvariable=self.address, width=62)
        self.addressEntered.grid(row=7, column=1)

        register = Button(self, text="Register", bg="salmon", fg="white", font=(None, 11), command=lambda:self.validateRegister())
        register.grid(row=8, column=1, sticky=E)

        statement = Button(self, text="Already a member? Log in", bg="salmon", fg="white", font=(None, 11, "underline"), command=lambda:self.showLogin())
        statement.grid(row=9, column=1, sticky=E)

        self.status = Label(self.content, "", fg="salmon")
        self.status.grid(row=9, column=0, sticky=W)

class Dashboard(Frame):
    def showPatientCreateAppointment(self):
        self.grid_forget()
        self.app = PatientCreateAppointment(self.master)
    
    def showPatientViewAppointments(self):
        self.grid_forget()
        self.app = PatientViewAppointments(self.master)
   
    def showDentistViewAppointments(self):
        self.grid_forget()
        self.content.grid_forget()
        self.app = DentistViewAppointments(self.master)

    def showDentistViewRecords(self):
        self.grid_forget()
        self.content.grid_forget()
        self.app = DentistViewRecords(self.master)
    
    def showNurseCreateRecord(self):
        self.grid_forget()
        self.content.grid_forget()
        self.app = NurseCreateRecord(self.master)

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.content = Frame(window)

        self.grid(sticky=NSEW)

        welcomeLabel = Label(self, text="Welcome, " + userType, fg="salmon", font=("Arial", 15))
        welcomeLabel.grid(row=0, column=0, sticky=W)

        bookLabel = Label(self, text="Book Your Appointment With Our Dentists", fg="salmon", font=("Arial", 12))
        bookLabel.grid(row=1, column=0, sticky=W)

        recentLabel = Label(self, text="Recent Appointment", fg="salmon", font=("Arial", 15))
        recentLabel.grid(row=2, column=0, sticky=W)

        if userType == "Patient":
            self.showAppointments = Button(self, text="My Appointments", bg="salmon", fg="white", font=(None, 11), command=lambda:self.showPatientViewAppointments())
            self.showAppointments.grid(row=3, column=0, sticky=W)

            self.showCreateAppointment = Button(self, text="New Appointment", bg="salmon", fg="white", font=(None, 11), command=lambda:self.showPatientCreateAppointment())
            self.showCreateAppointment.grid(row=4, column=0, sticky=W)
        elif userType == "Nurse":
            self.showCreateRecordButton = Button(self, text="Create Record", bg="salmon", fg="white", font=(None, 11), command=lambda:self.showNurseCreateRecord())
            self.showCreateRecordButton.grid(row=3, column=0, sticky=W)
        else:
            self.showAppointmentsButton = Button(self, text="Show Appointments", bg="salmon", fg="white", font=(None, 11), command=lambda:self.showDentistViewAppointments())
            self.showAppointmentsButton.grid(row=3, column=0, sticky=W)

            self.showRecordsButton = Button(self, text="Show Records", bg="salmon", fg="white", font=(None, 11), command=lambda:self.showDentistViewRecords())
            self.showRecordsButton.grid(row=4, column=0, sticky=W)

class PatientCreateAppointment(Frame):
    def showDashboard(self):
        self.grid_forget()
        self.content.grid_forget()
        self.app = Dashboard(self.master)

    def validateAppointment(self):
        global appointmentList
        
        appointmentList.append([userID, self.dentist.get(), treatmentTypes[self.typeOfTreatment.get()], self.date.get(), self.time.get(), self.remark.get(), "Pending"])
        pickle.dump(appointmentList, open("appointment", "wb"))
        print("Complete")

        self.grid_forget()
        self.content.grid_forget()
        self.app = PatientViewAppointments(self.master)
    
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.content = Frame(window)

        self.grid(sticky=NSEW)
        self.content.grid(sticky=NSEW)

        self.grid_rowconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=5)
        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)

        newLabel = Label(self, text="New Appointment", fg="salmon", font=("Arial", 15))
        newLabel.grid(row=0, column=0, sticky=W)

        home = Button(self, text="Home", bg="salmon", fg="white", font=(None, 11), command=lambda:self.showDashboard())
        home.grid(row=0, column=1, sticky=E)

        makeApppointment = Button(self, text="Confirm", bg="salmon", fg="white", font=(None,11), command=lambda:self.validateAppointment())
        makeApppointment.grid(row=0, column=1, sticky=W)

        dateSlots = [datetime.date.today(), 
                     datetime.date.today() + datetime.timedelta(days=1),
                     datetime.date.today() + datetime.timedelta(days=2),
                     datetime.date.today() + datetime.timedelta(days=3),
                     datetime.date.today() + datetime.timedelta(days=4),
                     datetime.date.today() + datetime.timedelta(days=5),
                     datetime.date.today() + datetime.timedelta(days=6)]

        def setTimes(self, d):
            timeSlots = ["9.00-9.30", "9.30-10.00", "10.00-10.30", "10.30-11.00", "11.30-12.00", "13.00-13.30", "13.30-14.00", "14.00-14.30", "14.30-15.00", "15.00-15.30", "15.30-16.00", "16.00-16.30", "16.30-17.00", "17.00-17.30", "17.30-18.00"]

            for appointment in appointmentList:
                if str(self.dentist.get()) == str(appointment[1]) and str(d) == str(appointment[3]) and (appointment[6] == "Pending" or appointment[6] == "Confirmed" or appointment[6] == "Completed" or appointment[6] == "No-Show"): #todo: check if appointment is cancelled or whatever
                    timeSlots.remove(appointment[4])

            self.time = StringVar(window)
            self.time.set(timeSlots[0])
            if hasattr(self, 'timeOption'):
                self.timeOption.grid_remove()
            self.timeOption = OptionMenu(self.content, self.time, *timeSlots)
            self.timeOption.grid(row=5, column=1, sticky=W)

        def OnDateChanged(d):
            setTimes(self, d)

        self.dentistLabel = Label(self.content, text="Dentist", fg="salmon", font=(None, 11))
        self.dentistLabel.grid(row=1, column=0, sticky=W)
        self.dentist = IntVar()
        self.stanley = Radiobutton(self.content, text="Dr. Stanley", variable=self.dentist, value=0, fg="salmon", command=lambda:setTimes(self, self.date.get()))
        self.stanley.grid(row=1, column=1, sticky=W)
        self.ong = Radiobutton(self.content, text="Dr. Ong", variable=self.dentist, value=1, fg="salmon", command=lambda:setTimes(self, self.date.get()))
        self.ong.grid(row=1, column=1)

        self.treatmentLabel = Label(self.content, text="Type of Treatment", fg="salmon", font=(None, 12))
        self.treatmentLabel.grid(row=2, column=0, sticky=W)
        self.typeOfTreatment = IntVar()
        self.extraction = Radiobutton(self.content, text="Extractions", variable=self.typeOfTreatment, value=0, fg="salmon")
        self.extraction.grid(row=3, column=0, sticky=W)
        self.filling = Radiobutton(self.content, text="Fillings & Repairs", variable=self.typeOfTreatment, value=1, fg="salmon")
        self.filling.grid(row=3, column=1, sticky=W)
        self.cleaning = Radiobutton(self.content, text="Teeth Cleaning", variable=self.typeOfTreatment, value=2, fg="salmon")
        self.cleaning.grid(row=3, column=1)
        self.denture = Radiobutton(self.content, text="Dentures", variable=self.typeOfTreatment, value=3, fg="salmon")
        self.denture.grid(row=3, column=1, sticky=E)

        self.dateLabel = Label(self.content, text="Date", fg="salmon", font=(None, 11))
        self.dateLabel.grid(row=4, column=0, sticky=W)
        self.date = StringVar(window)
        self.date.set(dateSlots[0])
        self.dateOption = OptionMenu(self.content, self.date, *dateSlots, command=OnDateChanged)
        self.dateOption.grid(row=4, column=1, sticky=W)

        self.timeLabel = Label(self.content, text="Time", fg="salmon", font=(None, 11))
        self.timeLabel.grid(row=5, column=0, sticky=W)

        self.remarkLabel = Label(self.content, text="Remark", fg="salmon", font=(None, 11))
        self.remarkLabel.grid(row=6, column=0, sticky=W)
        self.remark = StringVar()
        self.remarkEntered = Entry(self.content, textvariable=self.remark, width=60)
        self.remarkEntered.grid(row=6, column=1)

        warningLabel2 = Label(self.content, text="Your remark should be less than 20 words", fg="salmon", font=(None, 8))
        warningLabel2.grid(row=7, column=1, sticky=W)

        setTimes(self, dateSlots[0])

class PatientViewAppointments(Frame):
    def showPatientCreateAppointment(self):
        self.grid_forget()
        self.content.grid_forget()
        self.app = PatientCreateAppointment(self.master) 

    def cancelAppointment(self, tree):
        if tree.focus() == "":
            return
        selectedItem = tree.focus()
        selectedValues = tree.item(selectedItem, "values")
        if selectedValues[4] == "Pending" and (selectedValues[0] != str(datetime.date.today()) and selectedValues[0] != str(datetime.date.today() + datetime.timedelta(days=1))):
            tree.delete(selectedItem)
            tree.insert("", selectedItem, selectedItem,
                        values=(selectedValues[0], selectedValues[1], selectedValues[2], selectedValues[3], "Cancelled"))
            
            appointmentList[int(selectedItem)][6] = "Cancelled"
            pickle.dump(appointmentList, open("appointment", "wb"))
        else:
            messagebox.showerror(title="Oriental Dentist Clinic", message="Unable to cancel an appointment that is scheduled soon or not pending.")
    
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.content = Frame(window)

        self.grid(sticky=NSEW)
        self.content.grid(sticky=NSEW)

        self.grid_rowconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=5)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=8)

        yourAppointment = Label(self, text="Your Appointments", fg="salmon", font=("Arial", 12))
        yourAppointment.grid(row=0, column=0, sticky=W)
    
        createAppointment = Button(self, text="Create Appointment", bg="salmon", fg="white", font=(None, 10), command=lambda:self.showPatientCreateAppointment())
        createAppointment.grid(row=0, column=1, sticky=E)

        tree = ttk.Treeview(self.content, selectmode = "browse")

        tree["show"] = "headings"
        tree["columns"]=("1", "2", "3", "4", "5")
        
        tree.column("1", width=100, minwidth=100)
        tree.column("2", width=100, minwidth=100)
        tree.column("3", width=100, minwidth=100)
        tree.column("4", width=100, minwidth=100)
        tree.column("5", width=100, minwidth=100)

        tree.heading("1", text="Date", anchor=W)
        tree.heading("2", text="Time", anchor=W)
        tree.heading("3", text="Treatment", anchor=W)
        tree.heading("4", text="Dentist", anchor=W)
        tree.heading("5", text="Status", anchor=W)

        tree.grid(row=2, column=0, sticky=W)

        for appointment in appointmentList:
            if appointment[0] == userID:
                tree.insert("", appointmentList.index(appointment), appointmentList.index(appointment), values=(appointment[3], appointment[4], appointment[2], staffList[appointment[1]][2], appointment[6]))

        cancel = Button(self.content, text="Cancel Appointment", bg="salmon", fg="white", font=(None, 9), command=lambda:self.cancelAppointment(tree))
        cancel.grid(row=3, column=0, sticky=E)

class DentistViewAppointments(Frame):
    def updateStatus(self, tree):
        if tree.focus() == "":
            return
        selectedItem = tree.focus()
        selectedValues = tree.item(selectedItem, "values")
        selectedIndex = tree.index(selectedItem)
        tree.delete(selectedItem)
        tree.insert("", selectedIndex, selectedIndex,
                    values=(selectedValues[0], selectedValues[1], selectedValues[2], selectedValues[3], selectedValues[4], selectedValues[5], self.status.get()))
            
        appointmentList[int(selectedItem)][6] = self.status.get()
        pickle.dump(appointmentList, open("appointment", "wb"))

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.content = Frame(window)

        self.grid(sticky=NSEW)
        self.content.grid(sticky=NSEW)

        self.grid_rowconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=5)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=8)

        yourAppointment = Label(self, text="Your Appointments", fg="salmon", font=("Arial", 12))
        yourAppointment.grid(row=0, column=0, sticky=W)
    
        viewReport = Button(self, text="View report", bg="salmon", fg="white", font=(None, 10))
        viewReport.grid(row=0, column=1, sticky=E)

        tree = ttk.Treeview(self.content, selectmode = "browse")

        tree["show"] = "headings"
        tree["columns"]=("1", "2", "3", "4", "5", "6", "7")
        
        tree.column("1", width=72, minwidth=72)
        tree.column("2", width=72, minwidth=72)
        tree.column("3", width=72, minwidth=72)
        tree.column("4", width=72, minwidth=72)
        tree.column("5", width=68, minwidth=68)
        tree.column("6", width=68, minwidth=68)
        tree.column("7", width=72, minwidth=72)

        tree.heading("1", text="Name", anchor=W)
        tree.heading("2", text="IC Number", anchor=W)
        tree.heading("3", text="Treatment", anchor=W)
        tree.heading("4", text="Date", anchor=W)
        tree.heading("5", text="Time", anchor=W)
        tree.heading("6", text="Remark", anchor=W)
        tree.heading("7", text="Status", anchor=W)

        tree.grid(row=2, column=0, sticky=W)

        for appointment in appointmentList:
            if appointment[1] == userID:
                tree.insert("", appointmentList.index(appointment), appointmentList.index(appointment), values=(patientList[appointment[0]][2], patientList[appointment[0]][3], appointment[2], appointment[3], appointment[4], appointment[5], appointment[6]))

        statusSlot = ["Confirmed", "Rejected", "Completed", "No-show"]

        self.status = StringVar(window)
        self.status.set(statusSlot[0])
        self.slotOption = OptionMenu(self.content, self.status, *statusSlot)
        self.slotOption.grid(row=3, column=0, sticky=W)

        apply = Button(self.content, text="Apply", bg="salmon", fg="white", font=(None, 9), command=lambda:self.updateStatus(tree))
        apply.grid(row=3, column=0, sticky=E)

class DentistViewRecords(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.content = Frame(window)

        self.grid(sticky=NSEW)
        self.content.grid(sticky=NSEW)

        self.grid_rowconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=5)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=8)

        recordsLabel = Label(self, text="Appointment Records", fg="salmon", font=("Arial", 12))
        recordsLabel.grid(row=0, column=0, sticky=W)

        tree = ttk.Treeview(self.content, selectmode = "browse")
        #tree["show"] = "headings"
        tree["columns"]=("1", "2", "3", "4", "5", "6", "7", "8")
        
        tree.column("#0", width=20, minwidth=20)
        tree.column("1", width=100, minwidth=100)
        tree.column("2", width=100, minwidth=100)
        tree.column("3", width=100, minwidth=100)
        tree.column("4", width=100, minwidth=100)
        tree.column("5", width=100, minwidth=100)
        tree.column("6", width=100, minwidth=100)
        tree.column("7", width=100, minwidth=100)
        tree.column("8", width=100, minwidth=100)

        tree.heading("1", text="Dentist", anchor=W)
        tree.heading("2", text="Patient", anchor=W)
        tree.heading("3", text="IC Number", anchor=W)
        tree.heading("4", text="Treatment", anchor=W)
        tree.heading("5", text="Date", anchor=W)
        tree.heading("6", text="Time", anchor=W)
        tree.heading("7", text="Remark", anchor=W)
        tree.heading("8", text="Status", anchor=W)

        tree.grid(row=1, column=0, sticky=W)

        for record in recordsList:
            tree.insert("", recordsList.index(record), recordsList.index(record), values=(record[0] + ": " + record[1], "", "", "", record[2], "", "", ""))

            for appointment in record[3]:
                appointmentIndex = int(record[3][record[3].index(appointment)])
                tree.insert(recordsList.index(record), record[3].index(appointment), str(recordsList.index(record)) + str(record[3].index(appointment)), 
                            values=(staffList[appointmentList[appointmentIndex][1]][2], patientList[appointmentList[appointmentIndex][0]][2], patientList[appointmentList[appointmentIndex][0]][3], appointmentList[appointmentIndex][2], appointmentList[appointmentIndex][3], appointmentList[appointmentIndex][4], appointmentList[appointmentIndex][5], appointmentList[appointmentIndex][6]))

class NurseCreateRecord(Frame):
    def searchResults(self, tree):
        tree.delete(*tree.get_children())
        for appointment in appointmentList:
            isFound = False
            if self.search.get() == "Name":
                isFound = patientList[appointment[0]][2] == self.searchContent.get()
            elif self.search.get() == "IC Number":
                isFound = patientList[appointment[0]][3] == self.searchContent.get()
            else: #Type of Treatment
                isFound = appointment[2] == self.searchContent.get()

            if isFound:
                tree.insert("", appointmentList.index(appointment), appointmentList.index(appointment), values=(patientList[appointment[0]][2], patientList[appointment[0]][3], appointment[2], appointment[3], appointment[4], appointment[5], appointment[6]))

    def saveRecord(self, tree):
        if len(tree.get_children()) == 0:
            messagebox.showerror(title="Oriental Dentist Clinic", message="There are no records to save.")
        else:
            appointments = [] #list of appointment ID's
            for item in tree.get_children(): #"item" is the appointmentList index
                appointments.append(item)

            global recordsList
            recordsList.append([self.search.get(), self.searchContent.get(), datetime.date.today(), appointments])
            pickle.dump(recordsList, open("records", "wb"))

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.content = Frame(window)

        self.grid(sticky=NSEW)
        self.content.grid(sticky=NSEW)

        self.grid_rowconfigure(0, weight=1)
        self.content.grid_rowconfigure(2, weight=5)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)

        self.reportLabel = Label(self, text="Report", fg="salmon", font=("Arial", 15))
        self.reportLabel.grid(row=0, column=0, sticky=W)

        self.searchLabel = Label(self, text="Search by", fg="salmon", font=(None, 11))
        self.searchLabel.grid(row=1, column=0, sticky=W)

        self.searchChoice = ["Name", "IC Number", "Type of Treatment"]
        
        self.search = StringVar(window)
        self.search.set(self.searchChoice[0])
        self.searchOption = OptionMenu(self, self.search, *self.searchChoice)
        self.searchOption.grid(row=1, column=0, sticky=E)

        self.searchButton = Button(self, text="Search", fg="salmon", font=(None,11), command=lambda:self.searchResults(tree))
        self.searchButton.grid(row=1, column=1, sticky=E)

        self.saveButton = Button(self, text="Save Record", fg="salmon", font=(None,11), command=lambda:self.saveRecord(tree))
        self.saveButton.grid(row=1, column=2, sticky=E)
        
        self.searchContent = StringVar()
        self.searchBar = Entry(self.content, textvariable=self.searchContent, width=80)
        self.searchBar.grid(row=2, column=0)

        tree = ttk.Treeview(self.content, selectmode = "browse")

        tree["show"] = "headings"
        tree["columns"]=("1", "2", "3", "4", "5", "6", "7")
        
        tree.column("1", width=72, minwidth=72)
        tree.column("2", width=72, minwidth=72)
        tree.column("3", width=72, minwidth=72)
        tree.column("4", width=72, minwidth=72)
        tree.column("5", width=68, minwidth=68)
        tree.column("6", width=68, minwidth=68)
        tree.column("7", width=72, minwidth=72)

        tree.heading("1", text="Name", anchor=W)
        tree.heading("2", text="IC Number", anchor=W)
        tree.heading("3", text="Treatment", anchor=W)
        tree.heading("4", text="Date", anchor=W)
        tree.heading("5", text="Time", anchor=W)
        tree.heading("6", text="Dentist", anchor=W)
        tree.heading("7", text="Status", anchor=W)

        tree.grid(row=3, column=0, sticky=W)

window = Tk()
window.geometry("500x280")
window.title("Oriental Dentist Clinic")

Initiate()
window.mainloop()