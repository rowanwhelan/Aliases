import random
from flask import Flask, render_template, request 
from game_methods import generate_board
from clue_generator import clue_generator
import nltk
import gensim.downloader as api

#path = api.load("word2vec-google-news-300", return_path=True)
path = "C:/Users/rwhel/gensim-data/word2vec-google-news-300/word2vec-google-news-300.gz"

app = Flask(__name__,template_folder='../templates')

@app.route("/", methods=["GET", "POST"])
def index():
    nltk.download('wordnet')
    return render_template("index.html")

@app.route("/game", methods=["GET", "POST"])
def generate_game():
    board = generate_board('data/common_words.csv',seed=2)
    random.seed(1)
    turn = random.randint(0,1)
    return render_template("game.html", grid=board, turn=turn)

@app.route("/practice_guesser", methods=["GET", "POST"])
def generate_prac_gues_game():
    board = generate_board('data/common_words.csv', seed=2)
    cg_red = clue_generator(board=board, team=0, model_path=path)
    cg_blue = clue_generator(board=board, team=1, model_path=path)
    random.seed(1)
    turn = random.randint(0,1)
    if turn == 0:
        clue,related = cg_red.give_clue()
    else:
        clue,related = cg_blue.give_clue()
    return render_template("practice_guesser.html", grid=board, turn=turn, clue=clue, related=related)

@app.route("/practice_giver", methods=["GET", "POST"])
def generate_prac_give_game():
    board = generate_board('data/words.csv')
    return render_template("practice_giver.html", grid=board)

def main():
    app.run(debug=True)
    
main()