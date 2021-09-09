"""
calculate SER and WER
"""
from .data_process import del_symbol
from difflib import Differ
import re

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