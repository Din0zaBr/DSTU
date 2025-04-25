-- Создание базы данных
--CREATE DATABASE CompanyDB;

-- Подключение к базе данных
--\c CompanyDB;

-- Создание таблицы Department
CREATE TABLE Department (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    head_id INT
);

-- Создание таблицы Employee
CREATE TABLE Employee (
    id SERIAL PRIMARY KEY,
    last_name VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    job_position VARCHAR(255),
    department_id INT,
    specialization VARCHAR(255),
    birth_date DATE,
);

-- Создание таблицы Project
CREATE TABLE Project (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    budget DECIMAL(10, 2) NOT NULL,
    leader_id INT,
    employee_id INT UNIQUE,
);

-- Создание таблицы Contract
CREATE TABLE Contract (
    id SERIAL PRIMARY KEY,
    date_signed DATE NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) NOT NULL,
    project_id INT,
);

-- Создание таблицы Equipment
CREATE TABLE Equipment (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(255),
    department_id INT,
    assignment_date DATE,
    project_id INT,
);

-- Создание таблицы Subcontractor
CREATE TABLE Subcontractor (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    project_id INT,
    specialization VARCHAR(255),
    contact_info VARCHAR(255),
);

CREATE TABLE IF NOT EXISTS users
(
    id       SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100)       NOT NULL,
    role     VARCHAR(20)        NOT NULL CHECK (role IN ('admin', 'user'))
);

INSERT INTO users (username, password, role)
VALUES ('admin', 'admin123', 'admin')
ON CONFLICT (username) DO NOTHING;

INSERT INTO users (username, password, role)
VALUES ('user1', 'user123', 'user')
ON CONFLICT (username) DO NOTHING;

-- Вставка данных в таблицу Department
INSERT INTO Department (name, location, head_id) VALUES
('HR Department', 'Office 101', 1),
('IT Department', 'Office 102', 2),
('Finance Department', 'Office 103', 3),
('Marketing Department', 'Office 104', 4),
('Sales Department', 'Office 105', 5);

-- Вставка данных в таблицу Employee
INSERT INTO Employee (last_name, first_name, job_position, department_id, specialization, birth_date) VALUES
('Smith', 'John', 'Manager', 1, 'Human Resources', '1980-05-15'),
('Doe', 'Jane', 'Developer', 2, 'Software Engineering', '1985-07-20'),
('Brown', 'Alice', 'Analyst', 3, 'Financial Analysis', '1990-03-10'),
('Johnson', 'Bob', 'Marketing Specialist', 4, 'Digital Marketing', '1982-11-30'),
('Williams', 'Emma', 'Sales Representative', 5, 'Sales', '1988-09-05');

-- Вставка данных в таблицу Project
INSERT INTO Project (name, start_date, end_date, budget, leader_id, employee_id) VALUES
('Project Alpha', '2023-01-01', '2023-12-31', 100000.00, 1, 1),
('Project Beta', '2023-02-01', '2023-11-30', 150000.00, 2, 2),
('Project Gamma', '2023-03-01', '2023-10-31', 200000.00, 3, 3),
('Project Delta', '2023-04-01', '2023-09-30', 250000.00, 4, 4),
('Project Epsilon', '2023-05-01', '2023-08-31', 300000.00, 5, 5);

-- Вставка данных в таблицу Contract
INSERT INTO Contract (date_signed, amount, status, project_id) VALUES
('2023-01-15', 50000.00, 'Signed', 1),
('2023-02-20', 75000.00, 'Signed', 2),
('2023-03-25', 100000.00, 'Signed', 3),
('2023-04-30', 125000.00, 'Signed', 4),
('2023-05-31', 150000.00, 'Signed', 5);

-- Вставка данных в таблицу Equipment
INSERT INTO Equipment (name, type, department_id, assignment_date, project_id) VALUES
('Laptop', 'Electronics', 2, '2023-01-10', 1),
('Printer', 'Office Equipment', 3, '2023-02-15', 2),
('Server', 'IT Equipment', 2, '2023-03-20', 3),
('Projector', 'Presentation Equipment', 4, '2023-04-25', 4),
('Scanner', 'Office Equipment', 5, '2023-05-30', 5);

-- Вставка данных в таблицу Subcontractor
INSERT INTO Subcontractor (name, project_id, specialization, contact_info) VALUES
('Subcontractor A', 1, 'Construction', '123-456-7890'),
('Subcontractor B', 2, 'Electrical', '234-567-8901'),
('Subcontractor C', 3, 'Plumbing', '345-678-9012'),
('Subcontractor D', 4, 'HVAC', '456-789-0123'),
('Subcontractor E', 5, 'Landscaping', '567-890-1234');
