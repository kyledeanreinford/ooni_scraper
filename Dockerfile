FROM python:3.12-slim

WORKDIR /workspace

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py app.py

CMD ["python", "/workspace/app.py"]