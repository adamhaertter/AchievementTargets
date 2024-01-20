# Achievement Targets

A local, Python-based application using the [Steamworks Web API](https://partner.steamgames.com/doc/webapi) to collect and display a user's stats on their in-game achievements.

**Note**: You MUST have your Steam profile and library set to public for this to work. That is a limitation of the Steamworks Web API, not a personal choice.

## Getting Started

### Dependencies

This program is dependent on Python which you will need installed to run it. The base installation should cover all dependencies, but also ensure that you have Tkinter and Pillow installed on Python for the UI.

### Getting your API Key

You will need your own API Key and User ID at the very least to use this program. 
1. Log in to Steam at [this link](https://steamcommunity.com/dev/apikey) to retrieve your **private** API Key. Do not give it away ever, as they are private and one to an account.
2. Rename the ``.env.example`` file to ``.env``. This is where the program will attempt to pull your API Key from.
3. Copy your API Key from the link above into the ``STEAM_API_KEY`` field in the ``.env`` file. It should look like ``STEAM_API_KEY = YourKeyHere``

### Getting your Steam ID
You will need your Steam account ID (or the account ID of a public steam account) to sync your library to the app. The app doesn't save any of your data currently, so it makes an API call to retrieve your account details, library, and achievement list depending on the loaded game.
1. You can go to the [Account Details](https://store.steampowered.com/account/) on your Steam profile page and see your public Steam ID in the top left under [Your Name]'s Account