import codecs
import numpy


def load_lines(path):
    return [l.strip() for l in list(codecs.open(path, "r", encoding='utf8', errors='replace').readlines())]


def load_vocabulary(path_vocab, path_forbidden=None):
    vocab_dict = {}
    vocab_list = [x.split()[0] for x in load_lines(path_vocab)]
    for w in vocab_list:
        if w.lower() not in vocab_dict:
            vocab_dict[w.lower()] = len(vocab_dict)
    if path_forbidden:
        forbidden = load_lines(path_forbidden)
        vocab_dict = {k: v for k, v in vocab_dict.items() if k not in forbidden}
    return vocab_dict


def get_from_distribution(dist):
    r = numpy.random.rand()
    sum = 0
    for i in range(len(dist)):
        sum += dist[i]
        if r < sum:
            return i
    return -1
