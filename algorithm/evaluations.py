"""
calculate SER and WER
"""
from .data_process import del_symbol, number2cn
from difflib import Differ
from .violent_dist.np_matrix import levenshtein
import re
from .violent_dist.recursion import ViolentMinEditDistance_v2


def calculate_SER(ori_text, rec_text):
    """
    计算句错率
    :param ori_text: 正确的句子集合
    :param rec_text: 识别的句子集合
    :return: number
    """
    res = -1
    if len(ori_text) <= 0 or len(rec_text) <= 0:
        return res
    ori_texts = []
    for ori in ori_text:
        ori_texts.append(del_symbol(ori))

    rec_texts = []
    for rec in rec_text:
        rec_texts.append(del_symbol(rec))

    NUM = len(ori_texts)
    INSERT = 0
    DELETE = 0
    REPLACE = 0
    differ = Differ()
    result = list(differ.compare(ori_texts, rec_texts))
    import pprint
    pprint.pprint(result)
    for res in result:
        if res.startswith('?') or res.startswith(' '): continue

        if res.startswith('-'):
            INSERT += 1
        if res.startswith('+'):
            if INSERT > 0:
                INSERT -= 1
                REPLACE += 1
            else:
                DELETE += 1

    res = (INSERT + DELETE + REPLACE) / NUM

    return res

def calculate_WER(ori_text, rec_text):
    """
    计算字错率: (S+D+I)/N
        S is the number of substitutions,
        D is the number of deletions,
        I is the number of insertions,
        N is the number of words in the reference.
    :param ori_text: 真实结果
    :param rec_text: 识别结果
    :return: number 计算的WER结果
    """
    res = -1
    ori_text = ''.join(ori_text)
    rec_text = ''.join(rec_text)
    if len(ori_text) <= 0 or len(rec_text) <= 0:
        return res

    NUM = len(ori_text)

    ori_text = del_symbol(ori_text)
    rec_text = del_symbol(rec_text)

    differ = Differ()
    result = list(differ.compare(ori_text, rec_text))
    result = ''.join(result)
    result = re.findall(r"\+|-", result)

    INSERT = 0
    DELETE = 0
    REPLACE = 0
    for res in result:
        if res == '-':
            INSERT += 1
        if res == '+':
            if INSERT > 0:
                INSERT -= 1
                REPLACE += 1
            else:
                DELETE += 1
    res = (INSERT + DELETE + REPLACE) / NUM
    return res

def calculate_Levenshtein(ori_text, rec_text):
    """
    计算Levenshtein
    :param ori_text: 真实结果
    :param rec_text: 识别结果
    :return: number 计算的WER结果
    """
    res = -1
    ori_text = ''.join(ori_text)
    rec_text = ''.join(rec_text)
    if len(ori_text) <= 0 or len(rec_text) <= 0:
        return res

    ori_text = del_symbol(ori_text)
    rec_text = del_symbol(rec_text)

    from .violent_dist.enumerate import ViolentMinEditDistance_v1

    vilent_v1 = ViolentMinEditDistance_v1(ori_text, rec_text)
    vilent_v1.fit()

    return res

def calculate_Dynamic(ori_text, rec_text):
    """
    动态规划计算Levenshtein
    :param ori_text: 真实结果
    :param rec_text: 识别结果
    :return: number 计算的WER结果
    """
    res = -1
    ori_text = ''.join(ori_text)
    rec_text = ''.join(rec_text)
    if len(ori_text) <= 0 or len(rec_text) <= 0:
        return res

    ori_text = del_symbol(ori_text)
    rec_text = del_symbol(rec_text)
    print(ori_text)
    print(rec_text)
    from .violent_dist.dynamic import DPMinEditDistance

    dp_dist = DPMinEditDistance(ori_text, rec_text)
    dp_dist.fit()

    return res

def calculate_Recursion(ori_text, rec_text):
    """
    递归计算levenshtein
    :param ori_text: 真实结果
    :param rec_text: 识别结果
    :return: number 计算的WER结果
    """
    res = -1
    ori_text = ''.join(ori_text)
    rec_text = ''.join(rec_text)
    if len(ori_text) <= 0 or len(rec_text) <= 0:
        return res

    ori_text = del_symbol(ori_text)
    rec_text = del_symbol(rec_text)
    print(ori_text)
    print(rec_text)

    vilent_v2 = ViolentMinEditDistance_v2(ori_text, rec_text)
    vilent_v2.fit()

    return res

def calculate_np_levenshtein(ori_text, rec_text):
    """
    利用numpy计算levenshtein
    :param ori_text:
    :param rec_text:
    :return:
    """
    res = -1
    ori_text = ''.join(ori_text)
    rec_text = ''.join(rec_text)
    if len(ori_text) <= 0 or len(rec_text) <= 0:
        return res

    ori_text = del_symbol(ori_text)
    ori_text = number2cn(ori_text)
    rec_text = del_symbol(rec_text)
    rec_text = number2cn(rec_text)
    print(ori_text)
    print(rec_text)

    dist = levenshtein(ori_text, rec_text)

    print("leven SER: " + str(dist/len(ori_text)))

    return dist