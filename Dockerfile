FROM python:3.11-slim

# Define variáveis para não criar arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala ferramentas necessárias
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
# Copia e instala os requisitos primeiro (para melhor uso do cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Cria script de espera pelo banco de dados
COPY start.sh .
RUN chmod +x /app/start.sh

# Expõe a porta da aplicação
EXPOSE 8081

# Comando para iniciar a aplicação
CMD ["/app/start.sh"]
