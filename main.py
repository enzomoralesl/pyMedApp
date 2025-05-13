from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.doctor_controller import router as doctor_router
from app.controllers.patient_controller import router as patient_router
from app.database import create_tables
import uvicorn

# Criação da aplicação FastAPI
app = FastAPI(
    title="PyMedApp API",
    description="API para gerenciamento de pacientes e médicos",
    version="1.0.0"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restrinja às origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Eventos de inicialização e encerramento
@app.on_event("startup")
async def startup_event():
    """Evento executado na inicialização da aplicação"""
    # Cria todas as tabelas definidas nos modelos
    create_tables()
    print("✅ Banco de dados inicializado com sucesso!")

# Inclusão dos routers
app.include_router(doctor_router)
app.include_router(patient_router)

# Rota raiz
@app.get("/")
def read_root():
    """Rota raiz da API"""
    return {
        "message": "Bem-vindo à PyMedApp API!",
        "docs": "/docs",
        "endpoints": {
            "doctors": "/v1/doctor",
            "patients": "/v1/patient"
        }
    }

# Inicialização condicional para execução direta (não via Docker)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
