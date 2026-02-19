import os

from groq import Groq
from app.agents.feedback import record
from app.services import history
from app.services.feedback_utils import user_score
BURNOUT_MAP = {
    "low": 0,
    "medium": 1,
    "high": 2
}
SYSTEM_PROMPT = """
You are a productivity analysis engine.

Return a STRICT machine-readable response.

Rules:
- No markdown
- No asterisks
- No headings
- No bullet points
- No explanations outside format
- No motivational advice
- No extra commentary
- only analyze using the provided data
- If you don't know, say "I don't know" or "Not enough data", don't make up an answer
- always say bluntly what is happening, don't sugarcoat it

Output format EXACTLY:

SUGGESTION: <specific actionable suggestion based on productivity and burnout levels>
"""

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.1-8b-instant"

def intervene(userid,analysis):
    if not analysis:
        return "No data yet, keep logging activities!"
    
    p = analysis['productivity']
    b = analysis['burnout']
    b = BURNOUT_MAP.get(analysis['burnout'], 0)


    fb = user_score(userid)
    
    if fb['acceptance_rate'] is not None and fb['acceptance_rate'] <= 0.3:
        message=[{"role": "system", "content": f"Answer only using provided activity history and {SYSTEM_PROMPT}."},
        {"role": "user", "content": {"Question": "What is one actionable suggestion for this user based on their productivity {p} and burnout levels {b}, and the fact that their feedback acceptance rate is low? Their feedback acceptance rate is low, which may indicate they are not engaging with or benefiting from suggestions. Please provide a specific suggestion to help them improve their engagement and productivity.",}}]
        suggestion = message
        record(userid, suggestion, None, None)
        return suggestion
    
    if fb['avg_rate'] is not None and fb['avg_rate'] >= 4.0:
        message=[{"role": "system", "content": f"Answer only using provided activity history and {SYSTEM_PROMPT}."},
        {"role": "user", "content": {"Question": "What is one actionable suggestion for this user based on their productivity {p} and burnout levels {b}, and the fact that their feedback acceptance rate is low? Their feedback acceptance rate is low, which may indicate they are not engaging with or benefiting from suggestions. Please provide a specific suggestion to help them improve their engagement and productivity.",}}]
        suggestion = message
        record(userid, suggestion, None, None)
        return suggestion

    if b >= 2:
        message=[{"role": "system", "content": f"Answer only using provided activity history and {SYSTEM_PROMPT}."},
        {"role": "user", "content": {"Question": "What is one actionable suggestion for this user based on their productivity {p} and burnout levels {b}, and the fact that their feedback acceptance rate is low? Their feedback acceptance rate is low, which may indicate they are not engaging with or benefiting from suggestions. Please provide a specific suggestion to help them improve their engagement and productivity.",}}]
        suggestion = message
        record(userid, suggestion, None, None)
        return suggestion
    if 1 <= b < 2:
        message=[{"role": "system", "content": f"Answer only using provided activity history and {SYSTEM_PROMPT}."},
        {"role": "user", "content": {"Question": "What is one actionable suggestion for this user based on their productivity {p} and burnout levels {b}, and the fact that their feedback acceptance rate is low? Their feedback acceptance rate is low, which may indicate they are not engaging with or benefiting from suggestions. Please provide a specific suggestion to help them improve their engagement and productivity.",}}]
        suggestion = message
        record(userid, suggestion, None, None)
        return suggestion

    # Productivity rules (RANGES)
    if p >= 1.5:
        message=[{"role": "system", "content": f"Answer only using provided activity history and {SYSTEM_PROMPT}."},
        {"role": "user", "content": {"Question": "What is one actionable suggestion for this user based on their productivity {p} and burnout levels {b}, and the fact that their feedback acceptance rate is low? Their feedback acceptance rate is low, which may indicate they are not engaging with or benefiting from suggestions. Please provide a specific suggestion to help them improve their engagement and productivity.",}}]
        suggestion = message
        record(userid, suggestion, None, None)
        return suggestion
    if 0.5 <= p < 1.5:
        message=[{"role": "system", "content": f"Answer only using provided activity history and {SYSTEM_PROMPT}."},
        {"role": "user", "content": {"Question": "What is one actionable suggestion for this user based on their productivity {p} and burnout levels {b}, and the fact that their feedback acceptance rate is low? Their feedback acceptance rate is low, which may indicate they are not engaging with or benefiting from suggestions. Please provide a specific suggestion to help them improve their engagement and productivity.",}}]
        suggestion = message
        record(userid, suggestion, None, None)
        return suggestion
    if p < 0.5:
        message=[{"role": "system", "content": f"Answer only using provided activity history and {SYSTEM_PROMPT}."},
        {"role": "user", "content": {"Question": "What is one actionable suggestion for this user based on their productivity {p} and burnout levels {b}, and the fact that their feedback acceptance rate is low? Their feedback acceptance rate is low, which may indicate they are not engaging with or benefiting from suggestions. Please provide a specific suggestion to help them improve their engagement and productivity.",}}]
        suggestion = message
        record(userid, suggestion, None, None)
        return suggestion

    return "📌 Try scheduling deep work block to boost focus."





















