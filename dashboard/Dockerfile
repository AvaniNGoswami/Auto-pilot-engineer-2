FROM python:3.10

WORKDIR /app


RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY dashboard/ ./dashboard
COPY app/ ./app


EXPOSE 8501


ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501


CMD ["streamlit", "run", "dashboard/Dashboard.py"]
