import json
import os


def rem_banned(words):
    out = []
    for word in words:
        stripped_word = word
        for banned in ['\n', ',', '.', '!', '?', '"', '”', '“', '-', '—', ']', '[', ':', ';']:
            stripped_word = stripped_word.replace(banned, '')
        out.append(stripped_word.lower())
    return out


files = os.listdir("./sources/")

data = []
for i in files:
    with open(f"sources/{i}", 'r', errors='ignore') as f:
        data.extend(rem_banned(f.read().split()))

keys = list(set(data))

datadict = dict.fromkeys(keys)

for i in keys:
    datadict[i] = {}

for ind, word in enumerate(data):
    word_data = datadict[word]
    try:
        word_data[data[ind + 1]] += 1
    except KeyError:
        word_data[data[ind + 1]] = 1
    except IndexError:
        pass

print(datadict["glory"])
