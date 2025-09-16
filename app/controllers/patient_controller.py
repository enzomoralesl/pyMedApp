from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.patient import PatientRequest, PatientResponse
from app.services.patient_service import create_patient, get_patients, get_patient_by_id, delete_patient, update_patient
import logging

# Configuração de logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/patient", tags=["Patients"])

@router.post("", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create(patient_request: PatientRequest, response: Response, db: Session = Depends(get_db)):
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
            birthDate=patient.birth_date
        )
    except HTTPException as e:
        logger.warning(f"Erro ao criar paciente: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Erro inesperado ao criar paciente: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")

@router.get("", response_model=list[PatientResponse])
async def read_all(db: Session = Depends(get_db)):
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
                birthDate=patient.birth_date
            ) for patient in patients
        ]
    except HTTPException as e:
        logger.warning(f"Erro ao buscar pacientes: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar pacientes: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")

@router.get("/{patient_email}", response_model=PatientResponse)
async def read(patient_email: str, db: Session = Depends(get_db)):
    try:
        patient = get_patient_by_id(db, patient_email)
        if not patient:
            logger.warning(f"Paciente não encontrado: {patient_email}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")
        return PatientResponse(
            id=patient.id,
            email=patient.email,
            name=patient.name,
            cpf=patient.cpf,
            password=patient.password,
            phone=patient.phone,
            birthDate=patient.birth_date
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar paciente: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")

@router.put("/{patient_email}", response_model=PatientResponse)
async def update(patient_email: str, patient_request: PatientRequest, db: Session = Depends(get_db)):
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
            birthDate=patient.birth_date
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Erro inesperado ao atualizar paciente: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")

@router.delete("/{patient_email}", response_model=PatientResponse)
async def delete(patient_email: str, db: Session = Depends(get_db)):
    try:
        patient = delete_patient(db, patient_email)
        if not patient:
            logger.warning(f"Paciente não encontrado para exclusão: {patient_email}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")
        logger.info(f"Paciente removido: {patient_email}")
        return PatientResponse(
            id=patient.id,
            email=patient.email,
            name=patient.name,
            cpf=patient.cpf,
            password=patient.password,
            phone=patient.phone,
            birthDate=patient.birth_date
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Erro inesperado ao remover paciente: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")
