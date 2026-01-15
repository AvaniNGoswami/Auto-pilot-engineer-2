from app.agents.observer import observe
from app.agents.analyzer import analyze
from app.agents.intervention import intervene

def run_agent(userid:str):
    data = observe(userid)
    result = analyze(data)
    suggestion = intervene(userid,result)
    return suggestion