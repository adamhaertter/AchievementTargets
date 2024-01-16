import os

key = os.getenv("STEAM_API_KEY")
user_id = os.getenv("TEST_USER_ID")
test_app_id = 632360 # "Risk of Rain 2"

def demoQuery():
    return f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/?key={key}&steamid={user_id}&appid=632360"

def buildQueryFree():
    url_start = "https://api.steampowered.com/"
    url_interface = ""
    url_endpoint = ""
    url_version = ""
    url_args = ""

    return url_start + "f{url_interface}/{url_endpoint}/{url_version}/{url_args}"

def getPlayerAchievements(appid):
    return f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/?key={key}&steamid={user_id}&appid={appid}"

def getOwnedGames():
    return f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={key}&steamid={user_id}&include_played_free_games=true"