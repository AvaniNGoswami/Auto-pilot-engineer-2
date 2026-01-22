import streamlit as st
import pandas as pd
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.database import engine
from sqlalchemy.orm import Session
from app.models.features import Features
import requests
 



st.set_page_config(page_title="Productivity dashboard", layout="wide")


API_BASE = "http://127.0.0.1:8000"

def login_user(email):
    resp = requests.post(url=f"{API_BASE}/auth/login",params={"email":email})
    if resp.status_code !=200:
        return None
    return resp.json()['access_token']

st.title("Login for Dashboard")

email = st.text_input("enter email")
if st.button('Login'):
    token = login_user(email)
    if token:
        st.session_state.token = token
        st.rerun()
    else:
        st.error('Login failed')
        st.stop()


if 'token' not in st.session_state:
    st.error('please login')
    st.stop()


def get_current_user_from_api():
    resp = requests.get(url=f"{API_BASE}/me",headers={"Authorization": f"Bearer {st.session_state.token}"})
    resp.raise_for_status()
    return resp.json()


def load_data(userid):
    with Session(engine) as session:
        rows = session.query(Features).filter(Features.userid==userid).all()
        data = pd.DataFrame([
    {
        "userid": f.userid,
        "date": f.date,
        "total work": f.total_work_minutes,
        "total break": f.total_break_minutes,
        "context switch": f.context_switch_rate,
        "focus score": f.focus_score,
        "fatigue score": f.fatigue_score
    }
    for f in rows
    ])

    return data


user = get_current_user_from_api()
userid = user['id']



df = load_data(userid=userid)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')


st.subheader("Work vs Break minutes")
st.line_chart(df.set_index('date')[['total work','total break']])

st.subheader('Focus trend')
st.line_chart(df.set_index('date')['focus score'])

st.subheader('Context switch')
st.line_chart(df.set_index('date')['context switch'])

st.subheader('fatigue trend')
st.line_chart(df.set_index('date')['fatigue score'])


today = df.iloc[-1]
st.metric(label='todays focus score',value=round(today['focus score'],2),delta=None)

if today['focus score'] > 0.7 and today['fatigue score'] > 0.6:
    st.warning("🔥 You're on fire but ⚠️ you might burn out — take a break!")
elif today['fatigue score'] > 0.6:
    st.warning("⚠️ You might be burning out. Take a long break!")
elif today['focus score'] > 0.7:
    st.success("🔥 You're killing it today! Keep the streak.")
else:
    st.info("📈 You worked okay—try reducing context switches.")
