# ASR_Evaluation_CN
中文ASR评测指标，WER和SER计算。

Calculate asr evaluation like WER and SER in Chinese.
Calculate levenshtein distance.

### Requirements
- Python 3.7+

### WER
WER: Word Error Rate

$$ WER=\frac {S+D+I}{N} = \frac {S+D+I}{S+D+C} $$

- S: the number of subsitutions.
  替换的数量
- D: the number of deletions.
  删掉的数量
- I: the number of insertions.
  插入的数量
- C: the number of correct words.
  正确的数量
- N: the number of words in the reference.
    总字数

### SER (Same like flow)
SER: Sentence Error Rate

$$SER=\frac {S+D+I}{N} = \frac {S+D+I}{S+D+C}$$

- S: the number of subsitutions.
- D: the number of deletions.
- I: the number of insertions.
- C: the number of correct words.
- N: the number of words in the reference.

### Usage
```shell
git clone git@github.com:yanhuibin315/ASR_Evaluation_CN.git
python demo.py
```

### 例子
标准结果：

["你好", "中国"]

识别结果：

["你嗨", "中国"]

WER = 1/4 = 0.25

SER = 1/2 = 0.5