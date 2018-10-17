﻿import util
import numpy
import random


class Scrabble():
    def __init__(self):
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                        't', 'u', 'v', 'w', 'x', 'y', 'z', 'ü', 'ö', 'ß', 'ä']
        self.load_dict()
        self.compute_transition_probs()
        print("Scrabble initialized.")

    def load_dict(self, path="./vocab/german.dict", path_forbidden=None):
        self.vocabulary = util.load_vocabulary(path, path_forbidden)

    def compute_transition_probs(self):
        self.transitions = numpy.zeros((len(self.letters), len(self.letters)))
        cntr = 0
        for w in self.vocabulary:
            cntr += 1
            for i in range(len(w) - 1):
                if w[i] in self.letters and w[i + 1] in self.letters:
                    self.transitions[self.letters.index(w.lower()[i]), self.letters.index(w.lower()[i + 1])] += 1
        row_sums = self.transitions.sum(axis=1)
        self.transitions = self.transitions / row_sums[:, numpy.newaxis]
        self.priors = row_sums / row_sums.sum()

    def create_board(self, letters_path="./vocab/letters.txt", dim=15):
        self.board_size = dim
        self.board = numpy.full((dim, dim), '-')
        for i in range(self.board_size):
            for j in range(self.board_size):
                if i == 0 and j == 0:
                    self.board[i, j] = self.letters[util.get_from_distribution(self.priors)]
                elif i == 0:
                    self.board[i, j] = self.letters[
                        util.get_from_distribution(self.transitions[self.letters.index(self.board[i, j - 1])])]
                elif j == 0:
                    self.board[i, j] = self.letters[
                        util.get_from_distribution(self.transitions[self.letters.index(self.board[i - 1, j])])]
                else:
                    letter_hor = self.letters[
                        util.get_from_distribution(self.transitions[self.letters.index(self.board[i, j - 1])])]
                    letter_ver = self.letters[
                        util.get_from_distribution(self.transitions[self.letters.index(self.board[i - 1, j])])]
                    if numpy.random.rand() >= 0.5:
                        self.board[i, j] = letter_hor
                    else:
                        self.board[i, j] = letter_ver

    def get_solutions(self, min_len=3, level=0.5):
        sols_hor = self.find_words(horizontal=True, min_len=min_len)
        sols_vert = self.find_words(horizontal=False, min_len=min_len)
        self.allsolutions = sols_hor + sols_vert
        random.shuffle(self.allsolutions)
        self.retsolutions = self.allsolutions[: int(level * len(self.allsolutions))]

    def validate_solutions(self, solutions):
        valid = []
        for s in solutions:
            if len([x for x in self.allsolutions if x[0].lower() == s.lower()]) > 0:
                valid.append(s)
        return valid

    def find_words(self, horizontal=True, min_len=3):
        solutions = []
        for r in range(self.board_size):
            for i in range(self.board_size - min_len + 1):
                for j in range(i + min_len, self.board_size + 1):
                    word = ''.join(self.board[r, i:j] if horizontal else self.board[i:j, r])
                    if word in self.vocabulary:
                        solutions.append((word, 'right' if horizontal else 'down', r, i))
            for i in reversed(range(min_len, self.board_size + 1)):
                for j in reversed(range(i - min_len + 1)):
                    word = ''.join(reversed(self.board[r, j:i]) if horizontal else reversed(self.board[j:i, r]))
                    if word in self.vocabulary:
                        solutions.append((word, 'left' if horizontal else 'up', r, i - 1))
        return solutions


def main():
    scrabble = Scrabble()
    scrabble.load_dict()
    print(len(scrabble.vocabulary))


if __name__ == "__main__":
    main()
