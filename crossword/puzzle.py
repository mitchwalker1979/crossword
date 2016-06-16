#!/usr/bin/python3
import re
from . import utils
from .constants import *

class Space(object):
    letter = None
    blocked = None
    coordinates = None
    def __init__(self, coordinates, letter, blocked):
        self.coordinates = coordinates
        self.letter = letter
        self.blocked = blocked

    def __str__(self):
        return "{}({}, letter={}, blocked={})".format(
            self.__class__.__name__,
            self.coordinates,
            self.letter,
            self.blocked,
            )

class Answer(object):
    def __init__(self, puzzle, direction, spaces):
        self.puzzle = puzzle
        self.direction = direction
        self.spaces = spaces
        self.locked = False
        self.crosses = []
        self.crossed = False
        self.n = None

    def fill(self, word):
        for letter, space in zip(word, self.spaces):
            space.letter = letter

    def fits(self, word):
        """
        Check if the given word can fit into the answer as it's currently filled out.
        """
        if len(self) != len(word):
            return False
        for there, proposed in zip(self.word, word):
            if there == EMPTY:
                continue
            if proposed != there:
                return False
        return True

    def clear(self):
        for space in self.spaces:
            space.letter = EMPTY

    @property
    def word(self):
        return ''.join(s.letter for s in self.spaces)

    @property
    def complete(self):
        return not EMPTY in self.word
            
    @property
    def start(self):
        return self.spaces[0]

    def __len__(self):
        return len(self.spaces)

    def __str__(self):
        return "{}({} {}, {}, len={}, word='{}')".format(
            self.__class__.__name__,
            self.n,
            self.direction == ACROSS and 'Across' or 'Down',
            self.start,
            len(self),
            self.word,
            )

class Puzzle(object):
    spaces = None
    answers = None

    @classmethod
    def load(cls, source):
        """
        Create a Puzzle object from a marshalled grid.
        """
        grid = []
        for line in source:
            # Discard any characters that aren't a capital letter or the EMPTY or BLOCKED characters.
            line = re.sub('[^A-Z{}{}]'.format(BLOCKED, EMPTY), '', line)
            if line:
                grid.append(line)
        return cls(grid)

    def __init__(self, grid):
        self.spaces = self.create_spaces(grid)
        self.answers = self.create_answers()
        self.words = set()

    def create_spaces(self, grid):
        """
        Create spaces struct to house the spaces in the puzzle grid (including blocked spaces).
        """
        spaces = []
        for y, row in enumerate(grid):
            spaces.append([])
            for x, value in enumerate(row):
                space = Space((x,y), blocked=value==BLOCKED, letter=value)
                spaces[y].append(space)

        self.width = len(spaces[0])
        self.height = len(spaces)
        return spaces

    def create_answers(self):
        """
        Create the answers struct based on the puzzle grid.
        NOTE: This doesn't populate the answer words.
        """
        answers = []
        # Scan each column and look for DOWN answers.
        answer = None
        for x in range(self.width):
            blocked = True
            for y in range(self.height):
                space = self.spaces[y][x]
                if blocked:
                    if space.blocked:
                        continue
                    else:
                        # First non-blocked space after a block.  New answer.
                        answer = Answer(self,
                            direction=DOWN,
                            spaces=[space],
                            )
                        answers.append(answer)
                        blocked = False
                else:
                    if space.blocked:
                        blocked = True
                    else:
                        # Continuation of the current answer.
                        answer.spaces.append(space)
        # Scan each row and look for ACROSS answers.
        answer = None
        for y in range(self.height):
            blocked = True
            for x in range(self.width):
                space = self.spaces[y][x]
                if blocked:
                    if space.blocked:
                        continue
                    else:
                        # First non-blocked space after a block.  New answer.
                        answer = Answer(self,
                            direction=ACROSS,
                            spaces=[space],
                            )
                        answers.append(answer)
                        blocked = False
                else:
                    if space.blocked:
                        blocked = True
                    else:
                        # Continuation of the current answer.
                        answer.spaces.append(space)
        # Number answers.
        answers.sort(key=lambda a: (a.start.coordinates[1], a.start.coordinates[0]))
        last_start = None
        n = 0
        for answer in answers:
            if answer.start != last_start:
                n += 1
            answer.n = n
            last_start = answer.start

        # Populate Answer crosses.
        # TODO: Smart way to do this? AKA Yo, Dawg, I herd you like for loops.
        for answer in answers:
            for other in answers:
                if other is answer: continue
                for space in answer.spaces:
                    if space in other.spaces:
                        answer.crosses.append(other)
            answer.crosses.sort(key=lambda c: len(c))

        return answers

    def __str__(self):
        grid = ''
        for row in self.spaces:
            grid += ' '.join(space.letter for space in row) + '\n'
        return grid

if __name__ == '__main__':
    puzzle = Puzzle(154)
    print(puzzle)
