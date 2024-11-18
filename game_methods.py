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
    reservoir = []
    
    if seed is not None:
        random.seed(seed)
    
    with open(file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for index, row in enumerate(reader):
            word = row[0]  

            if index < num_samples:
                reservoir.append(word)
            else:
                j = random.randint(0, index)
                if j < num_samples:
                    reservoir[j] = word
    reservoir = post_process(reservoir)
    board = set_board_parameters(reservoir)
    return board

def main():
    pass
main()