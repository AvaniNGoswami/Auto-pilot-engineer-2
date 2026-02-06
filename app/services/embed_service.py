import os
from huggingface_hub import InferenceClient
from functools import lru_cache

@lru_cache(maxsize=1)
def get_hf_client():
    token = os.getenv("HF_TOKEN")
    if not token:
        raise RuntimeError("HF_TOKEN missing at runtime")

    return InferenceClient(
        model="sentence-transformers/all-MiniLM-L6-v2",
        token=token
    )

def embed_text(texts):
    print("HF_TOKEN at runtime:", bool(os.getenv("HF_TOKEN")))
    if isinstance(texts, str):
        texts = [texts]

    client = get_hf_client()
    return client.feature_extraction(texts)
