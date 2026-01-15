import numpy as np
from sentence_transformers import SentenceTransformer 
from gpt4all import GPT4All

embed_model = SentenceTransformer('all-MiniLM-L6-v2')
# llm_model = GPT4All("ggml-gpt4all-j-v1.3-groovy.bin")

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

# def generate_natural_explanation(suggestion, context_msg = None):
#     """
#     Generates natural explanation using local llm
#     combines suggestion + context message for polished output.
#     """
#     prompt = f"Explain this productivity suggestion in a friendly, encouraging tone:\n" \
#              f"Suggestion: {suggestion}\n"
#     if context_msg:
#         prompt += f"Recent activity context: {context_msg}\n"

#     prompt += "Make it clear, short, and motivational."
#     output = llm_model.generate(prompt,max_tokens=200)
#     return output