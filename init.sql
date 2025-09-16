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
    cpf VARCHAR(11) NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    birth_date VARCHAR(15)
);

-- Criação de índices para melhorar a performance
CREATE INDEX IF NOT EXISTS idx_patient_email ON tb_patient(email);


SET search_path TO public;
DROP EXTENSION IF EXISTS "uuid-ossp";

CREATE EXTENSION "uuid-ossp" SCHEMA public;


-- Insert data into tb_patient
INSERT INTO tb_patient (id, email, name, cpf, password, phone, birth_date)
VALUES
    (uuid_generate_v4(), 'john1000.doee@example.com', 'John doee', '12345678901', 'password', '1234567890', '1990-01-01'),
    (uuid_generate_v4(), 'enzo.moralesl@example.com', 'Enzo Morales', '12312312345', 'password', '1234567891', '1992-02-02'),
    (uuid_generate_v4(), 'maria.silva@example.com', 'Maria Silva', '98765432109', 'password', '1234567892', '1985-05-15'),
    (uuid_generate_v4(), 'carlos.santos@example.com', 'Carlos Santos', '45678912345', 'password', '1234567893', '1978-09-23'),
    (uuid_generate_v4(), 'ana.pereira@example.com', 'Ana Pereira', '78945612332', 'password', '1234567894', '1995-11-07'),
    (uuid_generate_v4(), 'pedro.oliveira@example.com', 'Pedro Oliveira', '32165498701', 'password', '1234567895', '1982-04-18'),
    (uuid_generate_v4(), 'julia.costa@example.com', 'Julia Costa', '65432198712', 'password', '1234567896', '1993-07-29'),
    (uuid_generate_v4(), 'roberto.almeida@example.com', 'Roberto Almeida', '12378945698', 'password', '1234567897', '1975-12-10'),
    (uuid_generate_v4(), 'fernanda.lima@example.com', 'Fernanda Lima', '98732165445', 'password', '1234567898', '1989-06-02'),
    (uuid_generate_v4(), 'lucas.martins@example.com', 'Lucas Martins', '45612378998', 'password', '1234567899', '1997-03-21');
