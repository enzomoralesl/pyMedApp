from sqlalchemy import Column, String, Table, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class Doctor(Base):
    """Modelo para a tabela de médicos, equivalente ao JPADoctorEntity do Java"""
    __tablename__ = "tb_doctor"
    __table_args__ = (
        UniqueConstraint('crm', name='uq_doctor_crm'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    specialty = Column(String(255), nullable=False)
    crm = Column(String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"<Doctor(id={self.id}, crm={self.crm}, name={self.name})>"
