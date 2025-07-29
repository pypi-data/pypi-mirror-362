import numpy as np
from sklearn.linear_model import Ridge
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.multioutput import MultiOutputRegressor
from .base import BaseGenerator
from .tokenizer import SimpleTokenizer

class GPMGenerator(BaseGenerator):
    """
    GPMGenerator: 전통 ML 기반 Autoregressive 생성기
    Ridge 회귀 앙상블 + one-hot 예측 방식
    """

    def __init__(self, n_models=3, sampler=None, tokenizer=None):
        super().__init__(sampler=sampler, tokenizer=tokenizer or SimpleTokenizer())
        self.vectorizer = CountVectorizer(ngram_range=(1, 3))
        self.label_encoder = LabelEncoder()
        self.models = [MultiOutputRegressor(Ridge(alpha=1.0)) for _ in range(n_models)]
        self.vocab_embeddings = None

    def fit(self, pairs):
        X, y_vecs = [], []
        tokens = []

        for inp, out in pairs:
            inp_tokens = self.tokenizer.tokenize(inp)
            out_tokens = self.tokenizer.tokenize(out) + ["<EOS>"]
            prefix = []
            for token in out_tokens:
                context = " ".join(inp_tokens + prefix)
                X.append(context)
                prefix.append(token)
                tokens.append(token)

        self.label_encoder.fit(tokens + ["<EOS>"])

        y_vecs = []
        for inp, out in pairs:
            inp_tokens = self.tokenizer.tokenize(inp)
            out_tokens = self.tokenizer.tokenize(out) + ["<EOS>"]
            prefix = []
            for token in out_tokens:
                context = " ".join(inp_tokens + prefix)
                vec = np.zeros(len(self.label_encoder.classes_))
                idx = self.label_encoder.transform([token])[0]
                vec[idx] = 1.0
                y_vecs.append(vec)
                prefix.append(token)

        X_vec = self.vectorizer.fit_transform(X)
        y_vecs = np.vstack(y_vecs)
        self.vocab_embeddings = np.eye(len(self.label_encoder.classes_))

        for model in self.models:
            model.fit(X_vec, y_vecs)

        self.is_fitted = True

    def generate(self, prompt, max_tokens=20):
        if not self.is_fitted:
            raise ValueError("GPMGenerator는 학습되지 않았습니다. 먼저 fit()을 호출하세요.")

    # prompt가 문자열이면 토큰화, 리스트면 그대로
        if isinstance(prompt, str):
            prompt_tokens = self.tokenizer.tokenize(prompt)
        else:
            prompt_tokens = prompt

        generated = []
        token_counts = {}

        for _ in range(max_tokens):
            context = " ".join(prompt_tokens + generated)
            X_vec = self.vectorizer.transform([context])
            preds = [model.predict(X_vec)[0] for model in self.models]
            avg_pred = np.mean(preds, axis=0)
            sims = np.dot(self.vocab_embeddings, avg_pred)
            sims = np.clip(sims, a_min=0, a_max=None)

            for token, count in token_counts.items():
                idx = self.label_encoder.transform([token])[0]
                sims[idx] *= 1.0 / (count + 1)

            next_idx = self.sampler.sample(sims) if self.sampler else np.argmax(sims)
            next_token = self.label_encoder.inverse_transform([next_idx])[0]

            if next_token == "<EOS>":
                break

            generated.append(next_token)
            token_counts[next_token] = token_counts.get(next_token, 0) + 1

        return generated  # 토큰 리스트 반환

