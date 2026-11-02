
import streamlit as st
import pandas as pd
from database.connection import get_connection

st.set_page_config(
    page_title="Reservations",
    page_icon="📖",
    layout="wide"
)

st.title("📖 Book Reservations")
st.caption("Reserve unavailable books and manage reservation requests.")


def db_query(query, params=None):

    conn = get_connection()

    if not conn:
        return None

    try:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            result = cur.fetchall()

        conn.commit()
        return result

    except Exception as e:
        conn.rollback()
        st.error(str(e))
        return None

    finally:
        conn.close()


tab1, tab2 = st.tabs([
    "➕ Reserve Book",
    "📋 Reservation Records"
])


# ==========================================
# CREATE RESERVATION
# ==========================================

with tab1:

    st.subheader("Create Reservation")

    members = db_query("""
        SELECT member_id, full_name
        FROM library.members
        WHERE membership_status = 'active'
        ORDER BY full_name
    """)

    books = db_query("""
        SELECT book_id, title
        FROM library.books
        WHERE is_active = TRUE
        ORDER BY title
    """)

    if members and books:

        member_map = {
            f"{m[1]} (ID: {m[0]})": m[0]
            for m in members
        }

        book_map = {
            f"{b[1]} (ID: {b[0]})": b[0]
            for b in books
        }

        member = st.selectbox(
            "Select Member",
            list(member_map)
        )

        book = st.selectbox(
            "Select Book",
            list(book_map)
        )

        if st.button("Reserve Book", type="primary"):

            result = db_query(
                "SELECT library.reserve_book(%s, %s)",
                (member_map[member], book_map[book])
            )

            if result is not None:
                st.success("Reservation created successfully!")
                st.rerun()

    else:

        st.warning("Active members or books are not available.")


# ==========================================
# ACTIVE RESERVATIONS
# ==========================================

with tab2:

    st.subheader("Pending Reservations")

    records = db_query("""
        SELECT
            r.reservation_id,
            m.full_name,
            b.title,
            r.reservation_date,
            r.expiry_date,
            r.status

        FROM library.reservations r

        JOIN library.members m
            ON r.member_id = m.member_id

        JOIN library.books b
            ON r.book_id = b.book_id

        WHERE r.status = 'pending'

        ORDER BY r.reservation_id DESC
    """)

    if records:

        df = pd.DataFrame(records, columns=[
            "Reservation ID",
            "Member",
            "Book",
            "Reservation Date",
            "Expiry Date",
            "Status"
        ])

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Total pending reservations: {len(df)}"
        )

    else:

        st.success("No pending reservations. All reservations are cleared!")
