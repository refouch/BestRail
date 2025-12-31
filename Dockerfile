FROM python:3.12-slim

# Dossier du code python dans l'image
WORKDIR /app

# Eviter les caches .pyc de fichiers .py
ENV PYTHONDONTWRITEBYTECODE=1
# Récupérer logs en temps réel
ENV PYTHONUNBUFFERED=1

# Installer les packages
COPY requirements.txt .
RUN pip install \
    --no-cache-dir \
    --default-timeout=200 \
    -r requirements.txt

# Ajouter tous le code à l'image
COPY . .

EXPOSE 8000

# Commandes à l'instanciation
CMD ["uvicorn", "server-fastapi.final_server:app", "--host", "0.0.0.0", "--port", "8000"]
