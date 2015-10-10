# TODO implement Markov chains
import sys

lines = []
words = []
words_filtered = []
consecutives = []

def create_chains(corpus):
    global words_filtered
    global consecutives

    wordct = 0
    for word in corpus:
        if word not in words_filtered:
            words_filtered.append(word)
        word_index = words_filtered.index(word)
        if len(consecutives) <= word_index:
            consecutives.append([])
            consecutives[-1].append(corpus[wordct + 1])
        else:
            consecutives[word_index].append(corpus[wordct + 1])
            wordct = wordct + 1

sub = sys.argv[1]
f = open(sub, 'r')
text = f.read().split(' ')
for word in text:
    temp = word.split('\n')
    for thing in temp:
        words.append(thing)

create_chains(words)
print len(words)
print len(words_filtered)
print len(consecutives)
for thing in consecutives:
    if len(thing) > 1:
        print thing

f.close()
