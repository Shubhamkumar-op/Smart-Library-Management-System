-- Create library views
-- Generated from the supplied PostgreSQL 18.6 plain dump.
-- Run scripts in the order documented in README_SQL.md.

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET search_path = library, public;

--
-- TOC entry 246 (class 1259 OID 16639)
-- Name: active_issues; Type: VIEW; Schema: library; Owner: postgres
--

CREATE VIEW library.active_issues AS
 SELECT ir.issue_id,
    m.full_name,
    m.email,
    b.title,
    bc.accession_number,
    ir.issue_date,
    ir.due_date,
    (CURRENT_DATE - ir.due_date) AS days_past_due,
        CASE
            WHEN (ir.due_date < CURRENT_DATE) THEN 'Overdue'::text
            ELSE 'Within Due Date'::text
        END AS borrowing_status
   FROM (((library.issue_records ir
     JOIN library.members m ON ((ir.member_id = m.member_id)))
     JOIN library.book_copies bc ON ((ir.copy_id = bc.copy_id)))
     JOIN library.books b ON ((bc.book_id = b.book_id)))
  WHERE ((ir.status)::text = 'issued'::text);


ALTER VIEW library.active_issues OWNER TO postgres;

--
-- TOC entry 247 (class 1259 OID 16644)
-- Name: book_inventory; Type: VIEW; Schema: library; Owner: postgres
--

CREATE VIEW library.book_inventory AS
 SELECT b.book_id,
    b.title,
    b.isbn,
    c.category_name,
    p.publisher_name,
    count(bc.copy_id) AS total_copies,
    count(bc.copy_id) FILTER (WHERE ((bc.status)::text = 'available'::text)) AS available_copies,
    count(bc.copy_id) FILTER (WHERE ((bc.status)::text = 'issued'::text)) AS issued_copies,
    count(bc.copy_id) FILTER (WHERE ((bc.status)::text = 'lost'::text)) AS lost_copies
   FROM (((library.books b
     LEFT JOIN library.categories c ON ((b.category_id = c.category_id)))
     LEFT JOIN library.publishers p ON ((b.publisher_id = p.publisher_id)))
     LEFT JOIN library.book_copies bc ON ((b.book_id = bc.book_id)))
  GROUP BY b.book_id, b.title, b.isbn, c.category_name, p.publisher_name;


ALTER VIEW library.book_inventory OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 16634)
-- Name: fine_payment_summary; Type: VIEW; Schema: library; Owner: postgres
--

CREATE VIEW library.fine_payment_summary AS
 SELECT f.fine_id,
    f.issue_id,
    m.full_name,
    b.title,
    f.fine_amount,
    COALESCE(sum(p.amount), (0)::numeric) AS paid_amount,
    (f.fine_amount - COALESCE(sum(p.amount), (0)::numeric)) AS remaining_amount,
    f.status
   FROM (((((library.fines f
     JOIN library.issue_records ir ON ((f.issue_id = ir.issue_id)))
     JOIN library.members m ON ((ir.member_id = m.member_id)))
     JOIN library.book_copies bc ON ((ir.copy_id = bc.copy_id)))
     JOIN library.books b ON ((bc.book_id = b.book_id)))
     LEFT JOIN library.payments p ON ((f.fine_id = p.fine_id)))
  GROUP BY f.fine_id, f.issue_id, m.full_name, b.title, f.fine_amount, f.status;


ALTER VIEW library.fine_payment_summary OWNER TO postgres;

