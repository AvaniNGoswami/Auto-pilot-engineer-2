# 🚀Auto-pilot-engineer
Auto-Pilot Engineer is an semi autonomous AI co-pilot that observes developer work patterns, learns personal productivity trends, and provides actionable suggestions to improve focus and prevent burnout — all without surveillance or micromanagement.

One-line pitch:
Auto-Pilot Engineer collects developer activity metadata, predicts productivity and fatigue levels, and provides suggestions and explanations to help developers work smarter, not longer.

Why This Project Exists
Modern developers face:
- Long working hours
- Constant context switching
- Burnout masked as "productivity"
- Tools that track time, not cognitive effectiveness
  
What’s broken today:
Tool Type	                Problem
Time trackers	       Surveillance, not insight
To-do apps	           Static, not adaptive
Productivity apps	   Generic advice
Managers	           Guess productivity
No existing system understands how developers actually work. Auto-Pilot Engineer is designed to learn behavioural patterns, not just count hours.

## 🎯 What Auto-Pilot Engineer Does
Auto-Pilot Engineer acts as a silent AI co-pilot that:

1.	Observes work patterns (metadata only)
-	Collects GitHub activity events via webhooks.
-	Collects developer activity metadata via GitHub API:
	 - Commits
	 - Timestamps
 	 - Activity frequency
-   Manual session tracker for:
	 - Work start / end
 	 - Break / work tracking
-	No code or private content is accessed; all data is opt-in.
2.	Learns productivity trends
-	Uses features like session length, break frequency, context switching, and fatigue score to train ML models.
-	Predicts:
     - Productivity score
     - Burnout/fatigue risk
	 - Outputs Low / Medium / High burnout risk and fatigue trends.
4.	Agentic decision layer (autonomous core)
-	Observer Agent -> gathers recent activity features
-	Analyzer Agent -> predicts productivity & burnout
-	Intervention Agent -> generates actionable suggestions using rules and feedback
-	Orchestrator -> runs the pipeline when Suggestion API is called
5.	Provides explainable suggestions
-	Suggestion API triggers actionable advice.
-	Explanation API returns human-readable rationale:
	 - Template-based explanation 
	 - Future support for local or API-based LLMs
6.	Stores user feedback
-	Users can accept/reject suggestions and provide ratings (0–5 stars).
-	Feedback is stored in the database and can be used to improve future versions.
-	Currently, ML models are not retrained in real-time, but feedback informs agent decisions.
What it does NOT do:
-	❌ Spy on keystrokes
-	❌ Read code or private content
-	❌ Force schedules
-	❌ Punish breaks

### 👥 Target Users
Primary:
-	Remote developers
-	Freelancers
-	Students / interns
-	Startup engineers
Secondary (Optional):
-	Team leads (aggregated insights only)
-	Remote-first companies (opt-in)

### System Architecture (High-Level)

<img width="1570" height="511" alt="image" src="https://github.com/user-attachments/assets/f2bf1ad0-0de2-4075-a8bf-0483e1ac60b6" />



- Developer Activity
- Signal Extraction (GitHub + manual session start / end)
- feature engineering pipeline to compute features at a specified interval of time
- Pattern Learning (ML)
- Agentic Reasoning (Observer → Analyzer → Intervention → Orchestrator)
- Action / Suggestion
- Feedback Storage & Future Learning
- In - Out API to record the session 
  
This loop operates continuously whenever APIs are called.

### 🧩 Core Modules
1.	Activity Signal Collector
-	Collects metadata (GitHub commits, session start/end, breaks, time of day,).
-	All data is opt-in.
2.	Productivity Pattern Engine (ML Brain)
-	Trains models for productivity and burnout risk.
-	Inputs: work duration, breaks, context switches, fatigue scores.
-	Outputs: personalized productivity and burnout predictions.
3.	Burnout & Risk Detection
-	Uses ML predictions to assess fatigue trends.
-	Outputs Low / Medium / High burnout risk.
4.	Agentic Decision Layer
-	Orchestrates Observer, Analyzer, and Intervention agents.
-	Suggestion API triggers agentic reasoning for actionable guidance.
5.	Explanation Engine
-	Returns template-based, human-readable explanations.
-	Optional embeddings for context; LLM integration is planned.
6.	Feedback System
-	Feedback is recorded with acceptance and rating.

