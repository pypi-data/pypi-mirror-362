import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import resample
from .base import BaseGenerator
from .tokenizer import SimpleTokenizer

class Radec(BaseGenerator):
    def __init__(self, n_models=3, sampler=None, tokenizer=None, max_features=0.7):
        super().__init__(sampler=sampler, tokenizer=tokenizer or SimpleTokenizer())
        self.vectorizer = CountVectorizer(ngram_range=(1, 3))
        self.label_encoder = LabelEncoder()
        # max_features 조절해서 랜덤 특성 서브셋 활용
        self.models = [
            MultiOutputRegressor(DecisionTreeRegressor(max_depth=15, max_features=max_features, random_state=i))
            for i in range(n_models)
        ]
        self.sampler = sampler
        self.tokenizer = tokenizer
        self.is_fitted = False

    def fit(self, pairs):
        X, y_vecs, tokens = [], [], []

        for inp, out in pairs:
            inp_tokens = self.tokenizer(inp)
            out_tokens = self.tokenizer(out) + ["<EOS>"]
            prefix = []
            for token in out_tokens:
                context = " ".join(inp_tokens + prefix)
                X.append(context)
                prefix.append(token)
                tokens.append(token)

        self.label_encoder.fit(tokens + ["<EOS>"])

        for inp, out in pairs:
            inp_tokens = self.tokenizer(inp)
            out_tokens = self.tokenizer(out) + ["<EOS>"]
            prefix = []
            for token in out_tokens:
                vec = np.zeros(len(self.label_encoder.classes_))
                idx = self.label_encoder.transform([token])[0]
                vec[idx] = 1.0
                y_vecs.append(vec)
                prefix.append(token)

        X_vec = self.vectorizer.fit_transform(X)
        y_vecs = np.vstack(y_vecs)

        # 각 모델마다 배깅: 데이터 샘플링 후 학습
        for i, model in enumerate(self.models):
            X_sample, y_sample = resample(X_vec, y_vecs, random_state=i)
            model.fit(X_sample, y_sample)

        self.vocab_embeddings = np.eye(len(self.label_encoder.classes_))
        self.is_fitted = True

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
            X_vec = self.vectorizer.transform([context])

            # 트리별 예측 결과에서 샘플링
            preds = [model.predict(X_vec)[0] for model in self.models]
            preds = np.array(preds)  # (n_models, vocab_size)

            # 트리별 예측 확률을 평균내는 대신 트리 중 하나를 랜덤 선택해 확률로 사용
            tree_idx = np.random.choice(len(self.models))
            prob_dist = preds[tree_idx]
            prob_dist = np.clip(prob_dist, 0, None)
            prob_dist /= prob_dist.sum() + 1e-9  # 정규화

            # 이미 나온 토큰 페널티 적용
            for token, count in token_counts.items():
                idx = self.label_encoder.transform([token])[0]
                prob_dist[idx] *= 1.0 / (count + 1)

            # 샘플러가 있으면 샘플링, 없으면 argmax
            if self.sampler:
                next_idx = self.sampler.sample(prob_dist)
            else:
                next_idx = np.argmax(prob_dist)

            next_token = self.label_encoder.inverse_transform([next_idx])[0]
            if next_token == "<EOS>":
                break

            generated.append(next_token)
            token_counts[next_token] = token_counts.get(next_token, 0) + 1

        return generated
