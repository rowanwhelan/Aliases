import random
import csv
from tile import tile

class grid:
    def __init__(self, size, file, seed=None):
        '''    
        this method gets 25 words from the list of words in file randomly without replacement
        input:
            file, a string representing the path to a csv with the word corpus
            num_samples, the number of words to grab DEFAULT=25
            seed, an int representing the random seed DEFAULT=NONE
        '''
        if seed is not None:
            random.seed(seed)
        
        self.seed = seed
        
        with open(file, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            words = [row[0] for row in reader]  

        unique_words = list(set(words))  
        if len(unique_words) < size:
            raise ValueError("Not enough unique words to sample.")
        
        reservoir = random.sample(unique_words, size)  
        reservoir = self.post_process(reservoir)
        self.size = size
        self.list = self.set_board_parameters(reservoir)
    
    def __iter__(self):
        return iter(self.list)
       
    def get_grid(self):
        return self.list
    
    def update_grid(self, guess):
        for tile in list:
            if tile.word == guess:
                tile.guess()
        return 

    def post_process(self, word_list):
        for i in range(len(word_list)):
            if "_" in word_list[i]:
                word_list[i] = word_list[i].replace("_", " ")
        return word_list
    
    def set_board_parameters(self, board):
        if self.seed is not None:
            random.seed(self.seed)
        random.shuffle(board)
        word_assignments = []
        for word in board[:9]:
            word_assignments.append(tile(word, 0, False))
        for word in board[9:17]:
            word_assignments.append(tile(word, 1, False))    
        word_assignments.append(tile(board[17], -1, False))
        for word in board[18:]:
            word_assignments.append(tile(word, 2, False))
        random.shuffle(word_assignments)
        return word_assignments