class Player:
    username: str
    player_id: int
    avatar: str

    def __init__(self, player_id, username, avatar):
        self.player_id = player_id
        self.username = username
        self.avatar = avatar

    def __str__(self) -> str:
        return f"{self.username} ({self.player_id})"