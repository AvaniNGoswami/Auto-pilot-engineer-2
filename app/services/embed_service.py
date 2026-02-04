from huggingface_hub import InferenceClient
from pyparsing import lru_cache

client = InferenceClient(
    model="sentence-transformers/all-MiniLM-L6-v2",
    token="REMOVEDwUnpsMAfVrDFPOfuGnWgLqkCfwNMzDvSkJ"
)

@lru_cache(maxsize=200)
def embed_text(texts):
    if isinstance(texts, str):
        texts = [texts]

    return client.feature_extraction(texts)
