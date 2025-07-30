import re

# ----------- SimpleTokenizer 정의 -----------
class SimpleTokenizer:
    def __init__(self, lower=True):
        self.lower = lower
        self.pattern = re.compile(r'\b\w+\b', re.UNICODE)
        self.vocab = []
        self.word2idx = {}
        self.idx2word = {}

    def tokenize(self, text):
        if self.lower:
            text = text.lower()
        tokens = self.pattern.findall(text)
        return tokens

    def detokenize(self, tokens):
        return ' '.join(tokens)

    def build_vocab(self, texts):
        vocab_set = set()
        for text in texts:
            tokens = self.tokenize(text)
            vocab_set.update(tokens)
        vocab_list = sorted(list(vocab_set))
        self.vocab = vocab_list
        self.word2idx = {word: idx+1 for idx, word in enumerate(vocab_list)}  # 0: PAD
        self.idx2word = {idx+1: word for idx, word in enumerate(vocab_list)}

    @property
    def vocab_size(self):
        return len(self.vocab) + 1  # PAD 포함

    def encode(self, text, max_len=None):
        tokens = self.tokenize(text)
        ids = [self.word2idx.get(tok, 0) for tok in tokens]  # OOV -> 0
        if max_len:
            ids = ids[:max_len] + [0] * max(0, max_len - len(ids))
        return ids

    def decode(self, ids):
        return self.detokenize([self.idx2word.get(i, "<UNK>") for i in ids if i != 0])
