import autograd.numpy as anp
from autograd import grad
import numpy as np


def relu(x):
    return anp.maximum(0, x)

def tanh(x):
    return anp.tanh(x)

def sigmoid(x):
    return 1 / (1 + anp.exp(-x))

def gelu(x):
    # 근사 GELU: 0.5 * x * (1 + tanh(sqrt(2/pi) * (x + 0.044715 * x^3)))
    return 0.5 * x * (1 + anp.tanh(anp.sqrt(2 / anp.pi) * (x + 0.044715 * x**3)))


def softmax(x, axis=-1):
    e_x = anp.exp(x - anp.max(x, axis=axis, keepdims=True))
    return e_x / anp.sum(e_x, axis=axis, keepdims=True)


__all__ = [
    "relu",
    "tanh",
    "sigmoid",
    "gelu",
    "softmax"
]
