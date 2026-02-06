

def embed_message(messages):
    """
    No embeddings anymore.
    Kept only to avoid breaking existing imports.
    """
    return messages

def get_most_relevant_message(suggestion, messages):
    """
    Simple fallback:
    pick the most recent / last message as context
    """
    if not messages:
        return None
    return messages[-1]

def generate_natural_explanation(suggestion, context_msg=None):
    """
    Template-based explanation (NO ML, NO API)
    """

    suggestion = suggestion.rstrip(".")

    if context_msg:
        return (
            f"{suggestion}. "
            f"This recommendation is based on your recent activity, "
            f"such as: {context_msg}."
        )

    return (
        f"{suggestion}. "
        f"This recommendation is based on your recent activity."
    )
