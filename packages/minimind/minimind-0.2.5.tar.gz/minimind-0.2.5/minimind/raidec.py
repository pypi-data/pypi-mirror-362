from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.linear_model import Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import numpy as np

class RaidecGenerator(BaseEstimator, RegressorMixin):
    def __init__(self, n_estimators=10, ridge_ratio=0.5, max_depth=5, random_state=None, sampler=None, tokenizer=None):
        self.n_estimators = n_estimators
        self.ridge_ratio = ridge_ratio
        self.max_depth = max_depth
        self.random_state = random_state
        self.sampler = sampler
        self.tokenizer = tokenizer if tokenizer is not None else self.default_tokenizer
        self.is_fitted = False

    def default_tokenizer(self, text):
        return text.strip().split()

    def fit(self, X_texts, y_texts):
        # 토크나이저 & 라벨 인코더, 벡터라이저 초기화
        all_texts = X_texts + y_texts + ["<EOS>"]
        tokenized = [self.tokenizer(txt) for txt in all_texts]
        tokens_flat = [tok for seq in tokenized for tok in seq]

        self.label_encoder = LabelEncoder()
        self.label_encoder.fit(tokens_flat)

        self.vectorizer = TfidfVectorizer(tokenizer=self.tokenizer)
        self.vectorizer.fit(all_texts)

        X_vec = self.vectorizer.transform(X_texts)
        y_tokens = [self.tokenizer(txt) for txt in y_texts]

        max_len = max(len(seq) for seq in y_tokens)
        y_indices = np.full((len(y_tokens), max_len), fill_value=-1, dtype=int)
        for i, seq in enumerate(y_tokens):
            idx_seq = self.label_encoder.transform(seq)
            y_indices[i, :len(idx_seq)] = idx_seq

        X_train = []
        y_train = []
        for i in range(len(X_texts)):
            for t in range(max_len):
                X_train.append(X_vec[i].toarray()[0])
                if y_indices[i, t] == -1:
                    y_train.append(self.label_encoder.transform(['<EOS>'])[0])
                else:
                    y_train.append(y_indices[i, t])

        X_train = np.array(X_train)
        y_train = np.array(y_train)

        # y_train 원-핫 인코딩
        num_classes = len(self.label_encoder.classes_)
        y_onehot = np.zeros((y_train.size, num_classes))
        y_onehot[np.arange(y_train.size), y_train] = 1

        rng = np.random.RandomState(self.random_state)
        self.models_ = []
        self.random_projections_ = []

        n_ridge = int(self.n_estimators * self.ridge_ratio)
        n_tree = self.n_estimators - n_ridge

        for _ in range(n_ridge):
            proj = rng.normal(size=(X_train.shape[1], X_train.shape[1] // 2))
            self.random_projections_.append(proj)
            X_proj = X_train @ proj
            model = MultiOutputRegressor(Ridge(random_state=rng.randint(1_000_000)))
            model.fit(X_proj, y_onehot)
            self.models_.append(model)

        for _ in range(n_tree):
            proj = rng.normal(size=(X_train.shape[1], X_train.shape[1] // 2))
            self.random_projections_.append(proj)
            X_proj = X_train @ proj
            model = MultiOutputRegressor(DecisionTreeRegressor(max_depth=self.max_depth,
                                                               random_state=rng.randint(1_000_000)))
            model.fit(X_proj, y_onehot)
            self.models_.append(model)

        self.is_fitted = True
        return self

    def softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / (e_x.sum() + 1e-9)

    def predict_proba(self, X_vec):
        preds = []
        for proj, model in zip(self.random_projections_, self.models_):
            X_proj = X_vec @ proj
            pred = model.predict(X_proj)
            preds.append(pred)
        preds = np.array(preds)  # (n_models, batch_size, num_classes)
        mean_pred = np.mean(preds, axis=0)  # (batch_size, num_classes)
        return mean_pred

    def generate(self, prompt, max_tokens=20):
        if not self.is_fitted:
            raise RuntimeError("모델이 학습되지 않았어요! fit() 먼저 호출하세요.")

        if isinstance(prompt, str):
            prompt_tokens = self.tokenizer(prompt)
        else:
            prompt_tokens = prompt

        generated = []
        token_counts = {}

        for _ in range(max_tokens):
            context = " ".join(prompt_tokens + generated)
            X_vec = self.vectorizer.transform([context]).toarray()

            mean_pred = self.predict_proba(X_vec)[0]  # (num_classes,)
            prob_dist = self.softmax(mean_pred)

            for token, count in token_counts.items():
                try:
                    idx = self.label_encoder.transform([token])[0]
                    prob_dist[idx] *= 1.0 / (count + 1)
                except ValueError:
                    pass

            prob_dist /= prob_dist.sum() + 1e-9  # 재정규화

            if self.sampler:
                next_idx = self.sampler.sample(prob_dist)
            else:
                next_idx = np.argmax(prob_dist)

            next_token = self.label_encoder.inverse_transform([next_idx])[0]
            if next_token == "<EOS>":
                break

            generated.append(next_token)
            token_counts[next_token] = token_counts.get(next_token, 0) + 1

        return [str(tok) for tok in generated]
