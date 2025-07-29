# minimind/tokenizer.py

import re

class SimpleTokenizer:
    """
    간단한 정규표현식 기반 토크나이저.
    기본적으로 영어/한글/숫자 단어 단위로 분리.
    """
    def __init__(self, lower=True):
        self.lower = lower
        self.pattern = re.compile(r'\b\w+\b', re.UNICODE)

    def tokenize(self, text):
        if self.lower:
            text = text.lower()
        tokens = self.pattern.findall(text)
        return tokens

    def detokenize(self, tokens):
        # 단순히 띄어쓰기 합치기 (더 정교하게 만들 수도 있음)
        return ' '.join(tokens)
