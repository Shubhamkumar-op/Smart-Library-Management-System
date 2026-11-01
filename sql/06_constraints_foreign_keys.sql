-- Add table constraints and foreign keys
-- Generated from the supplied PostgreSQL 18.6 plain dump.
-- Run scripts in the order documented in README_SQL.md.

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET search_path = library, public;

--
-- TOC entry 5014 (class 2606 OID 16623)
-- Name: audit_logs audit_logs_pkey; Type: CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.audit_logs
    ADD CONSTRAINT audit_logs_pkey PRIMARY KEY (audit_id);

--
-- TOC entry 4978 (class 2606 OID 16435)
-- Name: authors authors_pkey; Type: CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.authors
    ADD CONSTRAINT authors_pkey PRIMARY KEY (author_id);

--
-- TOC entry 4994 (class 2606 OID 16486)
-- Name: book_authors book_authors_pkey; Type: CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.book_authors
    ADD CONSTRAINT book_authors_pkey PRIMARY KEY (book_id, author_id);

--
-- TOC entry 4996 (class 2606 OID 16510)
-- Name: book_copies book_copies_accession_number_key; Type: CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.book_copies
    ADD CONSTRAINT book_copies_accession_number_key UNIQUE (accession_number);

--
-- TOC entry 4998 (class 2606 OID 16508)
-- Name: book_copies book_copies_pkey; Type: CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.book_copies
    ADD CONSTRAINT book_copies_pkey PRIMARY KEY (copy_id);

--
-- TOC entry 4988 (class 2606 OID 16469)
-- Name: books books_isbn_key; Type: CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.books
    ADD CONSTRAINT books_isbn_key UNIQUE (isbn);

--
-- TOC entry 4990 (class 2606 OID 16467)
-- Name: books books_pkey; Type: CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.books
    ADD CONSTRAINT books_pkey PRIMARY KEY (book_id);

--
-- TOC entry 4980 (class 2606 OID 16445)
-- Name: categories categories_category_name_key; Type: CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.categories
    ADD CONSTRAINT categories_category_name_key UNIQUE (category_name);

--
-- TOC entry 4982 (class 2606 OID 16443)
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (category_id);

--
-- TOC entry 5004 (class 2606 OID 16566)
-- Name: fines fines_issue_id_key; Type: CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.fines
    ADD CONSTRAINT fines_issue_id_key UNIQUE (issue_id);

--
-- TOC entry 5006 (class 2606 OID 16564)
-- Name: fines fines_pkey; Type: CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.fines
    ADD CONSTRAINT fines_pkey PRIMARY KEY (fine_id);

--
-- TOC entry 5001 (class 2606 OID 16535)
-- Name: issue_records issue_records_pkey; Type: CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.issue_records
    ADD CONSTRAINT issue_records_pkey PRIMARY KEY (issue_id);

--
-- TOC entry 4972 (class 2606 OID 16422)
-- Name: members members_email_key; Type: CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.members
    ADD CONSTRAINT members_email_key UNIQUE (email);

--
-- TOC entry 4974 (class 2606 OID 16418)
-- Name: members members_pkey; Type: CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.members
    ADD CONSTRAINT members_pkey PRIMARY KEY (member_id);

--
-- TOC entry 4976 (class 2606 OID 16420)
-- Name: members members_user_id_key; Type: CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.members
    ADD CONSTRAINT members_user_id_key UNIQUE (user_id);

--
-- TOC entry 5008 (class 2606 OID 16583)
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (payment_id);

--
-- TOC entry 4984 (class 2606 OID 16453)
-- Name: publishers publishers_pkey; Type: CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.publishers
    ADD CONSTRAINT publishers_pkey PRIMARY KEY (publisher_id);

--
-- TOC entry 4986 (class 2606 OID 16455)
-- Name: publishers publishers_publisher_name_key; Type: CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.publishers
    ADD CONSTRAINT publishers_publisher_name_key UNIQUE (publisher_name);

--
-- TOC entry 5011 (class 2606 OID 16600)
-- Name: reservations reservations_pkey; Type: CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.reservations
    ADD CONSTRAINT reservations_pkey PRIMARY KEY (reservation_id);

--
-- TOC entry 4967 (class 2606 OID 16404)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);

