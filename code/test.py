from game_methods import generate_board
def main():
    board1 = generate_board('data/common_words.csv',seed=1)
    board2 = generate_board('data/common_words.csv',seed=1)
    print(f"board1 = {board1}\nboard2 = {board2}")
main()