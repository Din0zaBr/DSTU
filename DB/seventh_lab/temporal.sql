--
CREATE TABLE IF NOT EXISTS users
(
    id       SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100)       NOT NULL,
    role     VARCHAR(20)        NOT NULL CHECK (role IN ('admin', 'user'))
);

--
CREATE TABLE IF NOT EXISTS my_object
(
    id             INTEGER,
    time_create    TIMESTAMP  NOT NULL DEFAULT NOW(),
    time_dead      TIMESTAMP,
    operation_type VARCHAR(1) NOT NULL DEFAULT 'I' CHECK (operation_type IN ('I', 'U', 'D')),
    changed_by     VARCHAR(50) DEFAULT CURRENT_USER,
    change_comment TEXT,
    PRIMARY KEY (id, time_create)
);

--        -
CREATE TABLE IF NOT EXISTS employee
(
    name     VARCHAR(100),
    position VARCHAR(100),
    salary   NUMERIC(10, 2)
) INHERITS (my_object);

CREATE TABLE IF NOT EXISTS department
(
    name     VARCHAR(100),
    location VARCHAR(100)
) INHERITS (my_object);

CREATE TABLE IF NOT EXISTS project
(
    title    VARCHAR(100),
    budget   NUMERIC(12, 2),
    deadline DATE
) INHERITS (my_object);

--
DROP FUNCTION IF EXISTS temporal_trigger() CASCADE;

--
CREATE OR REPLACE FUNCTION temporal_trigger()
RETURNS TRIGGER AS $$
DECLARE
    old_record RECORD;
