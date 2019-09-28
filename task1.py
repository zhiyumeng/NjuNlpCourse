# -*- coding: utf-8 -*-
import re

DIC_PATH = 'data/dic_ec.txt'

"""
1. 输入一个单词
2. 如果词典里有该词，输出该词及其属性，转4，否则，转3
3. 如果有该词的还原规则，并且，词典里有还原后的词，则输出还原后的词及其属性，转4，否则，调用<未登录词模块>
4. 如果输入中还有单词，转(1)，否则，结束。
"""


def load_dict(path=DIC_PATH):
    with open(DIC_PATH, 'r', encoding='ansi', errors='replace') as f:
        lines = f.readlines()
    dict = {}
    for line in lines:
        values = line.split('�')
        word = values[0]
        attribute = " ".join(values[1:-1])
        dict[word] = attribute
    return dict


verb_patterns = {
    r's$': [''],  # *s -> * (SINGULAR3)
    r'es$': [''],  # *es -> * (SINGULAR3)
    r'ies$': ['y'],  # *ies -> *y (SINGULAR3)
    r'ing$': ['', 'e'],  # *ing -> * (VING),*ing -> *e (VING)
    r'ying$': ['ie'],  # *ying -> *ie (VING)
    r"(.)(\1)ing$": [r'\1'],  # *??ing -> *? (VING)
    r"ed$": [r'', r'e'],  # *ed -> * (PAST)(VEN),*ed -> *e (PAST)(VEN)
    r'ied$': [r'y'],  # *ied -> *y (PAST)(VEN)
    r"(.)(\1)ed": [r'\1'],  # *??ed -> *? (PAST)(VEN)
}


def lemmatizationViaPatterns(patterns, word):
    for pattern, repls in patterns.items():
        if re.search(pattern, word):
            for repl in repls:
                new_word = re.sub(pattern, repl, word)
                print(word, '->', new_word)
                yield new_word


def noLogin(word):
    print(word, 'is not logged')


def checkWord(dict, word):
    if word in dict:
        print(word, dict[word])
        return True
    else:
        return False


if __name__ == '__main__':
    dict = load_dict(path=DIC_PATH)
    words = ['esgo', 'goies', 'playiied', 'gogging', 'goes', 'played']
    for word in words:
        finded = False
        finded = checkWord(dict, word)
        if not finded:
            for newword in lemmatizationViaPatterns(verb_patterns, word):
                if checkWord(dict, newword):
                    finded = True
                    break
        if not finded:
            noLogin(word)
