#!/usr/bin/python3
"""
Build a random, solved crossword puzzle.
"""
import random
import logging
import argparse
import sys
import glob
from crossword.builder import Builder, Unable
from crossword import utils


# Wrangle some convenient command-line arguments.
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--watch', action='store_true', help="Watch the build process.  This involves a huge amount of printing and clearing.  Watching slows building down a LOT.")
parser.add_argument('--progress', action='store_true', help="Show the progress of the builder periodically.")
parser.add_argument('--debug', action='store_true', help="Show debug messages. There will be many.")
parser.add_argument('--use', action='append', default=[], help="Specify a word to use in the puzzle.  Can used multiple times.")
parser.add_argument('--size', type=int, help="The size of the puzzle (height or width-- they're square).", required=None)

args = parser.parse_args()

# Set up logging.
level = logging.INFO
if args.debug:
    level = logging.DEBUG

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=level)
logger = logging.getLogger(__name__)

# Load a random template of the correct size.
matching_templates = utils.load_templates(size=args.size)
if not matching_templates:
    sys.stderr.write("No templates for size {}.\n".format(args.size))
    sys.exit(-1)
template = random.choice(matching_templates)

# Instantiate the builder, passing in appropriate arguments from the command-line.
builder = Builder(
    progress=args.progress,
    watch=args.watch,
    prefilled=args.use,
    )

# Try to actually build a puzzle.  The builder will raise the Unable error if it can't be done.
try:
    puzzle = builder.build_puzzle(template)
except Unable:
    sys.stderr.write("Unable to build a puzzle with these params. Tried {} words.\n".format(builder.tries))
    sys.exit(-1)
    
print(puzzle)
