Set-Location -Path "C:\Users\rwhel\Portfolio\Aliases\code"
conda activate wordgame-env
python setup_db.py
python -c "import nltk; nltk.download('wordnet')"