import pytest
from app.agents.observer import observe
from app.agents.analyzer import analyze
from app.agents.intervention import intervene

def test_observer_collects_signals():
    observer = observe()
    events = [{"activity_type": "coding", "duration": 90}]
    signals = observer.collect(events)
    assert "focus_score" in signals

def test_analyzer_patterns():
    analyzer = analyze()
    patterns = analyzer({"focus_score": 80})
    assert "peak_hours" in patterns

def test_intervention_decision():
    intervention = intervene()
    decision = intervention({"peak_hours": ["10:00-12:00"]})
    assert "suggestion_text" in decision
