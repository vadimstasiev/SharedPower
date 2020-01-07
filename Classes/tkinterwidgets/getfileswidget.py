from tkinter import Tk, Frame, Button, PhotoImage, LabelFrame
from tkinter import messagebox
from tkinter.filedialog import askopenfilename


class PathButton(Button):
    def __init__(self, master, **kwargs):
        Button.__init__(self, master, **kwargs)
        self.path_holder = ""
        self.filename_holder = ""


class GetFilesWidget(Frame):
    # e.g. for the file_types list:
    # file_types = [
    #     ('Python code files', '*.py'),
    #     ('Perl code files', '*.pl;*.pm'),  # semicolon trick
    #     ('Java code files', '*.java'),
    #     ('C++ code files', '*.cpp;*.h'),   # semicolon trick
    #     ('Text files', '*.txt'),
    #     ('All files', '*'),
    # ]
    def __init__(self, master, **kwargs):

        self.empty_message = kwargs.pop(
            'empty_message', 'Click to Select File')
        self.max_items = kwargs.pop('max_items', 100)
        self.ftypes = kwargs.pop('file_types', [])
        Frame.__init__(self, master, **kwargs)
        self.fileFrameList = []
        self.filePathButtonList = []
        self.files_name_str_list = []
        self.files_path_str_list = []
        self._original_SET_list = []  # to be compared with files_path_str_list for changes
        self.add_button = Button(self, text="+", command=self.place__fileFrame)
        self.place__fileFrame()

    def refresh__ADD_button(self):
        if len(self.fileFrameList) <= self.max_items-1:
            self.place__ADD_button()
        else:
            self.add_button.grid_forget()

    def place__ADD_button(self):
        self.add_button.grid(row=0, column=2, sticky='nw')

    def place__fileFrame(self):
        fileFrame = Frame(self)
        self.fileFrameList.append(fileFrame)
        filepath_button = PathButton(fileFrame, text=self.empty_message)
        self.filePathButtonList.append(filepath_button)
        filepath_button.config(
            command=lambda: self.onclick_get_filename(fileFrame, filepath_button))
        filepath_button.grid(sticky="w")
        self.place__DEL_button(fileFrame, filepath_button)
        __i = 0
        for i in self.fileFrameList:
            i.grid(row=__i, sticky="w")
            __i += 1
        self.refresh__ADD_button()

    def automatic__file_input(self, files):
        for i in range(0, len(files)-2):
            self.place__fileFrame()
        fileFrameANDpathbuttonList = zip(
            self.fileFrameList, self.filePathButtonList, files)
        for fileFrameANDpathbutton in fileFrameANDpathbuttonList:
            fileFrame, pathbutton, file = fileFrameANDpathbutton
            self.set_filename(fileFrame, pathbutton, file)

    def onclick_get_filename(self, parent, filepath_button: PathButton):
        file_obtained_Bool = False
        __text = filepath_button.cget('text')
        if __text == self.empty_message:
            if len(self.ftypes) != 0:
                filepath = askopenfilename(filetypes=self.ftypes)
            else:
                filepath = askopenfilename()
            self.current_filepath = filepath
            display_text = filepath[filepath.rfind('/')+1:]
            if display_text != "" and display_text not in self.files_name_str_list:
                file_obtained_Bool = True
                self.files_path_str_list.append(filepath)
                self.files_name_str_list.append(display_text)
                filepath_button.path_holder = filepath
                filepath_button.filename_holder = display_text
                filepath_button.config(text=display_text)
            elif(filepath == ""):
                pass
            else:
                messagebox.showerror(
                    "Error", "This file or a file with the same name was already added")
        return file_obtained_Bool

    def set_filename(self, parent, filepath_button: PathButton, filepath):
        self.current_filepath = filepath
        display_text = filepath[filepath.rfind('/')+1:]
        if display_text != "" and display_text not in self.files_name_str_list:
            self.files_path_str_list.append(filepath)
            self.files_name_str_list.append(display_text)
            self._original_SET_list.append(filepath)
            filepath_button.path_holder = filepath
            filepath_button.filename_holder = display_text
            filepath_button.config(text=display_text)
        elif(filepath == ""):
            pass
        else:
            messagebox.showerror(
                "Error", "This file or a file with the same name was already added")

    def place__DEL_button(self, parent, filepath_button: PathButton):
        del_button = Button(parent, text="-")
        del_button.config(command=lambda: self.onclick_DEL(
            parent, filepath_button))
        del_button.grid(row=0, column=1, sticky='ns')

    def onclick_DEL(self, parent, filepath_button: PathButton):
        if parent != self.fileFrameList[0]:
            self.fileFrameList.remove(parent)
            parent.destroy()
        else:
            filepath_button.config(text=self.empty_message)
        try:
            self.files_path_str_list.remove(filepath_button.path_holder)
            self.files_name_str_list.remove(filepath_button.filename_holder)
        except:
            pass
        self.refresh__ADD_button()

    def get_difference(self):
        added = []
        for i in self.files_path_str_list:
            if i not in self._original_SET_list:
                added.append(i)
        removed = []
        for j in self._original_SET_list:
            if j not in self.files_path_str_list:
                removed.append(j)
        return removed, added

    def get_PATHS(self):
        return self.files_path_str_list


class GetImagesWidget(GetFilesWidget):
    def __init__(self, master, **kwargs):
        self.image_references = []
        self.removed_items = []
        GetFilesWidget.__init__(self, master, **kwargs)
        self.ftypes = [
            ('Image files', '*.png'),
        ]

    def onclick_get_filename(self, parent, filepath_button: PathButton):
        if GetFilesWidget.onclick_get_filename(self, parent, filepath_button) == True:
            photo = PhotoImage(file=self.current_filepath)
            displayable_image = photo.subsample(4)
            self.image_references.append(displayable_image)
            filepath_button.config(image=displayable_image)

    def set_filename(self, parent, filepath_button: PathButton, filepath):
        GetFilesWidget.set_filename(self, parent, filepath_button, filepath)
        try:
            photo = PhotoImage(file=self.current_filepath)
            displayable_image = photo.subsample(4)
            self.image_references.append(displayable_image)
            filepath_button.config(image=displayable_image)
        except:
            self.onclick_DEL(parent, filepath_button)

    def onclick_DEL(self, parent, filepath_button: PathButton):
        filepath_button.config(image="")
        GetFilesWidget.onclick_DEL(self, parent, filepath_button)
        self.removed_items.append(filepath_button.path_holder)


class DisplayImagesWidget(GetImagesWidget):
    def __init__(self, master, **kwargs):
        GetImagesWidget.__init__(self, master, **kwargs)

    def place__fileFrame(self):
        fileFrame = Frame(self)
        self.fileFrameList.append(fileFrame)
        filepath_button = PathButton(fileFrame, text=self.empty_message)
        self.filePathButtonList.append(filepath_button)
        filepath_button.grid(sticky="w")
        __i = 0
        for i in self.fileFrameList:
            i.grid(row=0, padx=5, column=__i, sticky="w")
            __i += 1


if __name__ == "__main__":
    root = Tk()
    mywidget = GetImagesWidget(root)
    mywidget.grid(padx=100, pady=100)
    myFiles = [
        "./random.png",     # these files must be accessible in order to show up
        "./Empty.png"
    ]
    mywidget.automatic__file_input(myFiles)
    root.mainloop()
