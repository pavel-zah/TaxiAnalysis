FROM python:3.11-slim

WORKDIR /

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app
COPY . /app/

ENV PYTHONPATH=/

CMD ["python", "/app/main.py"]