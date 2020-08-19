from random import choice


def generate(seed, length, n_order, markov_chain):
    text = seed
    key_list = list(markov_chain.keys())

    def try_key(key):
        if key not in markov_chain.keys():
            key = choice(key_list)
        return key

    new_key = seed[-n_order:]

    for i in range(length):
        # seed may be ignored
        key = try_key(new_key)

        new_key = choice([item for item in markov_chain[key] if item != key])  # avoids repetition

        text += new_key
    return text


def markov_node_merge(markov_chain, tol=0.95):
    # If a node usually leads to the same node (probability > tol), then merge nodes

    key_list = list(markov_chain.keys())
    for i in range(len(key_list) - 1, -1, -1):
        children = markov_chain[key_list[i]]
        for child in set(children):
            if children.count(child) > len(children) * tol:
                # then the key (almost) always leads to the same other key

                # merging keys
                new_key = key_list[i] + child
                # making out-going connections
                new_connections = markov_chain[child]
                # creating merged node
                markov_chain.update({new_key: new_connections})
                # deleting old node
                deleted_key = key_list[i]
                del (key_list[i])
                del (markov_chain[deleted_key])

                for keys in key_list:                      # for each remaining key
                    if deleted_key in markov_chain[keys]:  # if it is found being used in the dict
                        aux = markov_chain[keys]
                        for i, item in enumerate(aux):
                            if item == deleted_key:
                                aux[i] = new_key            # replace it
                        markov_chain[keys] = aux            # and update the dict


def markov_simplify(markovChain, tol=0.95):
    # Removes redundancy by joining nodes according to tol (see markov_node_merge)
    chain_len = len(markovChain)
    markov_node_merge(markovChain, tol)
    new_len = len(markovChain)

    while chain_len != new_len:
        chain_len = new_len
        markov_node_merge(markovChain, tol)
        new_len = len(markovChain)
