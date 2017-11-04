from nltk.corpus import wordnet
import json
#
def transform():
    emoji_to_forms = {}
    with open('data/data.json', encoding='utf8') as f:
        emojis = json.load(f)
    for e in emojis:
        e_map = {}
        hs = {}
        if 'tags' in e and e['tags']:
            tags_synsets = {}
            tags_lemmas = []
            for t in e['tags']:
                if wordnet.synsets(t):
                    tags_synsets[t] = wordnet.synsets(t)
            if not tags_synsets:
                continue
            for i in range(max([len(synlist) for synlist in tags_synsets.values()])):
                for synset in tags_synsets.values():
                    if len(synset) > i and synset[i].lemmas():
                        tags_lemmas.append(synset[i].lemmas())
            for i in range(max([len(lemmas) for lemmas in tags_lemmas])):
                for lemmalist in tags_lemmas:
                    if len(lemmalist) > i:
                        form = ' '.join(lemmalist[i].name().split('_'))
                        pos = lemmalist[i].synset().pos()
                        if pos == 's':
                            pos = 'a'
                        h = form + pos
                        if h not in hs:
                            if pos in e_map:
                                e_map[pos].append(form)
                            else:
                                e_map[pos] = [form]
                            hs[h] = True

        emoji_to_forms[e['emoji']] = e_map
    with open('data/emoji_to_words.json', 'w', encoding='utf8') as f:
        json.dump(emoji_to_forms, f, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    return emoji_to_forms

def translate_emoji_string(e_string):
    with open('data/emoji_to_words.json', mode='r', encoding='utf8') as emoji_map_file:
        emoji_map = json.load(emoji_map_file)
    output_list = []
    for e in e_string:
        # print(e)
        output_list.append(emoji_map[e])
    return output_list
    