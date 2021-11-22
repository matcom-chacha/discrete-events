import os
from datetime import datetime

# creates a file
def create_file(name, hours, content, date=False):
    cwd = os.getcwd()
    new_path = os.path.join(cwd, "simulations")
    complete_path = os.path.join(new_path, name + ".txt")

    _file = open(complete_path, "w+")

    _file.write("Harbor simulation of " + str(hours) + " hours")

    if date:
        # datetime object containing current date and time
        now = datetime.now()

        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        _file.write("\n")
        _file.write("date: " + dt_string + "\r\n\n")

    _file.write(content)
    _file.close()


def edit_file(name, content):
    cwd = os.getcwd()
    new_path = os.path.join(cwd, "simulations")
    complete_path = os.path.join(new_path, name + ".txt")

    _file = open(complete_path, "a")

    _file.write("\n")
    _file.write(content)
    _file.close()


def write_data(name, content_list):
    for content in content_list:
        edit_file(name, content)
