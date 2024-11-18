from flask import Flask, render_template, request 
from game_methods import generate_board

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/game", methods=["GET", "POST"])
def generate_game():
    board = generate_board('data/words.csv')
    return render_template("game.html", grid=board)

@app.route("/practice_guesser", methods=["GET", "POST"])
def generate_prac_gues_game():
    board = generate_board('data/words.csv')
    return render_template("practice_guesser.html", grid=board)

@app.route("/practice_giver", methods=["GET", "POST"])
def generate_prac_give_game():
    board = generate_board('data/words.csv')
    return render_template("practice_giver.html", grid=board)

def main():
    app.run(debug=True)
    
main()