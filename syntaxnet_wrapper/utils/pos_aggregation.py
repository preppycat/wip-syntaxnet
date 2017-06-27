# coding=utf-8


def pos_aggregate(tag_tree):
    """
    function making easier to aggregate pos tagging
    input should come as an array of transform_tag output.
    This allow to aggregate more than one sentence
    """

    tagging = []
    for tagged_sent in tag_tree:
        for value in tagged_sent.values():
            value.pop('index')
            value.pop('pos')  # not the actual pos, specific for each language and does not exist for french in syntaxnet
            tagging.append(value.copy())
    data_tags = count_tags(tagging)

    data_tags['ratio'] = create_ratio(data_tags)

    return data_tags


def count_tags(matches):
    possible_tags = ['adj', 'adp', 'adv', 'aux', 'cconj', 'det', 'intj', 'noun', 'num', 'part', 'pron', 'propn',
                     'punct', 'sconj', 'sym', 'verb', 'x']

    # feature are specification of basic pos
    feature_categories = ['prontype', 'numtype', 'gender', 'animacy', 'number', 'definite', 'degree', 'verbform',
                          'mood', 'tense', 'aspect', 'voice',
                          'evident', 'polarity', 'person', 'polite']

    possible_feature = {
        # http://universaldependencies.org/u/feat/PronType.html
        'prontype': ['art', 'dem', 'emp', 'exc', 'ind', 'int', 'neg', 'prs', 'rcp', 'rel', 'tot'],
        # http://universaldependencies.org/u/feat/NumType.html
        'numtype': ['card', 'dist', 'frac', 'mult', 'ord', 'range', 'sets'],
        # http://universaldependencies.org/u/feat/Gender.html
        'gender': ['com', 'fem', 'masc', 'neut'],
        # http://universaldependencies.org/u/feat/Animacy.html
        'animacy': ['anim', 'hum', 'inan', 'nhum'],
        # http://universaldependencies.org/u/feat/Number.html
        'number': ['coll', 'count', 'dual', 'grpa', 'grpl', 'inv', 'pauc', 'plur', 'ptan', 'sing', 'tri'],
        # http://universaldependencies.org/u/feat/Definite.html
        'definite': ['com', 'cons', 'def', 'ind', 'spec'],
        # http://universaldependencies.org/u/feat/Degree.html
        'degree': ['abs', 'cmp', 'equ', 'pos', 'sup'],
        # http://universaldependencies.org/u/feat/VerbForm.html
        'verbform': ['conv', 'fin', 'gdv', 'ger', 'inf', 'part', 'sup', 'vnoun'],
        # http://universaldependencies.org/u/feat/Mood.html
        'mood': ['adm', 'cnd', 'des', 'imp', 'ind', 'jus', 'nec', 'opt', 'pot', 'prp', 'qot', 'sub'],
        # http://universaldependencies.org/u/feat/Tense.html
        'tense': ['fut', 'imp', 'past', 'pqp', 'pres'],
        # http://universaldependencies.org/u/feat/Aspect.html
        'aspect': ['hab', 'imp', 'iter', 'perf', 'prog', 'prosp'],
        # http://universaldependencies.org/u/feat/Voice.html
        'voice': ['act', 'antip', 'cau', 'dir', 'inv', 'mid', 'pass', 'rcp'],
        # http://universaldependencies.org/u/feat/Evident.html
        'evident': ['fh', 'nfh'],
        # http://universaldependencies.org/u/feat/Polarity.html
        'polarity': ['neg', 'pos'],
        # http://universaldependencies.org/u/feat/Person.html
        'person': ['0', '1', '2', '3', '4'],
        # http://universaldependencies.org/u/feat/Polite.html
        'polite': ['elev', 'form', 'humb', 'infm']
    }
    # The feature Poss, Reflex, Foreign and Abbr are just present, no possible value
    mono_features = ['poss', 'reflex', 'foreign', 'abbr']

    # init dict
    aggr_tag = {}
    aggr_tag['upos'] = {tag: 0 for tag in possible_tags}
    for feature_category in feature_categories:
        aggr_tag[feature_category] = {value: 0 for value in possible_feature[feature_category]}
    for mono_feature in mono_features:
        aggr_tag[mono_feature] = 0

    for token in matches:
        upos = token['label'].lower()
        if upos in aggr_tag['upos'].keys():
            aggr_tag['upos'][upos] += 1

        features = token['feats'].lower().split('|')
        for feature in features:
            feature_splitted = feature.split('=')
            category = feature_splitted[0]
            if category in mono_features:
                if category in aggr_tag:
                    aggr_tag[category] += 1
            elif category in aggr_tag and feature_splitted[1] in aggr_tag[category]:
                aggr_tag[category][feature_splitted[1]] += 1

    return aggr_tag


def create_ratio(tags):
    possible_ratio = ['ratio_adj_verb', 'ratio_adj_adv', 'ratio_adj_propn', 'ratio_adj_pron', 'ratio_adv_det',
                      'ratio_adv_propn', 'ratio_adv_pron', 'ratio_propn_verb', 'ratio_propn_det']

    aggr_ratio = {tag: 0 for tag in possible_ratio}

    for ratio in possible_ratio:
        _, tag1, tag2 = ratio.split('_')
        tag1_complete = [value for tag, value in tags['upos'].items() if tag.startswith(tag1)]
        tag2_complete = [value for tag, value in tags['upos'].items() if tag.startswith(tag2)]
        if sum(tag2_complete) != 0:
            aggr_ratio[ratio] = sum(tag1_complete) / float(sum(tag2_complete))

    return aggr_ratio
