class Player:
    username: str
    player_id: int

    def __init__(self, player_id, username):
        self.player_id = player_id
        self.username = username

    def __str__(self) -> str:
        return f"{self.username} ({self.player_id})"