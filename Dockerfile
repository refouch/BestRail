FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installer les packages
COPY requirements.txt .
RUN pip install \
    --no-cache-dir \
    --default-timeout=200 \
    -r requirements.txt

COPY . .

EXPOSE 8000

# Run l'appli
CMD ["uvicorn", "server-fastapi.final_server:app", "--host", "0.0.0.0", "--port", "8000"]
