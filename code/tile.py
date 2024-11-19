class tile:
    def __init__(self, word, team, used=False):
        self.word = word
        self.team = team
        self.used = used
        
    def guess(self):
        if not self.used:
            self.used == True
        return 