#!/usr/bin/python3
import os
import random
import logging
from .puzzle import Puzzle
from .lexicon import Lists
from . import utils

logger = logging.getLogger(__name__)

class Unable(Exception):
    pass

class Builder(object):
    def __init__(self, watch=False, progress=False, prefilled=tuple()):
        self.tries = 0
        self.watch = watch
        self.progress = progress
        self.prefilled = [word.upper() for word in prefilled]
        # If we're watching the builder, only log errors.
        # This assumes the logging is done to stdout/stderr, and the show function
        # constantly clears the screen, so logging is A) useless and B) ruins this crude animation.
        if self.watch:
            logger.setLevel(logging.ERROR)

    def build_puzzle(self, template, word_file=None):
        if word_file is None:
            word_file = 'words/multi'

        self.puzzle = Puzzle(template)
        self.lexicon = Lists(open(word_file))

        # Prefill any provided words.
        for word in self.prefilled:
            answers = [a for a in self.puzzle.answers if len(a) == len(word) and not a.locked]
            if answers:
                random.shuffle(answers)
                for answer in answers:
                    if answer.fits(word):
                        answer.fill(word)
                        answer.puzzle.words.add(word)
                        answer.locked = True
                        break

        logging.info("Attempting to build {}x{} puzzle.".format(self.puzzle.width, self.puzzle.height))
        logging.info("Using lexicon {}.".format(self.lexicon))

        self.solve(self.puzzle.answers[0], stack=set())
        return self.puzzle

    def solve(self, answer, stack, depth=0):
        puzzle = self.puzzle
        if answer in stack: return
        if answer.crossed: return

        # Create a copy of the stack so far.
        # TODO: We should be able to reuse this stack, if we're good about popping
        # answers off it when this function returns.
        stack = stack.union(set([answer]))

        for cross in answer.crosses:
            cross.crossed = False
        original = answer.word
        if answer.locked:
            options = [original]
        else:
            options = self.lexicon.find(original)
        if not options:
            raise Unable

        random.shuffle(options)
        for option in options:
            if option in puzzle.words:
                continue
            answer.fill(option)
            self.tries += 1
            # Show progress, if requested:
            if self.progress and self.tries and (self.tries % 100000) == 0:
                logger.info("Tried {} words so far.".format(self.tries))
                print(puzzle)

            puzzle.words.add(option)
            if self.watch:
                self.show()
            # Make a shallow pass of all crosses to see if any are suddenly impossible.
            # This prevents wasting a ton of time decending into cross 1 if cross 6 won't work anyway.
            cross_options = []
            for cross in answer.crosses:
                if cross.locked: count = 1
                else: count = len(self.lexicon.find(cross.word))
                cross_options.append((count, cross))
            if any(s == 0 for s,c in cross_options):
                puzzle.words.remove(option)
                continue
            # If all the crosses are at least possible, recurse into each, in order.
            for cross in answer.crosses:
                try:
                    self.solve(cross, stack, depth=depth + 1)
                except Unable:
                    try:
                        puzzle.words.remove(option)
                    except KeyError:
                        pass
                    break
            else:
                answer.crossed = True
                return True
        try:
            puzzle.words.remove(option)
        except KeyError:
            pass
        answer.fill(original)
        raise Unable

    def show(self):
        os.system('clear')
        print(self.puzzle)
