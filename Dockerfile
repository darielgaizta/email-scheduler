FROM python:3.13.5-slim-bullseye

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Avoid Python output buffering
ENV PYTHONUNBUFFERED=1

CMD ["python", "run.py"]