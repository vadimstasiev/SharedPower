from tkinter import Button, Label, Entry, Menu, Radiobutton, IntVar
from Classes.tkinterwidgets.dateentry import DateEntry
from tkinter import Frame


def reset_window(self):
    self.root.title("Shared Power")
    self.root.resizable(width=True, height=True)
    self.root.minsize(0, 0)
    self.root.unbind('<Return>')
    __list = self.get_all_children()
    for __child in __list:
        __child.destroy()
    self.root_frame = Frame(self.root, height=2, bd=1)
    self.root.geometry("")
    self.root_frame.grid()
    self.image_references = []  # keeps references so they don't dissapear


def get_all_children(self):
    __list = self.root.winfo_children()
    for item in __list:
        if item.winfo_children():
            __list.extend(item.winfo_children())
    return __list


def generate_action_buttons_UI(self, __widget, __list, **kw):
    __label_padx = kw.pop('label_width', 20)
    __entry_width = kw.pop('entry_width', 25)
    for __line in __list:
        __text, function = __line
        if function != None:
            __button = Button(__widget, text=__text,
                              width=30, command=function)
        else:
            __button = Button(__widget, text=__text, width=30)
        if len(kw) == 0:
            __button.grid(ipady=15, padx=20, pady=20, sticky='w')
        else:
            __button.grid(kw)


def generate_labels_and_entries_UI(self, __widget, __list, **kw):
    __label_padx = kw.pop('label_width', 20)
    __entry_width = kw.pop('entry_width', 25)
    str_keywords = [
        "{type=pw",
    ]
    label_list = []
    entries_list = []
    for __line in __list:
        label_display, var = __line
        __index = __list.index(__line)
        __property = ""
        if(label_display.find("#") != -1):
            for i in str_keywords:
                label_display = label_display.strip(i)
                __property = i
            label_display = label_display.strip("#")
        __label = Label(__widget, text=label_display,
                        padx=__label_padx, pady=3)
        __label.grid(row=__index, sticky='nw')
        label_list.append(__label)
        if var != None:
            entry_dic = {}
            entry_dic['width'] = __entry_width
            entry_dic['textvariable'] = var
            # Apply the right properties
            if(__property == "{type=pw"):
                entry_dic['show'] = "*"
                __entry = Entry(__widget, entry_dic)
            else:
                __entry = Entry(__widget, entry_dic)
            __entry.grid(row=__index, column=1, columnspan=2, sticky='w')
            entries_list.append(__entry)
        else:
            entries_list.append(None)
    return label_list, entries_list


def place_date_entry_get_entry(self, __widget, __var, **kw):
    de_kw = {}
    _date = kw.pop("date", "default")
    if _date != "default":
        de_kw["day"] = _date.day
        de_kw["month"] = _date.month
        de_kw["year"] = _date.year
    __date_entry = DateEntry(
        __widget, width=22, textvariable=__var, date_pattern='d/m/yyyy', **de_kw)
    __date_entry.grid(kw)
    return __date_entry


def place_usertype_entry_get_var(self, __widget, __textB1, __textB2, **kw):
    __user_type_input = IntVar()
    __radio_button1 = Radiobutton(
        __widget, text="Tool User", variable=__user_type_input, value=1)
    __radio_button2 = Radiobutton(
        __widget, text="Tool Owner", variable=__user_type_input, value=2)
    kw['column'] = 1
    __radio_button1.grid(kw)
    kw['column'] = 2
    __radio_button2.grid(kw)
    return __user_type_input


def add_menu_bar_UI_1(self):   # used for Login Screen
    self.menubar = Menu(self.root)
    __submenu = Menu(self.menubar, tearoff=0)
    __submenu.add_command(label="Contact Admin",
                          command=self.contact_admin)
    self.menubar.add_cascade(label="Forgot Password", menu=__submenu)
    self.menubar.add_command(label="Quit", command=self.quit)
    self.root.config(menu=self.menubar)


def add_menu_bar_UI_2(self):   # used for Register Screen
    self.menubar = Menu(self.root)
    __submenu = Menu(self.menubar, tearoff=0)
    __submenu.add_command(label="Go Back", command=self.log_in_UI)
    __submenu.add_command(label="Quit", command=self.quit)
    self.menubar.add_cascade(label="Options", menu=__submenu)
    self.root.config(menu=self.menubar)


def add_menu_bar_UI_3(self):   # used for the tool users/owners UI
    self.menubar = Menu(self.root)
    __submenu = Menu(self.menubar, tearoff=0)
    __submenu.add_command(label="Log Out", command=self.log_in_UI)
    __submenu.add_command(label="Quit", command=self.quit)
    self.menubar.add_cascade(label="Options", menu=__submenu)
    self.root.config(menu=self.menubar)


def add_menu_bar_UI_4(self):   # used for the sub pages of the tool users/owners UI
    __user_type = self.user_instance.get_user_type()
    self.menubar = Menu(self.root)
    __submenu = Menu(self.menubar, tearoff=0)
    __submenu.add_command(label="Go Back", command=lambda: self.go_back_menu())
    __submenu.add_command(label="Quit", command=self.quit)
    self.menubar.add_cascade(label="Options", menu=__submenu)
    self.root.config(menu=self.menubar)


def contact_admin(self):
    print("Contact Admin")


def quit(self):
    self.root.destroy()
    self.root.quit()
