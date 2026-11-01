
import streamlit as st
import pandas as pd
from database.connection import get_connection
from utils.helpers import require_role

st.set_page_config(
    page_title="Book Management",
    page_icon="📚",
    layout="wide"
)

require_role(["admin", "librarian"])


# DATABASE FUNCTION
def fetch_data(query, params=None):
    conn = get_connection()

    if not conn:
        st.error("Database connection failed.")
        return None

    try:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]

        return pd.DataFrame(rows, columns=columns)

    except Exception as e:
        st.error(f"Database Error: {e}")
        return None

    finally:
        conn.close()


# PAGE HEADER
st.title("📚 Book Management")
st.caption("Manage and monitor library book inventory.")

st.divider()


# METRICS
total = fetch_data("SELECT COUNT(*) AS total FROM library.books")

copies = fetch_data(
    "SELECT COUNT(*) AS total FROM library.book_copies"
)

available = fetch_data("""
    SELECT COUNT(*) AS total
    FROM library.book_copies
    WHERE status = 'available'
""")

c1, c2, c3 = st.columns(3)

if total is not None:
    c1.metric("Total Titles", int(total.iloc[0, 0]))

if copies is not None:
    c2.metric("Total Copies", int(copies.iloc[0, 0]))

if available is not None:
    c3.metric("Available Copies", int(available.iloc[0, 0]))

st.divider()


# BOOK LIST
st.subheader("📖 All Library Books")

search = st.text_input("🔍 Search Books")

books = fetch_data("""
    SELECT *
    FROM library.books
    ORDER BY book_id DESC
""")

if books is not None:

    if search.strip():
        mask = books.astype(str).apply(
            lambda col: col.str.contains(
                search,
                case=False,
                na=False
            )
        ).any(axis=1)

        books = books[mask]

    st.dataframe(
        books,
        use_container_width=True,
        hide_index=True
    )

    st.caption(f"Total books displayed: {len(books)}")

else:
    st.error("Unable to load books from database.")
