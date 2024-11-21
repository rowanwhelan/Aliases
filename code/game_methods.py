import csv
from enum import Enum
import random

"""class WordType(Enum):
    PLAYER1 = 0
    PLAYER2 = 1
    ASSASSIN = -1
    NEUTRAL = 2"""

def post_process(word_list):
    for i in range(len(word_list)):
        if "_" in word_list[i]:
            word_list[i] = word_list[i].replace("_", " ")
    return word_list

def set_board_parameters(board, seed=None):
    if seed is not None:
        random.seed(seed)
    
    random.shuffle(board)
    word_assignments = []
    for word in board[:9]:
        word_assignments.append((word, 0))
    for word in board[9:17]:
        word_assignments.append((word, 1))    
    word_assignments.append((board[17], -1))
    for word in board[18:]:
        word_assignments.append((word, 2))
    random.shuffle(word_assignments)
    return word_assignments


def generate_board(file, num_samples=25, seed=None):
    '''    
    this method gets 25 words from the list of words in file randomly without replacement
    input:
        file, a string representing the path to a csv with the word corpus
        num_samples, the number of words to grab DEFAULT=25
        seed, an int representing the random seed DEFAULT=NONE
    '''
    if seed is not None:
        random.seed(seed)
    
    with open(file, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        words = [row[0] for row in reader]  

    unique_words = list(set(words))  
    if len(unique_words) < num_samples:
        raise ValueError("Not enough unique words to sample.")
    
    reservoir = random.sample(unique_words, num_samples)  
    reservoir = post_process(reservoir)
    board = set_board_parameters(reservoir)
    return board

def main():
    pass
main()