FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN useradd -m appuser
USER appuser

EXPOSE 8080
CMD ["python", "app.py"]