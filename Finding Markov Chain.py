from TextGenerator import generate
from MarkovHelper import markov_simplify
import os
import json

# This script:
# 1. Loads a pre-processed file (see Text Filter)
# 2. Generates the Markov Chain as a dict
#       2.1. Simplifies the chain merging nodes
# 3. Saves the dict as a text file

# Length of text segments:
order = 3  # These are not a proper n-grams, as I do not split using whitespace
# Content to use:
filtered = "mineral"
current_path = os.path.abspath("")
abspath = current_path + "/" + filtered + " filtered.txt"

f = open(abspath, "r")
txt = f.read()

listed = [txt[i:i + order] for i in range(0, len(txt), order)]
if len(listed[-1]) < order:
    listed.remove(listed[-1])

grams = [listed[0]]
connections = [[listed[1]]]
occurrences = [1]
for i in range(1, len(listed) - 1):
    if listed[i] in grams:
        print(round(99 * i / (len(listed) - 1)), '%')
        for j, gram in enumerate(grams):
            if listed[i] == gram:
                connections[j].append(listed[i + 1])
                occurrences[j] += 1
    else:
        grams.append(listed[i])
        connections.append([listed[i + 1]])
        occurrences.append(1)
print('100 %')

# Erasing rare connections (this is not suitable for every application, but it is useful for me)
threshold = 1
for i in range(len(grams) - 1, -1, -1):
    if occurrences[i] <= threshold:
        del (occurrences[i])
        del (connections[i])
        del (grams[i])

markovChain = dict(zip(grams, connections))

# this is absolutely unecessary, but it merges nodes making the dict cleaner and the generation slightly faster
markov_simplify(markovChain)

# Example of generated text:
generated_text_sample = generate(3, markovChain)
print(generated_text_sample)

with open(current_path + '/' + filtered + ' dict storage.txt', 'w') as outfile:
    json.dump(markovChain, outfile)
