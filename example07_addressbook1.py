from datetime import date
from tkinter import *
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from tkcalendar import Calendar

import csv


def show_calendar():
    root1 = Tk()
    root1.geometry("300x200")
    cal = Calendar(root1, selectmode ='day', year=2021, month=9, day=20)
    cal.pack(pady=20)


class App(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.filename = None

        # list to store data in memory
        self.datalist = []

        # currently displayed record
        self.currentindex = 0

        self.mainframe = Frame()
        Label(self.mainframe, text="First Name:").grid(column=0, row=0, sticky="W")
        self.firstname_entry = Entry(self.mainframe, width=30)
        self.firstname_entry.grid(column=1, row=0, sticky="W")

        Label(self.mainframe, text="Last Name:").grid(column=0, row=1, sticky="W")
        self.lastname_entry = Entry(self.mainframe, width=30)
        self.lastname_entry.grid(column=1, row=1, sticky="W")

        Label(self.mainframe, text="Address:").grid(column=0, row=2, sticky="W")
        self.address_entry = Entry(self.mainframe, width=30)
        self.address_entry.grid(column=1, row=2, sticky="W")

        Label(self.mainframe, text="Phone:").grid(column=0, row=3, sticky="W")
        self.phone_entry = Entry(self.mainframe, width=30)
        self.phone_entry.grid(column=1, row=3, sticky="W")

        Label(self.mainframe, text="Email:").grid(column=0, row=4, sticky="W")
        self.email_entry = Entry(self.mainframe, width=30)
        self.email_entry.grid(column=1, row=4, sticky="W")




        self.add_button = Button(self.mainframe, text="Add", width=12, command=self.add_record)
        self.add_button.grid(column=2, row=0, padx=5)

        self.delete_button = Button(self.mainframe, text="Delete", width=12, command=self.delete_record)
        self.delete_button.grid(column=2, row=1, padx=10)

        self.update_button = Button(self.mainframe, text="Update", width=12, command=self.update_record)
        self.update_button.grid(column=2, row=2, padx=10)

        self.save_as_button = Button(self.mainframe, text="Save As...", width=12, command=self.save_as)
        self.save_as_button.grid(column=2, row=3, padx=10)

        self.save_button = Button(self.mainframe, text="Save", width=12, command=self.save)
        self.save_button.grid(column=2, row=4, padx=10)

        self.openfile_button = Button(self.mainframe, text="Open File...", width=12, command=self.readfile)
        self.openfile_button.grid(column=2, row=5, padx=10)

        self.clear_button = Button(self.mainframe, text="Clear", width=12, command=self.clear_entries)
        self.clear_button.grid(column=2, row=6, padx=10)

        self.calendar_button = Button(self.mainframe, text="Calendar", width=12, command=show_calendar)
        self.calendar_button.grid(column=1, row=6, padx=10)
        self.mainframe.pack(side=TOP)

        names = ["First", "Previous", "Next", "Last"]
        self.nav_buttons = []
        self.navFrame = Frame()
        # The lambda values are  0 = First, 1 = Previous 2 = Next, 3 = Last
        for item in range(0, len(names)):
            b = Button(self.navFrame, text=names[item], bg="steelblue", fg="white", width=12,
                       command=lambda i=item: self.check_navigation(i))
            self.nav_buttons.append(b)
            self.nav_buttons[item].grid(row=0, column=item, padx=2, pady=4)

        self.navFrame.pack(side=BOTTOM)

    def add_record(self):  # reads data from GUI and adds each record to datalist[]
        print(self.firstname_entry.get(), self.lastname_entry.get(),
              self.address_entry.get(), self.phone_entry.get(), self.email_entry.get())

        record = (self.firstname_entry.get(), self.lastname_entry.get(),
                  self.address_entry.get(), self.phone_entry.get(), self.email_entry.get())

        self.datalist.append(record)  # adds record
        self.currentindex = len(self.datalist) - 1
        print(self.datalist)
        mb.showinfo("Record Added", "One Record Added")
        self.clear_entries()

    def delete_record(self):
        try:
            del self.datalist[self.currentindex]
            self.display(self.currentindex)
        except Exception:
            mb.showinfo("Nothing to delete", "No Record Found")

    def update_record(self):
        record = (self.firstname_entry.get(), self.lastname_entry.get(),
                  self.address_entry.get(), self.phone_entry.get(), self.email_entry.get())
        self.datalist[self.currentindex] = record
        print(self.datalist[self.currentindex])

    def check_navigation(self, value):
        if value == 0:  # first _button
            self.currentindex = 0
        elif value == 1:  # previous _button
            self.currentindex -= 1
        elif value == 2:  # next _button
            self.currentindex += 1
        elif value == 3:  # last _button
            self.currentindex = len(self.datalist) - 1
        else:  # just in case!
            self.currentindex = 0

        self.display(self.currentindex)

    def display(self, index):
        self.clear_entries()

        if index < 0:
            index = 0

        if index >= (len(self.datalist) - 1):
            index = (len(self.datalist) - 1)

        row = self.datalist[index]
        self.firstname_entry.insert(0, row[0])
        self.lastname_entry.insert(0, row[1])
        self.address_entry.insert(0, row[2])
        self.phone_entry.insert(0, row[3])
        self.email_entry.insert(0, row[4])

        self.currentindex = index

    def clear_entries(self):
        self.firstname_entry.delete(0, END)
        self.lastname_entry.delete(0, END)
        self.address_entry.delete(0, END)
        self.phone_entry.delete(0, END)
        self.email_entry.delete(0, END)

    def save_as(self):

        self.filename = fd.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("csv files", ".csv"), ("all files", ".*")])
        self.writefile()

    def save(self):
        if self.filename is None or self.filename == "":
            self.save_as()
        else:
            self.writefile()

    def writefile(self):

        if len(self.datalist) > 0:
            csvfile = open(file=self.filename, mode='a', newline='\n')
            writer = csv.writer(csvfile, delimiter=",")

            for lcv in range(0, len(self.datalist)):
                writer.writerow(self.datalist[lcv])

            csvfile.close()

        else:
            print("Nothing to save")

    def readfile(self):

        self.datalist.clear()
        self.filename = fd.askopenfilename(defaultextension=".csv",
                                           filetypes=[("csv files", ".csv"), ("all files", ".*")])
        csvfile = open(self.filename, 'r')
        reader = csv.reader(csvfile, delimiter=',')

        for line in reader:
            print(tuple(line))
            self.datalist.append(line)

        self.display(0)  # display first record
        csvfile.close()
        self.currentindex = 0
        print(self.datalist)






if __name__ == "__main__":
    root = Tk()
    root.title("Address Book")
    root.geometry("400x220+0+0")
    app = App(master=root)  # call constructor
    app.mainloop()
