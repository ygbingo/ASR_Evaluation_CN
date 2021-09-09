# -*- coding: utf-8 -*-

from algorithm.evaluations import calculate_WER

ori_data = ["你好", "北京"]
rec_data = ["你嗨", "北京"]
wer = calculate_WER(ori_data, rec_data)
print(wer)