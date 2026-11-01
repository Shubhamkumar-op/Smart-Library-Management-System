-- Create library PL/pgSQL functions
-- Generated from the supplied PostgreSQL 18.6 plain dump.
-- Run scripts in the order documented in README_SQL.md.

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET search_path = library, public;

--
-- TOC entry 264 (class 1255 OID 16650)
-- Name: audit_table_changes(); Type: FUNCTION; Schema: library; Owner: postgres
--

CREATE FUNCTION library.audit_table_changes() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_record JSONB;
    v_action VARCHAR(100);
    v_record_id BIGINT;
BEGIN

    IF TG_OP = 'DELETE' THEN
        v_record := to_jsonb(OLD);
        v_action := 'DELETE';
    ELSE
        v_record := to_jsonb(NEW);
        v_action := TG_OP;
    END IF;

    v_record_id := (v_record ->> TG_ARGV[0])::BIGINT;

    INSERT INTO audit_logs (
        action,
        table_name,
        record_id,
        details
    )
    VALUES (
        v_action,
        TG_TABLE_NAME,
        v_record_id,
        v_record
    );

    IF TG_OP = 'DELETE' THEN
        RETURN OLD;
    END IF;

    RETURN NEW;

END;
$$;


ALTER FUNCTION library.audit_table_changes() OWNER TO postgres;

--
-- TOC entry 261 (class 1255 OID 16631)
-- Name: issue_book(bigint, bigint, bigint); Type: FUNCTION; Schema: library; Owner: postgres
--

CREATE FUNCTION library.issue_book(p_member_id bigint, p_book_id bigint, p_librarian_id bigint) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_copy_id BIGINT;
    v_issue_id BIGINT;
BEGIN

    IF NOT EXISTS (
        SELECT 1
        FROM members
        WHERE member_id = p_member_id
        AND membership_status = 'active'
    ) THEN
        RAISE EXCEPTION 'Member is not active or does not exist';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM users
        WHERE user_id = p_librarian_id
        AND role IN ('admin', 'librarian')
        AND is_active = TRUE
    ) THEN
        RAISE EXCEPTION 'Invalid librarian account';
    END IF;

    SELECT copy_id
    INTO v_copy_id
    FROM book_copies
    WHERE book_id = p_book_id
    AND status = 'available'
    ORDER BY copy_id
    LIMIT 1
    FOR UPDATE SKIP LOCKED;

    IF v_copy_id IS NULL THEN
        RAISE EXCEPTION 'No available copies of this book';
    END IF;

    INSERT INTO issue_records (
        copy_id,
        member_id,
        issued_by,
        issue_date,
        due_date
    )
    VALUES (
        v_copy_id,
        p_member_id,
        p_librarian_id,
        CURRENT_DATE,
        CURRENT_DATE + 14
    )
    RETURNING issue_id INTO v_issue_id;

    RETURN v_issue_id;

END;
$$;


ALTER FUNCTION library.issue_book(p_member_id bigint, p_book_id bigint, p_librarian_id bigint) OWNER TO postgres;

--
-- TOC entry 262 (class 1255 OID 16633)
-- Name: process_fine_payment(bigint, numeric, character varying, character varying); Type: FUNCTION; Schema: library; Owner: postgres
--

CREATE FUNCTION library.process_fine_payment(p_fine_id bigint, p_amount numeric, p_method character varying, p_reference character varying DEFAULT NULL::character varying) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_fine_amount NUMERIC(10,2);
    v_paid_amount NUMERIC(10,2);
    v_status VARCHAR(20);
    v_payment_id BIGINT;
BEGIN

    IF p_amount <= 0 THEN
        RAISE EXCEPTION 'Payment must be greater than zero';
    END IF;

    SELECT fine_amount, status
    INTO v_fine_amount, v_status
    FROM fines
    WHERE fine_id = p_fine_id
    FOR UPDATE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Fine record not found';
    END IF;

    IF v_status IN ('paid', 'waived') THEN
        RAISE EXCEPTION 'Fine is already settled or waived';
    END IF;

    SELECT COALESCE(SUM(amount), 0)
    INTO v_paid_amount
    FROM payments
    WHERE fine_id = p_fine_id;

    IF v_paid_amount + p_amount > v_fine_amount THEN
        RAISE EXCEPTION 'Payment exceeds outstanding fine';
    END IF;

    INSERT INTO payments (
        fine_id, amount, payment_method, transaction_reference
    )
    VALUES (
        p_fine_id, p_amount, p_method, p_reference
    )
    RETURNING payment_id INTO v_payment_id;

    v_paid_amount := v_paid_amount + p_amount;

    UPDATE fines
    SET status = CASE
        WHEN v_paid_amount = v_fine_amount THEN 'paid'
        ELSE 'partial'
    END
    WHERE fine_id = p_fine_id;

    RETURN v_payment_id;

