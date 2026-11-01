
import streamlit as st
import pandas as pd
from database.connection import get_connection

st.set_page_config(page_title="Issue & Return", page_icon="📚", layout="wide")

st.title("📚 Issue & Return Management")
st.caption("Issue books, process returns and monitor overdue records.")

def run_query(query, params=None, fetch=True):
    conn = get_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            result = cur.fetchall() if fetch else None
        conn.commit()
        return result if fetch else True
    except Exception as e:
        conn.rollback()
        st.error(str(e))
        return None
    finally:
        conn.close()


tab1, tab2, tab3 = st.tabs([
    "📤 Issue Book",
    "📥 Return Book",
    "📋 Active Issues"
])

# ISSUE BOOK
with tab1:
    st.subheader("Issue a Book")

    members = run_query("""
        SELECT member_id, full_name
        FROM library.members
        WHERE membership_status = 'active'
        ORDER BY full_name
    """)

    books = run_query("""
        SELECT b.book_id, b.title
        FROM library.books b
        JOIN library.book_copies c ON b.book_id = c.book_id
        WHERE c.status = 'available'
        GROUP BY b.book_id, b.title
        ORDER BY b.title
    """)

    librarians = run_query("""
        SELECT user_id, username
        FROM library.users
        ORDER BY username
    """)

    if members and books and librarians:
        member_map = {f"{m[1]} (ID: {m[0]})": m[0] for m in members}
        book_map = {f"{b[1]} (ID: {b[0]})": b[0] for b in books}
        librarian_map = {f"{u[1]} (ID: {u[0]})": u[0] for u in librarians}

        member = st.selectbox("Select Member", list(member_map))
        book = st.selectbox("Select Available Book", list(book_map))
        librarian = st.selectbox("Issued By", list(librarian_map))

        if st.button("Issue Book", type="primary"):
            result = run_query(
                "SELECT library.issue_book(%s, %s, %s)",
                (member_map[member], book_map[book],
                 librarian_map[librarian])
            )
            if result is not None:
                st.success("Book issued successfully!")
                st.rerun()
    else:
        st.warning("No active members, available books or users found.")

# RETURN BOOK
with tab2:
    st.subheader("Return Issued Book")

    issues = run_query("""
        SELECT i.issue_id, b.title, m.full_name, i.due_date
        FROM library.issue_records i
        JOIN library.book_copies c ON i.copy_id = c.copy_id
        JOIN library.books b ON c.book_id = b.book_id
        JOIN library.members m ON i.member_id = m.member_id
        WHERE i.status = 'issued'
        ORDER BY i.due_date
    """)

    if issues:
        issue_map = {
            f"Issue #{i[0]} | {i[1]} | {i[2]} | Due: {i[3]}": i[0]
            for i in issues
        }

        selected = st.selectbox("Select Issued Book", list(issue_map))

        if st.button("Return Book", type="primary"):
            result = run_query(
                "SELECT library.return_book(%s)",
                (issue_map[selected],)
            )
            if result is not None:
                st.success("Book returned successfully!")
                st.rerun()
    else:
        st.info("No active issued books.")

# ACTIVE ISSUES
with tab3:
    st.subheader("Currently Issued Books")

    records = run_query("""
        SELECT i.issue_id, b.title, m.full_name,
               i.issue_date, i.due_date, i.status
        FROM library.issue_records i
        JOIN library.book_copies c ON i.copy_id = c.copy_id
        JOIN library.books b ON c.book_id = b.book_id
        JOIN library.members m ON i.member_id = m.member_id
        WHERE i.status = 'issued'
        ORDER BY i.due_date
    """)

    if records:
        df = pd.DataFrame(
            records,
            columns=[
                "Issue ID", "Book", "Member",
                "Issue Date", "Due Date", "Status"
            ]
        )
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.metric("Active Issues", len(records))
    else:
        st.info("No active issues found.")
