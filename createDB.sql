


GRANT ALL PRIVILEGES ON DATABASE scanner TO marcus;


CREATE TABLE config_database (
    key VARCHAR(50) PRIMARY KEY,
    value VARCHAR(128)
);
GRANT ALL PRIVILEGES ON TABLE config_database TO marcus;
INSERT INTO config_database (key, value) VALUES
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

CREATE TABLE people_database (
    id SERIAL PRIMARY KEY, 
    employee_id INTEGER UNIQUE,
    first_name VARCHAR(50) UNIQUE,
    last_name VARCHAR(50) UNIQUE,
    email VARCHAR(50) UNIQUE, 
    phone VARCHAR(15) UNIQUE,
    pic_path VARCHAR(128) UNIQUE,
    employee_role VARCHAR(50),
    position VARCHAR(50),
    department VARCHAR(50)
    );
GRANT ALL PRIVILEGES ON TABLE people_database TO marcus;

CREATE TABLE timesheet_database (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES people_database(employee_id) ON DELETE CASCADE,
    clock_in TIMESTAMPTZ,
    clock_out TIMESTAMPTZ,
    work_date DATE
    );
GRANT ALL PRIVILEGES ON TABLE timesheet_database TO marcus;

\dt

-- Uncomment next three line to insert test data into people_database
--INSERT INTO people_database (employee_id, first_name, last_name, email, phone, pic_path, employee_role, position, department) VALUES
    --(2001, 'Jojo', 'Bob', 'jbob@scanner.com', '100-555-1234', '/images/2001.jpg', 'Testsubject', 'CTO', 'Thing-a-ma-jig Development'),
    --(2002, 'Luke', 'Skywalker', 'lskywalker@scanner.com', '100-555-1978', '/images/2002.jpg', 'Jedi Master', 'Like his father', 'Peace and Justice');

-- Uncomment next three line to insert test data into timesheet_database
--INSERT INTO timesheet_database (employee_id, clock_in, clock_out, work_date) VALUES
    --(2001, '2025-10-01 08:00:00+00', '2025-10-01 16:00:00+00', '2025-10-01'),
    --(2002, '2025-10-01 08:00:00+00', '2025-10-01 16:00:00+00', '2025-10-01');

-- Uncomment next three lines to verify data insertion
SELECT * FROM config_database;
SELECT * FROM people_database;
SELECT * FROM timesheet_database;

