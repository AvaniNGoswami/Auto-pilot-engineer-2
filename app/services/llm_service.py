import os
from groq import Groq
from openai import OpenAI
from app.core.config import GROQ_API_KEY

from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.1-8b-instant"


# SYSTEM_ROLE = """
# You are an engineering productivity analyst.
# You analyze developer activity metrics and give factual reasoning.
# Never give generic motivational advice.
# Explain patterns using the provided data only.
# """

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

SUMMARY: <1-2 sentences>

PROBLEMS:
1. <short problem>
2. <short problem>
3. <short problem>

CAUSE:
<single paragraph explaining root cause>

ACTION:
1. <specific actionable step>
2. <specific actionable step>
3. <specific actionable step>
"""
SYSTEM_ROLE = SYSTEM_PROMPT
# MODELS = [
#     "meta-llama/llama-3.1-8b-instant",
#     "meta-llama/llama-3.3-70b-versatile",
#     "mixtral-8x7b-32768"
# ]
def call_llm(messages):
    res = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.3
    )
    return res.choices[0].message.content



def analyze_metrics(metrics: dict):
    prompt = f"""
    Analyze the developer metrics:

    {metrics}

    Provide:
    - Summary
    - Problems
    - Cause
    """

    messages = [
        {"role": "system", "content": SYSTEM_ROLE},
        {"role": "user", "content": prompt}
    ]

    return call_llm(messages)
# def analyze_metrics(metrics: dict):
#     user_prompt = f"""
#     Analyze the following developer metrics and explain what is happening:

#     {metrics}

#     Output format:
#     - Summary
#     - Key Problems
#     - Why it happened
#     """

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",   # cheap + fast
#         messages=[
#             {"role": "system", "content": SYSTEM_ROLE},
#             {"role": "user", "content": user_prompt}
#         ],
#         temperature=0.3
#     )

#     return response.choices[0].message.content


def answer_question(question: str, history: list):
    messages = [
        {"role": "system", "content": f"Answer only using provided activity history and {SYSTEM_ROLE}."},
        {"role": "user", "content": f"Question: {question}\nHistory: {history}"}
    ]

    return call_llm(messages)
