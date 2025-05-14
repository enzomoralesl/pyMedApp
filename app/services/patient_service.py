from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.patient import Patient
from app.schemas.patient import PatientRequest
import uuid
import logging

# Configuração de logging
logger = logging.getLogger(__name__)

def create_patient(db: Session, patient_request: PatientRequest):
    """
    Cria um novo paciente no banco de dados.
    
    Args:
        db: Sessão do banco de dados
        patient_request: Dados do paciente a ser criado
    
    Returns:
        Patient: Paciente criado
        
    Raises:
        HTTPException: Se ocorrer algum erro ao criar o paciente
    """
    try:
        patient = Patient(
            id=uuid.uuid4(),
            email=patient_request.email,
            name=patient_request.name,
            cpf=patient_request.cpf,
            password=patient_request.password,
            phone=patient_request.phone,
            birth_date=patient_request.birth_date
        )
        db.add(patient)
        db.commit()
        db.refresh(patient)
        logger.info(f"Paciente criado com sucesso: {patient.id}")
        return patient
    except IntegrityError as e:
        db.rollback()
        # Não lançar HTTPException manualmente para unicidade (email/cpf), deixar handler global tratar
        logger.error(f"Erro ao criar paciente: {str(e)}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Erro inesperado ao criar paciente: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

def get_patients(db: Session):
    """
    Recupera todos os pacientes do banco de dados.
    
    Args:
        db: Sessão do banco de dados
    
    Returns:
        list[Patient]: Lista de pacientes encontrados
    """
    try:
        return db.query(Patient).all()
    except Exception as e:
        logger.error(f"Erro ao buscar pacientes: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao buscar pacientes")

def get_patient_by_id(db: Session, patient_id: uuid.UUID):
    """
    Recupera um paciente pelo ID.
    
    Args:
        db: Sessão do banco de dados
        patient_id: ID do paciente a ser recuperado
    
    Returns:
        Patient: Paciente encontrado ou None se não encontrado
    """
    try:
        return db.query(Patient).filter(Patient.id == patient_id).first()
    except Exception as e:
        logger.error(f"Erro ao buscar paciente por ID: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao buscar paciente")

def update_patient(db: Session, patient_id: uuid.UUID, patient_request: PatientRequest):
    """
    Atualiza um paciente existente.
    
    Args:
        db: Sessão do banco de dados
        patient_id: ID do paciente a ser atualizado
        patient_request: Novos dados do paciente
    
    Returns:
        Patient: Paciente atualizado ou None se não encontrado
        
    Raises:
        HTTPException: Se ocorrer algum erro ao atualizar o paciente
    """
    try:
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if patient:
            patient.email = patient_request.email
            patient.name = patient_request.name
            patient.cpf = patient_request.cpf
            patient.password = patient_request.password
            patient.phone = patient_request.phone
            patient.birth_date = patient_request.birth_date
            db.commit()
            db.refresh(patient)
            logger.info(f"Paciente atualizado com sucesso: {patient.id}")
            return patient
        return None
    except IntegrityError as e:
        db.rollback()
        # Não lançar HTTPException manualmente para unicidade (email/cpf), deixar handler global tratar
        logger.error(f"Erro ao atualizar paciente: {str(e)}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Erro inesperado ao atualizar paciente: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

def delete_patient(db: Session, patient_id: uuid.UUID):
    """
    Remove um paciente do banco de dados.
    
    Args:
        db: Sessão do banco de dados
        patient_id: ID do paciente a ser removido
    
    Returns:
        Patient: Paciente removido ou None se não encontrado
        
    Raises:
        HTTPException: Se ocorrer algum erro ao remover o paciente
    """
    try:
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if patient:
            db.delete(patient)
            db.commit()
            logger.info(f"Paciente removido com sucesso: {patient_id}")
            return patient
        return None
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao remover paciente: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao remover paciente")
