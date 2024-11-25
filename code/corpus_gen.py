import nltk
from nltk.corpus import words, wordnet as wn
import csv

nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('words')

def extract_wordnet_words():
    wordnet_words = {'nouns': set(), 'adjectives': set(), 'verbs': set()}
    for synset in wn.all_synsets():
        if synset.pos() == 'n':  # Nouns
            wordnet_words['nouns'].update([lemma.name() for lemma in synset.lemmas()])
        elif synset.pos() == 'a':  # Adjectives
            wordnet_words['adjectives'].update([lemma.name() for lemma in synset.lemmas()])
        elif synset.pos() == 'v':  # Verbs
            wordnet_words['verbs'].update([lemma.name() for lemma in synset.lemmas()])
    print("words successfully extracted")
    return wordnet_words

def extract_common_words():

    # Get all English words
    english_words = set(words.words())
    
    # Define a helper function to check if a word belongs to a specific category
    def is_common_word(word, pos_tag):
        synsets = wn.synsets(word, pos=pos_tag)
        # A word is considered common if it has at least one matching synset
        return len(synsets) > 5
    
    # Filter common nouns, verbs, and adjectives
    common_nouns = [word for word in english_words if is_common_word(word, wn.NOUN) and 3 <= len(word) <= 8]
    common_verbs = [word for word in english_words if is_common_word(word, wn.VERB) and 3 <= len(word) <= 8]
    common_adjectives = [word for word in english_words if is_common_word(word, wn.ADJ) and 3 <= len(word) <= 8]
    
    # Prepare the list of words to save
    common_words = {
        "nouns": common_nouns[:200],       # Save the first 200 nouns for brevity
        "verbs": common_verbs[:200],      # Save the first 200 verbs for brevity
        "adjectives": common_adjectives[:200]  # Save the first 200 adjectives for brevity
    }
    
    return common_words

def extract_common_nouns():
    # Get all English words
    english_words = set(words.words())
    
    # Define a helper function to check if a word belongs to a specific category
    def is_common_word(word, pos_tag):
        synsets = wn.synsets(word, pos=pos_tag)
        # A word is considered common if it has at least one matching synset
        return len(synsets) > 10
    
    # Filter common nouns, verbs, and adjectives
    common_nouns = [word for word in english_words if is_common_word(word, wn.NOUN) and 3 <= len(word) <= 8]
    common_verbs = [word for word in english_words if is_common_word(word, wn.VERB) and 3 <= len(word) <= 8]
    common_adjectives = [word for word in english_words if is_common_word(word, wn.ADJ) and 3 <= len(word) <= 8]
    
    # Prepare the list of words to save
    common_words = {
        "nouns": common_nouns[:100],       # Save the first 200 nouns for brevity
    }
    
    return common_words

def save_words_to_csv(words, output_file):
    with open(output_file, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['word', 'pos'])  # Header row

        for pos, word_set in words.items():
            for word in word_set:
                writer.writerow([word, pos])
    return

def main():
    filename = 'common_nouns'
    #wordnet_words = extract_wordnet_words()
    common_words = extract_common_nouns()
    save_words_to_csv(common_words, f'data/{filename}.csv')
    print(f"corpus successfully saved to data/{filename}.csv")
    
    
main()
