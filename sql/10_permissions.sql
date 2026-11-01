-- Apply grants from the supplied database dump.
-- Run after 09_create_roles.sql, as a PostgreSQL administrator.
-- library_app is a LOGIN role and must be created separately with your own password.

SET search_path = library, public;

--
-- TOC entry 5212 (class 0 OID 0)
-- Dependencies: 6
-- Name: SCHEMA library; Type: ACL; Schema: -; Owner: postgres
--

GRANT USAGE ON SCHEMA library TO library_analyst;
GRANT USAGE ON SCHEMA library TO library_admin;
GRANT USAGE ON SCHEMA library TO library_librarian;

--
-- TOC entry 5213 (class 0 OID 0)
-- Dependencies: 264
-- Name: FUNCTION audit_table_changes(); Type: ACL; Schema: library; Owner: postgres
--

GRANT ALL ON FUNCTION library.audit_table_changes() TO library_admin;
GRANT ALL ON FUNCTION library.audit_table_changes() TO library_librarian;

--
-- TOC entry 5214 (class 0 OID 0)
-- Dependencies: 261
-- Name: FUNCTION issue_book(p_member_id bigint, p_book_id bigint, p_librarian_id bigint); Type: ACL; Schema: library; Owner: postgres
--

GRANT ALL ON FUNCTION library.issue_book(p_member_id bigint, p_book_id bigint, p_librarian_id bigint) TO library_admin;
GRANT ALL ON FUNCTION library.issue_book(p_member_id bigint, p_book_id bigint, p_librarian_id bigint) TO library_librarian;

--
-- TOC entry 5215 (class 0 OID 0)
-- Dependencies: 262
-- Name: FUNCTION process_fine_payment(p_fine_id bigint, p_amount numeric, p_method character varying, p_reference character varying); Type: ACL; Schema: library; Owner: postgres
--

GRANT ALL ON FUNCTION library.process_fine_payment(p_fine_id bigint, p_amount numeric, p_method character varying, p_reference character varying) TO library_admin;
GRANT ALL ON FUNCTION library.process_fine_payment(p_fine_id bigint, p_amount numeric, p_method character varying, p_reference character varying) TO library_librarian;

--
-- TOC entry 5216 (class 0 OID 0)
-- Dependencies: 263
-- Name: FUNCTION reserve_book(p_member_id bigint, p_book_id bigint); Type: ACL; Schema: library; Owner: postgres
--

GRANT ALL ON FUNCTION library.reserve_book(p_member_id bigint, p_book_id bigint) TO library_admin;
GRANT ALL ON FUNCTION library.reserve_book(p_member_id bigint, p_book_id bigint) TO library_librarian;

--
-- TOC entry 5217 (class 0 OID 0)
-- Dependencies: 260
-- Name: FUNCTION return_book(p_issue_id bigint); Type: ACL; Schema: library; Owner: postgres
--

GRANT ALL ON FUNCTION library.return_book(p_issue_id bigint) TO library_admin;
GRANT ALL ON FUNCTION library.return_book(p_issue_id bigint) TO library_librarian;

--
-- TOC entry 5218 (class 0 OID 0)
-- Dependencies: 248
-- Name: FUNCTION update_copy_status(); Type: ACL; Schema: library; Owner: postgres
--

GRANT ALL ON FUNCTION library.update_copy_status() TO library_admin;
GRANT ALL ON FUNCTION library.update_copy_status() TO library_librarian;

--
-- TOC entry 5219 (class 0 OID 0)
-- Dependencies: 234
-- Name: TABLE book_copies; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT ON TABLE library.book_copies TO library_analyst;
GRANT ALL ON TABLE library.book_copies TO library_admin;
GRANT SELECT,INSERT,UPDATE ON TABLE library.book_copies TO library_librarian;

--
-- TOC entry 5220 (class 0 OID 0)
-- Dependencies: 231
-- Name: TABLE books; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT ON TABLE library.books TO library_analyst;
GRANT ALL ON TABLE library.books TO library_admin;
GRANT SELECT,INSERT,UPDATE ON TABLE library.books TO library_librarian;

