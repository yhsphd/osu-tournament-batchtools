import re
from configparser import ConfigParser


def links2ids(config: ConfigParser):
    WORKING_FOLDER = config["paths"]["working_folder"].rstrip("/")

    content = ""

    with open(WORKING_FOLDER + "/links.csv", "r") as f:
        content = f.read().rstrip()

    content = re.sub("[^0-9\n\r]", "", content)

    with open(WORKING_FOLDER + "/ids.csv", "w") as f:
        f.write(content)
