# import os
# from huggingface_hub import InferenceClient
# from pyparsing import lru_cache

# client = InferenceClient(
#     model="sentence-transformers/all-MiniLM-L6-v2",
#     token=os.getenv("HF_TOKEN")
# )

# @lru_cache(maxsize=200)
# def embed_text(texts):
#     if isinstance(texts, str):
#         texts = [texts]
#     print("HF_TOKEN present:", bool(os.getenv("HF_TOKEN")))


#     return client.feature_extraction(texts)


# embed_service.py
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
