import sys
import math
import random

# init lists
lines = []
words = []
words_filtered = []
consecutives = []

# make the markov chains
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
            if wordct + 1 < len(corpus):
                consecutives[word_index].append(corpus[wordct + 1])
        wordct = wordct + 1

sub = sys.argv[1]
f = open(sub, 'r')
text = f.read().split(' ')
for word in text:
    temp = word.split('\n')
    for thing in temp:
        words.append(thing)

# make the chains
create_chains(words)

# init the sentences
# currently more 'ten commandments' than 'words of wisdom' but that can change
sentence_rand = []
sentence = ['Thou','shalt']
consec_word = ""
start_rand = int(math.floor(random.random() * len(words_filtered)))
if 'not' in words_filtered:
    start = words_filtered.index('not')
else:
    start = words_filtered.index('Not')
sentence.append(words_filtered[start])

# tries very hard to generate a full sentence
# still gotta fix some of the special characters that come up
while "." not in consec_word:
    consec_index = int(math.floor(random.random() * len(consecutives[start])))
    consec_word = consecutives[start][consec_index]
    sentence.append(consec_word)
    start = words_filtered.index(consec_word)

print " ".join(sentence)
f.close()
