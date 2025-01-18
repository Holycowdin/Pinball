

class Player():
    def __init__(self):
        self.score = 0
        self.multiplier = 1

    def increaseScore(self, points:int):
        self.score += points * self.multiplier