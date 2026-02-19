from app.agents.feedback import record
from app.services.feedback_utils import user_score
BURNOUT_MAP = {
    "low": 0,
    "medium": 1,
    "high": 2
}

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.1-8b-instant"

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

SUGGESTION: <specific actionable suggestion to improve productivity or well-being>
"""
# def intervene(userid,analysis):
#     if not analysis:
#         return "No data yet, keep logging activities!"
    
#     p = analysis['productivity']
#     b = analysis['burnout']
#     b = BURNOUT_MAP.get(analysis['burnout'], 0)


#     fb = user_score(userid)
    
#     if fb['acceptance_rate'] is not None and fb['acceptance_rate'] <= 0.3:
#         suggestion = "📌 I notice you've skipped suggestions lately — try completing just **one small task** today 💪"
#         record(userid, suggestion, None, None)
#         return suggestion
    
#     if fb['avg_rate'] is not None and fb['avg_rate'] >= 4.0:
#         suggestion= "🔥 Love that suggestions are helping! Try increasing your weekly goals 📈"
#         record(userid, suggestion, None, None)
#         return suggestion

#     if b >= 2:
#         suggestion = "🚨 Burnout risk high! Take a long break + hydrate."
#         record(userid, suggestion, None, None)
#         return suggestion
#     if 1 <= b < 2:
#         suggestion = "⚠️ Moderate stress. Try a 10-min walk."
#         record(userid, suggestion, None, None)
#         return suggestion

#     # Productivity rules (RANGES)
#     if p >= 1.5:
#         suggestion= "🔥 Peak focus! Keep pushing!"
#         record(userid, suggestion, None, None)
#         return suggestion
#     if 0.5 <= p < 1.5:
#         suggestion= "🙂 You're doing okay, maintain rhythm."
#         record(userid, suggestion, None, None)
#         return suggestion
#     if p < 0.5:
#         suggestion = "📉 Low productivity — try a 25-minute deep work sprint."
#         record(userid, suggestion, None, None)
#         return suggestion

#     return "📌 Try scheduling deep work block to boost focus."


def build_prompt(p,b,fb):
        context = f"""
        Analyze the developer's state:
    
        Productivity: {p}
        Burnout: {b}
        Feedback Score: {fb}
    
        Provide a specific, actionable suggestion to improve their productivity or well-being. 
        If feedback score is low, encourage them to engage with suggestions. 
        If burnout is high, prioritize self-care advice.
        """
        return context

def generate_suggestion(prompt):
     response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": SYSTEM_PROMPT},
                  {"role": "user", "content": prompt}],
        temperature=0.3
            
     )
     return response.choices[0].message.content.strip()



def intervene(userid,analysis):
    if not analysis:
        return "No data yet, keep logging activities!"
    
    p = analysis['productivity']
    b = analysis['burnout']
    b = BURNOUT_MAP.get(analysis['burnout'], 0)


    fb = user_score(userid)

    prompt = build_prompt(p, b, fb)
    suggestion = generate_suggestion(prompt)

    record(userid, suggestion, None, None)

    return suggestion

