--
-- TOC entry 5221 (class 0 OID 0)
-- Dependencies: 236
-- Name: TABLE issue_records; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT ON TABLE library.issue_records TO library_analyst;
GRANT ALL ON TABLE library.issue_records TO library_admin;
GRANT SELECT,INSERT,UPDATE ON TABLE library.issue_records TO library_librarian;

--
-- TOC entry 5222 (class 0 OID 0)
-- Dependencies: 223
-- Name: TABLE members; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT ON TABLE library.members TO library_analyst;
GRANT ALL ON TABLE library.members TO library_admin;
GRANT SELECT,INSERT,UPDATE ON TABLE library.members TO library_librarian;

--
-- TOC entry 5223 (class 0 OID 0)
-- Dependencies: 246
-- Name: TABLE active_issues; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT ON TABLE library.active_issues TO library_analyst;
GRANT ALL ON TABLE library.active_issues TO library_admin;
GRANT SELECT ON TABLE library.active_issues TO library_librarian;

--
-- TOC entry 5224 (class 0 OID 0)
-- Dependencies: 244
-- Name: TABLE audit_logs; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT ON TABLE library.audit_logs TO library_analyst;
GRANT ALL ON TABLE library.audit_logs TO library_admin;

--
-- TOC entry 5225 (class 0 OID 0)
-- Dependencies: 243
-- Name: SEQUENCE audit_logs_audit_id_seq; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE library.audit_logs_audit_id_seq TO library_admin;
GRANT SELECT,USAGE ON SEQUENCE library.audit_logs_audit_id_seq TO library_librarian;

--
-- TOC entry 5226 (class 0 OID 0)
-- Dependencies: 225
-- Name: TABLE authors; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT ON TABLE library.authors TO library_analyst;
GRANT ALL ON TABLE library.authors TO library_admin;
GRANT SELECT ON TABLE library.authors TO library_librarian;

--
-- TOC entry 5227 (class 0 OID 0)
-- Dependencies: 224
-- Name: SEQUENCE authors_author_id_seq; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE library.authors_author_id_seq TO library_admin;
GRANT SELECT,USAGE ON SEQUENCE library.authors_author_id_seq TO library_librarian;

--
-- TOC entry 5228 (class 0 OID 0)
-- Dependencies: 232
-- Name: TABLE book_authors; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT ON TABLE library.book_authors TO library_analyst;
GRANT ALL ON TABLE library.book_authors TO library_admin;
GRANT SELECT ON TABLE library.book_authors TO library_librarian;

--
-- TOC entry 5229 (class 0 OID 0)
-- Dependencies: 233
-- Name: SEQUENCE book_copies_copy_id_seq; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE library.book_copies_copy_id_seq TO library_admin;
GRANT SELECT,USAGE ON SEQUENCE library.book_copies_copy_id_seq TO library_librarian;

--
-- TOC entry 5230 (class 0 OID 0)
-- Dependencies: 227
-- Name: TABLE categories; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT ON TABLE library.categories TO library_analyst;
GRANT ALL ON TABLE library.categories TO library_admin;
GRANT SELECT ON TABLE library.categories TO library_librarian;

--
-- TOC entry 5231 (class 0 OID 0)
-- Dependencies: 229
-- Name: TABLE publishers; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT ON TABLE library.publishers TO library_analyst;
GRANT ALL ON TABLE library.publishers TO library_admin;
GRANT SELECT ON TABLE library.publishers TO library_librarian;

--
-- TOC entry 5232 (class 0 OID 0)
-- Dependencies: 247
-- Name: TABLE book_inventory; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT ON TABLE library.book_inventory TO library_analyst;
GRANT ALL ON TABLE library.book_inventory TO library_admin;
GRANT SELECT ON TABLE library.book_inventory TO library_librarian;

--
-- TOC entry 5233 (class 0 OID 0)
-- Dependencies: 230
-- Name: SEQUENCE books_book_id_seq; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE library.books_book_id_seq TO library_admin;
GRANT SELECT,USAGE ON SEQUENCE library.books_book_id_seq TO library_librarian;

--
-- TOC entry 5234 (class 0 OID 0)
-- Dependencies: 226
-- Name: SEQUENCE categories_category_id_seq; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE library.categories_category_id_seq TO library_admin;
GRANT SELECT,USAGE ON SEQUENCE library.categories_category_id_seq TO library_librarian;

