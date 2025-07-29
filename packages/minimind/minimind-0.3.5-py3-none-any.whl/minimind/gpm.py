import numpy as np

class RidgeMultiOutputRegressor:
    def __init__(self, alpha=1.0, lr=0.01, epochs=500):
        self.alpha = alpha
        self.lr = lr
        self.epochs = epochs

    def fit(self, X, Y):
        # X: (n_samples, n_features)
        # Y: (n_samples, n_outputs)
        n_samples, n_features = X.shape
        n_outputs = Y.shape[1]

        self.w = np.zeros((n_features, n_outputs))
        self.b = np.zeros(n_outputs)

        for epoch in range(self.epochs):
            Y_pred = X @ self.w + self.b  # (n_samples, n_outputs)
            error = Y_pred - Y             # (n_samples, n_outputs)

            dw = (2/n_samples) * (X.T @ error + self.alpha * self.w)  # (n_features, n_outputs)
            db = (2/n_samples) * np.sum(error, axis=0)                # (n_outputs,)

            self.w -= self.lr * dw
            self.b -= self.lr * db

    def predict(self, X):
        return X @ self.w + self.b  # (n_samples, n_outputs)


from .base import BaseGenerator
from .tokenizer import SimpleTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
import numpy as np


class GPMGenerator(BaseGenerator):
    def __init__(self, n_models=3, sampler=None, tokenizer=None, alpha=1.0, lr=0.01, epochs=500):
        super().__init__(sampler=sampler, tokenizer=tokenizer or SimpleTokenizer())
        self.vectorizer = CountVectorizer(ngram_range=(1, 3))
        self.label_encoder = LabelEncoder()
        self.models = [RidgeMultiOutputRegressor(alpha=alpha, lr=lr, epochs=epochs) for _ in range(n_models)]
        self.vocab_embeddings = None
        self.is_fitted = False

    def fit(self, pairs):
        X_text, y_vecs = [], []
        tokens = []

        for inp, out in pairs:
            inp_tokens = self.tokenizer.tokenize(inp)
            out_tokens = self.tokenizer.tokenize(out) + ["<EOS>"]
            prefix = []
            for token in out_tokens:
                context = " ".join(inp_tokens + prefix)
                X_text.append(context)
                prefix.append(token)
                tokens.append(token)

        self.label_encoder.fit(tokens + ["<EOS>"])

        y_vecs = []
        for inp, out in pairs:
            inp_tokens = self.tokenizer.tokenize(inp)
            out_tokens = self.tokenizer.tokenize(out) + ["<EOS>"]
            prefix = []
            for token in out_tokens:
                vec = np.zeros(len(self.label_encoder.classes_))
                idx = self.label_encoder.transform([token])[0]
                vec[idx] = 1.0
                y_vecs.append(vec)
                prefix.append(token)

        X_vec = self.vectorizer.fit_transform(X_text).toarray()
        y_vecs = np.vstack(y_vecs)
        self.vocab_embeddings = np.eye(len(self.label_encoder.classes_))

        # 각 모델 독립적으로 학습
        for model in self.models:
            model.fit(X_vec, y_vecs)

        self.is_fitted = True

    def generate(self, prompt, max_tokens=20):
        if not self.is_fitted:
            raise ValueError("GPMGenerator는 학습되지 않았습니다. 먼저 fit()을 호출하세요.")

        if isinstance(prompt, str):
            prompt_tokens = self.tokenizer.tokenize(prompt)
        else:
            prompt_tokens = prompt

        generated = []
        token_counts = {}

        for _ in range(max_tokens):
            context = " ".join(prompt_tokens + generated)
            X_vec = self.vectorizer.transform([context]).toarray()
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

        return generated
