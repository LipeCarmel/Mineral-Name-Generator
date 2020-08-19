import json
import os
from random import choice


def MineralGenerator(n_order=3, min_len=5, post=True):
    filtered = "mineral"
    current_path = os.path.abspath("")

    # Loading dict
    with open(current_path + '/' + filtered + ' dict storage.txt', 'r') as outfile:
        markovChain = json.load(outfile)

    # Loading real data
    abspath = current_path + "/" + filtered + " filtered.txt"
    f = open(abspath, "r")
    txt = f.read()
    real_names = txt.split()

    # Generating
    text = generate(n_order, markovChain)
    gen_names = text.split()

    # Post-processing
    if post:
        # Deleting real words, short words, text between parentheses and words not ending with 'ite'
        for i in range(len(gen_names) - 1, -1, -1):
            if gen_names[i] in real_names or len(gen_names[i]) < min_len:
                del (gen_names[i])
            elif gen_names[i][-3:] != 'ite':
                del (gen_names[i])

        # Retrying if needed
        if len(gen_names) == 0:
            gen_names += MineralGenerator(n_order, min_len, True)
        return gen_names

def generate(n_order, markov_chain, seed='', length=100):
    # This never uses the same key twice, which is a common problem with markov text generation.
    # Although it avoids a node permanently looping to itself, it does limit the generation capabilities,
    # i.e: the word "repetition" would never be generated for n_order=2, as "ti" would not lead to "ti".

    text = seed
    new_key = seed[-n_order:]  # this seed may be ignored if it does not match a key
    key_list = list(markov_chain.keys())

    def try_key(key):
        if key not in markov_chain.keys():
            key = choice(key_list)
        return key

    for i in range(length):
        key = try_key(new_key)
        new_key = choice([item for item in markov_chain[key] if item != key])  # avoids repetition

        text += new_key
    return text


def save_gen(label, gen_list):
    current_path = os.path.abspath("")
    complement = label + " generated list.txt"
    abspath = current_path + "/" + complement

    if complement in os.listdir(current_path):
        # Appends new data to current list
        with open(abspath, 'r') as f:
            current_list = f.readlines()

        for i in gen_list:
            aux = i + '\n'
            if aux not in current_list:
                current_list.append(aux)

        with open(abspath, 'w') as outfile:
            for item in current_list:
                outfile.write(item)
    else:
        # Creates list
        with open(abspath, 'w') as outfile:
            for item in gen_list:
                outfile.write('%s\n' % item)


def save_first_gen(label, gen_list):
    current_path = os.path.abspath("")
    complement = label + " generated list.txt"
    abspath = current_path + "/" + complement

    with open(abspath, 'w') as outfile:
        for item in gen_list:
            outfile.write('%s\n' % item)
