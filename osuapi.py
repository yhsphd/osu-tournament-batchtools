from configparser import ConfigParser
import json
import requests


def get_token(config: ConfigParser):
    TOKEN_URL = config["api"]["token_url"].rstrip("/")
    CLIENT_ID = config["api"]["client_id"]
    CLIENT_SECRET = config["api"]["client_secret"]

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": "public"
    }
    response = requests.post(TOKEN_URL, data=data)
    token = response.json().get("access_token")
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }


def get_players_info(config: ConfigParser, mode: int):
    """Get players' info from osu!api and saves it as playersinfo.json.

    Args:
        mode (int): 0 to get players' ids and 1 to get players' nicknames
    """

    WORKING_FOLDER = "working folders/" + \
                     config["paths"]["working_folder"].rstrip("/")
    MODE = config["osu"]["mode"]
    API_URL = config["api"]["api_url"].rstrip("/")

    nicklist = []
    idlist = []
    playersinfo = {
        "users": []
    }

    headers = get_token(config)

    if mode == 0:  # id list
        with open(f"./{WORKING_FOLDER}/ids.csv", "r") as f:
            idlist = f.read().rstrip().split("\n")

        for i in range(len(idlist)):
            response = requests.get(
                f"{API_URL}/users/{idlist[i]}/{MODE}", headers=headers).json()
            playersinfo["users"].append(response)
            try:
                nicklist.append(response["username"])
            except KeyError:
                nicklist.append("")
                print(
                    f"No key named 'username' for player {idlist[i]}. osu! api response:\n{json.dumps(response, indent=2)}")
            print(end="\x1b[2K")
            print(
                f"{i + 1}/{len(idlist)} downloaded! ({nicklist[i]})", end="\r")
        print()

        # generate nicks.csv
        with open(f"{WORKING_FOLDER}/nicks.csv", "w") as f:
            f.write("\n".join(nicklist))

    elif mode == 1:  # nick list
        with open(f"./{WORKING_FOLDER}/nicks.csv", "r") as f:
            nicklist = f.read().rstrip().split("\n")

        for i in range(len(nicklist)):
            response = requests.get(
                f"{API_URL}/users/{nicklist[i]}/{MODE}?key=asdf", headers=headers).json()
            try:
                idlist.append(response["id"])
            except KeyError:
                idlist.append(0)
                print(
                    f"No key named 'id' for player {nicklist[i]}. osu! api response:\n{json.dumps(response, indent=2)}")
            playersinfo["users"].append(response)
            print(end="\x1b[2K")
            print(
                f"{i + 1}/{len(nicklist)} downloaded! ({nicklist[i]})", end="\r")
        print()

        # generate ids.csv
        with open(f"{WORKING_FOLDER}/ids.csv", "w") as f:
            f.write("\n".join(map(str, idlist)))

    # generate links.csv
    with open(f"{WORKING_FOLDER}/links.csv", "w") as f:
        text2write = ""
        for id in idlist:
            text2write += f"https://osu.ppy.sh/users/{id}\n"
        f.write(text2write.rstrip())

    # got all information
    with open(f"{WORKING_FOLDER}/playersinfo.json", "w") as f:
        f.write(json.dumps(playersinfo))
