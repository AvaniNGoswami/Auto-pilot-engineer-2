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
    print("p🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥", p)
    print("b🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥", b)


    if fb['acceptance_rate'] is not None and fb['acceptance_rate'] <= 0.3:
        return "📌 I notice you've skipped suggestions lately — try completing just **one small task** today 💪"
    
    if fb['avg_rate'] is not None and fb['avg_rate'] >= 4.0:
        return "🔥 Love that suggestions are helping! Try increasing your weekly goals 📈"

    # if b == 2:
    #     suggestion = "🚨 Burnout risk high! Take a long break + hydrate."
    #     return "🚨 Burnout risk high! Take a long break + hydrate."
    # if b == 1:
    #     suggestion = "⚠️ Moderate stress. Try a 10-min walk."
    #     return "⚠️ Moderate stress. Try a 10-min walk."
    # if p == 2:
    #     suggestion = "🔥 Peak focus! Keep pushing!"
    #     return "🔥 Peak focus! Keep pushing!"
    # if p == 1:
    #     suggestion = "🙂 You're doing okay, maintain rhythm."
    #     return "🙂 You're doing okay, maintain rhythm."
    
    # suggestion = "📌 Try scheduling deep work block to boost focus."
    # record(userid, suggestion, None, None)

    # return "📌 Try scheduling deep work block to boost focus."
    if b >= 2:
        return "🚨 Burnout risk high! Take a long break + hydrate."
    if 1 <= b < 2:
        return "⚠️ Moderate stress. Try a 10-min walk."

    # Productivity rules (RANGES)
    if p >= 1.5:
        return "🔥 Peak focus! Keep pushing!"
    if 0.5 <= p < 1.5:
        return "🙂 You're doing okay, maintain rhythm."
    if p < 0.5:
        suggestion = "📉 Low productivity — try a 25-minute deep work sprint."
        record(userid, suggestion, None, None)
        return suggestion

    return "📌 Try scheduling deep work block to boost focus."