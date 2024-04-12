import string
import re
import numpy as np
from collections import Counter
import streamlit as st

# Importing data
def read_corpus(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        words = []
        for word in lines:
            words += re.findall(r'\w+', word.lower())
    return words

# Invoke this function
corpus = read_corpus(r"C:\Users\Suyash\Downloads\big.txt")
vocab = set(corpus)
words_count = Counter(corpus)
total_words_count = float(sum(words_count.values()))
word_probabs = {word: words_count[word] / total_words_count for word in words_count.keys()}

def split(word):
    return [(word[:i], word[i:]) for i in range(len(word) + 1)]

def delete(word):
    return [left + right[1:] for left, right in split(word) if right]

def swap(word):
    return [left + right[1] + right[0] + right[2:] for left, right in split(word) if len(right) > 1]

def replace(word):
    return [left + center + right[1:] for left, right in split(word) if right for center in string.ascii_lowercase]

def insert(word):
    return [left + center + right for left, right in split(word) for center in string.ascii_lowercase]

def level_one_edits(word):
    return set((delete(word) + swap(word) + replace(word) + insert(word)))

def level_two_edits(word):
    return set(e2 for e1 in level_one_edits(word) for e2 in level_one_edits(e1))

def correct_spelling(word, vocab, word_probabs):
    if word in vocab:
        return f"{word} is already correctly spelled"
    
    suggestions = level_one_edits(word) or level_two_edits(word) or [word]
    best_guesses = [w for w in suggestions if w in vocab]
    
    if not best_guesses:
        return f"Sorry, no suggestions found for {word}"
    
    suggestions_with_probabs = [(w, word_probabs[w]) for w in best_guesses]
    suggestions_with_probabs.sort(key=lambda x: x[1], reverse=True)
    
    return f"Suggestions for {word}: " + ', '.join([f"{w} ({prob:.2%})" for w, prob in suggestions_with_probabs[:10]])

# GUI or Web App
st.title("SpellCheck Pro: Auto-Correct Misspelled Word Search Engine")
word = st.text_input('Search Here')

if st.button('Check'):
    result = correct_spelling(word, vocab, word_probabs)
    st.write(result)



