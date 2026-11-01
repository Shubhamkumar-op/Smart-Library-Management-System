-- Create triggers
-- Generated from the supplied PostgreSQL 18.6 plain dump.
-- Run scripts in the order documented in README_SQL.md.

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET search_path = library, public;

--
-- TOC entry 5030 (class 2620 OID 16651)
-- Name: books trg_books_audit; Type: TRIGGER; Schema: library; Owner: postgres
--

CREATE TRIGGER trg_books_audit AFTER INSERT OR DELETE OR UPDATE ON library.books FOR EACH ROW EXECUTE FUNCTION library.audit_table_changes('book_id');

--
-- TOC entry 5031 (class 2620 OID 16630)
-- Name: issue_records trg_update_copy_status; Type: TRIGGER; Schema: library; Owner: postgres
--

CREATE TRIGGER trg_update_copy_status AFTER INSERT OR UPDATE OF status ON library.issue_records FOR EACH ROW EXECUTE FUNCTION library.update_copy_status();

