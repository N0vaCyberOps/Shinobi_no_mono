# Użyj pełnego obrazu Pythona 3.11
FROM python:3.11

# Zapobiegaj tworzeniu plików .pyc w kontenerze
ENV PYTHONDONTWRITEBYTECODE=1

# Wyłącz buforowanie dla łatwiejszego logowania w kontenerze
ENV PYTHONUNBUFFERED=1

# Skopiuj plik requirements.txt do kontenera
COPY requirements.txt .

# Zainstaluj zależności Pythona
RUN python -m pip install --no-cache-dir -r requirements.txt

# Ustaw katalog roboczy na /app
WORKDIR /app

# Skopiuj cały projekt do kontenera
COPY . /app

# Utwórz użytkownika bez uprawnień roota dla zwiększenia bezpieczeństwa
RUN adduser --uid 5678 --disabled-password --gecos "" appuser && \
    chown -R appuser /app

# Przełącz się na użytkownika appuser
USER appuser

# Ustaw domyślną komendę uruchamiającą aplikację
CMD ["uvicorn", "core.api:app", "--host", "0.0.0.0", "--port", "8000"]
FROM python:3.11-slim


# Skopiuj CAŁY projekt do kontenera (łącznie z podkatalogami)
COPY . /app             # Ważne: kropka oznacza bieżący katalog