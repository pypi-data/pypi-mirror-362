from .nn import softmax
import autograd.numpy as anp
from autograd import grad
import numpy as np

"""
MiniMind / layers
"""

def dense(x, W, b):
    return anp.dot(x, W) + b

import autograd.numpy as anp

def token_embedding(x, W_embed):
    """
    x: (batch_size, seq_len) 정수 인덱스 배열
    W_embed: (vocab_size, embed_dim) 임베딩 행렬 (학습 가능)
    """
    vocab_size = W_embed.shape[0]

    # 1. x를 원핫 벡터로 변환 (batch, seq, vocab)
    one_hot = (x[..., None] == anp.arange(vocab_size)).astype(anp.float32)

    # 2. 원핫 * 임베딩 행렬 곱해서 임베딩 결과 얻기 (batch, seq, embed_dim)
    embedded = anp.einsum('bsv,ve->bse', one_hot, W_embed)
    return embedded


def positional_embedding(seq_len, W_pos):
    # (seq_len, embed_dim) -> (1, seq_len, embed_dim)
    return anp.expand_dims(W_pos, axis=0)


def attention(Q, K, V, mask=None):
    d_k = Q.shape[-1]
    scores = anp.matmul(Q, K.transpose((0, 2, 1))) / anp.sqrt(d_k)
    if mask is not None:
        scores = scores + mask
    weights = softmax(scores, axis=-1)
    out = anp.matmul(weights, V)
    return out, weights

__all__ = [
    "dense",
    "token_embedding",
    "positional_embedding",
    "attention",
] 