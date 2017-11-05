from nltk.parse.generate import generate
from nltk import CFG
import itertools
import random
import demoji_app.emojipaths as ep

perm = {1: ['n'], 2: ['an', 'nv'], 3:['anv', 'nvr'], 4: ['anvr']}

grammar = """
Se -> NP VP
NP -> Det AP
Det -> 'the'
AP -> a n 
VP -> v r
"""

preps = [' with ', ' among ', ' for ', ' amidst ', ' by ', ' beside ']
conjs = [', and ', ', but ']
verb_endings = {'h', 's'}

class WordCounts:
    def __init__(self):
        self.and_count = 0

def gen(l):
    sequences = []

    while len(l) > 2:
        sequences += [gen_clause(l[:2])]
        l = l[2:]

    if len(l) > 0:
        sequences += [gen_clause(l)]

    print(sequences)
    generated_strs = build_cfg_strings(sequences)
    return clause_perms(generated_strs)


def cleanup_word(word, pos):
    word = word.replace("'", "") if "'" in word else word
    if pos is 'v':
        if word[-1:] in verb_endings:
            word += 'es'
        else:
            word += 's'
    return word


def build_cfg_strings(sequences):
    seq_list = []
    for seq in sequences:
        for key in seq.keys():
            emoji_seq = []
            for tuple in seq[key]:
                local_grammar = grammar
                used_pos = {'n', 'a', 'v', 'r'}
                for index, word in enumerate(tuple):
                    word = cleanup_word(word, key[index])
                    local_grammar += "{} -> '{}'\n".format(key[index], word)
                    used_pos.remove(key[index])
                for k in used_pos:
                    local_grammar += "{} -> ' '\n".format(k)
                for s in generate(CFG.fromstring(local_grammar), n=100000):
                    sentence = ' '.join(s)
                    if len(sentence) > 0:
                        emoji_seq.append((key, sentence))
            if len(emoji_seq) > 0:
                seq_list.append(emoji_seq)
    return seq_list

def clause_perms(clauses):
    # clauses is a list of tuples in the following format:
    # (<POS_string>, clause)
    # The POS_string determines how I will connect the clauses.
    # Since all clauses are 4 to start (if there is more than 1), NV + N or NP + NP.
    # RETURN: A list of strings
    ret = [""]
    word_counts = WordCounts()
    for clause_perms in clauses:
        new_ret = []
        for perm in clause_perms:
            new_ret += [combine_clauses(start_clause, perm, word_counts) for start_clause in ret]
        ret = new_ret
    return ret

def combine_clauses(clause, tup2, word_counts):
    # Tups are (<POS_string>, clause).
    # tup1 is guarenteed to either have a NV structure or be empty,
    # tup2 could be either another NV or jut a N.
    ret = clause
    new_clause = tup2[1]
    verb = ('v' in tup2[0])
    if ret is "":
        # This is our first clause.
        ret += new_clause
    elif not verb:
        # We're given a N phrase after NP.
        ret += random.choice(preps) + new_clause
    else:
        # We're given a NP to add onto NP.
        if word_counts.and_count == 1:
            ret += '. ' + new_clause[0].upper() + new_clause[1:]
            word_counts.and_count = 0
        else:
            ret += random.choice(conjs) + new_clause
            word_counts.and_count += 1
    return ret


def gen_clause(l):
    # Returns CFG strings for all possible permutations.

    # At a pos_string in cfg_values, there exists a list of lists of words in that POS_String order.
    # Example output:
    # {"NV": [['dog', 'run'], ['pet', 'exercise']]}
    cfg_values = {}
    for pos_string in perm[len(l)]:
        # a is a list of lists of possible words per POS. this will be turned into a permutation lists.
        a = []
        for emoji_index in range(len(pos_string)):
            pos = pos_string[emoji_index]
            if pos not in l[emoji_index]:
                l[emoji_index][pos] = []
            a.append(l[emoji_index][pos_string[emoji_index]])
        pos_perms = list(itertools.product(*a))
        cfg_values[pos_string] = pos_perms
    return cfg_values


def format_sentence(l):
    if len(l) == 0:
        return ""
    ret = l[0][0].upper() + l[0][1:].lower()
    for word in l[1:]:
        if word is ',' or word is '.':
            ret += word
        else:
            ret += " " + word
    ret += "."
    return ret


def get_sentence(emoji_str):
    l = ep.translate_emoji_string(emoji_str)
    for x in l:
        if len(x) == 0:
            l.remove(x)
        else:
            for key in x.keys():
                x[key] = [x[key][0]]

    ret = gen(l)[0].split()
    return format_sentence(ret)
