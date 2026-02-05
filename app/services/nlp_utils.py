# import numpy as np
# from sentence_transformers import SentenceTransformer 

# embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# def embed_message(messages):
#     return embed_model.encode(messages)

# def get_most_relevant_message(suggestion,messages):
#     sugg_embed = embed_model.encode([suggestion])
#     msg_embed = embed_model.encode(messages)
#     similarities = np.dot(msg_embed,sugg_embed.T).flatten()
#     idx = np.argmax(similarities)
#     return messages[idx]


# def generate_natural_explanation(suggestion, context_msg = None):
#     prompt = f'explain the productivity suggestion in simple terms: {suggestion}'
#     if context_msg:
#         prompt+= f'related to recent activity {context_msg}'


#     return f'{suggestion} consider this based on recent activity : {context_msg or "N/A"} '



import numpy as np
from app.services.embed_service import embed_text


def embed_message(messages):
    """
    Get embeddings for list of messages using HF API
    """
    return embed_text(messages)


# def get_most_relevant_message(suggestion, messages):

#     # Get embedding for suggestion
#     sugg_embed = np.array(embed_text([suggestion]))

#     # Get embeddings for messages
#     msg_embed = np.array(embed_text(messages))

#     # Cosine-like similarity using dot product
#     similarities = np.dot(msg_embed, sugg_embed.T).flatten()

#     idx = np.argmax(similarities)

#     return messages[idx]

def get_most_relevant_message(suggestion, messages):
    sugg_embed = np.array(embed_text(suggestion))

    msg_embeds = np.array([
        embed_text(msg) for msg in messages
    ])

    similarities = np.dot(msg_embeds, sugg_embed)

    idx = np.argmax(similarities)
    return messages[idx]



def generate_natural_explanation(suggestion, context_msg=None):

    # You are not using any LLM yet
    return f"{suggestion} consider this based on recent activity : {context_msg or 'N/A'}"
