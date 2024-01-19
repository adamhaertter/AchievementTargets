class Game:
    game_id: int
    title: str
    boxart: str

    def __init__(self, game_id, title, boxart):
        self.game_id = game_id
        self.title = title
        self.boxart = boxart

    def __str__(self) -> str:
        return f"{self.title} ({self.game_id})"
    
    # Artwork retrieval by game id
    def get_capsule_art(self):
        return f"https://cdn.cloudflare.steamstatic.com/steam/apps/{self.game_id}/library_600x900.jpg"
    
    def get_header_art(self):
        return f"https://cdn.cloudflare.steamstatic.com/steam/apps/{self.game_id}/header.jpg"
    
    def get_hero_art(self):
        return f"https://cdn.cloudflare.steamstatic.com/steam/apps/{self.game_id}/library_hero.jpg"
    
    def get_logo_art(self):
        return f"https://cdn.cloudflare.steamstatic.com/steam/apps/{self.game_id}/logo.png"
    
    def get_preview_art(self):
        return f"https://cdn.akamai.steamstatic.com/steam/apps/{self.game_id}/capsule_184x69.jpg"