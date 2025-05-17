-- Criação da extensão UUID se não existir
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Recriação do esquema (comentado para evitar perda de dados em produção)
-- DROP SCHEMA public CASCADE;
-- CREATE SCHEMA public;

-- Criação das tabelas se não existirem


CREATE TABLE IF NOT EXISTS tb_patient (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    birth_date VARCHAR(15)
);

-- Criação de índices para melhorar a performance
CREATE INDEX IF NOT EXISTS idx_patient_email ON tb_patient(email);