--
-- TOC entry 4969 (class 2606 OID 16406)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.users
    ADD CONSTRAINT users_username_key UNIQUE (username);

--
-- TOC entry 5029 (class 2606 OID 16624)
-- Name: audit_logs audit_logs_user_id_fkey; Type: FK CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.audit_logs
    ADD CONSTRAINT audit_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES library.users(user_id) ON DELETE SET NULL;

--
-- TOC entry 5019 (class 2606 OID 16492)
-- Name: book_authors book_authors_author_id_fkey; Type: FK CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.book_authors
    ADD CONSTRAINT book_authors_author_id_fkey FOREIGN KEY (author_id) REFERENCES library.authors(author_id) ON DELETE CASCADE;

--
-- TOC entry 5020 (class 2606 OID 16487)
-- Name: book_authors book_authors_book_id_fkey; Type: FK CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.book_authors
    ADD CONSTRAINT book_authors_book_id_fkey FOREIGN KEY (book_id) REFERENCES library.books(book_id) ON DELETE CASCADE;

--
-- TOC entry 5021 (class 2606 OID 16511)
-- Name: book_copies book_copies_book_id_fkey; Type: FK CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.book_copies
    ADD CONSTRAINT book_copies_book_id_fkey FOREIGN KEY (book_id) REFERENCES library.books(book_id);

--
-- TOC entry 5017 (class 2606 OID 16470)
-- Name: books books_category_id_fkey; Type: FK CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.books
    ADD CONSTRAINT books_category_id_fkey FOREIGN KEY (category_id) REFERENCES library.categories(category_id);

--
-- TOC entry 5018 (class 2606 OID 16475)
-- Name: books books_publisher_id_fkey; Type: FK CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.books
    ADD CONSTRAINT books_publisher_id_fkey FOREIGN KEY (publisher_id) REFERENCES library.publishers(publisher_id);

--
-- TOC entry 5025 (class 2606 OID 16567)
-- Name: fines fines_issue_id_fkey; Type: FK CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.fines
    ADD CONSTRAINT fines_issue_id_fkey FOREIGN KEY (issue_id) REFERENCES library.issue_records(issue_id);

--
-- TOC entry 5022 (class 2606 OID 16536)
-- Name: issue_records issue_records_copy_id_fkey; Type: FK CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.issue_records
    ADD CONSTRAINT issue_records_copy_id_fkey FOREIGN KEY (copy_id) REFERENCES library.book_copies(copy_id);

--
-- TOC entry 5023 (class 2606 OID 16546)
-- Name: issue_records issue_records_issued_by_fkey; Type: FK CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.issue_records
    ADD CONSTRAINT issue_records_issued_by_fkey FOREIGN KEY (issued_by) REFERENCES library.users(user_id);

--
-- TOC entry 5024 (class 2606 OID 16541)
-- Name: issue_records issue_records_member_id_fkey; Type: FK CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.issue_records
    ADD CONSTRAINT issue_records_member_id_fkey FOREIGN KEY (member_id) REFERENCES library.members(member_id);

--
-- TOC entry 5016 (class 2606 OID 16423)
-- Name: members members_user_id_fkey; Type: FK CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.members
    ADD CONSTRAINT members_user_id_fkey FOREIGN KEY (user_id) REFERENCES library.users(user_id) ON DELETE SET NULL;

--
-- TOC entry 5026 (class 2606 OID 16584)
-- Name: payments payments_fine_id_fkey; Type: FK CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.payments
    ADD CONSTRAINT payments_fine_id_fkey FOREIGN KEY (fine_id) REFERENCES library.fines(fine_id);

--
-- TOC entry 5027 (class 2606 OID 16606)
-- Name: reservations reservations_book_id_fkey; Type: FK CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.reservations
    ADD CONSTRAINT reservations_book_id_fkey FOREIGN KEY (book_id) REFERENCES library.books(book_id);

--
-- TOC entry 5028 (class 2606 OID 16601)
-- Name: reservations reservations_member_id_fkey; Type: FK CONSTRAINT; Schema: library; Owner: postgres
--

ALTER TABLE ONLY library.reservations
    ADD CONSTRAINT reservations_member_id_fkey FOREIGN KEY (member_id) REFERENCES library.members(member_id);

