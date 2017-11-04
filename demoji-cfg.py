from nltk.parse.generate import generate
from nltk import CFG
import itertools

# N
# V
# A
# S

l = [{'N': ['boy', 'man', 'person'], 'V': ['boyed', 'made'], 'A': ['boyish', 'manly', 'masculine'], 'S': ['manly']},
{'N': ['dog', 'pet', 'friend'], 'V': ['dogly'], 'A': ['doggy'], 'S': ['doggly']},
{'N': ['runner'], 'V': ['run', 'exercise'], 'A': ['athletic'], 'S': ['athletically']},
{'N': [], 'V': [], 'A': ['strange'], 'S': ['quickly', 'speedily', 'hastily']},
{'N': ['cat'], 'V': [], 'A': [''], 'S': ['', '', '']},
     ]
perm = {1: ['N'], 2: ['AN', 'NV'], 3:['ANV', 'NVS'], 4: ['ANVS']}

grammar = """
Se -> NP VP
NP -> Det AP
Det -> 'The'
AP -> A N
VP -> V S
"""

# combine_grammar = """
# Se -> ANVS N
# NP -> 'with' N
# """

def gen(l):
    sequences = []
    # 1. list of gen_clause returns.
    # 2. Convert that list of dictionaries into cfg_strings. (each entry in the list will be a different clause)
    # 3. Run those cfg_strings through the tree to create clause strings.
    # 4. Combine clause strings to create sentences. 
    # 5. Judge the sentences.
    strs = []
    while(len(l)>= 4):
        sequences += [gen_clause(l[:4])]
        l = l[4:]

    if len(l) > 0:
        sequences += [gen_clause(l)]

    generated_strs = build_cfg_strings(sequences)
    return generated_strs

def build_cfg_strings(sequences):
    seq_list = []
    for seq in sequences:
        key = list(seq.keys())[0]
        emoji_seq = []
        for tuple in seq[key]:
            local_grammar = grammar
            used_pos = {'N', 'A', 'V', 'S'}
            for index, word in enumerate(tuple):
                local_grammar += "{} -> '{}'\n".format(key[index], word)
                used_pos.remove(key[index])
            for k in used_pos:
                local_grammar += "{} -> ' '\n".format(k)
            sentence = ""
            for s in generate(CFG.fromstring(local_grammar), n=len(seq)):
                sentence = ' '.join(s)
            if len(sentence) > 0:
                emoji_seq.append((key, sentence))
        seq_list.append(emoji_seq)
    return seq_list


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
            a.append(l[emoji_index][pos_string[emoji_index]])
        pos_perms = list(itertools.product(*a))
        cfg_values[pos_string] = pos_perms
    # return build_cfg_strings(cfg_values)
    return cfg_values


#print(gen(l))
gen(l)
#for sentence in generate(CFG.fromstring(grammar), n=100):
#    print(' '.join(sentence))
