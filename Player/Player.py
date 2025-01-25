

class Player():
    def __init__(self):
        self.resetScore()

    def increaseScore(self, points:int):
        self.score += points * self.multiplier

    def resetScore(self):
        self.score = 0
        self.multiplier = 1