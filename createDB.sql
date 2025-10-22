---This SQL script creates the necessary database and tables for the Scanner application.
-- It sets up the config_database, people_database, and timesheet_database tables,
-- and inserts initial configuration data into the config_database table.

-- Create config_database table to hold configuration settings
CREATE TABLE config_database (
    key VARCHAR(50) PRIMARY KEY,
    value VARCHAR(128)
);
--- Insert default configuration data into config_database 
--- If option 3 was chosen from psql_setup.sh this data will NOT be overwritten.
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

--- Create people_database table to hold employee information 
--- Data can be inserted via the web interface run by setttings.py
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

--- Create timesheet_database table to hold clock-in and clock-out records.
--- Reports will be generated from this data. 
CREATE TABLE timesheet_database (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES people_database(employee_id) ON DELETE CASCADE, -- Foreign key reference to people_database query can only be made using employee_id
    clock_in TIMESTAMPTZ DEFAULT NOW(),
    clock_out TIMESTAMPTZ DEFAULT NOW(),
    work_date DATE DEFAULT CURRENT_DATE
    );

-- marcus will be the main user for the scanner database tables are made with defult postgres user but we need to give marcus access to them.
GRANT ALL PRIVILEGES ON TABLE config_database TO marcus;
GRANT ALL PRIVILEGES ON TABLE people_database TO marcus;
GRANT ALL PRIVILEGES ON TABLE timesheet_database TO marcus;

--- Update config status to True and set config date to current date 
--- main.py uses these two values to determine if initial setup has been completed.
--- These values can be reset in the setttings.py web interface re-enabling launch of initial setup. 
UPDATE config_database SET value = 'True' WHERE key = 'config_status';
UPDATE config_database SET value = CURRENT_DATE WHERE key = 'config_date';

--- Feedback for user to verify tables were created successfully
\dt

--- Below this line are options to verify database functionality. They will be left in for advanced users. 

-- Uncomment next line to verify config data insertion
-- SELECT * FROM config_database LIMIT (SELECT COUNT(*) FROM config_database)

-- Uncomment next three line to insert test data into people_database
-- INSERT INTO people_database (employee_id, first_name, last_name, email, phone, pic_path, employee_role, position, department) VALUES
    --(2001, 'Han', 'Solo', 'hsolo@scanner.com', '100-555-1976', '/images/2001.jpg', 'Scoundrel', 'Pilot', 'Only in it for the money'),
    --(2002, 'Luke', 'Skywalker', 'lskywalker@scanner.com', '100-555-1978', '/images/2002.jpg', 'Jedi Master', 'Like his father', 'Peace and Justice');

-- Uncomment next three line to insert test data into timesheet_database
-- INSERT INTO timesheet_database (employee_id, clock_in, clock_out, work_date) VALUES
    --(2001, '2025-10-01 08:00:00+00', '2025-10-01 16:00:00+00', '2025-10-01'),
    --(2002, '2025-10-01 08:00:00+00', '2025-10-01 16:00:00+00', '2025-10-01');

-- Uncomment next three lines to verify data schemas
-- \d+ config_database; SELECT * FROM config_database;
-- \d+ people_database; SELECT * FROM people_database;
-- \d+ timesheet_database; SELECT * FROM timesheet_database;
