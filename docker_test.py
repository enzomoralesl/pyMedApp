#!/usr/bin/env python
"""
Script para testar a API dentro do contêiner Docker
"""

import requests
import json
import uuid
import time

API_BASE_URL = "http://app:8081"  # Use o nome do serviço no Docker Compose

def print_json(data):
    print(json.dumps(data, indent=2))

def test_api():
    """Executa os testes na API"""
    print("\n=== Testando a API PyMedApp ===\n")
    
    # Espera a API estar disponível
    max_retries = 10
    for i in range(max_retries):
        try:
            response = requests.get(f"{API_BASE_URL}/")
            if response.status_code == 200:
                print("✅ API está online!")
                break
        except requests.exceptions.RequestException:
            print(f"⏳ Aguardando a API iniciar... ({i+1}/{max_retries})")
            time.sleep(3)
    else:
        print("❌ API não iniciou após várias tentativas")
        return False
    
    # Testar pacientes
    print("\n==== Testando CRUD de Pacientes ====\n")
    patient_data = {
        "email": f"patient{uuid.uuid4().hex[:5]}@docker.test",
        "name": "Patient Docker Test",
        "cpf": f"123.456.789-{uuid.uuid4().hex[:2]}",
        "password": "dockerpass",
        "phone": "(00) 12345-6789",
        "birthDate": "1985-05-05"
    }
    
    print(f"Criando paciente: {patient_data}")
    response = requests.post(f"{API_BASE_URL}/v1/patient/", json=patient_data)
    
    if response.status_code == 200:
        print("✅ Paciente criado com sucesso!")
        patient = response.json()
        patient_id = patient.get("id")
        print_json(patient)
        
        # Atualizar o paciente
        updated_data = {
            "email": patient_data["email"],
            "name": "Patient Docker Updated",
            "cpf": patient_data["cpf"],
            "password": "newpass123",
            "phone": "(11) 98765-4321",
            "birthDate": "1986-06-06"
        }
        
        print(f"\nAtualizando paciente para: {updated_data}")
        response = requests.put(f"{API_BASE_URL}/v1/patient/{patient_id}", json=updated_data)
        
        if response.status_code == 200:
            print("✅ Paciente atualizado com sucesso!")
            print_json(response.json())
        else:
            print(f"❌ Erro ao atualizar paciente: {response.status_code}")
            
        # Listar todos os pacientes
        print("\nListando todos os pacientes:")
        response = requests.get(f"{API_BASE_URL}/v1/patient/")
        
        if response.status_code == 200:
            patients = response.json()
            print(f"✅ {len(patients)} pacientes encontrados")
            
        # Deletar o paciente
        print(f"\nDeletando o paciente {patient_id}")
        response = requests.delete(f"{API_BASE_URL}/v1/patient/{patient_id}")
        
        if response.status_code == 200:
            print("✅ Paciente removido com sucesso!")
        else:
            print(f"❌ Erro ao remover paciente: {response.status_code}")
    else:
        print(f"❌ Erro ao criar paciente: {response.status_code}")
    
    print("\n==== Testes concluídos ====")
    return True

if __name__ == "__main__":
    test_api()
