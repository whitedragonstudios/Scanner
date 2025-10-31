-- This SQL script creates the necessary database and tables for the Scanner application.
-- It sets up the config_database, people_database, and timesheet_database tables,
-- and inserts initial configuration data into the config_database table.

-- Note: the scanner database and user marcus are created in classInstall.py
-- default password 'stoic'

DROP TABLE IF EXISTS timesheet_database CASCADE;
DROP TABLE IF EXISTS people_database CASCADE;
DROP TABLE IF EXISTS config_database CASCADE;

-- Create config_database table
CREATE TABLE config_database (
    key VARCHAR(50) PRIMARY KEY,
    value VARCHAR(128)
);

-- Insert default config data
INSERT INTO config_database (key, value) VALUES
    ('config_status', 'False'),
    ('config_date', '2025-01-01'),
    ('CSV_path', NULL),
    ('XLSX_path', NULL),
    ('JSON_path', NULL),
    ('webpage_title', 'Populus Numerus'),
    ('company','Scanner'),
    ('main_background_color','#333333'),
    ('main_text_color','#f5f5f5'), 
    ('button_color','#4CAF50'),
    ('button_text_color','#ffffff'),
    ('button_border_color','#388E3C'),
    ('button_border_hover_color','#2E7D32'),
    ('sidebar_color','#222222'),
    ('sidebar_text_color','#f5f5f5');

-- Create people_database table
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

-- Create timesheet_database table
CREATE TABLE timesheet_database (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES people_database(employee_id) ON DELETE CASCADE,
    clock_in TIMESTAMPTZ DEFAULT NOW(),
    clock_out TIMESTAMPTZ DEFAULT NOW(),
    work_date DATE DEFAULT CURRENT_DATE
);


GRANT ALL PRIVILEGES ON DATABASE scanner TO marcus;
GRANT ALL PRIVILEGES ON SCHEMA public TO marcus;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO marcus;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO marcus;


-- Update config status
-- UPDATE config_database SET value = 'True' WHERE key = 'config_status';
-- UPDATE config_database SET value = CURRENT_DATE WHERE key = 'config_date';

-- Optional test data
-- INSERT INTO people_database (employee_id, first_name, last_name, email, phone, pic_path, employee_role, position, department) VALUES
--     (0001, 'Han', 'Solo', 'hsolo@scanner.com', '100-555-1976', '/images/0001.jpg', 'Scoundrel', 'Pilot', 'Only in it for the money'),
--     (0002, 'Luke', 'Skywalker', 'lskywalker@scanner.com', '100-555-1978', '/images/0002.jpg', 'Jedi Master', 'Like his father', 'Peace and Justice');

-- INSERT INTO timesheet_database (employee_id, clock_in, clock_out, work_date) VALUES
--     (0001, '2025-10-01 08:00:00+00', '2025-10-01 16:00:00+00', '2025-10-01'),
--     (0002, '2025-10-01 08:00:00+00', '2025-10-01 16:00:00+00', '2025-10-01');
