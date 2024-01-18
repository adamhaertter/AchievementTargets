class Achievement:
    achievement_id: int
    name: str
    desc: str

    def __init__(self, achievement_id, name, desc):
        self.achievement_id = achievement_id
        self.name = name
        self.desc = desc

    def __str__(self) -> str:
        return f"{self.name}: {self.desc} ({self.achievement_id})"