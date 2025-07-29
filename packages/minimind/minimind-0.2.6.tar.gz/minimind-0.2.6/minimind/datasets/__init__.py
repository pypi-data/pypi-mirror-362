# minimind/datasets.py
# csv 경로는 minimind/MLdata.csv

import os
import csv
import re
import numpy as np

def simple_tokenizer(text):
    return re.findall(r'\b\w+\b', text.lower())

def build_vocab(tokens, min_freq=2):
    from collections import Counter
    counter = Counter(tokens)
    vocab = [w for w, c in counter.items() if c >= min_freq]
    vocab = sorted(vocab)
    stoi = {w: i for i, w in enumerate(vocab)}
    itos = {i: w for i, w in enumerate(vocab)}
    return stoi, itos

def encode(tokens, stoi):
    return [stoi[t] for t in tokens if t in stoi]

def pad_seq(seq, max_len, pad_idx):
    return seq[:max_len] + [pad_idx]*(max_len - len(seq))

def load_ml_dataset(max_len=20, min_freq=2, max_samples=None):
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, "MLdata.csv")

    inputs = []
    outputs = []
    all_tokens = []

    with open(csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= max_samples:
                break
            inp_tokens = simple_tokenizer(row['input_text'])
            out_tokens = simple_tokenizer(row['output_text']) + ["<EOS>"]
            all_tokens.extend(inp_tokens)
            all_tokens.extend(out_tokens)
            inputs.append(inp_tokens)
            outputs.append(out_tokens)

    stoi, itos = build_vocab(all_tokens, min_freq)
    pad_idx = len(stoi)  # 패딩 토큰

    X_enc = []
    X_dec = []
    Y = []

    for inp_tokens, out_tokens in zip(inputs, outputs):
        enc_encoded = encode(inp_tokens, stoi)
        dec_encoded = encode(out_tokens[:-1], stoi)
        y_encoded = encode(out_tokens[1:], stoi)

        enc_padded = pad_seq(enc_encoded, max_len, pad_idx)
        dec_padded = pad_seq(dec_encoded, max_len, pad_idx)
        y_padded = pad_seq(y_encoded, max_len, pad_idx)

        X_enc.append(enc_padded)
        X_dec.append(dec_padded)
        Y.append(y_padded)

    vocab_size = len(stoi) + 1  # 패딩 포함
    return np.array(X_enc), np.array(X_dec), np.array(Y), stoi, itos, pad_idx, vocab_size

__all__ = ["load_ml_dataset", "simple_tokenzier", "build_vocab", "encode", "pad_seq"]