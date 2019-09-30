"""
Proj. 2 实现一个基于词典与规则的汉语自动分词系统。
(词典：http://nlp.nju.edu.cn/MT_Lecture/dic_ce.rar)
"""
DIC_PATH = 'data/ce（ms-word）.txt'


def load_dict(path):
    """
    加载汉语词典，返回包含汉语词语的list
    :param path:
    :return:
    """
    with open(path, 'r') as f:
        lines = f.readlines()
    words = [l.split(',')[0] for l in lines]
    return words


def FMM(dict, text, max_len=5):
    """
    正向最大匹配
    :param dict:
    :param text:
    :param max_len:单个词语的最大长度
    :return:
    """
    rs = []
    start_pos = 0
    while start_pos < len(text):
        sub_word = text[start_pos:start_pos + max_len]
        while len(sub_word) > 0:
            if sub_word in dict or len(sub_word) == 1:
                rs.append(sub_word)
                start_pos += len(sub_word)
                break
            else:
                sub_word = sub_word[:-1]
    return rs


def RMM(dict, text, max_len=5):
    """
    逆向最大匹配
    :param dict:
    :param text:
    :param max_len:单个词语的最大长度
    :return:
    """
    rs = []
    start_pos = len(text)
    while start_pos > 0:
        split_start = max(start_pos - max_len, 0)
        split_end = start_pos
        sub_word = text[split_start:split_end]
        while len(sub_word) > 0:
            if sub_word in dict or len(sub_word) == 1:
                rs.append(sub_word)
                start_pos -= len(sub_word)
                break
            else:
                sub_word = sub_word[1:]
    rs.reverse()
    return rs


if __name__ == '__main__':
    words = load_dict(path=DIC_PATH)
    text = '幼儿园地节目'
    print('FMM:', FMM(words, text))
    print("RMM:", RMM(words, text))

