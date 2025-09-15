from sqlalchemy import Column, String, Table, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class Patient(Base):
    """Modelo para a tabela de pacientes, equivalente ao JPAPatientEntity do Java"""
    __tablename__ = "tb_patient"
    __table_args__ = (
        UniqueConstraint('email', name='uq_patient_email')
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    cpf = Column(String(11), nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    birth_date = Column(String(15), nullable=True)

    def __repr__(self):
        return f"<Patient(id={self.id}, email={self.email}, name={self.name})>"
