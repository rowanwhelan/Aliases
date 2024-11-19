class tile:
    def __init__(self, word, team, used=False):
        self.word = word
        self.team = team
        self.used = used
        
    def guess(self, team):
        if not self.used:
            self.used == True
        return self.team == team

    def get_word(self):
        return self.word