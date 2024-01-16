import requests
import apiQueryBuilder
import os

url = "http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=440&count=1"
response = requests.get(apiQueryBuilder.getPlayerAchievements(apiQueryBuilder.test_app_id))

if response.status_code == 200:
    json_data = response.json()
    print(json_data)
else:
    print(f"Error {response.status_code}: {response.text}")