# minimind/utils.py

import os
import json
import random
import numpy as np

def set_seed(seed=42):
    """
    랜덤 시드 고정 (numpy, random)
    """
    random.seed(seed)
    np.random.seed(seed)

def save_json(obj, filepath):
    """
    객체를 JSON 파일로 저장
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def load_json(filepath):
    """
    JSON 파일에서 객체 로드
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"{filepath} 파일이 없습니다.")
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

import os
import json
import numpy as np
import joblib

def save_model_weights(weights_dict, filepath, format='npz'):
    """
    딕셔너리 형태의 가중치 저장 (format: 'npz', 'joblib', 'json')
    """
    format = format.lower()
    if format == 'npz':
        np.savez(filepath, **weights_dict)
    elif format == 'joblib':
        joblib.dump(weights_dict, filepath)
    elif format == 'json':
        # JSON 저장용으로 넘파이 배열을 리스트로 변환
        json_compatible = {k: v.tolist() if isinstance(v, np.ndarray) else v for k, v in weights_dict.items()}
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(json_compatible, f, ensure_ascii=False, indent=2)
    else:
        raise ValueError(f"지원하지 않는 저장 포맷입니다: {format}")

def load_model_weights(filepath, format='npz'):
    """
    저장된 가중치 딕셔너리로 불러오기 (format: 'npz', 'joblib', 'json')
    """
    format = format.lower()
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"{filepath} 파일이 없습니다.")

    if format == 'npz':
        weights = np.load(filepath, allow_pickle=True)
        return {key: weights[key] for key in weights.files}
    elif format == 'joblib':
        return joblib.load(filepath)
    elif format == 'json':
        with open(filepath, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        # 리스트를 numpy 배열로 다시 변환
        return {k: np.array(v) for k, v in json_data.items()}
    else:
        raise ValueError(f"지원하지 않는 로드 포맷입니다: {format}")

def simple_logger(message):
    """
    간단한 로그 출력, 필요하면 확장 가능
    """
    print(f"[MiniMind LOG] {message}")

