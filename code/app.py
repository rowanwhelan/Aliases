import random
from flask import Flask, jsonify, redirect, render_template, request, session, url_for 
from game_methods import generate_board
from bots.clue_generator import clue_generator
import nltk
import gensim.downloader as api
from grid import grid

app = Flask(__name__,template_folder='../templates', static_folder='../static')
app.secret_key = 'ijbafibsiygfadnafhiqrubqfk'

@app.route("/", methods=["GET", "POST"])
def index():
    nltk.download('wordnet')
    return render_template("index.html")

@app.route("/game", methods=["GET", "POST"])
def generate_game():
    random.seed(2)
    if 'board' in session:
        board_data = session['board']
        board = grid.from_dict(board_data)
    else:
        board = grid(25, 'data/common_words.csv',seed=1)
    game_board = board.to_dict()
    session['board'] = game_board
    return render_template("game.html", grid=board)

@app.route('/update-grid', methods=['POST'])
def update_grid():
    data = request.json
    word = data.get('word')
    if 'board' in session:
        board_data = session['board']
        board = grid.from_dict(board_data)
    else:
        board = grid(25, 'wordlist.csv')
        
    turn = board.update_grid(word)
    session['board'] = grid.to_dict()

    # Return the updated game state (including the turn)
    return jsonify({
        'turn': turn
    })

@app.route("/stastics", methods=["GET", "POST"])
def generate_stastics():
    return render_template("stastics.html")

def main():
    app.run(debug=True)
    
main()