from enum import Enum
import json
import gensim.downloader as api
from grid import grid
from nltk.corpus import wordnet

class clue_generator:
    def __init__(self, board, turn, limit=15):
        self.board = board
        self.turn = turn
        self.limit = limit
        
        self.word_list = [
            tile.word for tile in board.list 
            if tile.team == self.turn and not tile.used
        ]
        
    def related(self, clue, word):
        '''
        this method is a single version of the score_clue method, where this methods goal is to score how likely a clue is to give the guesser a word. 
        input:
            clue, a string representing the clue the robot is supposed to reason about
            word, a given word in play on the board
        output:
            probability, a double value representing the likelihood of the given clue making the given word guessable
        '''       
        #After a bit of research I have found three methods to detect the similarity of words, I won't reason about their effectiveness right now but I will later in the project when teh rest of the architecture is built up enough that this reasoning is based on more that intuition
        """#GENSIM
        model = api.load("glove-wiki-gigaword-50") 

        def gensim_word_similarity(word1, word2):
            try:
                return model.similarity(word1, word2)
            except KeyError:
                return 0
        """
        """#SPACY
        nlp = spacy.load("en_core_web_sm")

        def spacy_word_similarity(word1, word2):
            token1 = nlp(word1)
            token2 = nlp(word2)
            return token1.similarity(token2)"""

        #NLTK
        def nltk_word_similarity(word1, word2):
            if word1 == None or word2 == None:
                return 0
            synsets1 = wordnet.synsets(word1)
            synsets2 = wordnet.synsets(word2)

            if synsets1 and synsets2:
                similarity = max([synset1.wup_similarity(synset2) for synset1 in synsets1 for synset2 in synsets2])
                return similarity
            else:
                return 0
        #FOR RIGHT NOW: I'm going to use NLTK because that happens to correspond to the data I'm using but I'll do some testing in a later version to see what performs best and gives the best user experience
        probability = nltk_word_similarity(clue, word)
        return probability
    
    def score_clue(self, clue):
        '''
        the idea of this method is that every clue that could possibly given should be given a score. This helps transform the abstract idea of word similarity to a value the computers can reason about.
        input: 
            clue, a string representing the clue the robot is supposed to reason about
        
        output: 
            score, (implementation unclear right now, this will be updated once the method is finalized)
            related, the number of words the model thinks the clue gives hint for
        '''
        total_relational_score = 0
        total_related_clues = 0
        for i in self.board:
            current_related = self.related(clue, i.word)
            if current_related >= 1.0:
                total_related_clues += 1
            if i.team == self.turn:
                total_relational_score += current_related
            elif i.team == abs(self.turn-1):
                total_relational_score -= (current_related/4)
            elif i.team == -1:
                total_relational_score -= current_related
        score = total_relational_score * (total_related_clues + 0.01)
        return score, total_related_clues
    
    def get_synonyms(self, word):
        '''
        This method takes a word and returns a list of synonyms using WordNet.
        
        input: 
            word: A string representing the word to find synonyms for
        
        output: 
            filtered_list: A list of synonym strings (excluding one-letter words)
        '''
        try:
            synonyms = set()  # Using a set to avoid duplicates
            # Get synsets for the word
            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    # Only add synonyms that are not one-letter words
                    if len(lemma.name()) > 1 and lemma.name().lower() != word.lower() and not any(c in lemma.name() for c in [' ', '_', '-']):
                        synonyms.add(lemma.name())
                    
            
            # Convert the set back to a list and return it
            return list(synonyms)[:self.limit]

        except Exception as e:
            print(f"Error while fetching synonyms: {e}")
            return []
    
    def give_clue(self):
        '''
        this method will look at the given board state and try to find a clue among the synonims of words on the board that scores the highest based on the criteria defined in the score clue method
        input:
            none
        output:
            clue, a string that the algorithm thinks is the best given the current board state
        '''
        best_clue = ''
        highest_score = -1
        highest_related_clues = 0
        for word in self.word_list:
            #print(f"Generating clues for '{word}'...")
            synonyms = self.get_synonyms(word)
            
            for synonym in synonyms:
                score, related_clues = self.score_clue(synonym)
                #print(f"  Clue: {synonym} - Score: {score}, Related: {related_clues}")
                
                # Check if the current synonym has a higher score
                if score > highest_score:
                    highest_score = score
                    best_clue = synonym
                    highest_related_clues = related_clues
        
        return best_clue, highest_related_clues
    
    def update_team(self):
        '''
        This method changes the team and updates the word list so a single clue giver can be used for both teams.
        '''
        self.turn = 1 - self.turn
        self.word_list = [
            tile.word for tile in self.board.list 
            if tile.team == self.turn and not tile.used
        ]
        
    def update_bot(self, board):
        self.board = board
        self.turn = board.turn
        
        self.word_list = [
            tile.word for tile in board.list 
            if tile.team == self.turn and not tile.used
        ]
    
    def toString(self):
        return self.board.toString()
    
    def to_json(self):
        """
        Converts the clue_generator object to a JSON serializable dictionary.
        Returns:
            dict: JSON-serializable dictionary representation of the clue_generator object.
        """

        board_json = self.board.to_json()  

        data = {
            'board': board_json,
            'turn': self.turn,
            'limit': self.limit,
        }
        return json.dumps(data)

    def from_json(cls, data):
        """
        Converts a JSON serializable dictionary back to a clue_generator object.
        Args:
            data (dict): The dictionary to convert back into a clue_generator object.
        Returns:
            clue_generator: The reconstructed clue_generator object.
        """
        parsed_data = json.loads(data)

        board = grid.from_json(grid,parsed_data['board'])  
        turn = parsed_data['turn']
        limit = parsed_data['limit']
        
        return clue_generator(board, turn, limit)