import numpy as np
from sentence_transformers import SentenceTransformer 
from gpt4all import GPT4All

embed_model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_message(messages):
    return embed_model.encode(messages)

def get_most_relevant_message(suggestion,messages):
    sugg_embed = embed_model.encode([suggestion])
    msg_embed = embed_model.encode(messages)
    similarities = np.dot(msg_embed,sugg_embed.T).flatten()
    idx = np.argmax(similarities)
    return messages[idx]


def generate_natural_explanation(suggestion, context_msg = None):
    prompt = f'explain the productivity suggestion in simple terms: {suggestion}'
    if context_msg:
        prompt+= f'related to recent activity {context_msg}'


    return f'{suggestion} consider this based on recent activity : {context_msg or "N/A"} '
