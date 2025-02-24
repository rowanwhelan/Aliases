from datetime import datetime
from flask import Flask, jsonify, redirect, render_template, request, session, url_for 
from bots.clues.clue_generator import clue_generator
from grid import grid
from flask_sqlalchemy import SQLAlchemy # type: ignore

app = Flask(__name__,template_folder='../templates', static_folder='../static')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:/Users/rwhel/Portfolio/Aliases/code/instance/Aliases.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "sodfnsognosfn"
db = SQLAlchemy(app)

### CLASS DEFINITIONS ###
class GameBoard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_state = db.Column(db.JSON, nullable=False)
    turn = db.Column(db.Integer, nullable=False)

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
    team = db.Column(db.Integer, nullable=False)  # 0 (red) or 1 (blue) for team assignment
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    role = db.Column(db.Integer, nullable=False) # 0 (guesser) or 1 (clue giver) 


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
        # Get the player's username from the form
        username = request.form.get('username')

        # Count current players to decide the team
        current_players = Player.query.filter_by(game_id=game.id).count()
        if current_players >= 4:
            return "Game is full", 400
        
        team = current_players % 2  # Alternate teams (0, 1, 0, 1)
        role = 1 if current_players in [0, 1] else 0  # First two players get role 1
        
        # Create and save the new player
        new_player = Player(username=username, team=team, game_id=game.id, role=role)
        db.session.add(new_player)
        db.session.commit()

        # Store the role in the session
        session['username'] = username

        return redirect(url_for('lobby', game_id=game.id))

    # For GET requests, show the join form
    return render_template('join_game.html', game=game)

@app.route('/lobby/<int:game_id>')
def lobby(game_id):
    game = Game.query.get_or_404(game_id)
    join_link = request.host_url + 'join_game/' + str(game.id)
    players = Player.query.filter_by(game_id=game.id).all()
    return render_template('lobby.html', game_id=game.id, join_link=join_link, players=players)

@app.route("/game/<int:game_id>", methods=["GET", "POST"])
def start_multiplayer_game(game_id):
    # Retrieve the game and its players
    game = Game.query.get_or_404(game_id)
    players = Player.query.filter_by(game_id=game.id).all()

    # Identify the current player (assuming their username is stored in session)
    username = session.get("username")
    if not username:
        return redirect(url_for("lobby", game_id=game_id))  # Redirect if not logged in

    current_player = next((p for p in players if p.username == username), None)
    if not current_player:
        return redirect(url_for("lobby", game_id=game_id))  # Redirect if not in the game

    # Initialize the game board
    board = grid(25, 'C:/Users/rwhel/Portfolio/Aliases/data/common_words.csv', seed=1)
    game_board = GameBoard(board_state=board.to_json(), turn=board.turn)
    db.session.add(game_board)
    db.session.commit()

    # Render the game page with player role
    return render_template("game.html", grid=board, players=players, role=current_player.role)

@app.route('/get_active_games', methods=['GET'])
def get_active_games():
    # Get the page number from the query string (default to 1 if not provided)
    page = request.args.get('page', 1, type=int)
    
    # Fetch games that are waiting for players, with pagination (25 per page)
    games = Game.query.filter_by(status='waiting').paginate(page=page, per_page=25, error_out=False)

    # Prepare data to be displayed
    active_games = [{"game_id": game.id, "players": len(game.players)} for game in games.items]
    
    # Render the active_games.html template with the active games data and pagination info
    return render_template('active_games.html', active_games=active_games, page=page, total_pages=games.pages)

@app.route('/end_game/<int:game_id>', methods=['POST'])
def end_game(game_id):
    game = Game.query.get(game_id)

    if not game:
        return jsonify({"message": "Game not found"}), 404

    game.status = 'completed'
    db.session.commit()

    return jsonify({"message": "Game ended"}), 200

@app.route('/submit_clue', methods=['POST'])
def submit_clue():
    # Ensure a user is logged in
    username = session.get("username")
    if not username:
        return jsonify({"error": "User not logged in"}), 403

    # Find the player
    player = Player.query.filter_by(username=username).first()
    if not player:
        return jsonify({"error": "Player not found"}), 404

    # Ensure the player is role 1 (clue giver)
    if player.role != 1:
        return jsonify({"error": "Only role 1 players can submit clues"}), 403

    # Get the clue data from the request
    data = request.get_json()
    clue_text = data.get("clue")
    clue_number = data.get("number")

    # Validate inputs
    if not clue_text or not isinstance(clue_number, int) or clue_number <= 0:
        return jsonify({"error": "Invalid clue input"}), 400

    # Save the clue (assuming there's a GameState or ClueLog model)
    game = Game.query.get(player.game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404

    # Append clue to the game log (assuming game has a clue_log column)
    if game.clue_log is None:
        game.clue_log = []
    game.clue_log.append(f"{clue_text} ({clue_number})")

    db.session.commit()

    # Return success response
    return jsonify({"message": "Clue submitted successfully", "clue": clue_text, "number": clue_number})


### GENERALIZED GAME METHODS ###
@app.route("/game", methods=["GET", "POST"])
def generate_game():
    board = grid(25, 'C:/Users/rwhel/Portfolio/Aliases/data/common_words.csv', seed=1)
    game = GameBoard(board_state=board.to_json(), turn=board.turn)
    db.session.add(game)
    db.session.commit()
    return render_template("game.html", grid=board, role=0)

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