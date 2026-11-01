-- Create all tables and identity sequences
-- Generated from the supplied PostgreSQL 18.6 plain dump.
-- Run scripts in the order documented in README_SQL.md.

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET search_path = library, public;

--
-- TOC entry 234 (class 1259 OID 16498)
-- Name: book_copies; Type: TABLE; Schema: library; Owner: postgres
--

CREATE TABLE library.book_copies (
    copy_id bigint NOT NULL,
    book_id bigint NOT NULL,
    accession_number character varying(50) NOT NULL,
    status character varying(20) DEFAULT 'available'::character varying,
    acquired_date date DEFAULT CURRENT_DATE,
    CONSTRAINT book_copies_status_check CHECK (((status)::text = ANY ((ARRAY['available'::character varying, 'issued'::character varying, 'lost'::character varying, 'damaged'::character varying, 'maintenance'::character varying])::text[])))
);


ALTER TABLE library.book_copies OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 16457)
-- Name: books; Type: TABLE; Schema: library; Owner: postgres
--

CREATE TABLE library.books (
    book_id bigint NOT NULL,
    isbn character varying(20) NOT NULL,
    title character varying(200) NOT NULL,
    category_id bigint,
    publisher_id bigint,
    publication_year integer,
    edition character varying(50),
    language character varying(50) DEFAULT 'English'::character varying,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT books_publication_year_check CHECK (((publication_year >= 1400) AND (publication_year <= 2100)))
);


ALTER TABLE library.books OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 16517)
-- Name: issue_records; Type: TABLE; Schema: library; Owner: postgres
--

CREATE TABLE library.issue_records (
    issue_id bigint NOT NULL,
    copy_id bigint NOT NULL,
    member_id bigint NOT NULL,
    issued_by bigint NOT NULL,
    issue_date date DEFAULT CURRENT_DATE NOT NULL,
    due_date date NOT NULL,
    return_date date,
    renewal_count integer DEFAULT 0,
    status character varying(20) DEFAULT 'issued'::character varying,
    CONSTRAINT issue_records_check CHECK ((due_date >= issue_date)),
    CONSTRAINT issue_records_check1 CHECK (((((status)::text = 'returned'::text) AND (return_date IS NOT NULL)) OR (((status)::text <> 'returned'::text) AND (return_date IS NULL)))),
    CONSTRAINT issue_records_check2 CHECK (((return_date IS NULL) OR (return_date >= issue_date))),
    CONSTRAINT issue_records_renewal_count_check CHECK ((renewal_count >= 0)),
    CONSTRAINT issue_records_status_check CHECK (((status)::text = ANY ((ARRAY['issued'::character varying, 'returned'::character varying, 'lost'::character varying])::text[])))
);


ALTER TABLE library.issue_records OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16408)
-- Name: members; Type: TABLE; Schema: library; Owner: postgres
--

CREATE TABLE library.members (
    member_id bigint NOT NULL,
    user_id bigint,
    full_name character varying(100) NOT NULL,
    email character varying(150) NOT NULL,
    phone character varying(20),
    department character varying(100),
    membership_date date DEFAULT CURRENT_DATE,
    membership_status character varying(20) DEFAULT 'active'::character varying,
    CONSTRAINT members_membership_status_check CHECK (((membership_status)::text = ANY ((ARRAY['active'::character varying, 'suspended'::character varying, 'expired'::character varying])::text[])))
);


ALTER TABLE library.members OWNER TO postgres;

--
-- TOC entry 244 (class 1259 OID 16613)
-- Name: audit_logs; Type: TABLE; Schema: library; Owner: postgres
--

CREATE TABLE library.audit_logs (
    audit_id bigint NOT NULL,
    user_id bigint,
    action character varying(100) NOT NULL,
    table_name character varying(100) NOT NULL,
    record_id bigint,
    details jsonb,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE library.audit_logs OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 16612)
-- Name: audit_logs_audit_id_seq; Type: SEQUENCE; Schema: library; Owner: postgres
--

ALTER TABLE library.audit_logs ALTER COLUMN audit_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME library.audit_logs_audit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

--
-- TOC entry 225 (class 1259 OID 16429)
-- Name: authors; Type: TABLE; Schema: library; Owner: postgres
--

CREATE TABLE library.authors (
    author_id bigint NOT NULL,
    author_name character varying(150) NOT NULL
);


ALTER TABLE library.authors OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 16428)
-- Name: authors_author_id_seq; Type: SEQUENCE; Schema: library; Owner: postgres
--

ALTER TABLE library.authors ALTER COLUMN author_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME library.authors_author_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

--
-- TOC entry 232 (class 1259 OID 16480)
-- Name: book_authors; Type: TABLE; Schema: library; Owner: postgres
--

CREATE TABLE library.book_authors (
    book_id bigint NOT NULL,
    author_id bigint NOT NULL
);


ALTER TABLE library.book_authors OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 16497)
-- Name: book_copies_copy_id_seq; Type: SEQUENCE; Schema: library; Owner: postgres
--

ALTER TABLE library.book_copies ALTER COLUMN copy_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME library.book_copies_copy_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

