from minimind import GPMGenerator, Sampler, SimpleTokenizer

def main():
    print("MiniMind GPMGenerator 테스트 시작!")


    import csv
    csv_path = "MLdata.csv"  # 네 데이터셋 경로로 변경

    pairs = []
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pairs.append((row['input_text'].strip(), row['output_text'].strip()))


    # 샘플러 생성 (top-k 예시)
    sampler = Sampler(method='top_k', k=3)
    tokenizer = SimpleTokenizer()

    # 생성기 초기화 시 sampler 연결
    gpm = GPMGenerator(sampler=sampler, tokenizer=tokenizer)
    gpm.fit(pairs[:327])

    # 생성 테스트
    prompt = "안녕하세요"
    response = gpm.chat(prompt, max_tokens=10)

    print("입력 프롬프트:", prompt)
    print("생성된 텍스트:", response)

    prompt = "오늘 날씨 어때?"
    response = gpm.chat(prompt, max_tokens=10)

    print("입력 프롬프트:", prompt)
    print("생성된 텍스트:", response)

    prompt = "지금 뭐해?"
    response = gpm.chat(prompt, max_tokens=10)

    print("입력 프롬프트:", prompt)
    print("생성된 텍스트:", response)

if __name__ == "__main__":
    main()



import autograd.numpy as anp
from autograd import grad
import numpy as np
from minimind.neuralnet import token_embedding, positional_embedding, attention, dense, tanh, softmax 

class SimpleModel:
    def __init__(self, vocab_size, seq_len, embed_dim, hidden_dim):
        rng = np.random.default_rng(42)
        self.vocab_size = vocab_size
        self.seq_len = seq_len
        self.embed_dim = embed_dim
        self.hidden_dim = hidden_dim

        self.params = {
            "W_embed": rng.normal(0, 0.1, (vocab_size, embed_dim)),
            "W_pos": rng.normal(0, 0.1, (seq_len, embed_dim)),
            "W_dense": rng.normal(0, 0.1, (embed_dim, hidden_dim)),
            "b_dense": np.zeros(hidden_dim),
            "W_out": rng.normal(0, 0.1, (hidden_dim, vocab_size)),
            "b_out": np.zeros(vocab_size)
        }

    def forward(self, X, params):
        emb_tokens = token_embedding(X, params["W_embed"])  # (batch, seq_len, embed_dim)
        emb_positions = positional_embedding(self.seq_len, params["W_pos"])
        emb = emb_tokens + emb_positions
        Q, K, V = emb, emb, emb
        attn_out, _ = attention(Q, K, V)
        attn_out_flat = attn_out.reshape(-1, self.embed_dim)
        hidden = tanh(dense(attn_out_flat, params["W_dense"], params["b_dense"]))
        logits = dense(hidden, params["W_out"], params["b_out"])  # (batch*seq_len, vocab_size)
        logits = logits.reshape(-1, self.seq_len, self.vocab_size)
        return logits

    def loss(self, params, X, Y):
        logits = self.forward(X, params)
        probs = softmax(logits, axis=2)
        batch_size = X.shape[0]
        loss = 0.0
        count = 0
        for i in range(batch_size):
            for t in range(self.seq_len):
                loss -= anp.log(probs[i, t, Y[i, t]] + 1e-12)
                count += 1
        return loss / count


def train(model, X_train, Y_train, epochs=20, batch_size=8, lr=0.01):
    loss_grad = grad(model.loss)
    N = X_train.shape[0]

    for epoch in range(epochs):
        perm = np.random.permutation(N)
        total_loss = 0
        for i in range(0, N, batch_size):
            idx = perm[i:i+batch_size]
            X_batch, Y_batch = X_train[idx], Y_train[idx]
            grads = loss_grad(model.params, X_batch, Y_batch)

            # 파라미터 업데이트 (SGD)
            for k in model.params:
                model.params[k] -= lr * grads[k]

            batch_loss = model.loss(model.params, X_batch, Y_batch)
            total_loss += batch_loss * len(idx)

        avg_loss = total_loss / N
        print(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.4f}")



if __name__ == "__main__":
    # 더미 데이터 생성 (단어 인덱스 시퀀스)
    vocab_size = 50
    seq_len = 4
    batch_size = 64

    np.random.seed(123)
    X_train = np.random.randint(0, vocab_size, (batch_size*10, seq_len))
    Y_train = np.random.randint(0, vocab_size, (batch_size*10, seq_len))  # 정답도 토큰 인덱스

    model = SimpleModel(vocab_size, seq_len, embed_dim=8, hidden_dim=16)
    train(model, X_train, Y_train, epochs=20, batch_size=batch_size, lr=0.01)


from minimind.dl import MLPTrainer, NeuralGenerator
import numpy as np

num_samples = 100

X_train = np.random.randn(num_samples, 10)
y_train = np.random.randint(0, 3, size=num_samples)

model = NeuralGenerator(vocab_size=1000, embed_dim=64, hidden_layer_sizes=(128,64))
trainer = MLPTrainer(model, learning_rate=0.001)

