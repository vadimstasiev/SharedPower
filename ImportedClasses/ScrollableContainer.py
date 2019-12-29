# original source: https://stackoverflow.com/questions/53383943
from tkinter import Tk, Frame, Scrollbar, Canvas, Label, Button, Checkbutton


class ScrollableContainer(Frame):
    def __init__(self, master, **kwargs):
        scroll = kwargs.pop("scroll", 'both')
        self.moveto = kwargs.pop("moveto", 0)
        Frame.__init__(self, master, **kwargs)  # holds canvas & scrollbars
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas = Canvas(self, bd=0, highlightthickness=0)
        self.hScroll = Scrollbar(self, orient='horizontal',
                                 command=self.canvas.xview)
        self.vScroll = Scrollbar(
            self, orient='vertical', command=self.canvas.yview)

        hScrollGrid = {"row": 1, "column": 0, "sticky": 'we'}
        vScrollGrid = {"row": 0, "column": 1, "sticky": 'ns'}
        if scroll == 'both':
            self.hScroll.grid(hScrollGrid)
            self.vScroll.grid(vScrollGrid)
        elif scroll == 'horizontal':
            self.hScroll.grid(hScrollGrid)
        elif scroll == 'vertical':
            self.vScroll.grid(vScrollGrid)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.canvas.configure(xscrollcommand=self.hScroll.set,
                              yscrollcommand=self.vScroll.set)

        self.container = Frame(self.canvas, bd=2)
        self.container.grid_columnconfigure(0, weight=1)

        self.canvas.create_window(
            0, 0, window=self.container, anchor='nw', tags='inner')

    def update_layout(self):
        self.container.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        self.canvas.yview_moveto(self.moveto)
        self.size = self.container.grid_size()
        self.canvas.bind('<Configure>', self.on_configure)

    def on_configure(self, event):
        w, h = event.width, event.height
        natural = self.container.winfo_reqwidth()
        self.canvas.itemconfigure('inner', width=w if w > natural else natural)
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def grid(self, **kw):
        self.update_layout()
        Frame.grid(self, kw)


if __name__ == "__main__":
    # e.g.
    root = Tk()
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    sc = ScrollableContainer(root, bd=2, scroll='vertical', moveto=1)
    #####
    product_label = Label(sc.container, text='Products')
    product_label.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)
    products = []
    for i in range(1, 21):
        item = Frame(sc.container, bd=2)
        item.grid_rowconfigure(1, weight=1)
        item.grid_columnconfigure(0, weight=1)
        text = Label(item, text=('Product' + str(i)), anchor='w')
        text.grid(row=0, column=0, sticky='nsew')
        check = Checkbutton(item, anchor='w')
        check.grid(row=0, column=1)
        item.grid(row=i, column=0, sticky='nsew', padx=2, pady=2)
    products.append(item)
    button_frame = Frame(sc.container)
    button_frame.grid(row=21, column=0)
    remove_server_button = Button(button_frame, text='Remove server')
    remove_server_button.grid(row=0, column=0)
    #####
    sc.grid(row=0, column=0, sticky='nsew')
    root.mainloop()
