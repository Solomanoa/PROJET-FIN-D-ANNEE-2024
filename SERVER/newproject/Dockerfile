FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libboost-all-dev \
    libgtk2.0-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    python3-dev \
    libzbar0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Créer le dossier de travail
WORKDIR /app

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y libzbar-dev

RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Commande de démarrage
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
