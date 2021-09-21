import PySimpleGUI as sg

def input_field_check(input_field):
    """Helper function to perform input field checks against all spaces and illegal characters"""
    #This checks to make sure that the input is not blank or spaces
    if input_field.isspace() == True or input_field == "":
        sg.popup("The file field cannot be empty", title = " ")
        return True

    #This checks for invalid file characters
    if input_field.find("<") != -1 or input_field.find(">") != -1 \
        or input_field.find(":") != -1 or input_field.find("\\") != -1 \
        or input_field.find("/") != -1 or input_field.find("\"") != -1 \
        or input_field.find("|") != -1 or input_field.find("?") != -1 \
        or input_field.find("*") != -1:
            sg.popup("The following characters cannot be used:"
                "< > : \ / \" | ? * ", title= " ")
            return True

    else:
        return False

if __name__ == "__main__":
    input_field_check(input_field)
