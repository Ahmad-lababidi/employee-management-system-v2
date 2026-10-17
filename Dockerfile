FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY frontend/frontend.py ./frontend.py
COPY config.py ./

EXPOSE 8501
CMD ["streamlit", "run", "frontend.py", "--server.address=0.0.0.0", "--server.port=8501"]
