# minimind/sampling.py

import numpy as np

def top_k_sampling(probabilities, k=10):
    """
    확률 분포에서 상위 k개 토큰 중 하나를 샘플링한다.
    """
    if k <= 0:
        raise ValueError("k must be positive")
    sorted_indices = np.argsort(probabilities)[::-1]
    top_k_indices = sorted_indices[:k]
    top_k_probs = probabilities[top_k_indices]
    top_k_probs = top_k_probs / np.sum(top_k_probs)
    choice = np.random.choice(top_k_indices, p=top_k_probs)
    return choice


def top_p_sampling(probabilities, p=0.9):
    """
    누적 확률이 p 이하인 토큰 중에서 샘플링한다.
    """
    sorted_indices = np.argsort(probabilities)[::-1]
    sorted_probs = probabilities[sorted_indices]
    cumulative_probs = np.cumsum(sorted_probs)
    cutoff = np.searchsorted(cumulative_probs, p) + 1
    candidates = sorted_indices[:cutoff]
    candidate_probs = sorted_probs[:cutoff]
    candidate_probs = candidate_probs / np.sum(candidate_probs)
    choice = np.random.choice(candidates, p=candidate_probs)
    return choice


def temperature_sampling(probabilities, temperature=1.0):
    """
    온도 조절 후 샘플링.
    temperature > 1 : 분포를 평평하게 하여 다양성 증가
    temperature < 1 : 분포를 뾰족하게 하여 보수적 예측
    """
    if temperature <= 0:
        raise ValueError("temperature must be positive")
    logits = np.log(probabilities + 1e-20) / temperature
    exp_logits = np.exp(logits - np.max(logits))
    probs = exp_logits / np.sum(exp_logits)
    choice = np.random.choice(len(probs), p=probs)
    return choice


# 기본 샘플러 모듈 클래스
class Sampler:
    def __init__(self, method='top_p', p=0.9, k=10, temperature=1.0):
        self.method = method
        self.p = p
        self.k = k
        self.temperature = temperature

    def sample(self, probabilities):
        if self.method == 'top_p':
            return top_p_sampling(probabilities, self.p)
        elif self.method == 'top_k':
            return top_k_sampling(probabilities, self.k)
        elif self.method == 'temperature':
            return temperature_sampling(probabilities, self.temperature)
        else:
            raise ValueError(f"Unknown sampling method: {self.method}")
