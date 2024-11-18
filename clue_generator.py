from enum import Enum
import gensim.downloader as api
#import spacy
from nltk.corpus import wordnet

class words(Enum):
    IN = 0
    OUT = 1

class clue_generator:
    def __init__(self, board, team, limit=5):
        self.board = board
        self.team = team
        list = []
        for word in board:
            if word[1] == self.team:
                list.append(word[0])
        self.word_list = list
        self.limit = limit
        
        
    def related(self, clue, word):
        '''
        this method is a single version of the score_clue method, where this methods goal is to score how likely a clue is to give the guesser a word. 
        input:
            clue, a string representing the clue the robot is supposed to reason about
            word, a given word in play on the board
        output:
            probability, a double value representing the likelihood of the given clue making the given word guessable
        '''       
        #After a bit of research I have found three methods to detect the similarity of words, I won't reason about their effectiveness right now but I will later in the projec twhen teh rest of the architecture is built up enough that this reasoning is based on more that intuition
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
        '''
        total_relational_score = 0
        for i in self.board:
            current_related = self.related(clue, i[0])
            if i[1] == self.team:
                total_relational_score += current_related
            elif i[1] == -1:
                total_relational_score -= current_related
            else:
                continue
        score = total_relational_score
        return score
    
    def get_synonyms(self, word):
        '''
        this method will take a word and return a list of synonyms for a word
        input: 
            word, a word we want synomyms for

        output:
            list, a list of strings which are synonyms for the given word
        '''
        synonyms = set()
        for syn in wordnet.synsets(word[0]):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name())  # Add synonym to set (set to avoid duplicates)
        return list(synonyms)[:self.limit]
    
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
        for word in self.word_list:
            print(f"Generating clues for '{word}'...")
            synonyms = self.get_synonyms(word)
            
            for synonym in synonyms:
                score = self.score_clue(synonym)
                print(f"  Clue: {synonym} - Score: {score}")
                
                # Check if the current synonym has a higher score
                if score > highest_score:
                    highest_score = score
                    best_clue = synonym
        
        return best_clue
    

    