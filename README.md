# ASR_Evaluation_CN
calculate asr evaluation like WER and SER.

评测asr的识别结果，计算WER和SER

### WER
WER: Word Error Rate
$$ WER=\frac {S+D+I}{N} = \frac {S+D+I}{S+D+C} $$
- S: the number of subsitutions.
- D: the number of deletions.
- I: the number of insertions.
- C: the number of correct words.
- N: the number of words in the reference.