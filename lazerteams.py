from configparser import ConfigParser
import json
import os


def generate_lazer_teams(config: ConfigParser):
    WORKING_FOLDER = config["paths"]["working_folder"].rstrip("/")

    teams = {
        "Teams": []
    }

    playersinfo = {}

    if not os.path.isfile(f"{WORKING_FOLDER}/playersinfo.json"):
        print(
            f"File {WORKING_FOLDER}/playersinfo.json doesn't exist!")
        return
    with open(f"{WORKING_FOLDER}/playersinfo.json", "r") as f:
        playersinfo = json.load(f)

    for i in range(len(playersinfo["users"])):
        teams["Teams"].append({
            "FullName": playersinfo["users"][i]["username"],
            "FlagName": playersinfo["users"][i]["username"],
            "Acronym": playersinfo["users"][i]["username"],
            "SeedingResults": [],
            "Seed": "",
            "LastYearPlacing": 1,
            "Players": []
        })
        print(end="\x1b[2K")
        print(
            f"{i+1}/{len(playersinfo['users'])} added! ({playersinfo['users'][i]['username']})", end="\r")
    print()

    with open(f"{WORKING_FOLDER}/lazerteams.json", "w") as f:
        f.write(json.dumps(teams)[1:-1])    # remove top bracket
