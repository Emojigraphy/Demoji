from nltk.corpus import wordnet
# from emoji2vec import phrase2vec
from unicode_codes import EMOJI_UNICODE
import json

# def transform():
#     emoji_to_forms = {}
#     with open('data/data.json', encoding='utf8') as f:
#         emojis = json.load(f)
#     for e in emojis:
#         e_map = {}
#         hs = {}
#         if 'tags' in e and e['tags']:
#             tags_synsets = []
#             tags_lemmas = []
#             words_synsets = []
#             words_lemmas = []
#             for w in e['annotation'].split():
#                 if wordnet.synsets(w):
#                     words_synsets.append(wordnet.synsets(w))
#             if not words_synsets:
#                 continue
#             for i in range(max([len(synlist) for synlist in words_synsets])):
#                 for synset in words_synsets:
#                     if len(synset) > i and synset[i].lemmas():
#                         words_lemmas.append(synset[i].lemmas())
#             for i in range(max([len(lemmas) for lemmas in words_lemmas])):
#                 for lemmalist in words_lemmas:
#                     if len(lemmalist) > i:
#                         form = ' '.join(lemmalist[i].name().split('_'))
#                         pos = lemmalist[i].synset().pos()
#                         if pos == 's':
#                             pos = 'a'
#                         h = form + pos
#                         if h not in hs:
#                             if pos in e_map:
#                                 e_map[pos].append(form)
#                             else:
#                                 e_map[pos] = [form]
#                             hs[h] = True
#             for t in e['tags']:
#                 if wordnet.synsets(t):
#                     tags_synsets.append(wordnet.synsets(t))
#             if not tags_synsets:
#                 continue
#             for i in range(max([len(synlist) for synlist in tags_synsets])):
#                 for synset in tags_synsets:
#                     if len(synset) > i and synset[i].lemmas():
#                         tags_lemmas.append(synset[i].lemmas())
#             for i in range(max([len(lemmas) for lemmas in tags_lemmas])):
#                 for lemmalist in tags_lemmas:
#                     if len(lemmalist) > i:
#                         form = ' '.join(lemmalist[i].name().split('_'))
#                         pos = lemmalist[i].synset().pos()
#                         if pos == 's':
#                             pos = 'a'
#                         h = form + pos
#                         if h not in hs:
#                             if pos in e_map:
#                                 e_map[pos].append(form)
#                             else:
#                                 e_map[pos] = [form]
#                             hs[h] = True
#
#         emoji_to_forms[e['emoji']] = e_map
#     with open('data/emoji_to_words.json', 'w', encoding='utf8') as f:
#         json.dump(emoji_to_forms, f, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
#     return emoji_to_forms

def translate_emoji_string(e_string, use_embeddings=True):
    map_file = 'data/new_map.json' if use_embeddings else 'data/emoji_to_words.json'
    with open(map_file, mode='r', encoding='utf8') as emoji_map_file:
        emoji_map = json.load(emoji_map_file)
    output_list = []
    for e in e_string:
        if e in emoji_map:
            output_list.append(emoji_map[e])
    return output_list
    
# def build_map_from_embeddings():
#     model = phrase2vec.Phrase2Vec.from_word2vec_paths(300, 'emoji2vec/GoogleNews-vectors-negative300.bin', 'emoji2vec/pre-trained/emoji2vec.bin')
#     emoji_map = {}
#     total, missed = 0, 0
#     for e in EMOJI_UNICODE.values():
#         total += 1
#         try:
#             emoji_similar = model.from_emoji(model.emojiVecModel[e])
#             emoji_map[e] = [tup[0] for tup in emoji_similar]
#         except KeyError:
#             emoji_map[e] = []
#             missed += 1
#     print("Total emoji: {} Missed: {}".format(total, missed))
#     with open('data/emoji_to_words.json', encoding='utf8') as f:
#         old_map = json.load(f)
#     for e, words in emoji_map.items():
#         if not words and e in old_map:
#             emoji_map[e] = old_map[e]
#         else:
#             pos_map = {}
#             hs = {}
#             synsets = []
#             lemmas = []
#             for word in words:
#                 synsets.append(wordnet.synsets(word))
#             if not synsets:
#                 if e in old_map:
#                     emoji_map[e] = old_map[e]
#                 else:
#                     emoji_map[e] = pos_map
#                 continue
#             for i in range(max([len(synset) for synset in synsets])):
#                 for synset in synsets:
#                     if len(synset) > i:
#                         lemmas.append(synset[i].lemmas())
#             if not lemmas:
#                 if e in old_map:
#                     emoji_map[e] = old_map[e]
#                 else:
#                     emoji_map[e] = pos_map
#                 continue
#             for i in range(max([len(lemmalist) for lemmalist in lemmas])):
#                     for lemmalist in lemmas:
#                         if len(lemmalist) > i:
#                             form = ' '.join(lemmalist[i].name().split('_'))
#                             pos = lemmalist[i].synset().pos()
#                             if pos == 's':
#                                 pos = 'a'
#                             h = form + pos
#                             if h not in hs:
#                                 if pos in pos_map:
#                                     pos_map[pos].append(form)
#                                 else:
#                                     pos_map[pos] = [form]
#                                 hs[h] = True
#             emoji_map[e] = pos_map
#     with open('data/new_map.json', mode='w', encoding='utf8') as f:
#         json.dump(emoji_map, f, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
#
#     return emoji_map