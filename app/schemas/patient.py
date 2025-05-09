from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class PatientRequest(BaseModel):
    """Esquema de requisição para pacientes, equivalente ao PatientRequest do Java"""
    email: str = Field(..., description="Email do paciente")
    name: str = Field(..., description="Nome do paciente")
    cpf: str = Field(..., description="CPF do paciente")
    password: str = Field(..., description="Senha do paciente")
    phone: Optional[str] = Field(None, description="Telefone do paciente")
    birth_date: Optional[str] = Field(None, alias="birthDate", description="Data de nascimento")

    model_config = {
        "populate_by_name": True,
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "email": "paciente@exemplo.com",
                "name": "Maria Silva",
                "cpf": "12345678901",
                "password": "senha123",
                "phone": "(11) 98765-4321",
                "birthDate": "1980-01-01"
            }
        }
    }

class PatientResponse(BaseModel):
    """Esquema de resposta para pacientes, equivalente ao PatientResponse do Java"""
    id: UUID
    email: str
    name: str
    cpf: str
    password: str
    phone: Optional[str] = None
    birth_date: Optional[str] = Field(None, alias="birthDate")

    model_config = {
        "populate_by_name": True,
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "email": "paciente@exemplo.com",
                "name": "Maria Silva",
                "cpf": "12345678901",
                "password": "senha123",
                "phone": "(11) 98765-4321",
                "birthDate": "1980-01-01"
            }
        }
    }
