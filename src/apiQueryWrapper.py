import os
import requests
from model.player import Player
from model.achievement import Achievement
from model.game import Game

key = os.getenv("STEAM_API_KEY")
test_user_id = os.getenv("TEST_USER_ID")
test_app_id = 632360 # "Risk of Rain 2"

def demoQuery():
    return f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/?key={key}&steamid={test_user_id}&appid={test_app_id}"

# Takes in a complete API Request URL and returns the formatted JSON response.
def execute(url):
    response = requests.get(url)

    if response.status_code != 200:
        return f"Error {response.status_code}: {response.text}"
            
    return response.json()

# args_string must be fully concatenated into a url string before passing to this method to work.
def build_free_query(interface, endpoint, version, args_string):
    url_start = "https://api.steampowered.com/"
    url_interface = interface
    url_endpoint = endpoint
    url_version = version
    url_args = args_string

    return url_start + "f{url_interface}/{url_endpoint}/{url_version}/{url_args}"

# Get Player Data (Name, ID, Profile Picture)
def get_player_data(user_id):
    parsed = execute(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={key}&steamids={user_id}")
    
    # Query can return multiple players if multiple ids are specified
    player_array = [Player(player_id=players['steamid'], username=players['personaname'], avatar=players['avatarfull']) for players in parsed['response']['players']] 
    
    # Return first player only (for now)
    try:
        return player_array[0]
    except Exception as e:
        return None

# Get Achievements by Player & Game
# Returns a tuple with index 0 as the internal achievement name/id and index 1 as a bool whether the player has obtained this achievement
def get_player_achievements(user_id, app_id):
    parsed = execute(f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/?key={key}&steamid={user_id}&appid={app_id}")

    achievement_ids = [(query['apiname'], query['achieved']) for query in parsed['playerstats']['achievements']]

    return achievement_ids

# Get All Achievements for a Single Game
# Returns an array of Achievement class objects (by default, all are set to unachieved and will need to be set later TODO)
def get_game_achievements(app_id):
    parsed = execute(f"https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key={key}&appid={app_id}")

    achievements = []
    for query in parsed.get('game', {}).get('availableGameStats', {}).get('achievements', []):
        achievement_id = query['name']
        name = query['displayName']
        desc = query.get('description', 'HIDDEN ACHIEVEMENT')  
        icon = query['icon']

        achievement = Achievement(achievement_id=achievement_id, name=name, desc=desc, icon=icon)
        achievements.append(achievement)

    return achievements

# Get All Games Owned by a Player (include free)
# Returns an array of Game class objects including appid and name
def get_owned_games(user_id):
    parsed = execute(f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={key}&steamid={user_id}&include_played_free_games=true&include_appinfo=true")

    library = [Game(game_id=games['appid'], title=games['name'], boxart=games['img_icon_url']) for games in parsed['response']['games']]

    return library

# TEMPORARY TESTING METHODS 

#get_player_achievements(test_user_id, test_app_id)
# temp = get_game_achievements(945360)
# # resp = get_owned_games(test_user_id)
# for obj in resp:
#     print(f"{obj.title} ({obj.game_id})")