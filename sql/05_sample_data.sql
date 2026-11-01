-- Safe demo catalog data only.
-- Personal member details, user password hashes, audit logs, issue history,
-- fines, payments, and reservations were intentionally excluded.
-- This file is safe to use as starter/sample data for a public repository.

SET client_encoding = 'UTF8';
SET search_path = library, public;

--
-- TOC entry 5187 (class 0 OID 16429)
-- Dependencies: 225
-- Data for Name: authors; Type: TABLE DATA; Schema: library; Owner: postgres
--

COPY library.authors (author_id, author_name) FROM stdin;
1	Abraham Silberschatz
2	Brian W. Kernighan
3	S. Sudarshan
4	Andrew S. Tanenbaum
5	Charles E. Leiserson
6	Henry F. Korth
7	Dennis M. Ritchie
8	Thomas H. Cormen
9	Ramez Elmasri
\.

--
-- TOC entry 5194 (class 0 OID 16480)
-- Dependencies: 232
-- Data for Name: book_authors; Type: TABLE DATA; Schema: library; Owner: postgres
--

COPY library.book_authors (book_id, author_id) FROM stdin;
1	1
6	1
4	2
1	3
7	4
1	6
4	7
\.

--
-- TOC entry 5196 (class 0 OID 16498)
-- Dependencies: 234
-- Data for Name: book_copies; Type: TABLE DATA; Schema: library; Owner: postgres
--

COPY library.book_copies (copy_id, book_id, accession_number, status, acquired_date) FROM stdin;
2	1	LIB002	available	2026-10-31
3	1	LIB003	available	2026-10-31
4	1	LIB0003	available	2026-10-31
5	1	LIB0002	available	2026-10-31
6	1	LIB0001	available	2026-10-31
7	3	LIB0005	available	2026-10-31
8	3	LIB0004	available	2026-10-31
9	4	LIB0008	available	2026-10-31
10	5	LIB0013	available	2026-10-31
12	6	LIB0009	available	2026-10-31
13	7	LIB0011	available	2026-10-31
14	8	LIB0012	available	2026-10-31
15	9	LIB0015	available	2026-10-31
1	1	LIB001	available	2026-10-31
16	10	LIB0014	available	2026-10-31
11	6	LIB0010	available	2026-10-31
\.

--
-- TOC entry 5193 (class 0 OID 16457)
-- Dependencies: 231
-- Data for Name: books; Type: TABLE DATA; Schema: library; Owner: postgres
--

COPY library.books (book_id, isbn, title, category_id, publisher_id, publication_year, edition, language, created_at) FROM stdin;
3	9780133970777	Fundamentals of Database Systems	2	1	2015	7th	English	2026-10-31 13:17:03.659048+05:30
4	9780131103627	The C Programming Language	3	6	1988	2nd	English	2026-10-31 13:17:03.659048+05:30
5	9780596007126	Head First Design Patterns	3	4	2004	1st	English	2026-10-31 13:17:03.659048+05:30
6	9780133591620	Operating System Concepts	4	5	2018	10th	English	2026-10-31 13:17:03.659048+05:30
7	9780131873254	Modern Operating Systems	4	1	2014	4th	English	2026-10-31 13:17:03.659048+05:30
8	9780132126953	Computer Networking: A Top-Down Approach	5	1	2012	6th	English	2026-10-31 13:17:03.659048+05:30
9	9781491957660	Hands-On Machine Learning	6	4	2017	2nd	English	2026-10-31 13:17:03.659048+05:30
10	9780134610993	Artificial Intelligence: A Modern Approach	6	1	2016	3rd	English	2026-10-31 13:17:03.659048+05:30
1	9780073523323	Database System Concepts	1	1	2019	Updated Edition	English	2026-10-31 13:13:11.744652+05:30
\.

--
-- TOC entry 5189 (class 0 OID 16437)
-- Dependencies: 227
-- Data for Name: categories; Type: TABLE DATA; Schema: library; Owner: postgres
--

COPY library.categories (category_id, category_name) FROM stdin;
1	Computer Science
2	Database Management
3	Data Structures and Algorithms
4	Operating Systems
5	Computer Networks
6	Artificial Intelligence
\.

--
-- TOC entry 5191 (class 0 OID 16447)
-- Dependencies: 229
-- Data for Name: publishers; Type: TABLE DATA; Schema: library; Owner: postgres
--

COPY library.publishers (publisher_id, publisher_name) FROM stdin;
1	Pearson
3	McGraw Hill
4	O Reilly Media
5	Wiley
6	Prentice Hall
7	MIT Press
\.

--
-- TOC entry 5248 (class 0 OID 0)
-- Dependencies: 224
-- Name: authors_author_id_seq; Type: SEQUENCE SET; Schema: library; Owner: postgres
--

SELECT pg_catalog.setval('library.authors_author_id_seq', 9, true);

--
-- TOC entry 5249 (class 0 OID 0)
-- Dependencies: 233
-- Name: book_copies_copy_id_seq; Type: SEQUENCE SET; Schema: library; Owner: postgres
--

SELECT pg_catalog.setval('library.book_copies_copy_id_seq', 16, true);

--
-- TOC entry 5250 (class 0 OID 0)
-- Dependencies: 230
-- Name: books_book_id_seq; Type: SEQUENCE SET; Schema: library; Owner: postgres
--

SELECT pg_catalog.setval('library.books_book_id_seq', 10, true);

--
-- TOC entry 5251 (class 0 OID 0)
-- Dependencies: 226
-- Name: categories_category_id_seq; Type: SEQUENCE SET; Schema: library; Owner: postgres
--

SELECT pg_catalog.setval('library.categories_category_id_seq', 6, true);

--
-- TOC entry 5256 (class 0 OID 0)
-- Dependencies: 228
-- Name: publishers_publisher_id_seq; Type: SEQUENCE SET; Schema: library; Owner: postgres
--

SELECT pg_catalog.setval('library.publishers_publisher_id_seq', 7, true);

