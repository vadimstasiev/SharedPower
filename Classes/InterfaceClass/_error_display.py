from tkinter import Label


def get_buffered_user_errors(self):
    __db_class_error_buffer = self.db_link.db_class_error_buffer
    if(len(__db_class_error_buffer) > 0):
        self.buffered_errors.append(str("#"*40))
        self.buffered_errors.append("Database Class Errors:")
        self.buffered_errors.extend(__db_class_error_buffer)
    __user_class_error_buffer = self.user_instance.user_class_error_buffer
    if(len(__user_class_error_buffer) > 0):
        self.buffered_errors.append(str("#"*40))
        self.buffered_errors.append("User Class Errors:")
        self.buffered_errors.extend(__user_class_error_buffer)
    __tool_class_error_buffer = self.tool_instance.tool_class_error_buffer
    if(len(__tool_class_error_buffer) > 0):
        self.buffered_errors.append(str("#"*40))
        self.buffered_errors.append("User Class Errors:")
        self.buffered_errors.extend(__user_class_error_buffer)
    buffered_errors = tuple(self.buffered_errors)
    self.buffered_errors.clear()
    return buffered_errors


def generate_output_errors_UI(self, __widget, **kw):
    __buffered_errors = self.get_buffered_user_errors()
    __start_on = kw.pop('starting_index', 0)
    for __line in __buffered_errors:
        __index = __buffered_errors.index(__line) + __start_on
        __label = Label(__widget, text=__line, fg="#ff0000")
        if len(kw) == 0:
            __label.grid(row=__index, column=1)
        else:
            kw['row'] = __index
            __label.grid(kw)
        self.outputed_errors_list.append(__label)


def clear_errors(self):
    for __l in self.outputed_errors_list:
        __l.destroy()
