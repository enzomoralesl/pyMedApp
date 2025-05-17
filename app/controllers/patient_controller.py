from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.patient import PatientRequest, PatientResponse
from app.services.patient_service import create_patient, get_patients, get_patient_by_id, delete_patient, update_patient
from uuid import UUID
import logging

# Configuração de logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/patient", tags=["Patients"])

@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create(patient_request: PatientRequest, response: Response, db: Session = Depends(get_db)):
    """
    Cria um novo paciente
    
    Args:
        patient_request: Dados do paciente a ser criado
        response: Objeto de resposta
        db: Sessão do banco de dados
        
    Returns:
        PatientResponse: Paciente criado
    """
    try:
        patient = create_patient(db, patient_request)
        response.status_code = status.HTTP_201_CREATED
        logger.info(f"Paciente criado: {patient.id}")
        return PatientResponse(
            id=patient.id,
            email=patient.email,
            name=patient.name,
            cpf=patient.cpf,
            password=patient.password,
            phone=patient.phone,
            birth_date=patient.birth_date
        )
    except HTTPException as e:
        logger.warning(f"Erro ao criar paciente: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Erro inesperado ao criar paciente: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")

@router.get("/", response_model=list[PatientResponse])
async def read_all(db: Session = Depends(get_db)):
    """
    Recupera todos os pacientes
    
    Args:
        db: Sessão do banco de dados
        
    Returns:
        list[PatientResponse]: Lista de pacientes
    """
    try:
        patients = get_patients(db)
        return [
            PatientResponse(
                id=patient.id,
                email=patient.email,
                name=patient.name,
                cpf=patient.cpf,
                password=patient.password,
                phone=patient.phone,
                birth_date=patient.birth_date
            ) for patient in patients
        ]
    except HTTPException as e:
        logger.warning(f"Erro ao buscar pacientes: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar pacientes: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")

@router.get("/{patient_id}", response_model=PatientResponse)
async def read(patient_id: UUID, db: Session = Depends(get_db)):
    """
    Recupera um paciente pelo ID
    
    Args:
        patient_id: ID do paciente
        db: Sessão do banco de dados
        
    Returns:
        PatientResponse: Paciente encontrado
        
    Raises:
        HTTPException: Se o paciente não for encontrado
    """
    try:
        patient = get_patient_by_id(db, patient_id)
        if not patient:
            logger.warning(f"Paciente não encontrado: {patient_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")
        return PatientResponse(
            id=patient.id,
            email=patient.email,
            name=patient.name,
            cpf=patient.cpf,
            password=patient.password,
            phone=patient.phone,
            birth_date=patient.birth_date
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar paciente: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")

@router.put("/{patient_email}", response_model=PatientResponse)
async def update(patient_email: str, patient_request: PatientRequest, db: Session = Depends(get_db)):
    """
    Atualiza um paciente existente
    Args:
        patient_email: Email do paciente a ser atualizado
        patient_request: Novos dados do paciente
        db: Sessão do banco de dados
    Returns:
        PatientResponse: Paciente atualizado
    Raises:
        HTTPException: Se o paciente não for encontrado ou ocorrer algum erro
    """
    try:
        patient = update_patient(db, patient_email, patient_request)
        if not patient:
            logger.warning(f"Paciente não encontrado para atualização: {patient_email}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")
        logger.info(f"Paciente atualizado: {patient}")
        return PatientResponse(
            id=patient.id,
            email=patient.email,
            name=patient.name,
            cpf=patient.cpf,
            password=patient.password,
            phone=patient.phone,
            birth_date=patient.birth_date
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Erro inesperado ao atualizar paciente: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")

@router.delete("/{patient_id}", response_model=PatientResponse)
async def delete(patient_id: UUID, db: Session = Depends(get_db)):
    """
    Remove um paciente
    
    Args:
        patient_id: ID do paciente a ser removido
        db: Sessão do banco de dados
        
    Returns:
        PatientResponse: Paciente removido
        
    Raises:
        HTTPException: Se o paciente não for encontrado ou ocorrer algum erro
    """
    try:
        patient = delete_patient(db, patient_id)
        if not patient:
            logger.warning(f"Paciente não encontrado para exclusão: {patient_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")
        logger.info(f"Paciente removido: {patient_id}")
        return PatientResponse(
            id=patient.id,
            email=patient.email,
            name=patient.name,
            cpf=patient.cpf,
            password=patient.password,
            phone=patient.phone,
            birth_date=patient.birth_date
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Erro inesperado ao remover paciente: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")
