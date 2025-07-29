from .nn import softmax
import autograd.numpy as anp
from autograd import grad
import numpy as np

"""
MiniMind / layers
"""
# 🧩 MiniMind 호환 Conv2D
def conv2d(x, W, b, stride=1, padding=0):
    batch_size, h, w, in_ch = x.shape
    fh, fw, _, out_ch = W.shape

    if padding > 0:
        x = anp.pad(x, ((0,0), (padding,padding), (padding,padding), (0,0)), mode='constant')
    oh = (h + 2 * padding - fh) // stride + 1
    ow = (w + 2 * padding - fw) // stride + 1

    cols = []
    for i in range(oh):
        for j in range(ow):
            hs, ws = i * stride, j * stride
            x_slice = x[:, hs:hs+fh, ws:ws+fw, :]  # (batch, fh, fw, in_ch)
            cols.append(x_slice.reshape(batch_size, -1))  # (batch, fh*fw*in_ch)
    cols = anp.stack(cols, axis=1)  # (batch, oh*ow, fh*fw*in_ch)
    W_col = W.reshape(-1, out_ch)   # (fh*fw*in_ch, out_ch)
    out = anp.matmul(cols, W_col) + b  # (batch, oh*ow, out_ch)
    return out.reshape(batch_size, oh, ow, out_ch)


def dense(x, W, b):
    return anp.dot(x, W) + b

def upsample(x):
    return anp.repeat(anp.repeat(x, 2, axis=1), 2, axis=2)


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
    "upsample"
] 