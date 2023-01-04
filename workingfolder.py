import os
from configparser import ConfigParser


def change_working_folder(config:ConfigParser, folder: str):
    if not os.path.exists(folder):
        os.makedirs(folder)
    config["paths"]["working_folder"] = folder
    with open("settings.ini", "w") as f:
        config.write(f)
    print("Working folder changed!")
