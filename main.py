import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.patient_controller import router as patient_router
from app.database import create_tables
from app.exception_handler import add_exception_handlers
import uvicorn
from fastapi.responses import ORJSONResponse


app = FastAPI(
    title="PyMedApp API",
    description="API para gerenciamento de pacientes",
    version="1.0.0",
    default_response_class=ORJSONResponse,
)

add_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Cria todas as tabelas definidas nos modelos

    await create_tables()
    print("Banco de dados inicializado com sucesso!")
    running_env = os.getenv("RUNNING_ENV", "local")
    if running_env == "docker":
        print("Aplicação iniciada no Docker")
    else:
        print("Aplicação iniciada localmente")

app.include_router(patient_router)

@app.get("/")
def read_root():
    return {
        "message": "Bem-vindo à PyMedApp API!",
        "docs": "/docs",
        "endpoints": {
            "patients": "/v1/patient"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0", 
        port=8081,
        workers=5,
        loop="uvloop",
        http="httptools"
    )
