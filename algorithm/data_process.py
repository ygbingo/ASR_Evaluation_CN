"""
data_process:
delete some symbols like ', . ? ! ，。？~！'
"""

NEED_DEL_SYMBOLS = [',', '.', '?', '，', '。', '？', '、', '?', '\n', '\t', ' ']


def del_symbol(texts: str):
    """
    过滤掉一些符号
    :param texts: 字符串
    :return: 过滤结果
    """
    for symbol in NEED_DEL_SYMBOLS:
        texts = texts.replace(symbol, '')
    return texts