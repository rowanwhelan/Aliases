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
    
    def to_dict(self):
        return {
            'word': self.word,
            'team': self.team,
            'used': self.used
        }

    @staticmethod
    def from_dict(data):
        return tile(data['word'], data['team'], data['used'])