import random
from grid import grid
from bots.clues.clue_generator import clue_generator
from bots.guesses.bot import bot
from colorama import Fore, Style, init
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

    
    def toString(self):
        return self.grid.toString()
    
    def update(self):
        '''
        This method is the main update sequence of the game
        Returns:
            gamestate, (int) this is an integer representing the state of the game with the following convention (0: RED WIN, 1: BLUE WIN, -1:IN PROGRESS, -100:ERROR)
        '''
        if self.state == -1:
            clue, related = self.cg.give_clue()
            guesses = self.guessbot.guess(clue=clue,related=related)
            if guesses == []:
                state = -100
                return
            current_turn = self.grid.turn
            print(f"\n Turn {self.current_turn}\n")
            print(f"turn:{self.color_map[self.grid.turn]}{self.grid.turn}{self.color_map['reset']}, clue: {clue} {related}, guesses: {guesses}")
            print(self.guessbot.toString()+ "\n")
            self.current_turn += 1
            for guess in guesses:
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
                    return
                #GAME END ASSASSIN
                if val == -1:
                    self.state = self.grid.turn
                    print("GAME OVER \n")
                    print(f"{self.color_map[self.grid.turn]}{self.grid.turn} wins{self.color_map['reset']}")
                    print(self.toString())
                    return
                
                self.cg.update_bot(self.grid)
                self.guessbot.update_bot(self.grid)
                #TURN END (INCORRECT GUESS)
                if val != current_turn:
                    print(self.toString())
                    return
            #TURN END (PASS)
            self.grid.swap_turn()
            print(self.toString())
            return
        return

    def play(self):
        print(self.toString())
        while self.state == -1:
            self.update()
        return
            
        
def main():
    # seed 45643 has an active glitch
    new_game = game(seed=231)
    new_game.play()
    
    
main()