import sys
import math
import random
import glob

# get subreddit
sub = sys.argv[1].lower()

# init lists
lines = []
words = []
words_filtered = []
consecutives = []
filtered_reddits = []
for reddit in glob.glob('*_filtered.txt'):
    filtered_reddits.append(reddit[:-13])

# filter the raw text
def filter_raw(corpus):
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

# make the markov chains
def generate(start):
    global words_filtered
    global consecutives
    sentence = start.split(' ')
    beginning = ''
    consec_word = ''
    start_rand = int(math.floor(random.random() * len(words_filtered)))
    if sentence[-1] in words_filtered:
        start_index = words_filtered.index(sentence[-1])
    elif sentence[-1].upper() in words_filtered:
        start_index = words_filtered.index(sentence[-1].upper())
    else:
        start_index = start_rand
    while '.' not in consec_word and ' ' not in consec_word and '?' not in consec_word and '!' not in consec_word:
        consec_index = int(math.floor(random.random() * len(consecutives[start_index])))
        consec_word = consecutives[start_index][consec_index]
        sentence.append(consec_word)
        start_index = words_filtered.index(consec_word)
    return ' '.join(sentence)

# write filtered text to the approprate files
def write_filtered_to_file():
    global words_filtered
    global consecutives
    w_words = open(sub + '_filtered.txt', 'w')
    w_consec = open(sub + '_consec.txt', 'w')
    for i in range(len(words_filtered)):
        w_words.write(words_filtered[i] + '\n')
        w_consec.write(' '.join(consecutives[i]) + '\n')
    w_words.close()
    w_consec.close()

# read filtered text from the appropriate files
def read_filtered_from_file():
    global words_filtered
    global consecutives
    global sub
    r_words = open(sub + '_filtered.txt', 'r')
    r_consec = open(sub + '_consec.txt', 'r')
    for word in r_words:
        words_filtered.append(word.rstrip())
    for consec in r_consec:
        consecutives.append(consec.split())
    r_words.close()
    r_consec.close()

f = open(sub + '.txt', 'r')
text = f.read().split(' ')
for word in text:
    temp = word.split('\n')
    for clean in temp:
        words.append(clean)

# get the words for the chains
if sub in filtered_reddits:
    read_filtered_from_file()
else:
    filter_raw(words)
    write_filtered_to_file()

# generate from a seed phrase
beginnings = ['Look both ways before you', 'Listen to your', 'Eat your', 'Say no to', 'Don\'t let your dreams be', 'Just do']
beg_index = int(math.floor(len(beginnings) * random.random()))
print generate(beginnings[beg_index])
f.close()
