from configparser import ConfigParser
import os
import requests
import magic


def download_pfps(config: ConfigParser):
    WORKING_FOLDER = "working folders/" + config["paths"]["working_folder"].rstrip("/")

    if not os.path.exists(f"{WORKING_FOLDER}/pfps"):
        os.makedirs(f"{WORKING_FOLDER}/pfps")
    if not (os.path.isfile(f"{WORKING_FOLDER}/ids.csv") and os.path.isfile(f"{WORKING_FOLDER}/nicks.csv")):
        print(f"File {WORKING_FOLDER}/ids.csv or {WORKING_FOLDER}/nicks.csv doesn't exist!")
        return

    playeridlist = []
    playernicklist = []

    print()
    print()
    print("Change file extensions to png?")
    print("(It doesn't converts the file, just for tricking the lazer client into displaying jpg)")
    print()
    print("1. Yes")
    print("2. No, preserve file extensions")

    png = False

    while (True):
        sel = input()
        if sel == "1":
            png = True
            break
        elif sel == "2":
            png = False
            break
        else:
            print("Please select again.")

    print()

    with open(f"./{WORKING_FOLDER}/ids.csv", "r") as f:
        playeridlist = f.read().rstrip().split("\n")
    with open(f"./{WORKING_FOLDER}/nicks.csv", "r") as f:
        playernicklist = f.read().rstrip().split("\n")

    for i in range(len(playeridlist)):
        response = requests.get(f"https://a.ppy.sh/{playeridlist[i]}")

        ext = "png"

        if not png:
            type = magic.from_buffer(response.content)

            if type.startswith("PNG image data"):
                ext = "png"
            elif type.startswith("JPEG image data"):
                ext = "jpg"
            elif type.startswith("GIF image data"):
                ext = "gif"
            elif "Web/P image" in type:
                ext = "webp"
            else:
                ext = ""

        filename = f"{playernicklist[i]}." + ext

        with open(f"{WORKING_FOLDER}/pfps/{filename}", "wb") as f:
            f.write(response.content)

        print(f"{i + 1}/{len(playeridlist)} downloaded! ({filename})")
    print()
