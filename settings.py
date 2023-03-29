from configparser import ConfigParser


def create_config():
    config = ConfigParser()

    config["paths"] = {
        "working_folder": "default"
    }
    config["api"] = {
        "api_url": "https://osu.ppy.sh/api/v2",
        "token_url": "https://osu.ppy.sh/oauth/token",
        "client_id": 0,
        "client_secret": ""
    }
    config["osu"] = {
        "mode": "osu"
    }

    with open("./settings.ini", "w") as f:
        config.write(f)