trainer.fit(X_train, y_train, epochs=50)




from minimind.ml import SAPGenerator
from minimind import SimpleTokenizer
def main():
    print("MiniMind SAPGenerator 테스트 시작!")

    import csv
    csv_path = "MLdata.csv"  # 네 데이터셋 경로로 변경

    pairs = []
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pairs.append((row['input_text'].strip(), row['output_text'].strip()))


    # SAPGenerator 인스턴스 생성 및 학습
    tokenizer = SimpleTokenizer()
    sap_gen = SAPGenerator(tokenizer=tokenizer)
    sap_gen.fit(pairs[:200])

    # 생성 테스트
    prompt = "오늘은 뭐 할까?"
    print(f"입력: {prompt}")
    generated = sap_gen.chat(prompt, max_tokens=10)
    print(f"생성 결과: {generated}")

if __name__ == "__main__":
    main()


# test_sampling.py

import numpy as np
from minimind import top_k_sampling, top_p_sampling, temperature_sampling, Sampler

def dummy_probs(size=100):
    probs = np.random.rand(size)
    return probs / probs.sum()

def test_sampling_functions():
    probs = dummy_probs()

    print("top_k_sampling:", top_k_sampling(probs, k=5))
    print("top_p_sampling:", top_p_sampling(probs, p=0.8))
    print("temperature_sampling (temp=0.5):", temperature_sampling(probs, temperature=0.5))
    print("temperature_sampling (temp=2.0):", temperature_sampling(probs, temperature=2.0))

def test_sampler_class():
    probs = dummy_probs()
    sampler = Sampler(method='top_p', p=0.9)
    print("Sampler top_p:", sampler.sample(probs))

    sampler.method = 'top_k'
    sampler.k = 3
    print("Sampler top_k:", sampler.sample(probs))

    sampler.method = 'temperature'
    sampler.temperature = 0.7
    print("Sampler temperature:", sampler.sample(probs))

if __name__ == "__main__":
    test_sampling_functions()
    test_sampler_class()

from minimind import SimpleTokenizer

tokenizer = SimpleTokenizer()

text = "Hello, 안녕하세요! Let's test the tokenizer 123."
tokens = tokenizer.tokenize(text)
print("토큰:", tokens)

reconstructed = tokenizer.detokenize(tokens)
print("복원된 문장:", reconstructed)

import os
import numpy as np
from minimind import set_seed, save_json, load_json, save_model_weights, load_model_weights, simple_logger


if __name__ == "__main__":
    # 테스트 함수들

    def test_set_seed():
        set_seed(123)
        a = np.random.rand(3)
        set_seed(123)
        b = np.random.rand(3)
        assert np.allclose(a, b), "set_seed 실패!"
        print("set_seed 테스트 통과!")

    def test_save_load_json():
        data = {'name': 'MiniMind', 'version': 1.0}
        filepath = 'test.json'
        save_json(data, filepath)
        loaded = load_json(filepath)
        assert data == loaded, "JSON 저장/로드 실패!"
        os.remove(filepath)
        print("save_json & load_json 테스트 통과!")

    def test_save_load_weights_multi_format():
        weights = {
            'W1': np.array([1, 2, 3]),
            'b1': np.array([0.1, 0.2, 0.3])
        }
        for fmt in ['npz', 'joblib', 'json']:
            filepath = f"weights_test.{fmt}"
            save_model_weights(weights, filepath, format=fmt)
            loaded = load_model_weights(filepath, format=fmt)
            for k in weights:
                assert np.allclose(weights[k], loaded[k]), f"{fmt} {k} 가중치 저장/로드 실패!"
            os.remove(filepath)
        print("멀티 포맷 가중치 저장/로드 테스트 통과!")

    def test_logger():
        simple_logger("테스트 로그 메시지")

    # 실행 테스트 모음
    test_set_seed()
    test_save_load_json()
    test_save_load_weights_multi_format()
    test_logger()


from minimind.dl import CNN_MNIST, load_mnist, predict
import autograd.numpy as anp

if __name__ == "__main__":
    X_train, X_val, Y_train, Y_val = load_mnist()
    model = CNN_MNIST()
    model.fit(X_train, Y_train, X_val, Y_val, epochs=1, batch_size=128, lr=0.01)

    # 샘플 디코딩
    idx = 0
    pred = predict(model, X_val[idx:idx+1])[0]
    label = anp.argmax(Y_val[idx])
    print(f"[예측 결과] 예측: {pred}, 실제: {label}")

from minimind.dl import VAE, init_params
from Conv2D import load_mnist


if __name__ == "__main__":
    X_train, X_val, _, _ = load_mnist()
    X_train = X_train.reshape(-1, 28, 28, 1)
    X_val = X_val.reshape(-1, 28, 28, 1)

    params = init_params(latent_dim=30, init_std=0.05)
    model = VAE((28, 28, 1), 30, params)

    model.fit(params, X_train, X_val=X_val, epochs=10, batch_size=64, lr=0.001)
