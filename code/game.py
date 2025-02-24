import math
import random
from grid import grid
from bots.clues.clue_generator import clue_generator
from bots.guesses.bot import bot
from colorama import Fore, Style, init
import copy
init(autoreset=True)


class game:
    def __init__(self, seed=None):
        '''
        At the start of every codenames game, a first team is picked. Then a board is generated and created. Then a clue giver is generated
        '''
        self.color_map = {
            0: Fore.RED,   # Red
            1: Fore.BLUE,  # Blue
            2: Fore.YELLOW, # Tan
            -1: Fore.BLACK, # Black
            "reset": Style.RESET_ALL}
        turn = -1
        if seed is not None:
            random.seed(seed)
            turn = random.randint(0,1)
            self.grid = grid(25, 'data/common_words.csv', turn=turn, seed=seed)
        else:
            turn = random.randint(0,1)
            self.grid = grid(25, 'data/common_words.csv', turn=turn)
        print(f"Starting game with {self.color_map[self.grid.turn]}{self.grid.turn}{self.color_map['reset']} going first\n")
        self.cg = clue_generator(self.grid,turn)
        self.guessbot = bot(self.grid)
        self.current_turn = 0 
        self.state = -1
        self.red = 0
        self.blue = 0
        self.starting_turn = self.grid.turn
        self.blue_turns = []
        self.red_turns = []
  
    def toString(self):
        return self.grid.toString()
       
    def __iter__(self):
        '''
        A function to define the Iterability of the Grid object
        '''
        return self.grid.__iter__()
    
    def get_grid(self):
        """
        Returns a deep copy of the current grid to avoid unintended modifications.
        """
        return copy.deepcopy(self.grid)

    def tabulate_entropy(self, old_grid):
        '''
        This method calculates the entropy decrease in the game after each clue.
        Is probability monotonic (ignores the probability of each clue given by the guessbot)
        Args: 
            grid: the grid state after the clue has been given but before the guesses have been inputted
        Returns:
            score: A postitive value which evaluates the entropy decrease of the system
                EDGE CASE: if a -1 is returned then there was an error
        '''
        score = 0
        total_tiles_before = 0
        for tile in old_grid:
            if not tile.used:
                total_tiles_before += 1
        total_tiles_after = 0
        for tile in self:
            if not tile.used:
                total_tiles_after += 1
        # These values are equivilent because we know each probability n is equivalent (this is a constraint of the input)
        entropy_before = math.log2(1/total_tiles_before)
        entropy_after = math.log2(1/total_tiles_after)
        
        score = entropy_before - entropy_after
        return score

    def tabulate_weighted_entropy(self, old_grid):
        '''
        This method calculates the entropy decrease in the game but only limited to the correct number of tiles
        Args:  
            grid: the grid state after the clue has been given but before the guesses have been inputted
        Returns:
            score: A value which evaluates the entropy decrease of the system
                EDGE CASE: will throw an error rather than return -1 because these scores can be negative
        '''    
        score = 0
        total_tiles_before = 0
        tiles_before = []
        for tile in old_grid:
            if not tile.used and tile.team == old_grid.turn:
                total_tiles_before += 1
                # Now add the probability to a list holding all of the probabilities
                tiles_before.append(self.guessbot.get_probability(tile))
        total_tiles_after = 0
        tiles_after = []
        for tile in self:
            if not tile.used and tile.team == old_grid.turn:
                total_tiles_after += 1
                # Now add the probability to a list holding all of the probabilities
                tiles_after.append(self.guessbot.get_probability(tile))
       
        # entropy formula
        entropy_before = -sum(p * math.log2(p) for p in tiles_before if p > 0)
        entropy_after = -sum(p * math.log2(p) for p in tiles_after if p > 0)
        
        score = entropy_before - entropy_after
        return score
    
    def tabulate_correctness_entropy(self, old_grid):
        '''
        This method calculates the entropy decrease in the game while also factoring in the "correctness" of the entropy. 
        Meaning a decrease in entropy in the opponenets clues or an increase in the entropy of this teams clues counts negatively against this score.
        Args:  
            grid: the grid state after the clue has been given but before the guesses have been inputted
        Returns:
            score: A value which evaluates the entropy decrease of the system
                EDGE CASE: will throw an error rather than return -1 because these scores can be negative
        '''    
        score = 0
        total_tiles_before = 0
        tiles_before = []
        for tile in old_grid:
            if not tile.used:
                total_tiles_before += 1
                # Now add the probability to a list holding all of the probabilities for and against
                
        total_tiles_after = 0
        tiles_after = []
        for tile in self:
            if not tile.used:
                total_tiles_after += 1
                # Now add the probability to a list holding all of the probabilities for and against
        '''
        THIS IS THE FORMULA BUT THIS WILL BE IMPLEMENTED LATER
        entropy_before = -sum(p * math.log2(p) for p in probabilities if p > 0)
        entropy_after = -sum(p * math.log2(p) for p in probabilities if p > 0)
        '''
        score = 0
        return score
    
    def update(self):
        '''
        This method is the main update sequence of the game
        Returns:
            gamestate, (int) this is an integer representing the state of the game with the following convention (0: RED WIN, 1: BLUE WIN, -1:IN PROGRESS, -100:ERROR)
        '''
        if self.state == -1:
            # This has to be a deepcopy to accurately track the changing state of the game
            prior_grid = self.get_grid()
            self.cg.update_bot(self.grid)
            self.guessbot.update_bot(self.grid)
            clue, related = self.cg.give_clue()
            guesses = self.guessbot.guess(clue=clue,related=related)
            if guesses == []:
                state = -100
                return
            current_turn = self.grid.turn
            print(f"\n Turn {self.current_turn}\n")
            print(f"turn:{self.color_map[self.grid.turn]}{self.grid.turn}{self.color_map['reset']}, clue: {clue} {related}, guesses: {guesses}")
            # to print the complete probabilities of the guessbot
            # print(self.guessbot.toString()+ "\n")
            self.current_turn += 1
            for guess in guesses:
                self.cg.update_bot(self.grid)
                self.guessbot.update_bot(self.grid)
                print(f"guess: {guess}")
                val = self.grid.update_grid(guess)
                if val == 1:
                    self.blue += 1
                if val == 0:
                    self.red += 1
                    
                # GAME END WINNER
                if self.red == 8 + (1-self.starting_turn) or self.blue == 8 + (self.starting_turn):
                    self.state = self.grid.turn
                    print("GAME OVER \n")
                    print(f"{self.color_map[self.grid.turn]}{self.grid.turn} wins{self.color_map['reset']}")
                    print(self.toString())
                    #print(f"entropy score: {self.tabulate_entropy(prior_list)}, turn: {self.turn}")
                    return
                #GAME END ASSASSIN
                if val == -1:
                    self.state = self.grid.turn
                    print("GAME OVER \n")
                    print(f"{self.color_map[self.grid.turn]}{self.grid.turn} wins{self.color_map['reset']}")
                    print(self.toString())
                    #print(f"entropy score: {self.tabulate_entropy(prior_list)}, turn: {self.grid.turn}")
                    return
                
                #TURN END (INCORRECT GUESS)
                if val != current_turn:
                    print(self.toString())
                    print(f"entropy score: {self.tabulate_weighted_entropy(prior_grid)}, turn: {self.grid.turn}")
                    return
            #TURN END (PASS)
            print(f"entropy score: {self.tabulate_weighted_entropy(prior_grid)}, turn: {self.grid.turn}")
            self.grid.swap_turn()
            print(self.toString())
            return
        return

    def play(self):
        '''
        This method is the main driver for creating games with only AI.
        '''
        print(self.toString())
        while self.state == -1:
            self.update()
        return
        
def main():
    # seed 45643 has an active glitch
    # seed 252 had a glitch which I think I fixed. Need to investigate the clue given under duress.
    new_game = game(seed=255)
    new_game.play()
    
    
main()