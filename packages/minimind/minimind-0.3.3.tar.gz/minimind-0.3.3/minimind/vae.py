import autograd.numpy as anp
import numpy as np
from autograd import grad
from .dl import conv2d, load_mnist
from .nn import sigmoid
import matplotlib.pyplot as plt

# 업샘플링 함수 (2배)
def upsample(x):
    # x: (batch, H, W, C)
    return anp.repeat(anp.repeat(x, 2, axis=1), 2, axis=2)

class VAE:
    def __init__(self, input_shape, latent_dim, params):
        self.input_shape = input_shape  # (H, W, C)
        self.latent_dim = latent_dim
        self.params = params

    def encode(self, x):
        c1 = conv2d(x, self.params['W_enc1'], self.params['b_enc1'], stride=2, padding=1)
        c1 = anp.tanh(c1)
        c2 = conv2d(c1, self.params['W_enc2'], self.params['b_enc2'], stride=2, padding=1)
        c2 = anp.tanh(c2)

        flat = c2.reshape(c2.shape[0], -1)
        mu = anp.dot(flat, self.params['W_mu']) + self.params['b_mu']
        logvar = anp.dot(flat, self.params['W_logvar']) + self.params['b_logvar']
        return mu, logvar

    def reparameterize(self, mu, logvar):
        eps = anp.random.normal(size=mu.shape)
        return mu + eps * anp.exp(logvar * 0.5)

    def decode(self, z):
        h = anp.dot(z, self.params['W_dec']) + self.params['b_dec']
        h = h.reshape((-1, 7, 7, 32))
        h = anp.tanh(h)

        h = upsample(h)
        h = conv2d(h, self.params['W_dec_conv1'], self.params['b_dec_conv1'], stride=1, padding=1)
        h = anp.tanh(h)

        h = upsample(h)
        h = conv2d(h, self.params['W_dec_conv2'], self.params['b_dec_conv2'], stride=1, padding=1)
        h = sigmoid(h)

        return h

    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        x_recon = self.decode(z)
        return x_recon, mu, logvar

    def loss(self, params, x):
        x_recon, mu, logvar = self.forward(x)
        recon_loss = anp.mean((x - x_recon) ** 2)
        kl_loss = -0.5 * anp.mean(1 + logvar - mu**2 - anp.exp(logvar))
        return recon_loss + kl_loss

    def show_reconstructions(self, params, X_val, n=1):
        x_sample = X_val[:n]
        x_recon, _, _ = self.forward(x_sample)
        x_recon = anp.clip(x_recon, 0, 1)

        plt.figure(figsize=(n * 2, 4))
        for i in range(n):
            plt.subplot(2, n, i + 1)
            plt.imshow(x_sample[i].squeeze(), cmap='gray')
            plt.axis('off')
            if i == 0: plt.title('Original')

            plt.subplot(2, n, i + 1 + n)
            plt.imshow(x_recon[i].squeeze(), cmap='gray')
            plt.axis('off')
            if i == 0: plt.title('Reconstruction')
        plt.show()

    def fit(self, params, X_train, X_val=None, epochs=10, batch_size=64, lr=0.001):
        loss_grad = grad(self.loss)
        N = X_train.shape[0]

        for epoch in range(epochs):
            perm = np.random.permutation(N)
            total_loss = 0
            for i in range(0, N, batch_size):
                idx = perm[i:i+batch_size]
                X_batch = X_train[idx]
                grads = loss_grad(params, X_batch)

                for k in params:
                    params[k] -= lr * grads[k]

                batch_loss = self.loss(params, X_batch)
                total_loss += batch_loss * len(idx)

            avg_loss = total_loss / N
            print(f"Epoch {epoch + 1}/{epochs}, Loss: {avg_loss:.4f}")

            if X_val is not None:
                self.show_reconstructions(params, X_val)


def init_params(latent_dim=20, init_std=0.1, rng_seed=42):
    rng = np.random.default_rng(rng_seed)
    params = {
        'W_enc1': rng.normal(0, init_std, (3, 3, 1, 16)),
        'b_enc1': np.zeros(16),

        'W_enc2': rng.normal(0, init_std, (3, 3, 16, 32)),
        'b_enc2': np.zeros(32),

        'W_mu': rng.normal(0, init_std, (7 * 7 * 32, latent_dim)),
        'b_mu': np.zeros(latent_dim),

        'W_logvar': rng.normal(0, init_std, (7 * 7 * 32, latent_dim)),
        'b_logvar': np.zeros(latent_dim),

        'W_dec': rng.normal(0, init_std, (latent_dim, 7 * 7 * 32)),
        'b_dec': np.zeros(7 * 7 * 32),

        'W_dec_conv1': rng.normal(0, init_std, (3, 3, 32, 16)),
        'b_dec_conv1': np.zeros(16),

        'W_dec_conv2': rng.normal(0, init_std, (3, 3, 16, 1)),
        'b_dec_conv2': np.zeros(1),
    }
    return params

