
import numpy as np
import autograd.numpy as anp
from autograd import grad

def relu(x):
    return anp.maximum(0, x)

def softmax(x):
    e_x = anp.exp(x - anp.max(x, axis=-1, keepdims=True))
    return e_x / anp.sum(e_x, axis=-1, keepdims=True)

def dense(x, W, b):
    return anp.dot(x, W) + b


class SeProD:
    def __init__(self, vocab_size, embed_dim=64, hidden_dim=128, max_len=20, pad_idx=None):
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        self.hidden_dim = hidden_dim
        self.max_len = max_len
        self.pad_idx = pad_idx

        rng = np.random.default_rng()
        self.params = {
            'W_embed_enc': rng.normal(0, 0.1, (vocab_size, embed_dim)),
            'W_embed_dec': rng.normal(0, 0.1, (vocab_size, embed_dim)),
            'W_pos_enc': rng.normal(0, 0.1, (max_len, embed_dim)),
            'W_pos_dec': rng.normal(0, 0.1, (max_len, embed_dim)),

            'W_enc': rng.normal(0, 0.1, (embed_dim, hidden_dim)),
            'b_enc': np.zeros(hidden_dim),

            'W_dec': rng.normal(0, 0.1, (embed_dim + hidden_dim, hidden_dim)),
            'b_dec': np.zeros(hidden_dim),

            'W_out': rng.normal(0, 0.1, (hidden_dim, vocab_size)),
            'b_out': np.zeros(vocab_size)
        }

    def forward(self, X_enc, X_dec, params=None):
        p = self.params if params is None else params
        batch_size = X_enc.shape[0]
        seq_len_enc = X_enc.shape[1]  # 인코더 실제 시퀀스 길이
        seq_len_dec = X_dec.shape[1]  # 디코더 실제 시퀀스 길이

        emb_enc = p['W_embed_enc'][X_enc] + p['W_pos_enc'][anp.arange(seq_len_enc)]
        h_enc = relu(dense(emb_enc.mean(axis=1), p['W_enc'], p['b_enc']))

        emb_dec = p['W_embed_dec'][X_dec] + p['W_pos_dec'][anp.arange(seq_len_dec)]

        dec_input = anp.concatenate([emb_dec, h_enc[:, anp.newaxis, :].repeat(seq_len_dec, axis=1)], axis=2)
        h_dec = relu(dense(dec_input.reshape(batch_size * seq_len_dec, -1), p['W_dec'], p['b_dec']))
        h_dec = h_dec.reshape(batch_size, seq_len_dec, self.hidden_dim)

        logits = dense(h_dec.reshape(batch_size * seq_len_dec, -1), p['W_out'], p['b_out'])
        logits = logits.reshape(batch_size, seq_len_dec, self.vocab_size)

        return logits


    def loss(self, params, X_enc, X_dec, Y):
        logits = self.forward(X_enc, X_dec, params)
        probs = softmax(logits)

        mask = (Y != self.pad_idx)
        loss = 0.0
        total_count = 0

        for i in range(Y.shape[0]):
            for t in range(Y.shape[1]):
                if not mask[i, t]:
                    continue
                loss -= anp.log(probs[i, t, Y[i, t]] + 1e-12)
                total_count += 1

        return loss / total_count

    def predict(self, X_enc, X_dec):
        logits = self.forward(X_enc, X_dec, self.params)
        probs = softmax(logits)
        return probs

    def summary(self):
        print("SeProD Model Summary")
        print(f"Vocab size: {self.vocab_size}")
        print(f"Embedding dim: {self.embed_dim}")
        print(f"Hidden dim: {self.hidden_dim}")
        print(f"Max sequence length: {self.max_len}")
        print(f"Padding idx: {self.pad_idx}")
        print("\nParameters:")
        total_params = 0
        for name, param in self.params.items():
            size = param.size
            total_params += size
            print(f"  {name}: shape {param.shape}, params {size}")
        print(f"\nTotal parameters: {total_params}")



# --- AutoTrainer에 맞는 인터페이스용 클래스 래퍼 ---
class SeProDTrainer:
    def __init__(self, model: SeProD, learning_rate=0.001, batch_size=32, verbose=True):
        self.model = model
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.verbose = verbose
        self.loss_grad = grad(self.model.loss)

    def fit(self, X_enc, X_dec, Y, epochs=10):
        N = X_enc.shape[0]

        for epoch in range(epochs):
            perm = np.random.permutation(N)
            total_loss = 0

            for i in range(0, N, self.batch_size):
                idx = perm[i:i+self.batch_size]
                X_enc_batch, X_dec_batch, Y_batch = X_enc[idx], X_dec[idx], Y[idx]

                grads = self.loss_grad(self.model.params, X_enc_batch, X_dec_batch, Y_batch)

                for k in self.model.params:
                    self.model.params[k] -= self.learning_rate * grads[k]

                batch_loss = self.model.loss(self.model.params, X_enc_batch, X_dec_batch, Y_batch)
                total_loss += batch_loss * len(idx)

            avg_loss = total_loss / N
            if self.verbose:
                print(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.4f}")

    def predict(self, X_enc, X_dec):
        return self.model.predict(X_enc, X_dec)

    def summary(self):
        self.model.summary()

