class tile:
    def __init__(self, word, team, used=False):
        self.word = word
        self.team = team
        self.used = used
        

    def get_word(self):
        return self.word
    
    def to_json(self):
        """
        Converts the Tile object to a JSON-serializable dictionary.
        """
        return {
            'word': self.word,
            'team': self.team,
            'used': self.used
        }
    
    def from_json(cls, json_data):
        """
        Reconstructs a Tile object from a JSON-serializable dictionary.
        """
        return cls(
            word=json_data['word'],
            team=json_data['team'],
            used=json_data['used']
        )