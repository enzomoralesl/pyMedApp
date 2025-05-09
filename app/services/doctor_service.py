from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorRequest
import uuid
import logging

# Configuração de logging
logger = logging.getLogger(__name__)

def create_doctor(db: Session, doctor_request: DoctorRequest):
    """
    Cria um novo médico no banco de dados.
    
    Args:
        db: Sessão do banco de dados
        doctor_request: Dados do médico a ser criado
    
    Returns:
        Doctor: Médico criado
        
    Raises:
        HTTPException: Se ocorrer algum erro ao criar o médico
    """
    try:
        doctor = Doctor(
            id=uuid.uuid4(),
            name=doctor_request.name,
            specialty=doctor_request.specialty,
            crm=doctor_request.crm
        )
        db.add(doctor)
        db.commit()
        db.refresh(doctor)
        logger.info(f"Médico criado com sucesso: {doctor.id}")
        return doctor
    except IntegrityError as e:
        db.rollback()
        if 'uq_doctor_crm' in str(e):
            raise HTTPException(status_code=400, detail="CRM já cadastrado")
        logger.error(f"Erro ao criar médico: {str(e)}")
        raise HTTPException(status_code=400, detail="Erro ao criar médico")
    except Exception as e:
        db.rollback()
        logger.error(f"Erro inesperado ao criar médico: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

def get_doctors(db: Session):
    """
    Recupera todos os médicos do banco de dados.
    
    Args:
        db: Sessão do banco de dados
    
    Returns:
        list[Doctor]: Lista de médicos encontrados
    """
    try:
        return db.query(Doctor).all()
    except Exception as e:
        logger.error(f"Erro ao buscar médicos: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao buscar médicos")

def get_doctor_by_id(db: Session, doctor_id: uuid.UUID):
    """
    Recupera um médico pelo ID.
    
    Args:
        db: Sessão do banco de dados
        doctor_id: ID do médico a ser recuperado
    
    Returns:
        Doctor: Médico encontrado ou None se não encontrado
    """
    try:
        return db.query(Doctor).filter(Doctor.id == doctor_id).first()
    except Exception as e:
        logger.error(f"Erro ao buscar médico por ID: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao buscar médico")

def update_doctor(db: Session, doctor_id: uuid.UUID, doctor_request: DoctorRequest):
    """
    Atualiza um médico existente.
    
    Args:
        db: Sessão do banco de dados
        doctor_id: ID do médico a ser atualizado
        doctor_request: Novos dados do médico
    
    Returns:
        Doctor: Médico atualizado ou None se não encontrado
        
    Raises:
        HTTPException: Se ocorrer algum erro ao atualizar o médico
    """
    try:
        doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
        if doctor:
            doctor.name = doctor_request.name
            doctor.specialty = doctor_request.specialty
            doctor.crm = doctor_request.crm
            db.commit()
            db.refresh(doctor)
            logger.info(f"Médico atualizado com sucesso: {doctor.id}")
            return doctor
        return None
    except IntegrityError as e:
        db.rollback()
        if 'uq_doctor_crm' in str(e):
            raise HTTPException(status_code=400, detail="CRM já cadastrado")
        logger.error(f"Erro ao atualizar médico: {str(e)}")
        raise HTTPException(status_code=400, detail="Erro ao atualizar médico")
    except Exception as e:
        db.rollback()
        logger.error(f"Erro inesperado ao atualizar médico: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

def delete_doctor(db: Session, doctor_id: uuid.UUID):
    """
    Remove um médico do banco de dados.
    
    Args:
        db: Sessão do banco de dados
        doctor_id: ID do médico a ser removido
    
    Returns:
        Doctor: Médico removido ou None se não encontrado
        
    Raises:
        HTTPException: Se ocorrer algum erro ao remover o médico
    """
    try:
        doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
        if doctor:
            db.delete(doctor)
            db.commit()
            logger.info(f"Médico removido com sucesso: {doctor_id}")
            return doctor
        return None
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao remover médico: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao remover médico")
