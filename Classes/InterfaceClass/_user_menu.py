from tkinter import Label, Frame


def menu_user_options_UI(self):
    self.reset_window()
    self.root.resizable(width=False, height=False)
    self.add_menu_bar_UI_3()
    User_Type = self.user_instance.get_user_type()
    User_Name = self.user_instance.get_user_firstname(
    ) + " " + self.user_instance.get_user_surname()
    user_photos = self.user_instance.get_user_profilephotos()
    User_PhotoImages = self.generate_PhotoImage_list(user_photos, 4)
    button_text_and_functions = []
    if (User_Type == "Tool_User"):
        button_text_and_functions = [
            ("Search for tools", None),
            ("View current orders", None),
            ("View next Invoice", None),
            ("Log Out", self.log_in_UI),
        ]
    elif (User_Type == "Tool_Owner"):
        button_text_and_functions = [
            ("Register tool", self.register_tool_UI),
            ("View Listed Inventory", self.view_listed_inventory_UI),
            ("Search for tools", None),
            ("View current orders", None),
            ("View Purchase History", None),
            ("View next Invoice", None),
            ("Log Out", self.log_in_UI),
        ]
    else:
        self.buffered_errors.append(
            "Database Error - Type of User Unknown")
        self.log_in_UI()
    self.generate_action_buttons_UI(self.root_frame, button_text_and_functions)
    if len(User_PhotoImages) > 0:  # There should only be 1 user photo
        photo_frame = Frame(self.root)
        Label(photo_frame, text='User Photo',
              image=User_PhotoImages[0]).grid(padx=40, row=0)
        Label(photo_frame, text=User_Name, font=(
            "Helvetica", 13)).grid(padx=40, sticky='n', row=1)
        photo_frame.grid(column=2, pady=40, row=0, sticky='n')
    self.root.mainloop()
