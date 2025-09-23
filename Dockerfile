FROM python:3.12-alpine

# Define variáveis para não criar arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala ferramentas necessárias
RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-client \
    libffi-dev \
    openssl-dev \
    python3-dev \
    build-base

# Define o diretório de trabalho
# Copia e instala os requisitos primeiro (para melhor uso do cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

#COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 8081
CMD ["/app/start.sh"]
