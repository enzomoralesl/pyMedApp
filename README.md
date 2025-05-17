# PyMedApp - FastAPI Medical Application

PyMedApp é uma API RESTful desenvolvida com Python e FastAPI para gerenciar informações de pacientes. Este projeto é uma versão Python do aplicativo original MedApp desenvolvido em Java Spring Boot.

## Características

- API RESTful completa para gerenciar pacientes
- Estrutura modular e fácil de manter
- Persistência de dados usando PostgreSQL
- Gerenciamento de contêineres com Docker e Docker Compose
- Interface de administração de banco de dados com pgAdmin

## Requisitos

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Configuração e Execução

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/pymedapp.git
cd pymedapp
```

### 2. Inicie os serviços com Docker Compose

```bash
docker-compose up -d
```

Este comando iniciará:
- Servidor PostgreSQL na porta 5432
- pgAdmin na porta 16543 (interface web)
- A API PyMedApp na porta 8000

### 3. Acesse a API

A aplicação estará disponível em:
- API: http://localhost:8000
- Documentação Swagger: http://localhost:8000/docs
- Documentação ReDoc: http://localhost:8000/redoc

### 4. Acesse o pgAdmin (opcional)

- URL: http://localhost:16543
- Email: admin@admin.com
- Senha: 12345

## Estrutura do Projeto

```
pymedapp/
├── app/
│   ├── controllers/     # Controladores da API (endpoints)
│   ├── models/          # Modelos de dados (SQLAlchemy)
│   ├── schemas/         # Esquemas de validação (Pydantic)
│   └── services/        # Lógica de negócio
├── docker-compose.yml   # Configuração do Docker Compose
├── Dockerfile           # Configuração do contêiner Python
├── init.sql             # Script de inicialização do banco
├── main.py              # Ponto de entrada da aplicação
└── requirements.txt     # Dependências Python
```

## API Endpoints


### Pacientes (Patients)

- **GET /v1/patient**: Lista todos os pacientes
- **GET /v1/patient/{id}**: Obtém um paciente pelo ID
- **POST /v1/patient**: Cria um novo paciente
- **PUT /v1/patient/{id}**: Atualiza um paciente existente
- **DELETE /v1/patient/{id}**: Remove um paciente

## Exemplos de Uso

### Criar um novo paciente

```bash
curl -X 'POST' \
  'http://localhost:8000/v1/patient/' \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "paciente@exemplo.com",
    "name": "Maria Silva",
    "cpf": "123.456.789-00",
    "password": "senha123",
    "phone": "(11) 98765-4321",
    "birthDate": "1980-01-01"
  }'
```

## Parando os Serviços

Para parar todos os serviços:

```bash
docker-compose down
```

Para remover também os volumes (dados persistidos):

```bash
docker-compose down -v
```

## Desenvolvimento

### Executar localmente (sem Docker)

1. Instalar dependências:
```bash
pip install -r requirements.txt
```

2. Configurar variáveis de ambiente:
```bash
export POSTGRES_USER=user
export POSTGRES_PASSWORD=12345
export POSTGRES_DB=pyexampledb
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
```

3. Executar a aplicação:
```bash
uvicorn main:app --reload
```
