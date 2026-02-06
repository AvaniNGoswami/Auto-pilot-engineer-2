from app.agents.feedback import record
from app.services.feedback_utils import user_score
BURNOUT_MAP = {
    "low": 0,
    "medium": 1,
    "high": 2
}


def intervene(userid,analysis):
    if not analysis:
        return "No data yet, keep logging activities!"
    
    p = analysis['productivity']
    b = analysis['burnout']
    b = BURNOUT_MAP.get(analysis['burnout'], 0)


    fb = user_score(userid)
    
    if fb['acceptance_rate'] is not None and fb['acceptance_rate'] <= 0.3:
        suggestion = "📌 I notice you've skipped suggestions lately — try completing just **one small task** today 💪"
        record(userid, suggestion, None, None)
        return suggestion
    
    if fb['avg_rate'] is not None and fb['avg_rate'] >= 4.0:
        suggestion= "🔥 Love that suggestions are helping! Try increasing your weekly goals 📈"
        record(userid, suggestion, None, None)
        return suggestion

    if b >= 2:
        suggestion = "🚨 Burnout risk high! Take a long break + hydrate."
        record(userid, suggestion, None, None)
        return suggestion
    if 1 <= b < 2:
        suggestion = "⚠️ Moderate stress. Try a 10-min walk."
        record(userid, suggestion, None, None)
        return suggestion

    # Productivity rules (RANGES)
    if p >= 1.5:
        suggestion= "🔥 Peak focus! Keep pushing!"
        record(userid, suggestion, None, None)
        return suggestion
    if 0.5 <= p < 1.5:
        suggestion= "🙂 You're doing okay, maintain rhythm."
        record(userid, suggestion, None, None)
        return suggestion
    if p < 0.5:
        suggestion = "📉 Low productivity — try a 25-minute deep work sprint."
        record(userid, suggestion, None, None)
        return suggestion

    return "📌 Try scheduling deep work block to boost focus."





















