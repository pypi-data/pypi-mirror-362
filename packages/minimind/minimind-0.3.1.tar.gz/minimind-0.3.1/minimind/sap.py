import numpy as np

class RidgeRegressor:
    def __init__(self, alpha=1.0, lr=0.01, epochs=500):
        self.alpha = alpha      # L2 규제 강도
        self.lr = lr            # 학습률
        self.epochs = epochs    # 반복 횟수

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.w = np.zeros(n_features)
        self.b = 0.0

        for epoch in range(self.epochs):
            y_pred = X.dot(self.w) + self.b
            error = y_pred - y

            dw = (2/n_samples) * (X.T.dot(error) + self.alpha * self.w)
            db = (2/n_samples) * np.sum(error)

            self.w -= self.lr * dw
            self.b -= self.lr * db

            # 옵션: 손실 출력 (필요하면)
            if epoch % 100 == 0:
                loss = np.mean(error**2) + self.alpha * np.sum(self.w**2)
                print(f"Epoch {epoch} Loss: {loss:.4f}")

    def predict(self, X):
        return X.dot(self.w) + self.b

from .base import BaseGenerator
from .tokenizer import SimpleTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
import re
import numpy as np


class SAPGenerator(BaseGenerator):
    def __init__(self, tokenizer=None, alpha=1.0, lr=0.01, epochs=500):
        super().__init__(tokenizer=tokenizer or SimpleTokenizer())
        self.vectorizer = CountVectorizer(ngram_range=(1, 2))
        self.label_encoder = LabelEncoder()
        self.model = RidgeRegressor(alpha=alpha, lr=lr, epochs=epochs)
        self.is_fitted = False

    def fit(self, pairs):
        X_text, y = [], []
        token_set = set()

        for inp, out in pairs:
            inp_tokens = self.tokenizer.tokenize(inp)
            out_tokens = self.tokenizer.tokenize(out) + ["<EOS>"]

            prefix = []
            for tok in out_tokens:
                context = " ".join(inp_tokens + prefix)
                X_text.append(context)
                y.append(tok)
                prefix.append(tok)
                token_set.add(tok)

        self.label_encoder.fit(list(token_set) + ["<EOS>"])
        y_indices = self.label_encoder.transform(y)

        # 벡터화 후 넘파이 배열로 변환
        X_vec = self.vectorizer.fit_transform(X_text).toarray()

        # 모델 학습
        self.model.fit(X_vec, y_indices)
        self.is_fitted = True

    def generate(self, prompt, max_tokens=20):
        if not self.is_fitted:
            raise ValueError("SAPGenerator는 학습되지 않았습니다. 먼저 fit()을 호출하세요.")

        if isinstance(prompt, str):
            prompt_tokens = self.tokenizer.tokenize(prompt)
        else:
            prompt_tokens = list(prompt)

        generated = []

        for _ in range(max_tokens):
            context_tokens = prompt_tokens + generated
            context = " ".join(context_tokens)
            X_vec = self.vectorizer.transform([context]).toarray()
            pred = self.model.predict(X_vec)[0]
            pred_idx = int(round(pred))
            pred_idx = max(0, min(pred_idx, len(self.label_encoder.classes_) - 1))
            next_token = self.label_encoder.inverse_transform([pred_idx])[0]

            if next_token == "<EOS>":
                break

            generated.append(next_token)

        return generated