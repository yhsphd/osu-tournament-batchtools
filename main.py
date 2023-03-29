from configparser import ConfigParser
import os
from settings import create_config
from osuapi import get_players_info
from links2ids import links2ids
from pfpdownload import download_pfps
from lazerteams import generate_lazer_teams
from lazerbracket import generate_lazer_bracket
from workingfolder import change_working_folder


def taskdone():
    print()
    print("Task done!")
    print()
    input("Press ENTER to continue...")


def main():
    while True:
        config = ConfigParser()
        if not os.path.isfile("./settings.ini"):
            create_config()
        config.read("settings.ini")

        WORKING_FOLDER = "working folders/" + config["paths"]["working_folder"].rstrip("/")
        if not os.path.exists(WORKING_FOLDER):
            os.makedirs(WORKING_FOLDER)

        print()
        print("-" * 41)
        print(" - yhsphd's osu tournament batch tools -")
        print("-" * 41)
        print()
        print(f"Current working folder: [{WORKING_FOLDER}]")
        print()
        print("[ Generate playersinfo.json and other csv files ]")
        print("1. Retrieve information of players listed in 'ids.csv'")
        print("2. Retrieve information of players listed in 'links.csv'")
        print("3. Retrieve information of players listed in 'nicks.csv'")
        print()
        print("4. Download profile pictures of players (requires ids.csv and nicks.csv)")
        print()
        print("[ osu!lazer tournament client ]")
        print("5. Generate individual team listing (requires playersinfo.json)")
        print("6. Generate rounds and brackets")
        print()
        print("a. Change working folder")
        print("q. Quit program")
        if not (config["api"]["client_id"] and config["api"]["client_secret"]):
            print()
            print(
                "** osu!api(v2) key not set! please retrieve yours and put it to 'settings.ini'!")
            print()
        choice = input("\nYour Choice: ")

        if choice == "1":
            get_players_info(config, 0)
        elif choice == "2":
            links2ids(config)
            get_players_info(config, 0)
        elif choice == "3":
            get_players_info(config, 1)
        elif choice == "4":
            download_pfps(config)
        elif choice == "5":
            generate_lazer_teams(config)
        elif choice == "6":
            generate_lazer_bracket(config)
        elif choice == "a":
            change_working_folder(config)
            config.read("settings.ini")
            WORKING_FOLDER = "working folders/" + config["paths"]["working_folder"].rstrip("/")
        elif choice == "q":
            exit()

        taskdone()


if __name__ == "__main__":
    main()
