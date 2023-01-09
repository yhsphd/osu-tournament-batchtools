from configparser import ConfigParser
import math
import json


def lazer_match(id: int, losers: bool, position: list):
    return {
        "ID": id,
        "Team1Score": None,
        "Team2Score": None,
        "Completed": False,
        "Losers": losers,
        "PicksBans": [],
        "Current": False,
        "Date": "2023-01-01T00:00:00Z",
        "ConditionalMatches": [],
        "Position": {
            "X": position[0],
            "Y": position[1]
        },
        "Acronyms": [],
        "PointsToWin": 0
    }


def generate_lazer_bracket(config: ConfigParser):
    WORKING_FOLDER = config["paths"]["working_folder"].rstrip("/")

    rounds = {
        "Rounds": []
    }
    matches = {
        "Matches": []
    }
    roundnames = [{
        8: "Quarterfinals",
        4: "Semifinals",
        2: "Final"          # single elimination
    }, {
        8: "Quarterfinals",
        4: "Semifinals",
        2: "Finals",
        1: "Grand Finals"   # double elimination
    }]

    players = int(input("Number of players: "))

    if not ((players & (players-1) == 0) and players != 0):
        print("The number of players is not power of 2!")
        exit()

    # de: double elimination
    de = input("Is the tournament double elimination? (y/n): ")
    if de == "y":
        de = True
        roundnames = roundnames[1]

        print("(for tournaments where there are players starting from the losers round)")
        # fwl: first week losers
        fwl = input("Add losers bracket matches for the first week? (y/n): ")
        if fwl == "y":
            fwl = True
            players = players // 2
        else:
            fwl = False
    else:
        de = False
        roundnames = roundnames[0]

    n = players
    week = 1
    id = 1
    position = [100, 100]
    winnerYorigin = 100
    loserYorigin = 0
    while n >= 1:
        # ro1 doesnt exist in single elimination
        # and considered grand finals in double elimination
        if n == 1 and not de:
            break

        # add round
        rounds["Rounds"].append({
            "Name": roundnames[n] if n in roundnames.keys() else f"Round of {n}",
            "Description": f"Week {week}",
            "BestOf": 0,
            "Beatmaps": [],
            "StartDate": "2023-01-01T00:00:00Z",
            "Matches": []
        })

        # generate grand final matches
        if n == 1:
            # last match
            position[0] -= 100
            position[1] = winnerYorigin + 100 * int(math.pow(2, week-3)) - 50
            matches["Matches"].append(lazer_match(id, False, position))
            rounds["Rounds"][-1]["Matches"].append(id)  # grand final
            id += 1
            position[0] += 200
            matches["Matches"].append(lazer_match(id, False, position))
            rounds["Rounds"][-1]["Matches"].append(id)  # bracket reset
            id += 1
            position[0] -= 200
            position[1] = loserYorigin + 100 * \
                int(math.pow(2, week-(4-fwl))) - 50
            matches["Matches"].append(lazer_match(id, True, position))
            rounds["Rounds"][-1]["Matches"].append(id)  # losers final
            id += 1
            break

        # generate winner bracket matches
        position[1] = winnerYorigin
        if week != 1:
            position[1] += 100 * int(math.pow(2, week-2)) - 50
        for i in range(n//2):
            matches["Matches"].append(lazer_match(id, False, position))
            rounds["Rounds"][-1]["Matches"].append(id)
            id += 1
            position[1] += 100 * int(math.pow(2, week-1))
        position[0] += 400 if de else 200

        if not loserYorigin:    # set loser bracket Y position
            loserYorigin = position[1] + 200

        # generte loser bracket matches
        if de and week >= 2-fwl:
            position[0] -= 500
            position[1] = loserYorigin

            # phase 1: week 3 or later, week 2 or later for fwl
            if week != 2-fwl:
                if week != 3-fwl:
                    position[1] += 100 * int(math.pow(2, week-(4-fwl))) - 50
                for i in range(n):
                    matches["Matches"].append(lazer_match(id, True, position))
                    rounds["Rounds"][-1]["Matches"].append(id)
                    id += 1
                    position[1] += 100 * int(math.pow(2, week-(3-fwl)))
            position[0] += 200

            # phase 2
            position[1] = loserYorigin
            if week != 2-fwl:
                position[1] += 100 * int(math.pow(2, week-(3-fwl))) - 50
            for i in range(n//2):
                matches["Matches"].append(lazer_match(id, True, position))
                rounds["Rounds"][-1]["Matches"].append(id)
                id += 1
                position[1] += 100 * int(math.pow(2, week-(2-fwl)))
            position[0] += 300

        # for next round
        n = n//2
        week += 1

    print(f"{id-1} matches created.")
    print("Please setup the following manually:")
    print("\t- mappools")
    print("\t- round start date")
    print("\t- round bo")
    print("\t- connecting matches")
    print("\t- assigning players to matches")

    with open(f"{WORKING_FOLDER}/lazerrounds.json", "w") as f:
        f.write(json.dumps(rounds)[1:-1])   # remove top bracket
    with open(f"{WORKING_FOLDER}/lazermatches.json", "w") as f:
        f.write(json.dumps(matches)[1:-1])  # remove top bracket
