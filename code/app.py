import random
from flask import Flask, jsonify, redirect, render_template, request, session, url_for 
from bots.clues.clue_generator import clue_generator
import nltk
from grid import grid
from flask_sqlalchemy import SQLAlchemy # type: ignore

app = Flask(__name__,template_folder='../templates', static_folder='../static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wordgame.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

### CLASS DEFINITIONS ###
class GameBoard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_state = db.Column(db.JSON, nullable=False)
    turn = db.Column(db.String, nullable=False)

    def to_json(self):
        return {"board": self.board_state, "turn": self.turn}

    @classmethod
    def from_json(cls, data):
        return cls(board_state=data["board"], turn=data["turn"])

### GENERAL PAGES ###
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/statistics", methods=["GET", "POST"])
def generate_stastics():
    return render_template("statistics.html")


### GENERALIZED GAME METHODS ###
@app.route("/game", methods=["GET", "POST"])
def generate_game():
    board = grid(25, '../data/common_words.csv', seed=1)
    game = GameBoard(board_state=board.to_json(), turn=board.turn)
    db.session.add(game)
    db.session.commit()
    return render_template("game.html", grid=board)

@app.route('/update-grid', methods=['POST'])
def update_grid():
    data = request.json
    word = data.get('word')
    game = GameBoard.query.first()
    board = grid.from_json(grid, game.board_state)
    turn = board.update_grid(word)
    game.board_state = board.to_json()
    game.turn = turn
    db.session.commit()
    return jsonify({'turn': turn})
    
### BOT GAME METHODS ###
@app.route("/botgame", methods=["GET", "POST"])
def generate_botgame():
    # Create the game board
    board = grid(25, 'data/common_nouns.csv', seed=3)
    cg = clue_generator(board, board.turn)
    
    # Store the board state and turn in the database
    board_state = board.to_json()
    game_board = GameBoard(board_state=board_state, turn=board.turn)
    db.session.add(game_board)
    db.session.commit()
    
    # Give the initial clue
    clue, related = cg.give_clue()
    
    return render_template("botgame.html", grid=board, turn=board.turn, clue=clue, related=related)

@app.route('/update-botgame', methods=['POST'])
def update_botgame():
    data = request.json
    clue = data.get("clue")
    related = data.get("related")
    word = data.get("word")
    
    # Get the latest game board from the database
    game_board = GameBoard.query.order_by(GameBoard.id.desc()).first()
    board = grid.from_json(grid, game_board.board_state)
    
    # Update the board with the selected word
    turn = board.update_grid(word)
    
    # Update the clue generator if the turn has changed
    cg = clue_generator.from_json(clue_generator, game_board.board_state)
    if cg.turn != turn:
        cg.update_team()
        clue, related = cg.give_clue()
        print(f"new clue {clue} - new number {related} - new turn {turn}\n")
        print(board.toString())
    
    # Update the board state in the database
    game_board.board_state = board.to_json()
    game_board.turn = turn
    db.session.commit()
    
    return jsonify({
        'clue': clue,
        'related': related
    })

if __name__ == "__main__":
    app.run(debug=True)