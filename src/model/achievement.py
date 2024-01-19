class Achievement:
    achievement_id: str
    name: str
    desc: str
    achieved = False
    icon: str

    def __init__(self, achievement_id, name, desc, icon):
        self.achievement_id = achievement_id
        self.name = name
        self.desc = desc
        self.icon = icon

    def __str__(self) -> str:
        return f"{self.name}: {self.desc} ({self.achievement_id})"