BEGIN
    --
    IF TG_OP = 'INSERT' THEN
        --                                                    id
        EXECUTE format('SELECT * FROM %I WHERE id = $1 AND time_dead IS NULL', TG_TABLE_NAME)
        INTO old_record
        USING NEW.id;

        IF old_record IS NOT NULL THEN
            --                              ,
            EXECUTE format('UPDATE %I SET
                          time_dead = NOW(),
                          operation_type = ''U'',
                          changed_by = CURRENT_USER,
                          change_comment = ''                 ''
                          WHERE id = $1 AND time_dead IS NULL', TG_TABLE_NAME)
            USING NEW.id;
        END IF;

        --
        NEW.time_create := NOW();
        NEW.operation_type := 'I';
        NEW.changed_by := CURRENT_USER;
        NEW.change_comment := CASE WHEN old_record IS NOT NULL THEN '                   ' ELSE '                              ' END;

        RETURN NEW;

    --
    ELSIF TG_OP = 'UPDATE' THEN
        --
        EXECUTE format('INSERT INTO %I
                      SELECT
                          id,
                          time_create,
                          NOW() as time_dead,
                          ''U'' as operation_type,
                          CURRENT_USER as changed_by,
                          ''                 '' as change_comment,
                          name,
                          position,
                          salary
                      FROM %I
                      WHERE id = $1 AND time_dead IS NULL',
                      TG_TABLE_NAME, TG_TABLE_NAME)
        USING OLD.id;

        --
        NEW.time_create := NOW();
        NEW.time_dead := NULL;
        NEW.operation_type := 'I';
        NEW.changed_by := CURRENT_USER;
        NEW.change_comment := '                             ';

        RETURN NEW;

    --
    ELSIF TG_OP = 'DELETE' THEN
        --
        EXECUTE format('INSERT INTO %I
                      SELECT
                          id,
                          time_create,
                          NOW() as time_dead,
                          ''D'' as operation_type,
                          CURRENT_USER as changed_by,
                          ''               '' as change_comment,
                          name,
                          position,
                          salary
                      FROM %I
                      WHERE id = $1 AND time_dead IS NULL',
                      TG_TABLE_NAME, TG_TABLE_NAME)
        USING OLD.id;

        RETURN OLD;
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

--
CREATE TRIGGER employee_temporal_trigger
BEFORE INSERT OR UPDATE OR DELETE ON employee
FOR EACH ROW EXECUTE FUNCTION temporal_trigger();

CREATE TRIGGER department_temporal_trigger
BEFORE INSERT OR UPDATE OR DELETE ON department
FOR EACH ROW EXECUTE FUNCTION temporal_trigger();

CREATE TRIGGER project_temporal_trigger
BEFORE INSERT OR UPDATE OR DELETE ON project
FOR EACH ROW EXECUTE FUNCTION temporal_trigger();

--
CREATE OR REPLACE FUNCTION get_object_history(
    p_table_name VARCHAR,
    p_id INTEGER
)
    RETURNS TABLE
            (
                id             INTEGER,
                time_create    TIMESTAMP,
                time_dead      TIMESTAMP,
                operation_type VARCHAR(1),
                changed_by     VARCHAR(50),
                change_comment TEXT,
                table_data     JSONB
            )
AS
$$
BEGIN
    RETURN QUERY EXECUTE format('
        SELECT
            id,
            time_create,
            time_dead,
            operation_type,
            changed_by,
            change_comment,
            to_jsonb(r) - ''id'' - ''time_create'' - ''time_dead'' -
            ''operation_type'' - ''changed_by'' - ''change_comment'' as table_data
        FROM %I r
        WHERE id = $1
        ORDER BY time_create DESC',
        p_table_name)
        USING p_id;
END;
$$ LANGUAGE plpgsql;

--
CREATE OR REPLACE FUNCTION restore_object_version(
    p_table_name VARCHAR,
    p_id INTEGER,
    p_time_create TIMESTAMP
) RETURNS VOID AS
$$
BEGIN
    --
    EXECUTE format('ALTER TABLE %I DISABLE TRIGGER USER', p_table_name);

    --
    EXECUTE format('
        UPDATE %I
        SET time_dead = NOW(),
            operation_type = ''U'',
            changed_by = CURRENT_USER,
            change_comment = ''                            ''
        WHERE id = $1 AND time_dead IS NULL',
        p_table_name)
    USING p_id;

    --
    EXECUTE format('
        INSERT INTO %I
        SELECT
            id,
            NOW() as time_create,
            NULL as time_dead,
            ''I'' as operation_type,
            CURRENT_USER as changed_by,
            ''                      '' as change_comment,
            %s
        FROM %I
        WHERE id = $1 AND time_create = $2',
        p_table_name,
        CASE
            WHEN p_table_name = 'employee' THEN 'name, position, salary'
            WHEN p_table_name = 'department' THEN 'name, location'
            WHEN p_table_name = 'project' THEN 'title, budget, deadline'
        END,
        p_table_name)
    USING p_id, p_time_create;

    --
    EXECUTE format('ALTER TABLE %I ENABLE TRIGGER USER', p_table_name);
END;
$$ LANGUAGE plpgsql;

--
CREATE INDEX IF NOT EXISTS idx_my_object_active ON my_object (id) WHERE time_dead IS NULL;
CREATE INDEX IF NOT EXISTS idx_employee_active ON employee (id) WHERE time_dead IS NULL;
CREATE INDEX IF NOT EXISTS idx_department_active ON department (id) WHERE time_dead IS NULL;
CREATE INDEX IF NOT EXISTS idx_project_active ON project (id) WHERE time_dead IS NULL;

--
CREATE OR REPLACE VIEW current_objects AS
SELECT *
FROM my_object
WHERE time_dead IS NULL
  AND operation_type <> 'D';

--
DO
$$
    BEGIN
        --
        INSERT INTO users (username, password, role)
        VALUES ('admin', 'admin123', 'admin')
        ON CONFLICT (username) DO NOTHING;
        INSERT INTO users (username, password, role)
        VALUES ('user1', 'user123', 'user')
        ON CONFLICT (username) DO NOTHING;

        --
        --
        INSERT INTO employee (id, name, position, salary)
        VALUES (1, '           ', '           ', 100000);
        INSERT INTO employee (id, name, position, salary)
        VALUES (2, '           ', '        ', 150000);

        --                   ,
        UPDATE employee SET position = '                   ', salary = 120000
        WHERE id = 1 AND time_dead IS NULL;
        UPDATE employee SET salary = 160000
        WHERE id = 2 AND time_dead IS NULL;

        --
        DELETE FROM employee WHERE id = 1 AND time_dead IS NULL;
    END
$$;