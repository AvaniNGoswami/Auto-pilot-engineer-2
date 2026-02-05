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



import os
from huggingface_hub import InferenceClient
from functools import lru_cache

HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise RuntimeError("HF_TOKEN is missing at startup")

client = InferenceClient(
    model="sentence-transformers/all-MiniLM-L6-v2",
    token=HF_TOKEN
)

@lru_cache(maxsize=200)
def embed_text(texts):
    if isinstance(texts, str):
        texts = (texts,)
    elif isinstance(texts, list):
        texts = tuple(texts)

    return client.feature_extraction(list(texts))
