# please install the following non-standard libraries: bcrypt,  tkcalendar (includes Babel which is needed)
# pip install bcrypt
# pip install tkcalendar


# Import local classes
from Classes.InterfaceClass import UI_Interface


if __name__ == '__main__':
    program = UI_Interface()
    # program.run()
    # Skip Login for faster testing
    program.log_in_UI(email="test@test", password="123456789")
