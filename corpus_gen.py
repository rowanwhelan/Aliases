import nltk
from nltk.corpus import wordnet as wn
import csv

nltk.download('wordnet')
nltk.download('omw-1.4')

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

def save_words_to_csv(words, output_file):
    with open(output_file, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['word', 'pos'])  # Header row

        for pos, word_set in words.items():
            for word in word_set:
                writer.writerow([word, pos])
    return

def main():
    filename = 'words'
    wordnet_words = extract_wordnet_words()
    save_words_to_csv(wordnet_words, f'data/{filename}.csv')
    print(f"corpus successfully saved to data/{filename}.csv")
    
    
main()
