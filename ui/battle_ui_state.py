class BattleUIState:
    def __init__(self):
        self.show_bag = False
        self.bag_index = 0

        self.show_skills = False
        self.skill_index = 0

        self.logs = ["Battle started."]

    def add_log(self, text: str) -> None:
        self.logs.append(str(text))
        if len(self.logs) > 6:
            self.logs.pop(0)