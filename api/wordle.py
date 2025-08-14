from http.server import BaseHTTPRequestHandler
import json
import random

def load_words(filename='words_alpha.txt'):
    try:
        with open(filename, 'r') as file:
            return [word.strip().upper() for word in file if len(word.strip()) == 5]
    except FileNotFoundError:
        return ['APPLE', 'BRAVE', 'CRANE', 'SLATE', 'PLANE', 'FLUTE', 'GRAPE', 'BRAIN']

WORDS = load_words()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        word = random.choice(WORDS)
        response = json.dumps({'word': word})
        self.wfile.write(response.encode())
        return

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())

        if self.path == '/check_word':
            word = data.get('word', '').upper()
            is_valid = word in WORDS
            response = json.dumps({'valid': is_valid})
        elif self.path == '/check_guess':
            guess = data.get('guess', '').upper()
            word = data.get('word', '').upper()
            result = ['green' if g == w else 'yellow' if g in word else 'gray' for g, w in zip(guess, word)]
            response = json.dumps({'result': result})
        else:
            response = json.dumps({'error': 'Invalid endpoint'})

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response.encode())
        return