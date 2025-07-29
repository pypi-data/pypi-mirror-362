import abc
import os
import json
from .tokenizer import SimpleTokenizer

class BaseGenerator(abc.ABC):
    def __init__(self, sampler=None, tokenizer=None):
        self.is_fitted = False
        self.sampler = sampler
        self.model_state = {}
        self.tokenizer = tokenizer or SimpleTokenizer()

    @abc.abstractmethod
    def fit(self, pairs):
        raise NotImplementedError("fit()는 서브클래스에서 구현하세요.")

    @abc.abstractmethod
    def generate(self, prompt, max_tokens=20, **kwargs):
        raise NotImplementedError("generate()는 서브클래스에서 구현하세요.")

    def save(self, path):
        state = self._get_state()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def load(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"'{path}' 파일이 존재하지 않습니다.")
        with open(path, "r", encoding="utf-8") as f:
            state = json.load(f)
        self._set_state(state)
        self.is_fitted = True

    def _get_state(self):
        return self.model_state

    def _set_state(self, state):
        self.model_state = state

    def chat(self, prompt, max_tokens=50, **kwargs):
        prompt_tokens = self.tokenizer.tokenize(prompt)
        generated_tokens = self.generate(prompt_tokens, max_tokens=max_tokens, **kwargs)
        return self.tokenizer.detokenize(generated_tokens)