END;
$$;


ALTER FUNCTION library.process_fine_payment(p_fine_id bigint, p_amount numeric, p_method character varying, p_reference character varying) OWNER TO postgres;

--
-- TOC entry 263 (class 1255 OID 16649)
-- Name: reserve_book(bigint, bigint); Type: FUNCTION; Schema: library; Owner: postgres
--

CREATE FUNCTION library.reserve_book(p_member_id bigint, p_book_id bigint) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_reservation_id BIGINT;
BEGIN

    IF NOT EXISTS (
        SELECT 1
        FROM members
        WHERE member_id = p_member_id
        AND membership_status = 'active'
    ) THEN
        RAISE EXCEPTION 'Member is not active';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM books
        WHERE book_id = p_book_id
    ) THEN
        RAISE EXCEPTION 'Book does not exist';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM book_copies
        WHERE book_id = p_book_id
        AND status = 'available'
    ) THEN
        RAISE EXCEPTION 'Book is currently available; reservation not required';
    END IF;

    INSERT INTO reservations (
        member_id,
        book_id,
        expiry_date,
        status
    )
    VALUES (
        p_member_id,
        p_book_id,
        CURRENT_TIMESTAMP + INTERVAL '3 days',
        'pending'
    )
    RETURNING reservation_id INTO v_reservation_id;

    RETURN v_reservation_id;

END;
$$;


ALTER FUNCTION library.reserve_book(p_member_id bigint, p_book_id bigint) OWNER TO postgres;

--
-- TOC entry 260 (class 1255 OID 16632)
-- Name: return_book(bigint); Type: FUNCTION; Schema: library; Owner: postgres
--

CREATE FUNCTION library.return_book(p_issue_id bigint) RETURNS numeric
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_due_date DATE;
    v_status VARCHAR(20);
    v_fine NUMERIC(10,2);
BEGIN

    SELECT due_date, status
    INTO v_due_date, v_status
    FROM issue_records
    WHERE issue_id = p_issue_id
    FOR UPDATE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Issue record not found';
    END IF;

    IF v_status <> 'issued' THEN
        RAISE EXCEPTION 'Book is not currently issued';
    END IF;

    v_fine := GREATEST(
        CURRENT_DATE - v_due_date,
        0
    ) * 5;

    UPDATE issue_records
    SET
        return_date = CURRENT_DATE,
        status = 'returned'
    WHERE issue_id = p_issue_id;

    UPDATE fines
    SET
        fine_amount = v_fine,
        status = CASE
            WHEN v_fine = 0 THEN 'paid'
            ELSE 'unpaid'
        END
    WHERE issue_id = p_issue_id;

    IF NOT FOUND AND v_fine > 0 THEN
        INSERT INTO fines (issue_id, fine_amount)
        VALUES (p_issue_id, v_fine);
    END IF;

    RETURN v_fine;

END;
$$;


ALTER FUNCTION library.return_book(p_issue_id bigint) OWNER TO postgres;

--
-- TOC entry 248 (class 1255 OID 16629)
-- Name: update_copy_status(); Type: FUNCTION; Schema: library; Owner: postgres
--

CREATE FUNCTION library.update_copy_status() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN

        UPDATE book_copies
        SET status = 'issued'
        WHERE copy_id = NEW.copy_id;

    ELSIF TG_OP = 'UPDATE' THEN

        IF NEW.status = 'returned'
           AND OLD.status = 'issued' THEN

            UPDATE book_copies
            SET status = 'available'
            WHERE copy_id = NEW.copy_id;

        ELSIF NEW.status = 'lost'
           AND OLD.status = 'issued' THEN

            UPDATE book_copies
            SET status = 'lost'
            WHERE copy_id = NEW.copy_id;

        END IF;

    END IF;

    RETURN NEW;
END;
$$;


ALTER FUNCTION library.update_copy_status() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

