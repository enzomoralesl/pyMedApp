from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.patient import Patient
from app.schemas.patient import PatientRequest
import uuid
import logging

logger = logging.getLogger(__name__)

async def create_patient(db: AsyncSession, patient_request: PatientRequest):
    try:
        patient = Patient(
            id=uuid.uuid4(),
            email=patient_request.email,
            name=patient_request.name,
            cpf=patient_request.cpf,
            password=patient_request.password,
            phone=patient_request.phone,
            birth_date=patient_request.birthDate
        )
        db.add(patient)
        await db.commit()
        await db.refresh(patient)
        logger.info(f"Paciente criado com sucesso: {patient.id}")
        return patient
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"Erro ao criar paciente: {str(e)}")
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Erro inesperado ao criar paciente: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

async def get_patients(db: AsyncSession):
    try:
        result = await db.execute(select(Patient))
        return result.scalars().all()
    except Exception as e:
        logger.error(f"Erro ao buscar pacientes: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao buscar pacientes")

async def get_patient_by_id(db: AsyncSession, patient_email: str):
    try:
        result = await db.execute(select(Patient).filter(Patient.email == patient_email))
        return result.scalars().first()
    except Exception as e:
        logger.error(f"Erro ao buscar paciente por Email: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao buscar paciente")

async def update_patient(db: AsyncSession, patient_email: str, patient_request: PatientRequest):
    try:
        result = await db.execute(select(Patient).filter(Patient.email == patient_email))
        patient = result.scalars().first()
        if patient:
            patient.email = patient_request.email
            patient.name = patient_request.name
            patient.cpf = patient_request.cpf
            patient.password = patient_request.password
            patient.phone = patient_request.phone
            patient.birth_date = patient_request.birthDate
            await db.commit()
            await db.refresh(patient)
            logger.info(f"Paciente atualizado com sucesso: {patient.email}")
            return patient
        return None
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"Erro ao atualizar paciente: {str(e)}")
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Erro inesperado ao atualizar paciente: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

async def delete_patient(db: AsyncSession, patient_email: str):
    try:
        result = await db.execute(select(Patient).filter(Patient.email == patient_email))
        patient = result.scalars().first()
        if patient:
            await db.delete(patient)
            await db.commit()
            logger.info(f"Paciente removido com sucesso: {patient_email}")
            return patient
        return None
    except Exception as e:
        await db.rollback()
        logger.error(f"Erro ao remover paciente: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao remover paciente")
