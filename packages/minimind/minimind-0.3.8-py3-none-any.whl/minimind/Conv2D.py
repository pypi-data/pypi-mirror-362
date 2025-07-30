import autograd.numpy as anp
import numpy as np
from autograd import grad
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from .nn import softmax  # 이미 너 프레임워크에 있어!


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

# 🧠 모델 정의
class CNN_MNIST:
    def __init__(self):
        rng = np.random.default_rng(42)
        self.params = {
            "W_conv": rng.normal(0, 0.1, (3,3,1,8)),      # 1채널 → 8채널
            "b_conv": np.zeros(8),
            "W_dense": rng.normal(0, 0.1, (26*26*8, 10)), # (H=26, W=26) * 8채널 → 10 클래스
            "b_dense": np.zeros(10)
        }

    def forward(self, x, params):
        x = conv2d(x, params["W_conv"], params["b_conv"])
        x = anp.maximum(0, x)  # ReLU
        x = x.reshape(x.shape[0], -1)  # Flatten
        out = anp.dot(x, params["W_dense"]) + params["b_dense"]
        return out

    def loss(self, params, x, y):
        logits = self.forward(x, params)            # (batch, 10)
        probs = softmax(logits, axis=1)             # softmax 적용
        log_probs = anp.log(probs + 1e-12)          # 로그 안정성 확보
        return -anp.mean(anp.sum(y * log_probs, axis=1))  # Cross Entropy



# 🏋️‍♂️ 학습 함수
    def fit(self, X_train, Y_train, X_val, Y_val, epochs=10, batch_size=64, lr=0.01):
        loss_grad = grad(self.loss)
        N = X_train.shape[0]
        for epoch in range(epochs):
            perm = np.random.permutation(N)
            total_loss = 0
            for i in range(0, N, batch_size):
                idx = perm[i:i+batch_size]
                xb, yb = X_train[idx], Y_train[idx]
                grads = loss_grad(self.params, xb, yb)
                for k in self.params:
                    self.params[k] -= lr * grads[k]
                batch_loss = self.loss(self.params, xb, yb)
                total_loss += batch_loss * len(idx)
            val_loss = self.loss(self.params, X_val, Y_val)
            acc = accuracy(self, X_val, Y_val)
            print(f"Epoch {epoch+1}/{epochs}, Train Loss: {total_loss/N:.4f}, Val Loss: {val_loss:.4f}, Val Acc: {acc*100:.2f}%")

# 🔍 디코딩 및 정확도
def predict(model, X):
    logits = model.forward(X, model.params)
    return anp.argmax(logits, axis=1)

def accuracy(model, X, Y_true):
    logits = model.forward(X, model.params)
    probs = softmax(logits, axis=1)
    pred = anp.argmax(probs, axis=1)
    true = anp.argmax(Y_true, axis=1)
    return anp.mean(pred == true)


# 📦 MNIST 데이터셋 로더
def load_mnist():
    print("[INFO] MNIST 불러오는 중...")
    X, y = fetch_openml("mnist_784", version=1, return_X_y=True, as_frame=False)
    X = X.astype('float32') / 255.0
    X = X.reshape(-1, 28, 28, 1)
    y = y.astype(int)
    enc = OneHotEncoder(sparse_output=False)
    y_oh = enc.fit_transform(y.reshape(-1, 1))
    return train_test_split(X, y_oh, test_size=0.2, random_state=42)

