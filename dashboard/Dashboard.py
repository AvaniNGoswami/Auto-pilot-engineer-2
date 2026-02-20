import streamlit as st
import pandas as pd
import sys, os
import requests
from sqlalchemy.orm import Session

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.db.database import engine
from app.models.features import Features
from app.models.feedback import Feedback
from datetime import timedelta,date
import numpy as np
import os

st.set_page_config(page_title="Auto-Pilot Engineer Dashboard", layout="wide")

API_BASE = os.getenv("API_BASE", "https://auto-pilot-engineer-2-avani-n-goswami-production.up.railway.app")

def login_user(email):
    resp = requests.post(url=f"{API_BASE}/auth/login", params={"email": email})
    if resp.status_code != 200:
        return None
    return resp.json()['access_token']
 

st.title("Login for Dashboard")
email = st.text_input("Enter your email")
if st.button("Login"):
    token = login_user(email)
    if token:
        st.session_state.token = token
        st.rerun()
    else:
        st.error("Login failed")
        st.stop()

if 'token' not in st.session_state:
    st.error("Please login to view dashboard")
    st.stop()


def get_current_user_from_api():
    try:
        resp = requests.get(
            url=f"{API_BASE}/me/",
            headers={"Authorization": f"Bearer {st.session_state.token}"}
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        st.error(f"Authentication Error: {e.response.status_code} - {e.response.text}")
        if e.response.status_code == 401:
            st.error("Your session has expired or is invalid. Please log in again.")
            if 'token' in st.session_state:
                del st.session_state.token
        raise

try:
    user = get_current_user_from_api()
    userid = user['id']
except Exception as e:
    st.error(f"Failed to fetch user information: {str(e)}")
    st.stop()


def load_data(userid):
    with Session(engine) as session:
        rows = session.query(Features).filter(Features.userid == userid).all()
        data = pd.DataFrame([
            {
                "userid": f.userid,
                "datetime": f.date,  
                "total work": f.total_work_minutes,
                "total break": f.total_break_minutes,
                "context switch": f.context_switch_rate,
                "focus score": f.focus_score,
                "fatigue score": f.fatigue_score
            }
            for f in rows
        ])
    return data

df = load_data(userid)
if df.empty:
    st.info("No data available yet. Please check back later.")
    st.stop()

df['datetime'] = pd.to_datetime(df['datetime'])
df = df.sort_values('datetime')


today_data = df[df['datetime'].dt.date == df['datetime'].dt.date.max()]
today_focus = today_data['focus score'].mean()
today_fatigue = today_data['fatigue score'].mean()

if today_data['datetime'].dt.date.max() == date.today():
    st.subheader(f"Today's Metrics ({today_data['datetime'].dt.date.max()})")
else :
    st.subheader(f"Recent Metrics ({today_data['datetime'].dt.date.max()})")
st.metric(label="Focus Score", value=round(today_focus, 2))
st.metric(label="Fatigue Score", value=round(today_fatigue, 2))

if today_focus > 0.7 and today_fatigue > 0.6:
    st.warning("🔥 You're on fire but ⚠️ you might burn out — take a break!")
elif today_fatigue > 0.6:
    st.warning("⚠️ You might be burning out. Take a long break!")
elif today_focus > 0.7:
    st.success("🔥 You're killing it today! Keep the streak.")
else:
    st.info("📈 You worked okay—try reducing context switches.")


st.subheader("Work vs Break Minutes (Monthly)")
st.line_chart(df.set_index('datetime')[['total work', 'total break']])

st.subheader("Focus Trend (Monthly)")
st.line_chart(df.set_index('datetime')['focus score'])

st.subheader("Context Switch Trend (Monthly)")
st.line_chart(df.set_index('datetime')['context switch'])

st.subheader("Fatigue Trend (Monthly)")
st.line_chart(df.set_index('datetime')['fatigue score'])



df['date_only'] = df['datetime'].dt.normalize()

daily_df = df.groupby('date_only').agg({
    'total work': 'sum',
    'total break': 'sum',
    'context switch': 'mean',
    'focus score': 'mean',
    'fatigue score': 'mean'
}).reset_index()

daily_df = daily_df.rename(columns={'date_only': 'date'})


daily_df['date_str'] = daily_df['date'].dt.strftime('%Y-%m-%d')

st.subheader("Daily Summary (Aggregated)")

st.subheader('total work vs totak break')
st.line_chart(daily_df.set_index('date_str')[['total work', 'total break']])
st.subheader('focus score')
st.line_chart(daily_df.set_index('date_str')['focus score'])
st.subheader('context switch')
st.line_chart(daily_df.set_index('date_str')['context switch'])
st.subheader('fatigue score')
st.line_chart(daily_df.set_index('date_str')['fatigue score'])


with Session(engine) as session:

    accepted_feedback = session.query(Feedback).filter_by(userid=userid,accepted=True).order_by(Feedback.created_at.desc()).first()

    if not accepted_feedback:
        st.info("No accepted feedback found for AIS calculation.")
        st.stop()
    
    else:
        acepted_date = accepted_feedback.created_at.date()
        pre_features = session.query(Features).filter(Features.userid==userid,
                                                    Features.date >= acepted_date - timedelta(days=2),
                                                    Features.date <= acepted_date).all()
        
        post_features = session.query(Features).filter(Features.userid==userid,
                                                    Features.date <= acepted_date + timedelta(days=2),
                                                    Features.date >= acepted_date).all()
    

def calculate_metric(pre_values, post_values, label, positive_direction='increase'):
    """
    Computes % change and descriptive message.
    positive_direction: 'increase' if higher is better, 'decrease' if lower is better
    """
    import numpy as np
    
    avg_pre = np.mean(pre_values) if pre_values else 0
    avg_post = np.mean(post_values) if post_values else 0

    if avg_pre > 0:
        change = ((avg_post - avg_pre)/avg_pre) * 100
        if positive_direction == 'decrease':
            change = -change  
    else:
        change = 0

    if change >= 20:
        desc = f"✅ Strong Positive Impact\n{label} improved significantly after feedback."
    elif 5 <= change < 20:
        desc = f"🟡 Moderate Positive Impact\n{label} shows measurable improvement after feedback."
    elif -5 <= change < 5:
        desc = f"⚪ Neutral Impact\nNo meaningful change in {label} detected."
    else:
        desc = f"❌ Negative Impact\n{label} worsened after feedback. Strategy may need adjustment."

    return round(change, 2), desc


avg_focus_score, focus_desc = calculate_metric(
    [f.focus_score for f in pre_features],
    [f.focus_score for f in post_features],
    label='Focus',
    positive_direction='increase'
)

avg_fatigue_score, fatigue_desc = calculate_metric(
    [f.fatigue_score for f in pre_features],
    [f.fatigue_score for f in post_features],
    label='Fatigue',
    positive_direction='decrease'
)

avg_context_score, context_desc = calculate_metric(
    [f.context_switch_rate for f in pre_features],
    [f.context_switch_rate for f in post_features],
    label='Context Switching',
    positive_direction='decrease'
)

st.metric("AIS (Focus)", avg_focus_score)
st.info(focus_desc)

st.metric("Fatigue Score", avg_fatigue_score)
st.info(fatigue_desc)

st.metric("Context Switch Score", avg_context_score)
st.info(context_desc)

AES = round((avg_focus_score + avg_fatigue_score + avg_context_score)/3,2)
st.metric("Autopilot Effectiveness Score (AES)", AES)

