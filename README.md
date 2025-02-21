Word Association Game

Overview

This project is a word association game where players take turns selecting words based on given clues. The game dynamically updates the board state, maintains turn logic, and supports bot-driven gameplay. The backend is powered by Flask with SQLAlchemy for database management, while the frontend renders game updates in real-time.

Technical Stack

Backend: Flask (Python), Flask-SQLAlchemy

Database: SQLite (easily extendable to PostgreSQL or MySQL)

Frontend: HTML, Jinja2 templates

Deployment: Local development setup with Conda

Key Features

Game Logic:

Supports a 5x5 game grid with words categorized into different teams.

Tracks turns and updates game states dynamically.

Clue generation is handled by a bot-driven AI component.

Database Integration:

Uses SQLAlchemy ORM to manage game states.

Stores board states and turn history efficiently in SQLite.

Flask Web Framework:

Routes for generating and updating the game board.

JSON-based API for handling user interactions.

Bot Gameplay:

Automated clue generator for AI-assisted play.

Stores and retrieves game state efficiently for bot decision-making.

Setup Instructions

1. Install Dependencies

Ensure you have Conda installed, then create and activate the environment:

conda create --name wordgame-env python=3.9 -y
conda activate wordgame-env

2. Install Required Packages

pip install -r requirements.txt

3. Initialize the Database

python -c "from app import db; db.create_all()"

4. Run the Application

python app.py

Code Structure

├── app.py                # Main Flask application
├── models.py             # SQLAlchemy database models
├── templates/            # HTML templates for rendering game UI
├── static/               # CSS and JavaScript files
├── bots/
│   ├── clues/            # AI-powered clue generation logic
│   └── ...
├── grid.py               # Game grid logic
├── setup.bash            # Setup script for easy environment configuration
└── README.md             # Project documentation

Future Enhancements

Implement WebSocket support for real-time updates.

Deploy with PostgreSQL and Docker for scalable cloud hosting.

Add user authentication and multiplayer mode.

Contact

For questions or collaborations, feel free to reach out!

