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

def main():
    app.run(debug=True)
    
main()