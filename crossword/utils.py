#!/usr/bin/python3
import sys
import glob
from PIL import Image
from .constants import *

BLANK_SIZE = 15

def parse_blank(filename, size):
    """
    Produce a template from an image of a blank grid.
    """
    img = Image.open(filename).convert("RGB")
    h,w = img.size
    step = w // size
    grid = []
    for y in range(size // 2, h, step):
        row = []
        for x in range(size // 2, w, step):
            r,g,b = img.getpixel((x,y))
            if r < 0x80:
                row.append(BLOCKED)
            else:
                row.append(EMPTY)
        grid.append(''.join(row))
    return grid

def load_templates(size):
    """
    Load template files for the given grid size and convert them
    to the list of strings expected by the Puzzle constructor.
    """
    filenames = glob.glob('templates/{}.*'.format(size))
    templates = []
    for filename in filenames:
        template = []
        with open(filename) as f:
            for line in f:
                template.append(line.strip('\n'))
        templates.append(template)
    return templates
    
