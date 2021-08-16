from tkinter import *
from tkinter import filedialog
from backendv2 import Database


class UI:

    def __init__(self, master):
        self.database = Database()

        #Label widgets
        self.building_callsign_label = Label(master, text="Building callsign")       #Building callsign label
        self.building_callsign_label.grid(row=0, column=0)                           #Setup location for Building callsign label

        self.all_prism_label = Label(master, text="All Prisms")
        self.all_prism_label.grid(row=0, column=2)

        self.nw_prism_label = Label(master, text="NW Prism")
        self.nw_prism_label.grid(row=1, column=0)

        self.ne_prism_label = Label(master, text="NE Prism")
        self.ne_prism_label.grid(row=1, column=2)

        self.sw_prism_label = Label(master, text="SW Prism")
        self.sw_prism_label.grid(row=2, column=0)

        self.se_prism_label = Label(master, text="SE Prism")
        self.se_prism_label.grid(row=2, column=2)

        self.ns_distance_label = Label(master, text="NS Distance")
        self.ns_distance_label.grid(row=3, column=0)

        self.we_distance_label = Label(master, text="WE Distance")
        self.we_distance_label.grid(row=3, column=2)

        self.station_id_label = Label(master, text="Station ID")
        self.station_id_label.grid(row=4, column=0)

        self.variable_id_label = Label(master, text="Variable ID")
        self.variable_id_label.grid(row=4, column=2)


        #Input box widgets
        self.building_callsign_text = StringVar()                       #Create a StringVar object
        self.building_callsign_input_box = Entry(master, textvariable=self.building_callsign_text, width=40)      #Create Building callsign entry box widget
        self.building_callsign_input_box.grid(row=0, column=1)          #Setup Building callsign entry box widget location

        self.all_prism_text = StringVar()
        self.all_prism_input_box = Entry(master, textvariable=self.all_prism_text, width=40)
        self.all_prism_input_box.grid(row=0, column=3)

        self.nw_prism_text = StringVar()
        self.nw_prism_input_box = Entry(master, textvariable=self.nw_prism_text, width=40)
        self.nw_prism_input_box.grid(row=1, column=1)

        self.ne_prism_text = StringVar()
        self.ne_prism_input_box = Entry(master, textvariable=self.ne_prism_text, width=40)
        self.ne_prism_input_box.grid(row=1, column=3)

        self.sw_prism_text = StringVar()
        self.sw_prism_input_box = Entry(master, textvariable=self.sw_prism_text, width=40)
        self.sw_prism_input_box.grid(row=2, column=1)

        self.se_prism_text = StringVar()
        self.se_prism_input_box = Entry(master, textvariable=self.se_prism_text, width=40)
        self.se_prism_input_box.grid(row=2, column=3)

        self.ns_distance_text = StringVar()
        self.ns_distance_input_box = Entry(master, textvariable=self.ns_distance_text, width=40)
        self.ns_distance_input_box.grid(row=3, column=1)

        self.we_distance_text = StringVar()
        self.we_distance_input_box = Entry(master, textvariable=self.we_distance_text, width=40)
        self.we_distance_input_box.grid(row=3, column=3)

        self.station_id_text = StringVar()
        self.station_id_input_box = Entry(master, textvariable=self.station_id_text, width=40)
        self.station_id_input_box.grid(row=4, column=1)

        self.variable_id_text = StringVar()
        self.variable_id_input_box = Entry(master, textvariable=self.variable_id_text, width=40)
        self.variable_id_input_box.grid(row=4, column=3)

        #Filepath display for import button
        self.import_filepath_text = StringVar()
        self.import_filepath_display = Entry(master, textvariable=self.import_filepath_text, width=55)
        # columnspan argument as this widget's location is at row 12th, column 0th, the length expands to 2 columns
        self.import_filepath_display.grid(row=12, column=0, columnspan=2)


        #List box widget
        self.list_box = Listbox(master, height=9, width=55, selectmode=EXTENDED)       #Create a listbox and setup its size; selectmode=EXTENDED for multiple selection
        self.list_box.grid(row=5, column=0, rowspan=7, columnspan=2)                   #rowspan argument as this widget height expands to 7 rows


        #Vertical scrollbar widget
        self.vertical_scrollbar = Scrollbar(master)                                 #Create a scrollbar for the listbox
        self.vertical_scrollbar.grid(row=6, column=2, rowspan=4, sticky="NS")       #Setup the scrollbar's location and size - extends from top to bottom
        self.list_box.configure(yscrollcommand=self.vertical_scrollbar.set)         #Attach the vertical scrollbar to the listbox
        self.vertical_scrollbar.configure(command=self.list_box.yview)              #Setup scrollbar for vertical scrolling

        #Horizontal scrollbar widget
        self.horizontal_scrollbar = Scrollbar(master, orient="horizontal")
        self.horizontal_scrollbar.grid(row=11,column=0,columnspan=2,sticky="WE")    #Setup the scrollbar's location and size - extends from left to right
        self.list_box.configure(xscrollcommand=self.horizontal_scrollbar.set)       #Attach the horizontal scrollbar to the listbox
        self.horizontal_scrollbar.configure(command=self.list_box.xview)            #Setup scrollbar for horizontal scrolling


        self.list_box.bind('<<ListboxSelect>>', self.get_selected_row)          #Bind the method get_selected_row to Listbox selection event


        #Button widgets
        self.add_entry_button = Button(master, text="Add Entry", width=12, command=self.add_command)
        self.add_entry_button.grid(row=5, column=3)

        self.search_entry_button = Button(master, text="Search Entry", width=12, command=self.search_command)
        self.search_entry_button.grid(row=6, column=3)

        self.view_all_button = Button(master, text="View All", width=12, command=self.view_command)
        self.view_all_button.grid(row=7, column=3)

        self.update_button = Button(master, text="Update", width=12, command=self.update_command)
        self.update_button.grid(row=8, column=3)

        self.delete_button = Button(master, text="Delete", width=12, command=self.delete_command)
        self.delete_button.grid(row=9, column=3)

        self.export_button = Button(master, text="Export", width=12, command=self.Export_file)
        self.export_button.grid(row=10, column=3)

        self.manual_input_button = Button(master, text="Manual Input", width=12, command=self.manual_input)
        self.manual_input_button.grid(row=11, column=3)

        self.import_button = Button(master, text="Import", width=12, command=self.import_command)
        self.import_button.grid(row=12, column=3)


    def get_selected_row(self, event):
        try:
            index = self.list_box.curselection()[0]          #the index (id) of selected item
            # print(index)
            self.selected_tuple = self.list_box.get(index)
            self.building_callsign_input_box.delete(0, END)
            self.building_callsign_input_box.insert(END, self.selected_tuple[2])
            self.all_prism_input_box.delete(0, END)
            self.all_prism_input_box.insert(END, self.selected_tuple[5])
            self.station_id_input_box.delete(0, END)
            self.station_id_input_box.insert(END, self.selected_tuple[1])
            self.indexlist = [self.list_box.get(index1)[0] for index1 in self.list_box.curselection()]
            print(self.selected_tuple)
            print(self.indexlist)
        except IndexError:
            pass

    def add_command(self):
        self.database.calculate(self.building_callsign_text.get(), self.all_prism_text.get(), self.nw_prism_text.get(),
                                self.ne_prism_text.get(), self.sw_prism_text.get(), self.se_prism_text.get(),
                                self.ns_distance_text.get(), self.we_distance_text.get(), self.station_id_text.get(),
                                self.variable_id_text.get())

    def search_command(self):
        self.list_box.delete(0, END)            #Delete items in listbox
        # loop for fetching data in SQLite database based on search value
        for row in self.database.Search(self.building_callsign_text.get()):
            self.list_box.insert(END, row)                  #Insert data in listbox

    def view_command(self):
        self.list_box.delete(0, END)
        # loop for getting data in SQLite database
        for row in self.database.view():
            self.list_box.insert(END, row)

    def update_command(self):
        self.database.update(self.selected_tuple[0], self.station_id_text.get(),
                             self.building_callsign_text.get(), self.all_prism_text.get())

    def delete_command(self):
        if self.indexlist:
            self.database.delete(self.indexlist)
        #loop starting from the end of tuple for correct delete animation
        for item in self.list_box.curselection()[:]:
            self.list_box.delete(item)

    def Export_file(self):
        self.database.export()

    def manual_input(self):
        self.database.insert(self.station_id_text.get(), self.building_callsign_text.get(),
                             self.variable_id_text.get(), self.nw_prism_text.get(), self.all_prism_text.get())

    def import_command(self):
        filepath = filedialog.askopenfilename()         #interface for choosing import file
        self.import_filepath_display.insert(END, filepath)
        self.database.match(filepath)


if __name__ == "__main__":
    root = Tk()
    app = UI(root)
    root.mainloop()


