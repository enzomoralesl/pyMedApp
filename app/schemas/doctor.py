from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class DoctorRequest(BaseModel):
    """Esquema de requisição para médicos, equivalente ao DoctorRequest do Java"""
    name: str = Field(..., description="Nome do médico")
    specialty: str = Field(..., description="Especialidade médica")
    crm: str = Field(..., description="Registro no Conselho Regional de Medicina")
    
    model_config = {
        "populate_by_name": True,
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "name": "Dr. José Silva",
                "specialty": "Cardiologia",
                "crm": "12345-SP"
            }
        }
    }

class DoctorResponse(BaseModel):
    """Esquema de resposta para médicos, equivalente ao DoctorResponse do Java"""
    id: UUID
    name: str
    specialty: str
    crm: str
    
    model_config = {
        "populate_by_name": True,
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "name": "Dr. José Silva",
                "specialty": "Cardiologia",
                "crm": "12345-SP"
            }
        }
    }
