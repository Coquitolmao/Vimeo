FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia el código real (está en /app/app)
COPY app ./app

# (si usas scripts)
COPY docker/run_all.sh ./run_all.sh
COPY docker/set_env_secrets.sh ./set_env_secrets.sh
RUN chmod +x ./run_all.sh ./set_env_secrets.sh

EXPOSE 8000
CMD ["sh","-c","uvicorn app.main:app --host 0.0.0.0 --port 8000"]
