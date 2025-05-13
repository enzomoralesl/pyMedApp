from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class APIErrorResponse(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
    statusCode: int
    status: str
    message: str
    errorDetails: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%S")
        }
        schema_extra = {
            "example": {
                "timestamp": "2024-05-12T15:30:00",
                "statusCode": 400,
                "status": "BAD_REQUEST",
                "message": "Campo obrigatório ausente",
                "errorDetails": "Header X-Token ausente"
            }
        }
