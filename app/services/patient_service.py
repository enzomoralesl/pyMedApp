from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.patient import Patient
from app.schemas.patient import PatientRequest
import uuid
import logging

logger = logging.getLogger(__name__)

def create_patient(db: Session, patient_request: PatientRequest):
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
        db.commit()
        db.refresh(patient)
        logger.info(f"Paciente criado com sucesso: {patient.id}")
        return patient
    except IntegrityError as e:
        db.rollback()
        # Não lançar HTTPException manualmente para unicidade (email), deixar handler global tratar
        logger.error(f"Erro ao criar paciente: {str(e)}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Erro inesperado ao criar paciente: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

def get_patients(db: Session):
    try:
        return db.query(Patient).all()
    except Exception as e:
        logger.error(f"Erro ao buscar pacientes: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao buscar pacientes")

def get_patient_by_id(db: Session, patient_email: str):
    try:
        return db.query(Patient).filter(Patient.email == patient_email).first()
    except Exception as e:
        logger.error(f"Erro ao buscar paciente por Email: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao buscar paciente")

def update_patient(db: Session, patient_email: str, patient_request: PatientRequest):
    try:
        patient = db.query(Patient).filter(Patient.email == patient_email).first()
        if patient:
            patient.email = patient_request.email
            patient.name = patient_request.name
            patient.cpf = patient_request.cpf
            patient.password = patient_request.password
            patient.phone = patient_request.phone
            patient.birth_date = patient_request.birthDate
            db.commit()
            db.refresh(patient)
            logger.info(f"Paciente atualizado com sucesso: {patient.email}")
            return patient
        return None
    except IntegrityError as e:
        db.rollback()
        # Não lançar HTTPException manualmente para unicidade (email), deixar handler global tratar
        logger.error(f"Erro ao atualizar paciente: {str(e)}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Erro inesperado ao atualizar paciente: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

def delete_patient(db: Session, patient_email: str):
    try:
        patient = db.query(Patient).filter(Patient.email == patient_email).first()
        if patient:
            db.delete(patient)
            db.commit()
            logger.info(f"Paciente removido com sucesso: {patient_email}")
            return patient
        return None
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao remover paciente: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao remover paciente")
