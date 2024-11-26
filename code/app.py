import random
from flask import Flask, jsonify, redirect, render_template, request, session, url_for 
from bots.clues.clue_generator import clue_generator
import redis
import nltk
from grid import grid

app = Flask(__name__,template_folder='../templates', static_folder='../static')
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
nltk.download('wordnet')

### GENERAL PAGES
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/statistics", methods=["GET", "POST"])
def generate_stastics():
    return render_template("statistics.html")


### GENERALIZED GAME METHODS
@app.route("/game", methods=["GET", "POST"])
def generate_game():
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
    
### BOT GAME METHODS
@app.route("/botgame", methods=["GET", "POST"])
def generate_botgame():
    
    board = grid(25, 'data/common_nouns.csv',seed=3)
    cg = clue_generator(board, board.turn)
    
    redis_client.set("board", board.to_json())
    redis_client.set("cg", cg.to_json())
    
    clue, related = cg.give_clue()
    return render_template("botgame.html", grid=board, turn=board.turn, clue=clue, related=related)

@app.route('/update-botgame', methods=['POST'])
def update_botgame():
    data = request.json
    clue = data.get("clue")
    related = data.get("related")
    word = data.get("word")
    cg = clue_generator.from_json(clue_generator, redis_client.get("cg"))
    
    board = grid.from_json(grid, redis_client.get("board"))
    turn = board.update_grid(word)
    if cg.turn != turn:
        cg.update_team()
        clue, related = cg.give_clue()
        print(f"new clue {clue} - new number {related} - new turn {turn}\n")
        print(board.toString())
    return jsonify({
        'clue': clue,
        'related': related
    })
    
def main():
    app.run(debug=True)
    
main()