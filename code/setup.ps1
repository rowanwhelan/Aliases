conda activate wordgame-env
python -c "from app import db; db.create_all()"
python -c "import nltk; nltk.download('wordnet')"