## 🖥️ What Users See

Dashboard Overview

The dashboard provides developers with a real-time view of productivity, fatigue, and the impact of Auto-Pilot suggestions.

Login:
- Users enter their email to access personalized metrics (token-based authentication).
Today's Metrics:
- Focus Score – average focus for the current day.
- Fatigue Score – average fatigue for the current day.
- Contextual Advice: Smart messages based on focus and fatigue, e.g.:
	    -“🔥 You're killing it today! Keep the streak.”
        -“⚠️ You might be burning out. Take a long break!”
        -“📈 Work okay — try reducing context switches.”
monthy Trends (Line Charts):
- Work vs Break Minutes – visualize balance between work sessions and breaks.
- Focus Trend – track focus score.
- Context Switch Trend – monitor interruptions and task switching.
- Fatigue Trend – track fatigue accumulation.
Daily Summary (Aggregated):
- Total work vs break minutes per day
- Average focus score per day
- Average fatigue score per day
- Average context switch rate per day
Autopilot Effectiveness Score (AES):
- Measures the impact of agent suggestions over time by comparing metrics before and after accepted suggestions.
- Includes: Focus, Fatigue, Context Switching
- Displays % change and descriptive insights:
	   - ✅ Strong Positive Impact
       - 🟡 Moderate Positive Impact
       - ⚪ Neutral Impact
       - ❌ Negative Impact

### Interactive Features:
- Metrics update dynamically using SQLAlchemy queries from the database.
- Charts and AES help users understand trends and the effectiveness of Auto-Pilot guidance.

### Smart Suggestion:
- “You're doing okay, maintain rhythm.
- “Low productivity — try a 25-minute-deep work sprint.
- No spam; only high-signal interventions.

## 🛠️ Tech Stack
Backend: FastAPI, SQLAlchemy / SQLModel, PostgreSQL, JWT Auth
ML / Data: Pandas, NumPy, scikit-learn, Feature engineering
AI / NLP : Sentence Transformers
Dashboard: Streamlit 
DevOps (Optional): Docker, Docker Compose

### 🧪 Features Implemented
- Activity logging API (GitHub + manual session start / end events)
- Feature engineering pipeline
- ML models for productivity and burnout
- Agent-based decision logic
- Suggestion API
- Explanation API
- Feedback storage
- Interactive dashboard
- In - Out API to start and end seesion

### 🚦 Project Status
- ✅ Core backend implemented
- ✅ ML models integrated
- ✅ Agentic decision layer working (API-triggered)
- ✅ Dashboard available
- ⚠️ Docker support optional / under improvement

## 🧰 Local Setup (Without Docker)
### Clone repo
git clone https://github.com/AvaniNGoswami/Auto-pilot-engineer.git
cd auto-pilot-engineer

### Create virtual environment
- python -m venv venv
- source venv/bin/activate  # Windows: venv\Scripts\activate

### Install dependencies
pip install -r requirements.txt

### Configure environment
cp .env.example .env

### Run server
- uvicorn app.main:app --reload

### 🐳 Docker (Optional)
- Docker support is under improvement due to ML dependencies.
- docker-compose up --build

### 🧠 What This Project Proves
- Systems-level thinking
- Human-centered AI design
- Personalized ML modeling
- Agentic AI architecture
- Full-stack backend engineering
- Explainable AI

### ⚖️ Ethics & Privacy
- Opt-in data collection only
- Metadata-based, no content inspection
- Explainable decisions
- User-controlled feedback

### 📈 Future Enhancements
- Reinforcement learning for adaptive suggestions
- Team-level anonymized insights
- Advanced time-series models
________________________________________
👤 Author
Avani N. Goswami :

AI / Backend Developer
________________________________________
⭐ Final Note
Auto-Pilot Engineer helps developers work smarter, not longer, by understanding behaviour and acting only when it truly matters. This is a systems-level AI project demonstrating full-stack engineering, ML modeling, and agentic decision design.
