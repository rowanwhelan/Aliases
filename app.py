import random
from flask import Flask, render_template, request 
from game_methods import generate_board
from clue_generator import clue_generator
import nltk

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    nltk.download('wordnet')
    return render_template("index.html")

@app.route("/game", methods=["GET", "POST"])
def generate_game():
    board = generate_board('data/words.csv')
    return render_template("game.html", grid=board)

@app.route("/practice_guesser", methods=["GET", "POST"])
def generate_prac_gues_game():
    board = generate_board('data/words.csv')
    cg_red = clue_generator(board=board, team=0)
    cg_blue = clue_generator(board=board, team=1)
    turn = random.randint(0,1)
    if turn == 0:
        clue = cg_red.give_clue()
    else:
        clue = cg_blue.give_clue()
    return render_template("practice_guesser.html", grid=board, turn=turn, clue=clue)

@app.route("/practice_giver", methods=["GET", "POST"])
def generate_prac_give_game():
    board = generate_board('data/words.csv')
    return render_template("practice_giver.html", grid=board)

def main():
    app.run(debug=True)
    
main()