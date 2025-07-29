# minimind/neural.py



import autograd.numpy as anp
from autograd import grad
import autograd.numpy as anp
from autograd import grad
import autograd.numpy as np
from autograd import grad



class MLPTrainer:
    def __init__(self, model, loss_fn=None, learning_rate=0.01, batch_size=32):
        self.model = model
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.loss_fn = loss_fn if loss_fn else self.default_loss_fn
        self.loss_grad = grad(self.loss_fn)

    def default_loss_fn(self, params, x, y):
        logits = self.model.forward(x, params)
        probs = self.model.softmax(logits)  # (batch_size, vocab_size)

        batch_size = y.shape[0]
        clipped = anp.clip(probs, 1e-9, 1.0)
        log_probs = anp.log(clipped)

    # y가 정수 인덱스니까, 정답 위치만 선택해서 평균 손실 계산
        loss = -anp.mean(log_probs[anp.arange(batch_size), y])
        return loss


    def step(self, x, y):
        grads = self.loss_grad(self.model.params, x, y)
        for k in self.model.params:
            self.model.params[k] -= self.learning_rate * grads[k]

    def fit(self, x, y, epochs=1000, verbose=True):
        for epoch in range(epochs):
            # 미니배치 학습
            idx = np.random.permutation(x.shape[0])
            x_shuffled, y_shuffled = x[idx], y[idx]
            total_loss = 0

            for i in range(0, x.shape[0], self.batch_size):
                x_batch = x_shuffled[i:i+self.batch_size]
                y_batch = y_shuffled[i:i+self.batch_size]
                grads = self.loss_grad(self.model.params, x_batch, y_batch)

                for k in self.model.params:
                    self.model.params[k] -= self.learning_rate * grads[k]

                batch_loss = self.loss_fn(self.model.params, x_batch, y_batch)
                total_loss += batch_loss * x_batch.shape[0]

            avg_loss = total_loss / x.shape[0]
            if verbose and (epoch + 1) % 10 == 0:
                print(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.4f}")


class NeuralGenerator:
    def __init__(self, vocab_size, embed_dim=64, hidden_layer_sizes=(128,64), activation=None):
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        self.hidden_layer_sizes = hidden_layer_sizes
        self.activation = activation if activation else self.relu

        self.params = {}
        self._init_weights()

    def _init_weights(self):
        self.params['W_embed'] = np.random.randn(self.vocab_size, self.embed_dim) * 0.01
        layer_sizes = [self.embed_dim] + list(self.hidden_layer_sizes) + [self.vocab_size]
        for i in range(len(layer_sizes)-1):
            self.params[f'W{i}'] = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * 0.01
            self.params[f'b{i}'] = np.zeros(layer_sizes[i+1])

    def relu(self, x):
        return np.maximum(0, x)

    def softmax(self, x):
        e_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return e_x / e_x.sum(axis=1, keepdims=True)

    def forward(self, X, params=None):
        p = self.params if params is None else params
        X_int = X.astype(int)
        embedded = p['W_embed'][X_int].mean(axis=1)
        h = embedded
        num_layers = len(self.hidden_layer_sizes) + 1
        for i in range(num_layers):
            W = p[f'W{i}']
            b = p[f'b{i}']
            h = h @ W + b
            if i < num_layers - 1:
                h = self.activation(h)
        return h

    def loss(self, params, X, y_true):
        logits = self.forward(X, params)  # (batch, vocab_size)
        probs = self.softmax(logits)      # (batch, vocab_size)

    # y_true는 정수 인덱스 (batch,)
        batch_size = y_true.shape[0]
        clipped = np.clip(probs, 1e-9, 1.0)
        log_probs = np.log(clipped)
        loss_val = -np.mean(log_probs[np.arange(batch_size), y_true])
        return loss_val


    def predict(self, X, params=None):
        logits = self.forward(X, params)
        return self.softmax(logits)
