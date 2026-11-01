-- Create the NOLOGIN permission roles used by this project.
-- Run as a PostgreSQL administrator (for example, postgres).
-- Create/configure library_app separately with a NEW password on each machine.

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'library_admin') THEN
        EXECUTE 'CREATE ROLE library_admin NOLOGIN';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'library_librarian') THEN
        EXECUTE 'CREATE ROLE library_librarian NOLOGIN';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'library_analyst') THEN
        EXECUTE 'CREATE ROLE library_analyst NOLOGIN';
    END IF;
END
$$;
