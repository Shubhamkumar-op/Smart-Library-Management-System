
import streamlit as st
import pandas as pd

from database.connection import get_connection
from utils.helpers import require_role

st.set_page_config(
    page_title="Fine Management",
    page_icon="💰",
    layout="wide"
)

require_role(["admin", "librarian"])

def query_db(query, params=None):

    conn = get_connection()

    if not conn:
        st.error("Database connection failed.")
        return None

    try:
        with conn.cursor() as cur:

            cur.execute(query, params or ())

            result = cur.fetchall()

        conn.commit()
        return result

    except Exception as e:

        conn.rollback()
        st.error(f"Database Error: {e}")
        return None

    finally:
        conn.close()

st.title("💰 Fine Management")

st.caption(
    "Track library fines and process member payments."
)

summary = query_db("""
    SELECT
        COUNT(f.fine_id),
        COALESCE(SUM(f.fine_amount), 0),
        COALESCE(SUM(p.paid_amount), 0)
    FROM library.fines f
    LEFT JOIN (
        SELECT
            fine_id,
            SUM(amount) AS paid_amount
        FROM library.payments
        GROUP BY fine_id
    ) p ON f.fine_id = p.fine_id
""")

if summary is not None:

    total_records = summary[0][0]
    total_fines = float(summary[0][1])
    collected = float(summary[0][2])

    outstanding = total_fines - collected

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Fine Records",
        total_records
    )

    c2.metric(
        "Total Fines",
        f"₹{total_fines:.2f}"
    )

    c3.metric(
        "Collected",
        f"₹{collected:.2f}"
    )

    c4.metric(
        "Outstanding",
        f"₹{outstanding:.2f}"
    )


st.divider()


# ==========================================
# TABS
# ==========================================

tab1, tab2 = st.tabs([
    "📋 Fine Records",
    "💳 Record Payment"
])


# ==========================================
# TAB 1: FINE RECORDS
# ==========================================

with tab1:

    st.subheader("All Fine Records")

    records = query_db("""
        SELECT
            f.fine_id,
            f.issue_id,
            m.full_name,
            b.title,
            f.fine_amount,
            COALESCE(SUM(p.amount), 0) AS paid_amount,
            f.fine_amount - COALESCE(SUM(p.amount), 0)
                AS balance,
            f.status
        FROM library.fines f
        JOIN library.issue_records i
            ON f.issue_id = i.issue_id
        JOIN library.members m
            ON i.member_id = m.member_id
        JOIN library.book_copies c
            ON i.copy_id = c.copy_id
        JOIN library.books b
            ON c.book_id = b.book_id
        LEFT JOIN library.payments p
            ON f.fine_id = p.fine_id
        GROUP BY
            f.fine_id,
            f.issue_id,
            m.full_name,
            b.title,
            f.fine_amount,
            f.status
        ORDER BY f.fine_id DESC
    """)

    if records:

        df = pd.DataFrame(
            records,
            columns=[
                "Fine ID",
                "Issue ID",
                "Member",
                "Book",
                "Fine Amount",
                "Paid Amount",
                "Balance",
                "Status"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No fine records found.")


# ==========================================
# TAB 2: RECORD PAYMENT
# ==========================================

with tab2:

    st.subheader("Process Fine Payment")

    pending = query_db("""
        SELECT
            f.fine_id,
            f.fine_amount,
            COALESCE(SUM(p.amount), 0) AS paid_amount,
            f.fine_amount - COALESCE(SUM(p.amount), 0)
                AS balance
        FROM library.fines f
        LEFT JOIN library.payments p
            ON f.fine_id = p.fine_id
        GROUP BY
            f.fine_id,
            f.fine_amount
        HAVING
            f.fine_amount - COALESCE(SUM(p.amount), 0) > 0
        ORDER BY f.fine_id
    """)

    if pending:

        options = {
            (
                f"Fine #{r[0]} | "
                f"Total ₹{r[1]} | "
                f"Paid ₹{r[2]} | "
                f"Balance ₹{r[3]}"
            ): r
            for r in pending
        }

        selected = st.selectbox(
            "Select Fine",
            list(options.keys())
        )

        fine = options[selected]

        fine_id = int(fine[0])
        balance = float(fine[3])

        st.metric(
            "Outstanding Amount",
            f"₹{balance:.2f}"
        )

        amount = st.number_input(
            "Payment Amount (₹)",
            min_value=0.01,
            max_value=balance,
            value=balance,
            step=1.0
        )

        method = st.selectbox(
            "Payment Method",
            ["cash", "upi", "card", "online"]
        )

        reference = st.text_input(
            "Transaction Reference (optional)"
        )

        if st.button(
            "💳 Process Payment",
            type="primary",
            use_container_width=True
        ):

            if amount <= 0:

                st.error("Payment amount must be greater than zero.")

            elif amount > balance:

                st.error(
                    "Payment cannot exceed outstanding amount."
                )

            else:

                # Explicit PostgreSQL type casting
                result = query_db(
                    """
                    SELECT library.process_fine_payment(
                        %s::BIGINT,
                        %s::NUMERIC,
                        %s::VARCHAR,
                        %s::VARCHAR
                    )
                    """,
                    (
                        fine_id,
                        amount,
                        method,
                        reference.strip() or None
                    )
                )

                if result is not None:

                    st.success(
                        "Payment processed successfully!"
                    )

                    st.rerun()

    else:

        st.success("All fines are settled! No pending payments.")

st.divider()

st.caption(
    "Smart Library Management System | Fine Management"
)
