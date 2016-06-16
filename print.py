#!/usr/bin/python3
import sys
from crossword.constants import *
from crossword.puzzle import Puzzle
from PIL import Image, ImageDraw, ImageFont

DPI = 100
LINE_WIDTH = 2
LINE_COLOR = (0,0,0)
BOLD_COLOR = (0,0,0)
CHAR_COLOR = (0x60,0x60,0x60)
LABEL_COLOR = (0, 0, 0)
UNIT = DPI + LINE_WIDTH
FONT = '/usr/share/fonts/TTF/UbuntuMono-B.ttf'
FONT = '/usr/share/fonts/TTF/DroidSansMono.ttf'
FONT_SIZE = 100
LABEL_FONT_SIZE = 36

puzzle = Puzzle.load(open(sys.argv[1]))

width = puzzle.width * UNIT
height = puzzle.height * UNIT

font = ImageFont.truetype(FONT, FONT_SIZE)
label_font = ImageFont.truetype(FONT, LABEL_FONT_SIZE)

i = Image.new("RGB", (width + 2, height + 2), (0xff, 0xff, 0xff))
d = ImageDraw.Draw(i)

# Draw lines.
for c in range(puzzle.width + 1):
    x = c * UNIT
    xx = x
    y = 0
    yy = height
    d.line(((x, y), (xx, yy)), fill=LINE_COLOR, width=LINE_WIDTH)
for r in range(puzzle.height + 1):
    y = r * UNIT
    yy = y
    x = 0
    xx = width
    d.line(((x, y), (xx, yy)), fill=LINE_COLOR, width=LINE_WIDTH)

# Fill out spaces.
for row in puzzle.spaces:
    for space in row:
        (c, r) = space.coordinates
        x = c * UNIT
        y = r * UNIT
        if space.blocked:
            rect = ((x, y), (x+UNIT, y), (x+UNIT, y+UNIT), (x, y+UNIT))
            d.polygon(rect, fill=LINE_COLOR)
        else:
            d.text((x + 20,y), space.letter, font=font, fill=CHAR_COLOR)

# Add answer numbers to start spaces.
for answer in puzzle.answers:
    space = answer.start
    (c, r) = space.coordinates
    x = c * UNIT
    y = r * UNIT
    d.text((x + 10, y), str(answer.n), font=label_font, fill=LABEL_COLOR)

i.save('puzzle.jpg')
