import autograd.numpy as anp
import numpy as np
from autograd import grad
from .dl import conv2d
from .nn import sigmoid, gelu, relu

def upsample(x):
    return anp.repeat(anp.repeat(x, 2, axis=1), 2, axis=2)

def upsample(x):
    return anp.repeat(anp.repeat(x, 2, axis=1), 2, axis=2)

class Generator:
    def __init__(self, latent_dim=100):
        rng = np.random.default_rng(42)
        self.params = {
            "W1": rng.normal(0, 0.1, (latent_dim, 7 * 7 * 128)),
            "b1": anp.zeros(7 * 7 * 128),
            "W2": rng.normal(0, 0.1, (3, 3, 128, 64)),
            "b2": anp.zeros(64),
            "W3": rng.normal(0, 0.1, (3, 3, 64, 1)),
            "b3": anp.zeros(1)
        }

    def forward(self, z, params=None):
        if params is None:
            params = self.params
        h = relu(anp.dot(z, params["W1"]) + params["b1"]).reshape((-1, 7, 7, 128))
        h = upsample(h)  # 7x7 -> 14x14
        h = relu(conv2d(h, params["W2"], params["b2"], stride=1, padding=1))
        h = upsample(h)  # 14x14 -> 28x28
        x_fake = sigmoid(conv2d(h, params["W3"], params["b3"], stride=1, padding=1))
        return x_fake

class Discriminator:
    def __init__(self):
        rng = np.random.default_rng(1337)
        self.params = {
            "W1": rng.normal(0, 0.1, (3, 3, 1, 32)),
            "b1": anp.zeros(32),
            "W2": rng.normal(0, 0.1, (3, 3, 32, 64)),
            "b2": anp.zeros(64),
            "W3": rng.normal(0, 0.1, (7 * 7 * 64, 1)),
            "b3": anp.zeros(1)
        }

    def forward(self, x, params=None):
        if params is None:
            params = self.params
        h = relu(conv2d(x, params["W1"], params["b1"], stride=2, padding=1))
        h = relu(conv2d(h, params["W2"], params["b2"], stride=2, padding=1))
        h = h.reshape((x.shape[0], -1))
        out = anp.dot(h, params["W3"]) + params["b3"]
        return sigmoid(out)

def gan_loss(D_real, D_fake):
    return -anp.mean(anp.log(D_real + 1e-8) + anp.log(1 - D_fake + 1e-8))

def gan_loss_g(D_fake):
    return -anp.mean(anp.log(D_fake + 1e-8))

import matplotlib.pyplot as plt

def plot_generated_images(generator, params, latent_dim, n_images=8):
    z = np.random.normal(size=(n_images, latent_dim))
    gen_imgs = generator.forward(z, params)
    gen_imgs = anp.clip(gen_imgs, 0, 1)

    plt.figure(figsize=(n_images * 2, 2))
    for i in range(n_images):
        plt.subplot(1, n_images, i + 1)
        plt.imshow(gen_imgs[i].squeeze(), cmap='gray')
        plt.axis('off')
    plt.suptitle("Generated Images")
    plt.show()

def train_gan(generator, discriminator, X_train, epochs=3000, batch_size=64,
              g_lr=0.0002, d_lr=0.0002, latent_dim=100, sample_interval=1):
    g_params = generator.params
    d_params = discriminator.params

    g_loss_grad = grad(lambda gp, dp, z: gan_loss_g(discriminator.forward(generator.forward(z, gp), dp)))
    d_loss_grad = grad(lambda dp, gp, real, z: gan_loss(discriminator.forward(real, dp), discriminator.forward(generator.forward(z, gp), dp)))

    N = X_train.shape[0]

    for step in range(epochs):
        idx = np.random.randint(0, N, batch_size)
        real_imgs = X_train[idx]

        z = np.random.normal(size=(batch_size, latent_dim))

        # Discriminator 업데이트
        d_grads = d_loss_grad(d_params, g_params, real_imgs, z)
        for k in d_params:
            d_params[k] -= d_lr * d_grads[k]

        # Generator 업데이트
        g_grads = g_loss_grad(g_params, d_params, z)
        for k in g_params:
            g_params[k] -= g_lr * g_grads[k]

        if step % sample_interval == 0:
            d_real = discriminator.forward(real_imgs, d_params)
            d_fake = discriminator.forward(generator.forward(z, g_params), d_params)
            d_loss = gan_loss(d_real, d_fake)
            g_loss = gan_loss_g(d_fake)
            print(f"Step {step}, D Loss: {d_loss:.4f}, G Loss: {g_loss:.4f}")
            plot_generated_images(generator, g_params, latent_dim, n_images=8)
