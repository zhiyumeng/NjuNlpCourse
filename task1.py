# -*- coding: utf-8 -*-
import re

DIC_PATH = 'data/dic_ec.txt'
IRR_DIC_PATH = 'data/irregular.txt'
"""
1. 输入一个单词
2. 如果词典里有该词，输出该词及其属性，转4，否则，转3
3. 如果有该词的还原规则，并且，词典里有还原后的词，则输出还原后的词及其属性，转4，否则，调用<未登录词模块>
4. 如果输入中还有单词，转(1)，否则，结束。
"""


def load_dict(path=DIC_PATH):
    """加载单词词典"""
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
    """
    定义动词还原的规则
    """
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
    """
    对于输入的单词，为其寻找合适的还原规则并返回还原后的词语
    :param patterns:
    :param word:
    :return:
    """
    for pattern, repls in patterns.items():
        if re.search(pattern, word):
            for repl in repls:
                new_word = re.sub(pattern, repl, word)
                print(word, '->', new_word)
                yield new_word


def loadIrregularVerbs(path='data/irregular.txt'):
    """加载不规则动词词典"""
    with open(path, 'r') as f:
        lines = f.readlines()
    irregular_dict = {}
    for line in lines:
        word, past, pastParticiple, *nothing = line.lower().strip().split(',')
        irregular_dict[past] = word
        irregular_dict[pastParticiple] = word
    return irregular_dict


def ProcessIrregularVerb(irregular_dict, word):
    """返回不规则动词的原形，否则返回None"""
    if word in irregular_dict:
        return irregular_dict[word]
    return None


def noLogin(word):
    """
    未登录模块
    :param word:
    :return:
    """
    print(word, 'is not logged')


def checkWord(dict, irregular_dict, word):
    """
    查看给定的词语及其原型是否存在于词典中
    :param dict:
    :param word:
    :return:
    """
    # 词语是否在词典中
    word = word.lower()
    if word in dict:
        print(word, dict[word])
        return True
    # 词语的动词原形是否在词典中
    for newword in lemmatizationViaPatterns(verb_patterns, word):
        if newword in dict:
            print(newword, dict[newword])
            return True
    init_verb = ProcessIrregularVerb(irregular_dict, word)
    if init_verb and init_verb in dict:
        print(init_verb, dict[init_verb])
        return True

    return False


if __name__ == '__main__':
    dict = load_dict(path=DIC_PATH)
    irregular_dict = loadIrregularVerbs()
    while True:
        word = input('please input a word:\n')
        if not checkWord(dict, IRR_DIC_PATH, word):
            noLogin(word)
