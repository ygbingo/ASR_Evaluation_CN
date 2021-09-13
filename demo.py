# -*- coding: utf-8 -*-

from algorithm.evaluations import calculate_WER, calculate_Levenshtein, calculate_Dynamic, calculate_Recursion, calculate_np_levenshtein

ori_data = ["你好", "北京"]
rec_data = ["你嗨呀", "北的京"]
wer = calculate_WER(ori_data, rec_data)
print(wer)

# calculate_Levenshtein(ori_data, rec_data)
# calculate_Recursion(ori_data, rec_data)

dist = calculate_np_levenshtein(ori_data, rec_data)
print("Levens_Dist: " + str(dist))