--
-- TOC entry 227 (class 1259 OID 16437)
-- Name: categories; Type: TABLE; Schema: library; Owner: postgres
--

CREATE TABLE library.categories (
    category_id bigint NOT NULL,
    category_name character varying(100) NOT NULL
);


ALTER TABLE library.categories OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16447)
-- Name: publishers; Type: TABLE; Schema: library; Owner: postgres
--

CREATE TABLE library.publishers (
    publisher_id bigint NOT NULL,
    publisher_name character varying(150) NOT NULL
);


ALTER TABLE library.publishers OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 16456)
-- Name: books_book_id_seq; Type: SEQUENCE; Schema: library; Owner: postgres
--

ALTER TABLE library.books ALTER COLUMN book_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME library.books_book_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

--
-- TOC entry 226 (class 1259 OID 16436)
-- Name: categories_category_id_seq; Type: SEQUENCE; Schema: library; Owner: postgres
--

ALTER TABLE library.categories ALTER COLUMN category_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME library.categories_category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

--
-- TOC entry 238 (class 1259 OID 16553)
-- Name: fines; Type: TABLE; Schema: library; Owner: postgres
--

CREATE TABLE library.fines (
    fine_id bigint NOT NULL,
    issue_id bigint NOT NULL,
    fine_amount numeric(10,2) NOT NULL,
    status character varying(20) DEFAULT 'unpaid'::character varying,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fines_fine_amount_check CHECK ((fine_amount >= (0)::numeric)),
    CONSTRAINT fines_status_check CHECK (((status)::text = ANY ((ARRAY['unpaid'::character varying, 'partial'::character varying, 'paid'::character varying, 'waived'::character varying])::text[])))
);


ALTER TABLE library.fines OWNER TO postgres;

--
-- TOC entry 240 (class 1259 OID 16573)
-- Name: payments; Type: TABLE; Schema: library; Owner: postgres
--

CREATE TABLE library.payments (
    payment_id bigint NOT NULL,
    fine_id bigint NOT NULL,
    amount numeric(10,2) NOT NULL,
    payment_date timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    payment_method character varying(30),
    transaction_reference character varying(100),
    CONSTRAINT payments_amount_check CHECK ((amount > (0)::numeric)),
    CONSTRAINT payments_payment_method_check CHECK (((payment_method)::text = ANY ((ARRAY['cash'::character varying, 'upi'::character varying, 'card'::character varying, 'online'::character varying])::text[])))
);


ALTER TABLE library.payments OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 16552)
-- Name: fines_fine_id_seq; Type: SEQUENCE; Schema: library; Owner: postgres
--

ALTER TABLE library.fines ALTER COLUMN fine_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME library.fines_fine_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

--
-- TOC entry 235 (class 1259 OID 16516)
-- Name: issue_records_issue_id_seq; Type: SEQUENCE; Schema: library; Owner: postgres
--

ALTER TABLE library.issue_records ALTER COLUMN issue_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME library.issue_records_issue_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

--
-- TOC entry 222 (class 1259 OID 16407)
-- Name: members_member_id_seq; Type: SEQUENCE; Schema: library; Owner: postgres
--

ALTER TABLE library.members ALTER COLUMN member_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME library.members_member_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

--
-- TOC entry 239 (class 1259 OID 16572)
-- Name: payments_payment_id_seq; Type: SEQUENCE; Schema: library; Owner: postgres
--

ALTER TABLE library.payments ALTER COLUMN payment_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME library.payments_payment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

--
-- TOC entry 228 (class 1259 OID 16446)
-- Name: publishers_publisher_id_seq; Type: SEQUENCE; Schema: library; Owner: postgres
--

ALTER TABLE library.publishers ALTER COLUMN publisher_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME library.publishers_publisher_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

--
-- TOC entry 242 (class 1259 OID 16590)
-- Name: reservations; Type: TABLE; Schema: library; Owner: postgres
--

CREATE TABLE library.reservations (
    reservation_id bigint NOT NULL,
    member_id bigint NOT NULL,
    book_id bigint NOT NULL,
    reservation_date timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    expiry_date timestamp with time zone,
    status character varying(20) DEFAULT 'pending'::character varying,
    CONSTRAINT reservations_status_check CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'fulfilled'::character varying, 'cancelled'::character varying, 'expired'::character varying])::text[])))
);


ALTER TABLE library.reservations OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 16589)
-- Name: reservations_reservation_id_seq; Type: SEQUENCE; Schema: library; Owner: postgres
--

ALTER TABLE library.reservations ALTER COLUMN reservation_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME library.reservations_reservation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

--
-- TOC entry 221 (class 1259 OID 16391)
-- Name: users; Type: TABLE; Schema: library; Owner: postgres
--

CREATE TABLE library.users (
    user_id bigint NOT NULL,
    username character varying(50) NOT NULL,
    password_hash text NOT NULL,
    role character varying(20) NOT NULL,
    is_active boolean DEFAULT true,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT users_role_check CHECK (((role)::text = ANY ((ARRAY['admin'::character varying, 'librarian'::character varying])::text[])))
);


ALTER TABLE library.users OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16390)
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: library; Owner: postgres
--

ALTER TABLE library.users ALTER COLUMN user_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME library.users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

