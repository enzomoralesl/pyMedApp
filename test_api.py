#!/usr/bin/env python
"""
Script para testar os endpoints da API PyMedApp
"""

import requests
import json
import uuid
from pprint import pprint
import sys

API_BASE_URL = "http://localhost:8081"

# Cores para output no terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(message):
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== {message} ==={Colors.ENDC}\n")

def print_success(message):
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")

def print_error(message):
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")

def print_warning(message):
    print(f"{Colors.WARNING}! {message}{Colors.ENDC}")

def print_info(message):
    print(f"{Colors.OKBLUE}ℹ {message}{Colors.ENDC}")

def print_json(data):
    print(json.dumps(data, indent=2))

def check_api_health():
    """Verifica se a API está em funcionamento"""
    print_header("Verificando status da API")
    
    try:
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code == 200:
            print_success(f"API está online! Status: {response.status_code}")
            print_info("Resposta:")
            print_json(response.json())
            return True
        else:
            print_error(f"API retornou status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error(f"Não foi possível conectar à API em {API_BASE_URL}")
        print_warning("Certifique-se que a aplicação está em execução")
        return False

def test_patient_endpoints():
    """Testa os endpoints relacionados a pacientes"""
    print_header("Testando endpoints de pacientes (Patients)")
    
    # Dados para teste
    patient_data = {
        "email": f"test.patient{uuid.uuid4().hex[:5]}@example.com",  # Email único
        "name": "Test Patient",
        "cpf": f"123.456.789-{uuid.uuid4().hex[:2]}",  # CPF semi-único
        "password": "test123",
        "phone": "(99) 99999-9999",
        "birthDate": "1990-01-01"  # Note o camelCase aqui
    }
    
    # 1. Criar um paciente
    print_info("1. Criando um novo paciente")
    response = requests.post(f"{API_BASE_URL}/v1/patient/", json=patient_data)
    
    if response.status_code == 200:
        print_success(f"Paciente criado com sucesso! Status: {response.status_code}")
        patient = response.json()
        patient_id = patient.get("id")
        print_json(patient)
    else:
        print_error(f"Erro ao criar paciente. Status: {response.status_code}")
        print_warning(f"Resposta: {response.text}")
        return
    
    # 2. Obter todos os pacientes
    print_info("\n2. Obtendo lista de pacientes")
    response = requests.get(f"{API_BASE_URL}/v1/patient/")
    
    if response.status_code == 200:
        patients = response.json()
        print_success(f"Lista de pacientes obtida! Total: {len(patients)}")
    else:
        print_error(f"Erro ao obter pacientes. Status: {response.status_code}")
    
    # 3. Obter paciente por ID
    print_info(f"\n3. Obtendo paciente por ID ({patient_id})")
    response = requests.get(f"{API_BASE_URL}/v1/patient/{patient_id}")
    
    if response.status_code == 200:
        print_success(f"Paciente encontrado! Status: {response.status_code}")
        print_json(response.json())
    else:
        print_error(f"Erro ao obter paciente. Status: {response.status_code}")
    
    # 4. Atualizar paciente
    updated_patient_data = {
        "email": patient_data["email"],  # Mantém o mesmo email
        "name": "Updated Patient Name",
        "cpf": patient_data["cpf"],  # Mantém o mesmo CPF
        "password": "updated123",
        "phone": "(88) 88888-8888",
        "birthDate": "1991-02-02"
    }
    
    print_info(f"\n4. Atualizando paciente ({patient_id})")
    response = requests.put(f"{API_BASE_URL}/v1/patient/{patient_id}", json=updated_patient_data)
    
    if response.status_code == 200:
        print_success(f"Paciente atualizado! Status: {response.status_code}")
        print_json(response.json())
    else:
        print_error(f"Erro ao atualizar paciente. Status: {response.status_code}")
        print_warning(f"Resposta: {response.text}")
    
    # 5. Deletar paciente
    print_info(f"\n5. Deletando paciente ({patient_id})")
    response = requests.delete(f"{API_BASE_URL}/v1/patient/{patient_id}")
    
    if response.status_code == 200:
        print_success(f"Paciente removido! Status: {response.status_code}")
        print_json(response.json())
    else:
        print_error(f"Erro ao deletar paciente. Status: {response.status_code}")
        print_warning(f"Resposta: {response.text}")
    
    # Verificar se foi realmente deletado
    print_info(f"\n6. Verificando se o paciente foi realmente removido")
    response = requests.get(f"{API_BASE_URL}/v1/patient/{patient_id}")
    
    if response.status_code == 404:
        print_success(f"Paciente realmente não existe mais! Status: {response.status_code}")
    else:
        print_error(f"Paciente ainda existe! Status: {response.status_code}")
        print_warning(f"Resposta: {response.json()}")

def main():
    """Função principal que executa todos os testes"""
    if not check_api_health():
        sys.exit(1)

    test_patient_endpoints()
    
    print_header("Testes concluídos")

if __name__ == "__main__":
    main()
