from tkinter import *
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import csv


class App(Frame):  # App is name of the class

    def __init__(self, master=None):  # inheriting from class Frame
        Frame.__init__(self, master)

        self.filename = None

        # list to store data in memory
        self.datalist = []

        # currently displayed record
        self.currentindex = 0

        self.mainframe = Frame()
        Label(self.mainframe, text="ID:").grid(column=0, row=0, sticky="W")
        self.ID = Entry(self.mainframe, width=30)
        self.ID.grid(column=1, row=0, sticky="W")

        Label(self.mainframe, text="Booker Name:").grid(column=0, row=1, sticky="W")
        self.Booker_Name = Entry(self.mainframe, width=30)
        self.Booker_Name.grid(column=1, row=1, sticky="W")

        Label(self.mainframe, text="Room Name:").grid(column=0, row=2, sticky="W")
        self.Room_Name = Entry(self.mainframe, width=30)
        self.Room_Name.grid(column=1, row=2, sticky="W")

        Label(self.mainframe, text="From Date:").grid(column=0, row=3, sticky="W")
        self.From_Date = Entry(self.mainframe, text="", width=30)
        self.From_Date.grid(column=1, row=3, sticky="W")

        Label(self.mainframe, text="Until Date:").grid(column=0, row=4, sticky="W")
        self.Until_Date = Entry(self.mainframe, text="", width=30)
        self.Until_Date.grid(column=1, row=4, sticky="W")

        self.add_button = Button(self.mainframe, text="Add", bg="slate gray", width=12, command=self.add_record)
        self.add_button.grid(column=2, row=0, padx=5)

        self.delete_button = Button(self.mainframe, text="Delete", bg="slate gray", width=12,
                                    command=self.delete_record)
        self.delete_button.grid(column=2, row=1, padx=10)

        self.update_button = Button(self.mainframe, text="Update", bg="slate gray", width=12,
                                    command=self.update_record)
        self.update_button.grid(column=2, row=2, padx=10)

        self.save_as_button = Button(self.mainframe, text="Save As...", bg="slate gray", width=12, command=self.save_as)
        self.save_as_button.grid(column=2, row=3, padx=10)

        self.save_button = Button(self.mainframe, text="Save", bg="slate gray", width=12, command=self.save)
        self.save_button.grid(column=2, row=4, padx=10)

        self.openfile_button = Button(self.mainframe, text="Open File...", bg="slate gray", width=12,
                                      command=self.readfile)
        self.openfile_button.grid(column=2, row=5, padx=10)

        self.clear_button = Button(self.mainframe, text="Clear", bg="slate gray", width=12, command=self.clear_entries)
        self.clear_button.grid(column=2, row=6, padx=10)
        self.mainframe.pack(side=TOP)  # putting mainframe onto top side of office tool

        names = ["First", "Previous", "Next", "Last"]
        self.nav_buttons = []
        self.navFrame = Frame()
        # The lambda values are  0 = First, 1 = Previous 2 = Next, 3 = Last
        for item in range(0, len(names)):
            b = Button(self.navFrame, text=names[item], bg="dark slate gray", fg="white", width=12,
                       # creates the buttons
                       command=lambda i=item: self.check_navigation(i))
            self.nav_buttons.append(b)  # added to nav buttons
            self.nav_buttons[item].grid(row=0, column=item, padx=2, pady=4)  # positioning the buttons

        self.navFrame.pack(side=BOTTOM)  # places the buttons at the bottom of the screen

    def add_record(self):  # reads data from GUI and adds each record to datalist[]
        #   adds record to datalist
        print(self.ID.get(), self.Booker_Name.get(),  # prints out new record which has just been added
              self.Room_Name.get(), self.From_Date.get(), self.Until_Date.get())

        record = (self.ID.get(), self.Booker_Name.get(),  # local record variable
                  self.Room_Name.get(), self.From_Date.get(), self.Until_Date.get())

        self.datalist.append(record)  # adds record
        self.currentindex = len(self.datalist) - 1  # subtract 1 and it gives us our last record
        print(self.datalist)
        mb.showinfo("Record Added", "One Record Added")  # printing Message Box
        self.clear_entries()

    def delete_record(self):
        try:
            del self.datalist[self.currentindex]  # del keyword used to delete, does not update, have to click update
            self.display(self.currentindex)
        except Exception:
            mb.showinfo("Nothing to delete", "No Record Found")  # Message box

    def update_record(self):  # similar to add record
        # line below gets data from entries on GUI
        record = (self.ID.get(), self.Booker_Name.get(),
                  self.Room_Name.get(), self.From_Date.get(), self.Until_Date.get())
        # assign record to the datalist
        self.datalist[self.currentindex] = record
        print(self.datalist[self.currentindex])  # does not save data, must click save button
        mb.showinfo("Record update", "Record updated")

    def check_navigation(self, value):
        if value == 0:  # first _button
            self.currentindex = 0
        elif value == 1:  # previous _button
            self.currentindex -= 1  # reduce the index
        elif value == 2:  # next _button
            self.currentindex += 1  # increases the index
        elif value == 3:  # last _button
            self.currentindex = len(self.datalist) - 1  # gets length of the datalist -1
        else:  # just in case!
            self.currentindex = 0  # 0 displays the first record

        self.display(self.currentindex)

    def display(self, index):
        self.clear_entries()  # clears tx boxes

        if index < 0:
            index = 0

        if index >= (len(self.datalist) - 1):
            index = (len(self.datalist) - 1)

        row = self.datalist[index]  # puts records from file and into the display
        self.ID.insert(0, row[0])
        self.Booker_Name.insert(0, row[1])
        self.Room_Name.insert(0, row[2])
        self.From_Date.insert(0, row[3])
        self.Until_Date.insert(0, row[4])

        self.currentindex = index

    def clear_entries(self):  # clears the text boxes
        self.ID.delete(0, END)
        self.Booker_Name.delete(0, END)
        self.Room_Name.delete(0, END)
        self.From_Date.delete(0, END)
        self.Until_Date.delete(0, END)

    def save_as(self):
        #    displays the dialog box
        self.filename = fd.asksaveasfilename(defaultextension=".csv",  # defaults to csv
                                             filetypes=[("csv files", ".csv"), ("all files", ".*")])
        self.writefile()  # saves the records
        mb.showinfo("Save Record", "Record Saved")

    def save(self):
        if self.filename is None or self.filename == "":
            self.save_as()
        else:
            self.writefile()

    def writefile(self):

        if len(self.datalist) > 0:
            csvfile = open(file=self.filename, mode='w', newline='\n')
            writer = csv.writer(csvfile, delimiter=",")

            for lcv in range(0, len(self.datalist)):
                writer.writerow(self.datalist[lcv])  # writes the file

            csvfile.close()  # close file after to write it

        else:
            print("Nothing to save")

    def readfile(self):  # opens the file

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
    root = Tk()  # creating tk object, creating window
    root.title("Office Booking Tool")
    root.geometry("500x220+0+0")
    app = App(master=root)  # call constructor
    app.mainloop()
