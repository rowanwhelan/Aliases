# **Aliases - Flask Web App**

This is a **Flask-based word association game** where players take turns selecting words. The game dynamically updates based on team selections and features an integrated **bot mode** that generates clues for automated play. The project is designed for **scalability and maintainability**, using **Flask, SQLAlchemy, and SQLite** to manage game states and statistics.

---

## **Features**
- **Flask Backend**: Handles game logic, turn-based interactions, and clue generation.
- **Database-Driven State Management**: Uses SQLite + SQLAlchemy instead of Redis for persistent storage.
- **Bot Game Mode**: A bot generates word association clues using NLP techniques.
- **RESTful API**: Endpoints for updating the game board dynamically.
- **Scalable Architecture**: Built for easy transition to a more robust database (e.g., PostgreSQL) if needed.

---

## **⚙Tech Stack**
- **Backend**: Flask, Flask-SQLAlchemy
- **Database**: SQLite (easily replaceable with PostgreSQL/MySQL)
- **Game Logic**: Custom Python classes for board and bot-generated clues
- **Frontend**: Jinja2 templates (with dynamic rendering)