--
-- TOC entry 5235 (class 0 OID 0)
-- Dependencies: 238
-- Name: TABLE fines; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT ON TABLE library.fines TO library_analyst;
GRANT ALL ON TABLE library.fines TO library_admin;
GRANT SELECT,INSERT,UPDATE ON TABLE library.fines TO library_librarian;

--
-- TOC entry 5236 (class 0 OID 0)
-- Dependencies: 240
-- Name: TABLE payments; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT ON TABLE library.payments TO library_analyst;
GRANT ALL ON TABLE library.payments TO library_admin;
GRANT SELECT,INSERT,UPDATE ON TABLE library.payments TO library_librarian;

--
-- TOC entry 5237 (class 0 OID 0)
-- Dependencies: 245
-- Name: TABLE fine_payment_summary; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT ON TABLE library.fine_payment_summary TO library_analyst;
GRANT ALL ON TABLE library.fine_payment_summary TO library_admin;
GRANT SELECT ON TABLE library.fine_payment_summary TO library_librarian;

--
-- TOC entry 5238 (class 0 OID 0)
-- Dependencies: 237
-- Name: SEQUENCE fines_fine_id_seq; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE library.fines_fine_id_seq TO library_admin;
GRANT SELECT,USAGE ON SEQUENCE library.fines_fine_id_seq TO library_librarian;

--
-- TOC entry 5239 (class 0 OID 0)
-- Dependencies: 235
-- Name: SEQUENCE issue_records_issue_id_seq; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE library.issue_records_issue_id_seq TO library_admin;
GRANT SELECT,USAGE ON SEQUENCE library.issue_records_issue_id_seq TO library_librarian;

--
-- TOC entry 5240 (class 0 OID 0)
-- Dependencies: 222
-- Name: SEQUENCE members_member_id_seq; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE library.members_member_id_seq TO library_admin;
GRANT SELECT,USAGE ON SEQUENCE library.members_member_id_seq TO library_librarian;

--
-- TOC entry 5241 (class 0 OID 0)
-- Dependencies: 239
-- Name: SEQUENCE payments_payment_id_seq; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE library.payments_payment_id_seq TO library_admin;
GRANT SELECT,USAGE ON SEQUENCE library.payments_payment_id_seq TO library_librarian;

--
-- TOC entry 5242 (class 0 OID 0)
-- Dependencies: 228
-- Name: SEQUENCE publishers_publisher_id_seq; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE library.publishers_publisher_id_seq TO library_admin;
GRANT SELECT,USAGE ON SEQUENCE library.publishers_publisher_id_seq TO library_librarian;

--
-- TOC entry 5243 (class 0 OID 0)
-- Dependencies: 242
-- Name: TABLE reservations; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT ON TABLE library.reservations TO library_analyst;
GRANT ALL ON TABLE library.reservations TO library_admin;
GRANT SELECT,INSERT,UPDATE ON TABLE library.reservations TO library_librarian;

--
-- TOC entry 5244 (class 0 OID 0)
-- Dependencies: 241
-- Name: SEQUENCE reservations_reservation_id_seq; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE library.reservations_reservation_id_seq TO library_admin;
GRANT SELECT,USAGE ON SEQUENCE library.reservations_reservation_id_seq TO library_librarian;

--
-- TOC entry 5245 (class 0 OID 0)
-- Dependencies: 221
-- Name: TABLE users; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT ON TABLE library.users TO library_analyst;
GRANT ALL ON TABLE library.users TO library_admin;
-- Optional: after creating library_app, grant it SELECT on library.users for login verification.
--
-- TOC entry 5246 (class 0 OID 0)
-- Dependencies: 220
-- Name: SEQUENCE users_user_id_seq; Type: ACL; Schema: library; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE library.users_user_id_seq TO library_admin;
GRANT SELECT,USAGE ON SEQUENCE library.users_user_id_seq TO library_librarian;

--
-- TOC entry 2130 (class 826 OID 16659)
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: library; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA library GRANT SELECT ON TABLES TO library_analyst;


-- Completed on 2026-11-01 22:34:44

--
-- PostgreSQL database dump complete
--

\unrestrict J46wniZ9LCEfhvbZPByMS49FrOrsYH7Av6n1HPEBJMcfKrOJUfRCv3P1OXtuXWS

