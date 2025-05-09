from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.doctor import DoctorRequest, DoctorResponse
from app.services.doctor_service import create_doctor, get_doctors, get_doctor_by_id, delete_doctor, update_doctor
from uuid import UUID
import logging

# Configuração de logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/doctors", tags=["Doctors"])

@router.post("/", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
async def create(doctor_request: DoctorRequest, response: Response, db: Session = Depends(get_db)):
    """
    Cria um novo médico
    
    Args:
        doctor_request: Dados do médico a ser criado
        db: Sessão do banco de dados
        
    Returns:
        DoctorResponse: Médico criado
    """
    try:
        doctor = create_doctor(db, doctor_request)
        response.status_code = status.HTTP_201_CREATED
        logger.info(f"Médico criado: {doctor.id}")
        # Criar um dicionário explicitamente a partir do objeto Doctor para garantir a validação do modelo
        return DoctorResponse(
            id=doctor.id,
            name=doctor.name,
            specialty=doctor.specialty,
            crm=doctor.crm
        )
    except HTTPException as e:
        logger.warning(f"Erro ao criar médico: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Erro inesperado ao criar médico: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")

@router.get("/", response_model=list[DoctorResponse])
async def read_all(db: Session = Depends(get_db)):
    """
    Recupera todos os médicos
    
    Args:
        db: Sessão do banco de dados
        
    Returns:
        list[DoctorResponse]: Lista de médicos
    """
    try:
        doctors = get_doctors(db)
        return [
            DoctorResponse(
                id=doctor.id,
                name=doctor.name,
                specialty=doctor.specialty,
                crm=doctor.crm
            ) for doctor in doctors
        ]
    except HTTPException as e:
        logger.warning(f"Erro ao buscar médicos: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar médicos: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")

@router.get("/{doctor_id}", response_model=DoctorResponse)
async def read(doctor_id: UUID, db: Session = Depends(get_db)):
    """
    Recupera um médico pelo ID
    
    Args:
        doctor_id: ID do médico
        db: Sessão do banco de dados
        
    Returns:
        DoctorResponse: Médico encontrado
        
    Raises:
        HTTPException: Se o médico não for encontrado
    """
    try:
        doctor = get_doctor_by_id(db, doctor_id)
        if not doctor:
            logger.warning(f"Médico não encontrado: {doctor_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Médico não encontrado")
        return DoctorResponse(
            id=doctor.id,
            name=doctor.name,
            specialty=doctor.specialty,
            crm=doctor.crm
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar médico: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")

@router.put("/{doctor_id}", response_model=DoctorResponse)
async def update(doctor_id: UUID, doctor_request: DoctorRequest, db: Session = Depends(get_db)):
    """
    Atualiza um médico existente
    
    Args:
        doctor_id: ID do médico a ser atualizado
        doctor_request: Novos dados do médico
        db: Sessão do banco de dados
        
    Returns:
        DoctorResponse: Médico atualizado
        
    Raises:
        HTTPException: Se o médico não for encontrado ou ocorrer algum erro
    """
    try:
        doctor = update_doctor(db, doctor_id, doctor_request)
        if not doctor:
            logger.warning(f"Médico não encontrado para atualização: {doctor_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Médico não encontrado")
        logger.info(f"Médico atualizado: {doctor_id}")
        return DoctorResponse(
            id=doctor.id,
            name=doctor.name,
            specialty=doctor.specialty,
            crm=doctor.crm
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Erro inesperado ao atualizar médico: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")

@router.delete("/{doctor_id}", response_model=DoctorResponse)
async def delete(doctor_id: UUID, db: Session = Depends(get_db)):
    """
    Remove um médico
    
    Args:
        doctor_id: ID do médico a ser removido
        db: Sessão do banco de dados
        
    Returns:
        DoctorResponse: Médico removido
          Raises:
        HTTPException: Se o médico não for encontrado ou ocorrer algum erro
    """
    try:
        doctor = delete_doctor(db, doctor_id)
        if not doctor:
            logger.warning(f"Médico não encontrado para exclusão: {doctor_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Médico não encontrado")
        logger.info(f"Médico removido: {doctor_id}")
        return DoctorResponse(
            id=doctor.id,
            name=doctor.name,
            specialty=doctor.specialty,
            crm=doctor.crm
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Erro inesperado ao remover médico: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")
