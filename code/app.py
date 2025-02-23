from datetime import datetime
from flask import Flask, jsonify, redirect, render_template, request, session, url_for 
from bots.clues.clue_generator import clue_generator
from grid import grid
from flask_sqlalchemy import SQLAlchemy # type: ignore

app = Flask(__name__,template_folder='../templates', static_folder='../static')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:/Users/rwhel/Portfolio/Aliases/code/instance/Aliases.db"
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

class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    turn = db.Column(db.Integer, default=0)  # Track whose turn it is
    status = db.Column(db.String(50), default='waiting')  # 'waiting', 'in-progress', 'completed'
    players = db.relationship('Player', backref='game', lazy=True)

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    team = db.Column(db.Integer, nullable=False)  # 0 or 1 for team assignment
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)


### GENERAL PAGES ###
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/statistics", methods=["GET", "POST"])
def generate_stastics():
    return render_template("statistics.html")

### MULTIPLAYER ###
@app.route('/create_game', methods=['POST'])
def create_game():
    # Create the game in the database
    game = Game()
    db.session.add(game)
    db.session.commit()
    
    # Generate a join link using the host URL and game id.
    join_link = request.host_url + 'join_game/' + str(game.id)
    
    # Render the lobby template with game info and join link
    return render_template('lobby.html', game_id=game.id, join_link=join_link)

@app.route('/join_game/<int:game_id>', methods=['GET', 'POST'])
def join_game(game_id):
    game = Game.query.get_or_404(game_id)
    
    if request.method == 'POST':
        # Get the player's username from a form submission
        username = request.form.get('username')
        # Count current players to decide which team to assign
        current_players = Player.query.filter_by(game_id=game.id).count()
        if current_players >= 4:
            return "Game is full", 400
        team = current_players % 2  # alternate teams (0, then 1, then 0, ...)
        new_player = Player(username=username, team=team, game_id=game.id)
        db.session.add(new_player)
        db.session.commit()
        return redirect(url_for('lobby', game_id=game.id))
    
    # For GET requests, show the join form
    return render_template('join_game.html', game=game)

@app.route('/lobby/<int:game_id>')
def lobby(game_id):
    game = Game.query.get_or_404(game_id)
    join_link = request.host_url + 'join_game/' + str(game.id)
    players = Player.query.filter_by(game_id=game.id).all()
    return render_template('lobby.html', game_id=game.id, join_link=join_link, players=players)

@app.route('/get_active_games', methods=['GET'])
def get_active_games():
    games = Game.query.filter_by(status='waiting').all()
    active_games = [{"game_id": game.id, "players": len(game.players)} for game in games]
    return jsonify({"active_games": active_games}), 200

@app.route('/make_move/<int:game_id>/<int:player_id>', methods=['POST'])
def make_move(game_id, player_id):
    game = Game.query.get(game_id)
    player = Player.query.get(player_id)

    if not game or not player:
        return jsonify({"message": "Invalid game or player"}), 400

    if game.status != 'in-progress':
        return jsonify({"message": "Game not in progress"}), 400

    if player.team != game.turn:
        return jsonify({"message": "It's not your turn"}), 400

    # Logic to handle making a move (e.g., selecting a word, updating board, etc.)
    data = request.json
    word = data.get('word')
    turn = GameBoard.board_state.update_grid(word)
    # Update turn to the other team
    game.turn = turn # Toggle between team 0 and team 1
    db.session.commit()

    return jsonify({"message": "Move made", "turn": game.turn}), 200

@app.route('/end_game/<int:game_id>', methods=['POST'])
def end_game(game_id):
    game = Game.query.get(game_id)

    if not game:
        return jsonify({"message": "Game not found"}), 404

    game.status = 'completed'
    db.session.commit()

    return jsonify({"message": "Game ended"}), 200

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