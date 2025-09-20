from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from uuid import UUID

class PatientRequest(BaseModel):
    """Esquema de requisição para pacientes, equivalente ao PatientRequest do Java"""
    email: str = Field(..., description="Email do paciente")
    name: str = Field(..., description="Nome do paciente")
    cpf: str = Field(..., description="CPF do paciente")
    password: str = Field(..., description="Senha do paciente")
    phone: Optional[str] = Field(None, description="Telefone do paciente")
    birthDate: Optional[str] = Field(None, alias="birthDate", description="Data de nascimento")

class PatientResponse(BaseModel):
    """Esquema de resposta para pacientes, equivalente ao PatientResponse do Java"""
    id: UUID
    email: str
    name: str
    cpf: str
    password: str
    phone: Optional[str] = None
    birthDate: Optional[str] = Field(None)

    model_config = ConfigDict(from_attributes=True)