import requests
from bs4 import BeautifulSoup
from random import choice
from csv import DictReader
import tkinter as tk
from tkinter import messagebox

BASE_URL = "http://quotes.toscrape.com"

class QuoteGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quote Guessing Game")

        self.quotes = self.read_quotes("quotes.csv")

        self.label = tk.Label(root, text="Welcome to the Quote Guessing Game!")
        self.label.pack()

        self.start_button = tk.Button(root, text="Start Game", command=self.start_game)
        self.start_button.pack()

        self.quit_button = tk.Button(root, text="Quit", command=root.quit)
        self.quit_button.pack()

    def read_quotes(self, filename):
        with open(filename, "r") as file:
            csv_reader = DictReader(file)
            return list(csv_reader)

    def start_game(self):
        self.quote = choice(self.quotes)
        self.remaining_guesses = 4

        self.label.config(text="\nHere's a quote:\n" + self.quote["text"])

        self.guess_entry = tk.Entry(self.root)
        self.guess_entry.pack()

        self.submit_button = tk.Button(self.root, text="Submit Guess", command=self.check_guess)
        self.submit_button.pack()

    def check_guess(self):
        guess = self.guess_entry.get().strip()
        if guess.lower() == self.quote["author"].lower():
            messagebox.showinfo("Result", "CORRECT!!!")
        else:
            self.remaining_guesses -= 1
            if self.remaining_guesses == 0:
                messagebox.showinfo("Result", f"Sorry, you ran out of guesses.\nThe answer was {self.quote['author']}")
            else:
                hint = self.get_hint()
                messagebox.showinfo("Hint", hint)

    def get_hint(self):
        if self.remaining_guesses == 3:
            res = requests.get(f"{BASE_URL}{self.quote['bio-link']}")
            soup = BeautifulSoup(res.text, "html.parser")
            birth_date = soup.find(class_="author-born-date").get_text()
            birth_place = soup.find(class_="author-born-location").get_text()
            return f"Here's a hint: The author was born on {birth_date} {birth_place}"
        elif self.remaining_guesses == 2:
            first_initial = self.quote["author"][0]
            return f"Here's a hint: The author's first name starts with {first_initial}"
        elif self.remaining_guesses == 1:
            last_initial = self.quote["author"].split()[1][0]
            return f"Here's a hint: The author's last name starts with {last_initial}"

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGameApp(root)
    root.mainloop()
