FROM python:3.11-slim

WORKDIR /app

# 1. Prevent Python from writing .pyc files & enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


# 2. Copy dependency definition first for caching

COPY requirements.txt .

# 3. Install dependencies without caching wheel packages locally

RUN pip install --no-cache-dir -r requirements.txt


#4 Create non root system user

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Copy the actual app source code

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
