# minimind/sap.py

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
import re
from .base import BaseGenerator
from .tokenizer import SimpleTokenizer


def simple_tokenize(text):
    return re.findall(r"\b\w+\b", text.lower())


class SAPGenerator(BaseGenerator):
    """
    SAPGenerator: 전통 ML 기반의 Stacked Alignment Projection 생성기
    """

    def __init__(self, tokenizer=None):
        super().__init__(tokenizer=tokenizer or SimpleTokenizer())
        self.vectorizer = CountVectorizer(ngram_range=(1, 2))
        self.label_encoder = LabelEncoder()
        self.model = Ridge(alpha=1.0)

    def fit(self, pairs):
        X, y = [], []
        token_set = set()

        for inp, out in pairs:
            inp_tokens = self.tokenizer.tokenize(inp)
            out_tokens = self.tokenizer.tokenize(out) + ["<EOS>"]

            prefix = []
            for tok in out_tokens:
                context = " ".join(inp_tokens + prefix)
                X.append(context)
                y.append(tok)
                prefix.append(tok)
                token_set.add(tok)

        self.label_encoder.fit(list(token_set) + ["<EOS>"])
        y_indices = self.label_encoder.transform(y)
        X_vec = self.vectorizer.fit_transform(X)

        self.model.fit(X_vec, y_indices)
        self.is_fitted = True

    def generate(self, prompt, max_tokens=20):
        if not self.is_fitted:
            raise ValueError("SAPGenerator는 학습되지 않았습니다. 먼저 fit()을 호출하세요.")

    # 입력이 문자열이면 토크나이징, 리스트면 그대로 복사
        if isinstance(prompt, str):
            prompt_tokens = self.tokenizer.tokenize(prompt)
        else:
            prompt_tokens = list(prompt)

        generated = []

        for _ in range(max_tokens):
        # context: prompt_tokens + generated
            context_tokens = prompt_tokens + generated
            context = " ".join(context_tokens)
            X_vec = self.vectorizer.transform([context])
            pred = self.model.predict(X_vec)[0]
            pred_idx = int(round(pred))

        # index 범위 보정
            pred_idx = max(0, min(pred_idx, len(self.label_encoder.classes_) - 1))
            next_token = self.label_encoder.inverse_transform([pred_idx])[0]

            if next_token == "<EOS>":
                break

            generated.append(next_token)

        return generated  # 토큰 리스트 반환
