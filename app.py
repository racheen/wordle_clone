# app.py
from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

def load_words(filename):
    try:
        with open(filename, 'r') as file:
            return [word.strip().upper() for word in file if len(word.strip()) == 5]
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return ['APPLE', 'BRAVE', 'CRANE', 'SLATE', 'PLANE', 'FLUTE', 'GRAPE', 'BRAIN']

WORDS = load_words('words_alpha.txt')  # Load your words here

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_game')
def new_game():
    word = random.choice(WORDS)
    print(f"New game started: {word}")
    return jsonify({'word': word})

@app.route('/check_guess', methods=['POST'])
def check_guess():
    guess = request.json['guess']
    word = request.json['word']
    if guess not in WORDS:
        return jsonify({'error': 'Not a valid word'}), 400
    result = ['green' if g == w else 'yellow' if g in word else 'gray' for g, w in zip(guess, word)]
    return jsonify({'result': result})

@app.route('/check_word', methods=['POST'])
def check_word():
    word = request.json['word']
    return jsonify({'valid': word in WORDS})

if __name__ == '__main__':
    app.run(debug=True)