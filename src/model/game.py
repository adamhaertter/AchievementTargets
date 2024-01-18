class Game:
    game_id: int
    title: str

    def __init__(self, game_id, title):
        self.game_id = game_id
        self.title = title

    def __str__(self) -> str:
        return f"{self.title} ({self.game_id})"