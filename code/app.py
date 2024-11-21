import random
from flask import Flask, jsonify, redirect, render_template, request, session, url_for 
from game_methods import generate_board
from bots.clue_generator import clue_generator
import redis
import nltk
from grid import grid

app = Flask(__name__,template_folder='../templates', static_folder='../static')
app.secret_key = 'ijbafibsiygfadnafhiqrubqfk'
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
nltk.download('wordnet')

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/game", methods=["GET", "POST"])
def generate_game():
    random.seed(2)
    board = grid(25, 'data/common_words.csv',seed=1)
    redis_client.set("board", board.to_json())
    return render_template("game.html", grid=board)

@app.route('/update-grid', methods=['POST'])
def update_grid():
    data = request.json
    word = data.get('word')
    board = grid.from_json(grid, redis_client.get("board"))
    turn = board.update_grid(word)
    return jsonify({
        'turn': turn
    })

@app.route("/stastics", methods=["GET", "POST"])
def generate_stastics():
    return render_template("stastics.html")

def main():
    app.run(debug=True)
    
main()