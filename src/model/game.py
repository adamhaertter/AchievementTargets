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