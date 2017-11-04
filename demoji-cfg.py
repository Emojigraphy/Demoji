from nltk.parse.generate import generate
from nltk import CFG
import itertools

# N
# V
# A
# S

l = [{'N': []}, {'V':[]}, {'A': []}]
perm = {1: ['N'], 2:['AN', 'NV'], 3:['ANV', 'NVS'], 4: ['ANVS']}

grammar = """ 
S -> NP VP 
NP -> Det AP 
Det -> 'The' 
AP -> ADJ N 
ADJ -> 'sad' 
N -> 'dog' 
VP -> V ADV 
V -> 'ran'
ADV -> 'sadly'
"""

def gen(l):
    strs = []
    while(len(l)>= 4):
        strs += gen_clause(l[:4])
        l = l[4:]
    strs += gen_clause(l)

    return find_best(strs)

def build_cfg_strings(dict):
    pass

def gen_clause(l):
    ret = []
    local_grammar = grammar
    cfg_values = {}
    for pos_string in perm[len(l)]:
        a = []
        for emoji_index in range(len(pos_string)):
            # l[emoji_index] is emoji dict, pos_string[emoji_index] is the desired POS for that emoji.
            a.append(l[emoji_index][pos_string[emoji_index]])
        pos_perms = list(itertools.product(*a))
        cfg_values[pos_string] = pos_perms
    return build_cfg_strings(cfg_values)


for sentence in generate(CFG.fromstring(grammar), n=100): 
    print(' '.join(sentence)) 
