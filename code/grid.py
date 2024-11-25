import random
import csv
from tile import tile
import json
from colorama import Style, Fore, init
init(autoreset=True)

class grid:
    '''
    The grid class serves as the backbone of the entire app. This data structure houses the individual Tile data structures which represent the different words in the game 
    vairables:
        size, (int) the number of Tile objects the grid is initialized with
        file, (string) the file containing the word corpus which the grid will sample from
        turn, (int) a value representing who is currently on the play, either 0 for player 1 or 1 for player 2 
        seed, (int) the random seed that all randomization is based on 
    '''
    def __init__(self, size, file, list=None, turn=None, seed=None):
        '''
        A constructor for grid
        Args:
            size, (int) the number of Tile objects the grid is initialized with
            file, (string) the file containing the word corpus which the grid will sample from
            list, (list) the list of Tile objects (optional if creating a new grid)
            turn, (int) the current turn (optional if creating a new grid)
            seed, (int) the random seed that all randomization is based on (optional)
        '''
        self.seed = seed
        if seed is not None:
            random.seed(seed)
            
        self.turn = random.randint(0, 1) if turn is None else turn
        
        if list is None or turn is None:
            with open(file, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                words = [row[0] for row in reader]  
            reservoir = random.sample(words, size)  
            reservoir = self.post_process(reservoir)
            self.list = self.set_board_parameters(reservoir)
        else:
            self.list = list
            self.turn = turn

        self.size = size
        self.file = file
        
    def __iter__(self):
        '''
        A function to define the Iterability of the Grid object
        '''
        return iter(self.list)
    
    def __getitem__(self, index):
        '''
        A function to define the Subscriptability of the Grid object
        '''
        return self.tiles[index]
    
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
        Output:
            turn, (int) a value representing who is currently on the play, either 0 for player 1 or 1 for player 2 
        '''
        turn = self.turn
        for i in range(0, self.size):
            if self.list[i].get_word() == guess:
                self.list[i].used = True
                if self.list[i].team == self.turn:
                    self.turn = turn
                    return turn 
                else:
                    self.turn = 1 - turn
                    return self.list[i].team
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
                word_list[i] = (word_list[i].replace("_", " ")).lower()
            else:
                word_list[i] = word_list[i].lower()
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
            word_assignments.append(tile(word, self.turn, False))
        for word in board[9:17]:
            word_assignments.append(tile(word, 1-self.turn, False))    
        word_assignments.append(tile(board[17], -1, False))
        for word in board[18:]:
            word_assignments.append(tile(word, 2, False))
        random.shuffle(word_assignments)
        return word_assignments
    
    def to_json(self):
        """
        Converts the Grid object to a JSON-serializable dictionary.
        """
        return json.dumps({
            'size': self.size,
            'file': self.file,  # Keep track of the file if needed for reconstruction
            'turn': self.turn,
            'seed': self.seed,
            'tiles': [tile.to_json() for tile in self.list]
        })
        
    def from_json(cls, json_data):
        """
        Reconstructs a Grid object from a JSON string.
        """
        data = json.loads(json_data)
        grid = cls(size=data['size'], file=data['file'], turn=data['turn'], seed=data['seed'])
        grid.list = [tile.from_json(tile, tiles) for tiles in data['tiles']]
        return grid
    
    def toString(self):
        color_map = {
        0: Fore.RED,   # Red
        1: Fore.BLUE,  # Blue
        2: Fore.YELLOW, # Tan
        -1: Fore.BLACK, # Black
        "reset": Style.RESET_ALL}

        result = ""
        for i, tile in enumerate(self.list):
            if tile.used:
                # Format the word with the team's color
                result += f"{color_map[tile.team]}{tile.word}{color_map['reset']}"
            else:
                # Just the word with no formatting
                result += tile.word

            # Add spacing and line breaks to format the 5x5 grid
            if (i + 1) % 5 == 0:
                result += "\n"  # Newline after every 5 tiles
            else:
                result += "\t"  # Tab between tiles
        return result
    
    def swap_turn(self):
        self.turn = 1 - self.turn
        return