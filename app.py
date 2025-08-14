import os
from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Load words (you might want to move this to a separate file)
def load_words(filename='words_alpha.txt'):
    try:
        with open(filename, 'r') as file:
            return [word.strip().upper() for word in file if len(word.strip()) == 5]
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return ['APPLE', 'BRAVE', 'CRANE', 'SLATE', 'PLANE', 'FLUTE', 'GRAPE', 'BRAIN']

WORDS = load_words()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/new_game')
def new_game():
    word = random.choice(WORDS)
    return jsonify({'word': word})

@app.route('/api/check_guess', methods=['POST'])
def check_guess():
    data = request.json
    guess = data.get('guess', '').upper()
    word = data.get('word', '').upper()
    if len(guess) != 5 or len(word) != 5:
        return jsonify({'error': 'Guess and word must be 5 letters'}), 400
    if guess not in WORDS:
        return jsonify({'error': 'Not a valid word'}), 400
    result = ['green' if g == w else 'yellow' if g in word else 'gray' for g, w in zip(guess, word)]
    return jsonify({'result': result})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)