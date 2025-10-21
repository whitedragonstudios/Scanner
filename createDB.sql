
DROP DATABASE IF EXISTS scanner;
CREATE DATABASE scanner;
GRANT ALL PRIVILEGES ON DATABASE scanner TO marcus;

\c scanner;

DROP TABLE IF EXISTS config_db;
CREATE TABLE config_db (
    key VARCHAR(50) PRIMARY KEY,
    value VARCHAR(128)
);
GRANT ALL PRIVILEGES ON TABLE config_db TO marcus;
INSERT INTO config_db (key, value) VALUES
    ('config_status', 'False'),
    ('config_date', '2025-01-01'),
    ('CSV_path', NULL),
    ('XLSX_path', NULL),
    ('JSON_path', NULL),
    ('webpage title', 'Populus Numerus'),
    ('company','Scanner'),
    ('main_background_color','#333333'),
    ('main_text_color','#f5f5f5'), 
    ('button_color','#4CAF50'),
    ('button_text_color','#ffffff'),
    ('button_border_color','#388E3C'),
    ('button_border_hover_color','#2E7D32'),
    ('sidebar_color','#222222'),
    ('sidebar_text_color','#f5f5f5');

DROP TABLE IF EXISTS people_database;
CREATE TABLE people_database (
    id SERIAL PRIMARY KEY, 
    employee_id INTEGER UNIQUE,
    name VARCHAR(50) UNIQUE,
    email VARCHAR(50) UNIQUE, 
    phone VARCHAR(15) UNIQUE
    );
GRANT ALL PRIVILEGES ON TABLE people_database TO marcus;

DROP TABLE IF EXISTS roles_database;
CREATE TABLE roles_database (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES people_database(employee_id) ON DELETE CASCADE,
    name VARCHAR(50) NOT NULL REFERENCES people_database(name) ON DELETE CASCADE,
    role VARCHAR(50),
    position VARCHAR(50),
    department VARCHAR(50)
    );
GRANT ALL PRIVILEGES ON TABLE roles_database TO marcus;

DROP TABLE IF EXISTS timesheet_database;
CREATE TABLE timesheet_database (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL REFERENCES people_database(name) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL REFERENCES roles_database(role) ON DELETE CASCADE,
    clock_in TIMESTAMPTZ,
    clock_out TIMESTAMPTZ
    );
GRANT ALL PRIVILEGES ON TABLE timesheet_database TO marcus;

\dt;