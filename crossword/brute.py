#!/usr/bin/python3
import re
import time
words = [w.strip().lower() for w in file('words')]

for i in range(10):
    for pattern in ('..', '.as..', '.a..e'):
        start_time = time.time()
        p = re.compile('^' + pattern + '$')
        matches = []
        for word in words:
            if p.match(word):
                matches.append(word)
        duration = time.time() - start_time
        print("{}: {} matches ({}s)".format(pattern, len(matches), duration))
