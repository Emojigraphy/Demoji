from nltk.parse.generate import generate
from nltk import CFG
import itertools
import emojipaths as ep

# N
# V
# A
# S

# l = [{'N': ['boy', 'man', 'person'], 'V': [], 'A': ['boyish', 'manly', 'masculine'], 'S': ['manly']},
# {'N': ['dog', 'pet', 'friend'], 'V': ['dogly'], 'A': ['doggy'], 'S': ['doggly']},
# {'N': ['runner'], 'V': ['run', 'exercise'], 'A': ['athletic'], 'S': ['athletically']},
# {'N': [], 'V': [], 'A': ['strange'], 'S': ['quickly', 'speedily', 'hastily']},
# {'N': ['cat'], 'V': [], 'A': [''], 'S': ['', '', '']},
#      ]

# l = [{'n': ['boy']}, {'v':['run']}, {'n':['man']}]

# test_clauses = [[('ANVS', "The boy runs"), ('ANVS', "The man runs"), ('ANVS', "The boy exercises")], [('ANVS',"the kid reads the book"),('ANVS',"the student reads the book"),('ANVS',"the kid reads an article")],
#                 [('N',"the dog"),('N',"the pet"),('N',"the friend")]]
perm = {1: ['n'], 2: ['an', 'nv'], 3:['anv', 'nvr'], 4: ['anvr']}

grammar = """
Se -> NP VP
NP -> Det AP
Det -> 'the'
AP -> a n 
VP -> v r
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
    while(len(l)>= 4):
        sequences += [gen_clause(l[:4])]
        l = l[4:]

    if len(l) > 0:
        sequences += [gen_clause(l)]

    sequences.sort(key=len, reverse=True)
    #print(sequences)
    generated_strs = build_cfg_strings(sequences)
    return clause_perms(generated_strs)

def build_cfg_strings(sequences):
    seq_list = []
    for seq in sequences:
        key = list(seq.keys())[0]
        emoji_seq = []
        for tuple in seq[key]:
            local_grammar = grammar
            used_pos = {'n', 'a', 'v', 'r'}
            for index, word in enumerate(tuple):
                word = word.replace("'", "") if "'" in word else word
                word = word + 's' if key[index] is 'v' else word
                local_grammar += "{} -> '{}'\n".format(key[index], word)
                used_pos.remove(key[index])
            for k in used_pos:
                local_grammar += "{} -> ' '\n".format(k)
            sentence = ""
            for s in generate(CFG.fromstring(local_grammar), n=len(seq)):
                sentence = ' '.join(s)
                if len(sentence) > 0:
                    emoji_seq.append((key, sentence))
            #if len(sentence) > 0:
            #    print(sentence)
            #    emoji_seq.append((key, sentence))
        seq_list.append(emoji_seq)
    return seq_list

def clause_perms(clauses):
    # clauses is a list of tuples in the following format:
    # (<POS_string>, clause)
    # The POS_string determines how I will connect the clauses.
    # Since all clauses are 4 to start (if there is more than 1), NV + N or NP + NP.
    # RETURN: A list of strings
    ret = [""]
    for clause_perms in clauses:
        new_ret = []
        for perm in clause_perms:
            new_ret += [combine_clauses(start_clause, perm) for start_clause in ret]
        ret = new_ret
    return ret

def combine_clauses(clause, tup2):
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
        ret += ' with ' + new_clause
    else:
        # We're given a NP to add onto NP.
        ret += ', and ' + new_clause
    return ret


def gen_clause(l):
    # Returns CFG strings for all possible permutations.

    # At a pos_string in cfg_values, there exists a list of lists of words in that POS_String order.
    # Example output:
    # {"NV": [['dog', 'run'], ['pet', 'exercise']]}
    cfg_values = {} #{'a':[], 'n': [], 'v': [], 'r': []}
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
    # return build_cfg_strings(cfg_values)
    return cfg_values


def format_sentence(l):
    ret = l[0][0].upper() + l[0][1:].lower()
    for word in l[1:]:
        ret += " " + word
    ret += "."
    return ret


#print(gen(l))
#gen(l)
#for sentence in generate(CFG.fromstring(grammar), n=100):
#    print(' '.join(sentence))

emoji_str = "\U0001F4DA\U0001F412\U0001F6F3"
l = ep.translate_emoji_string(emoji_str)
#print(l)
ret = gen(l)[0].split()
print(format_sentence(ret))

