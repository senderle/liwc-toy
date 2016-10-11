from collections import defaultdict
import requests
import re

def loadliwc():
    with open('LIWC_2015.txt') as f:
        lines = f.readlines()
    stems = []
    tags = []
    for l in lines:
        l = l.strip().split()[1:-1]
        tags.append(l.pop())
        stems.append(' '.join(l))

    liwc_map = defaultdict(list)
    for s, t in zip(stems, tags):
        liwc_map[t].append(s)
    return liwc_map

liwc = loadliwc()

def loadgut(id):
    url = 'http://www.gutenberg.org/ebooks/{}.txt.utf-8'.format(id)
    r = requests.get(url)
    return r.text

def liwcify(text, key):
    try:
        text = loadgut(int(text))
    except:
        pass
    words = ' '.join(text.split()).lower()
    for stem in liwc[key]:
        words = re.sub(stem, key, words)
    words = words.split()
    blocks = [words[n:n + 500] for n in range(0, len(words), 500)]
    return [b.count(key) for b in blocks]

