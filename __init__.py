# please install the following non-standard libraries: bcrypt, pillow (should no longer be needed) , tkcalendar (includes Babel which is needed)


# Import local classes
from Classes.InterfaceClass import UI_Interface


if __name__ == '__main__':
    program = UI_Interface()
    # program.run()
    # Skip Login for faster testing
    program.log_in_UI(email="test@test", password="123456789")
