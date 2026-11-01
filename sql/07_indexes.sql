-- Create indexes
-- Generated from the supplied PostgreSQL 18.6 plain dump.
-- Run scripts in the order documented in README_SQL.md.

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET search_path = library, public;

--
-- TOC entry 5015 (class 1259 OID 16657)
-- Name: idx_audit_created; Type: INDEX; Schema: library; Owner: postgres
--

CREATE INDEX idx_audit_created ON library.audit_logs USING btree (created_at);

--
-- TOC entry 4991 (class 1259 OID 16654)
-- Name: idx_books_category; Type: INDEX; Schema: library; Owner: postgres
--

CREATE INDEX idx_books_category ON library.books USING btree (category_id);

--
-- TOC entry 4992 (class 1259 OID 16652)
-- Name: idx_books_isbn; Type: INDEX; Schema: library; Owner: postgres
--

CREATE INDEX idx_books_isbn ON library.books USING btree (isbn);

--
-- TOC entry 4999 (class 1259 OID 16655)
-- Name: idx_issue_dates; Type: INDEX; Schema: library; Owner: postgres
--

CREATE INDEX idx_issue_dates ON library.issue_records USING btree (issue_date, due_date);

--
-- TOC entry 4970 (class 1259 OID 16653)
-- Name: idx_members_email; Type: INDEX; Schema: library; Owner: postgres
--

CREATE INDEX idx_members_email ON library.members USING btree (email);

--
-- TOC entry 5009 (class 1259 OID 16656)
-- Name: idx_reservation_member; Type: INDEX; Schema: library; Owner: postgres
--

CREATE INDEX idx_reservation_member ON library.reservations USING btree (member_id);

--
-- TOC entry 5002 (class 1259 OID 16551)
-- Name: unique_active_copy_issue; Type: INDEX; Schema: library; Owner: postgres
--

CREATE UNIQUE INDEX unique_active_copy_issue ON library.issue_records USING btree (copy_id) WHERE ((status)::text = 'issued'::text);

--
-- TOC entry 5012 (class 1259 OID 16611)
-- Name: unique_pending_reservation; Type: INDEX; Schema: library; Owner: postgres
--

CREATE UNIQUE INDEX unique_pending_reservation ON library.reservations USING btree (member_id, book_id) WHERE ((status)::text = 'pending'::text);

