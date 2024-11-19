import random
import csv
from tile import tile

class grid:
    '''
    The grid class serves as the backbone of the entire app. This data structure houses the individual Tile data structures which represent the different words in the game 
    vairables:
        size, (int) the number of Tile objects the grid is initialized with
        file, (string) the file containing the word corpus which the grid will sample from
        seed, (int) the random seed that all randomization is based on 
    '''
    def __init__(self, size, file, seed=None):
        '''
        A constructor for grid
        Args:
            size, (int) the number of Tile objects the grid is initialized with
            file, (string) the file containing the word corpus which the grid will sample from
            seed, (int) the random seed that all randomization is based on 
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
        '''
        A function to define the Iterability of the Grid object
        '''
        return iter(self.list)
       
    def get_grid(self):
        '''
        A function to return the list of tiles
        Outputs:
            self.list, (list of Tiles)
        '''
        return self.list
    
    def update_grid(self, guess):
        '''
        A function to update the grid with game actions
        Args:
            guess, (string) a string representing the word the player has chosen to guess
        '''
        for tile in list:
            if tile.word == guess:
                tile.guess()
        return 

    def post_process(self, word_list):
        '''
        This function post processes the words in the corpus that have been added to the grid. For the current functionality, I decided to remove the _ character and replace it with spaces for readability
        Args:
            word_list, (list of strings) this list of strings is unfiltered
        Outputs:
            word_list, (list of string) the finished list of strings
        Planned Updates: change the input to prevent malevolent actors from attacking the site
        '''
        for i in range(len(word_list)):
            if "_" in word_list[i]:
                word_list[i] = word_list[i].replace("_", " ")
        return word_list
    
    def set_board_parameters(self, board):
        '''
        A function which takes a list of words, shuffles them into the finished board, and packages them as Tile objects
            Args: 
                board, (list of strings) a list of strings which is set to become the game Tiles
            Outputs:
                word_assignments, (list of Tiles) a list of tiles which is sorted such that the final board looks random to the user
        '''
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