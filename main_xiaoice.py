"""
读取识别结果
"""
import json
from difflib import Differ
import re
import jsonlines
from algorithm.evaluations import calculate_Levenshtein, calculate_np_levenshtein, calculate_Dynamic, calculate_Recursion
import os


def del_symbol(texts: str):
    """
    过滤掉一些符号
    :param texts: 字符串
    :return: 过滤结果
    """
    need_del_symbols = [',', '.', '?', '，', '。', '？', '、', '?', '\n', '\t', ' ']
    for symbol in need_del_symbols:
        texts = texts.replace(symbol, '')
    return texts

def generate_ori_text(path):
    """解析原始label文件的text内容"""
    with open(path, "r") as f:
        lines = f.readlines()
    ori_texts = []
    for line in lines:
        line = line.strip().split(" ")
        ori_texts.append(line[-1].replace("\n", ""))
    return ori_texts

def generate_ali_text(path):
    """解析阿里识别的text"""
    with open(path, "r") as f:
        ali_json = json.loads(f.read())
    ali_texts = []
    dialogues = ali_json['body']['Data']['Dialogues']['Dialogue']
    for dialogue in dialogues:
        ali_texts.append(dialogue['Words'])
    return ali_texts

def generate_tencent_text(path):
    """解析腾讯云识别的text"""
    with open(path, "r") as f:
        tencent_json = json.loads(f.read())
    tencent_texts = []
    dialogues = tencent_json['Data']['Result'].split('\n')
    for dialogue in dialogues:
        dialogue = dialogue.split(' ')[-1]
        tencent_texts.append(dialogue)
    return tencent_texts

def generate_xunfei_text(path):
    """解析讯飞识别的text"""
    with open(path, "r") as f:
        ifly_json = json.loads(f.read())
    ifly_texts = []
    dialogues = ifly_json['data']
    for dialogue in dialogues:
        dialogue = dialogue['onebest']
        ifly_texts.append(dialogue)
    return ifly_texts

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

def main(ori_path: str, rec_path: str):
    SER_Res = -1
    WER_Res = -1
    ori_texts = generate_ori_text(ori_path)
    rec_texts = []
    if rec_path.startswith("./data/ali") or 'ali' in rec_path:
        rec_texts = generate_ali_text(rec_path)
    elif rec_path.startswith("./data/tencent"):
        rec_texts = generate_tencent_text(rec_path)
    elif rec_path.startswith("./data/ty_xunfei") or rec_path.startswith("./data/xunfei"):
        rec_texts = generate_xunfei_text(rec_path)
    else:
        rec_texts = generate_ori_text(rec_path)

    print(ori_texts)
    print(rec_texts)

    if len(ori_texts) > 0 and len(rec_texts) > 0:
        levenshtein_dist = calculate_np_levenshtein(ori_texts, rec_texts)
        print("levens_dist: " + str(levenshtein_dist))
        SER_Res = calculate_SER(ori_texts, rec_texts)

        WER_Res = calculate_WER(ori_texts, rec_texts)

    return SER_Res, WER_Res, levenshtein_dist

if __name__ == '__main__':
    ori_root_path = "E:\\xiaoice\\asr_dataset\\1208训练数据[分轨音频文字校对]汇总\\1208训练数据转写\\"
    ori_files = os.listdir(ori_root_path)

    writer = jsonlines.open("eva_res.jsonl", "w")
    writer.write("file_name,SER,WER,LEVENSHTEIN")

    tencent_res_path = "E:\\User\\Documents\\github\\asr_rep\\1201训练数据\\"
    tencent_files = os.listdir(tencent_res_path)

    tencent_res_path_selfmodel = "E:\\User\\Documents\\github\\asr_rep\\1201训练数据-自学习\\"
    tencent_selfmodel_files = os.listdir(tencent_res_path_selfmodel)

    ali_res_path = "E:\\User\\Documents\\github\\asr_rep\\ali_asr\\ali_results\\"
    ali_files = os.listdir(ali_res_path)

    for ori_file in ori_files:
        print(ori_file)
        if ori_file not in tencent_files:
            print("Cannot find this res in tencent.")
            continue
        ori_file_path = ori_root_path + ori_file
        tencent_file_path = tencent_res_path + ori_file
        ali_file_path = ali_res_path + ori_file
        tencent_file_path_selfmodel = tencent_res_path_selfmodel + ori_file

        SER_Res, WER_Res, levenshtein_dist = main(ori_file_path, tencent_file_path_selfmodel)

        writer.write(str(ori_file + "," + str(SER_Res) + "," + str(WER_Res) + "," + str(levenshtein_dist)))