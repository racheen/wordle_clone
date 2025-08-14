import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class WordleGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Wordle Simulator')
        self.setGeometry(100, 100, 600, 800)

        self.WORDS = self.load_words('words_alpha.txt')
        self.init_game()

    def init_game(self):
        self.secret_word = self.choose_word()
        self.MAX_GUESSES = 6
        self.current_guess = 0

        print(f"Secret word chosen: {self.secret_word}")

        self.init_ui()

    def load_words(self, filename):
        try:
            with open(filename, 'r') as file:
                return [word.strip().upper() for word in file if len(word.strip()) == 5]
        except FileNotFoundError:
            print(f"Error: The file {filename} was not found.")
            return ['APPLE', 'BRAVE', 'CRANE', 'SLATE', 'PLANE', 'FLUTE', 'GRAPE', 'BRAIN']

    def choose_word(self):
        return random.choice(self.WORDS)

    def init_ui(self):
        # Clear the existing layout if there is one
        if self.centralWidget():
            old_layout = self.centralWidget().layout()
            if old_layout:
                while old_layout.count():
                    item = old_layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()
            self.centralWidget().deleteLater()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create grid
        grid_layout = QGridLayout()
        self.tiles = []
        for i in range(self.MAX_GUESSES):
            row = []
            for j in range(5):
                tile = QLabel(' ')
                tile.setAlignment(Qt.AlignCenter)
                tile.setStyleSheet('border: 2px solid black; font-size: 20px;')
                tile.setFixedSize(50, 50)
                grid_layout.addWidget(tile, i, j)
                row.append(tile)
            self.tiles.append(row)

        layout.addLayout(grid_layout)

        # Current guess label
        self.current_guess_label = QLabel("Current Guess: ")
        self.current_guess_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.current_guess_label)

        # Entry and button
        input_layout = QHBoxLayout()
        self.entry = QLineEdit()
        self.entry.setFont(QFont('Helvetica', 20))
        self.entry.setFixedWidth(150)
        input_layout.addWidget(self.entry)

        self.submit_btn = QPushButton('Submit')
        self.submit_btn.clicked.connect(self.check_guess)
        input_layout.addWidget(self.submit_btn)

        layout.addLayout(input_layout)

        # On-screen keyboard
        self.keyboard = self.create_keyboard()
        layout.addLayout(self.keyboard)

    def create_keyboard(self):
        keyboard_layout = QVBoxLayout()
        rows = [
            'QWERTYUIOP',
            'ASDFGHJKL',
            'ZXCVBNM'
        ]
        self.key_buttons = {}
        for row in rows:
            row_layout = QHBoxLayout()
            for letter in row:
                btn = QPushButton(letter)
                btn.setFixedSize(40, 40)
                btn.clicked.connect(self.on_key_press)
                row_layout.addWidget(btn)
                self.key_buttons[letter] = btn
            keyboard_layout.addLayout(row_layout)
        return keyboard_layout

    def on_key_press(self):
        sender = self.sender()
        current_text = self.entry.text()
        if len(current_text) < 5:
            self.entry.setText(current_text + sender.text())

    def check_guess(self):
        guess = self.entry.text().upper()
        print(f"Guess submitted: {guess}")
        if len(guess) != 5:
            QMessageBox.warning(self, 'Error', 'Guess must be 5 letters')
            return
        
        if guess not in self.WORDS:
            QMessageBox.warning(self, 'Error', 'Not a valid word')
            return

        self.current_guess_label.setText(f"Current Guess: {guess}")

        for i, letter in enumerate(guess):
            tile = self.tiles[self.current_guess][i]
            tile.setText(letter)
            if letter == self.secret_word[i]:
                tile.setStyleSheet('background-color: green; color: white; border: 2px solid black; font-size: 20px;')
                self.key_buttons[letter].setStyleSheet('background-color: green; color: white;')
            elif letter in self.secret_word:
                tile.setStyleSheet('background-color: yellow; color: black; border: 2px solid black; font-size: 20px;')
                if self.key_buttons[letter].styleSheet() != 'background-color: green; color: white;':
                    self.key_buttons[letter].setStyleSheet('background-color: yellow; color: black;')
            else:
                tile.setStyleSheet('background-color: gray; color: white; border: 2px solid black; font-size: 20px;')
                if self.key_buttons[letter].styleSheet() not in ['background-color: green; color: white;', 'background-color: yellow; color: black;']:
                    self.key_buttons[letter].setStyleSheet('background-color: gray; color: white;')

        self.current_guess += 1
        self.entry.clear()

        if guess == self.secret_word:
            self.game_over("You won!")
        elif self.current_guess == self.MAX_GUESSES:
            self.game_over("Game over!")

    def game_over(self, message):
        reply = QMessageBox.question(self, 'Wordle', f"{message} The word was {self.secret_word}. Do you want to play again?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.init_game()
        else:
            self.close()

def main():
    app = QApplication(sys.argv)
    game = WordleGame()
    game.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()