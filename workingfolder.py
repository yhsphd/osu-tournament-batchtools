import os
from configparser import ConfigParser


def change_working_folder(config: ConfigParser):
    folder = input("Please type the name of the working folder: ")
    if not os.path.exists("working folders/" + folder):
        os.makedirs("working folders/" + folder)
    config["paths"]["working_folder"] = folder
    with open("settings.ini", "w") as f:
        config.write(f)
    print("Working folder changed!")
