from configparser import ConfigParser
import os
import requests


def download_pfps(config: ConfigParser):
    WORKING_FOLDER = "working folders/" + config["paths"]["working_folder"].rstrip("/")

    if not os.path.exists(f"{WORKING_FOLDER}/pfps"):
        os.makedirs(f"{WORKING_FOLDER}/pfps")
    if not (os.path.isfile(f"{WORKING_FOLDER}/ids.csv") and os.path.isfile(f"{WORKING_FOLDER}/nicks.csv")):
        print(
            f"File {WORKING_FOLDER}/ids.csv or {WORKING_FOLDER}/nicks.csv doesn't exist!")
        return

    playeridlist = []
    playernicklist = []

    with open(f"./{WORKING_FOLDER}/ids.csv", "r") as f:
        playeridlist = f.read().rstrip().split("\n")
    with open(f"./{WORKING_FOLDER}/nicks.csv", "r") as f:
        playernicklist = f.read().rstrip().split("\n")

    for i in range(len(playeridlist)):
        response = requests.get(f"https://a.ppy.sh/{playeridlist[i]}")
        filename = f"{playernicklist[i]}.png"

        with open(f"{WORKING_FOLDER}/pfps/{filename}", "wb") as f:
            f.write(response.content)

        print(end="\x1b[2K")
        print(f"{i + 1}/{len(playeridlist)} downloaded! ({filename})", end="\r")
    print()
