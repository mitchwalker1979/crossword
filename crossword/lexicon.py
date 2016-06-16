#!/usr/bin/python3
import logging
from collections import defaultdict
logger = logging.getLogger(__name__)

WILDCARD = ' '
FREQUENCY = {
    'A': 8.167,
    'B': 1.492,
    'C': 2.782,
    'D': 4.253,
    'E': 12.70,
    'F': 2.228,
    'G': 2.015,
    'H': 6.094,
    'I': 6.966,
    'J': 0.153,
    'K': 0.772,
    'L': 4.025,
    'M': 2.406,
    'N': 6.749,
    'O': 7.507,
    'P': 1.929,
    'Q': 0.095,
    'R': 5.987,
    'S': 6.327,
    'T': 9.056,
    'U': 2.758,
    'V': 0.978,
    'W': 2.361,
    'X': 0.150,
    'Y': 1.974,
    'Z': 0.074,
}

class Node(object):
    def __init__(self, letter, depth):
        self.letter = letter
        self.depth = depth
        self.word = None
        self.children = []

class Tree(object):
    def __init__(self, source):
        self.root = Node(None, 0)
        self.load(source)

    def load(self, source):
        node_count = 0
        for word in source:
            word = word.strip().lower()
            node = self.root
            for depth, letter in enumerate(word):
                next_node = None
                for child in node.children:
                    if child.letter == letter:
                        next_node = child
                if next_node is None:
                    next_node = Node(letter, depth)
                    node_count += 1
                    node.children.append(next_node)

                node = next_node
            node.word = word
        logger.info("Created {} nodes.".format(node_count))

    def find(self, pattern):
        nodes = [self.root]
        for depth, letter in enumerate(pattern):
            new_nodes = []
            for node in nodes:
                if letter == WILDCARD:
                    new_nodes.extend(node.children)
                else:
                    for child in node.children:
                        if child.letter == letter:
                            new_nodes.append(child)
            #logger.debug("{}: {}: {} nodes {}.".format(depth, letter, len(new_nodes), [n.letter for n in new_nodes]))
            nodes = new_nodes
        words = []
        for node in nodes:
            if node.word:
                words.append(node.word)
        return words

class Lists(object):
    """
    Organize corpus into structure of:
        { letter: { position: { matching_words }, ... }, ...}
    Searching then requires starting with the full set of n-letter words, then
    taking successive intersections for the sets matching the provided letters at their given position.
    """
    
    def __init__(self, source):
        self.word_count = 0
        self.load(source)
        self.cache = {}

    def load(self, source):
        self.word_count = 0
        self.corpus = defaultdict(lambda: defaultdict(lambda: set()))
        self.all_by_length = defaultdict(lambda: set())

        for word in source:
            word = word.strip().upper()
            self.all_by_length[len(word)].add(word)
            for position, letter in enumerate(word):
                self.corpus[letter][position].add(word)
            self.word_count += 1

    def find(self, pattern):
        if pattern not in self.cache:
            words = self.all_by_length.get(len(pattern), set())
            for position, letter in enumerate(pattern):
                if letter == WILDCARD: continue
                matches = self.corpus.get(letter, {}).get(position)
                if not matches:
                    words = []
                    break
                else:
                    words = words.intersection(matches)
            self.cache[pattern] = list(words)
        return self.cache[pattern]

    def __str__(self):
        return '{}(word_count={})'.format(self.__class__.__name__, self.word_count)

if __name__ == '__main__':
    import time
    TEST_PATTERNS = ('  ', ' AT', ' AS  ', ' A  E', '         T', 'WIL CARD')
    lex = Lists(open('words'))
    for i in range(10):
        for pattern in TEST_PATTERNS:
            start_time = time.time()
            words = lex.find(pattern)
            duration = time.time() - start_time

            print("{}: {} {} ({}s)".format(pattern, len(words), words[:5], duration))

