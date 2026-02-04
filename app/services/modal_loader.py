import os
import requests

MODEL_URLS = {
    "productivity": "https://huggingface.co/Avani21/auto-pilot-engineer/resolve/main/productivity.pkl",
    "burnout": "https://huggingface.co/Avani21/auto-pilot-engineer/resolve/main/burnout.pkl"
}

BASE_DIR = "app/models_storage"

os.makedirs(BASE_DIR, exist_ok=True)

def load_model(model_name):
    import joblib

    model_path = os.path.join(BASE_DIR, f"{model_name}.pkl")

    if not os.path.exists(model_path):
        url = MODEL_URLS[model_name]
        response = requests.get(url)
        with open(model_path, "wb") as f:
            f.write(response.content)

    return joblib.load(model_path)
