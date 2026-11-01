
import streamlit as st
import pandas as pd
import plotly.express as px

from database.connection import get_connection
from utils.helpers import require_login

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Smart Library Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# LOGIN PROTECTION
# --------------------------------------------------

require_login()

# --------------------------------------------------
# DATABASE FUNCTION
# --------------------------------------------------

def fetch_data(query, params=None):
    conn = get_connection()

    if not conn:
        return None

    try:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            rows = cur.fetchall()

        return rows

    except Exception as e:
        st.error(f"Database Error: {e}")
        return None

    finally:
        conn.close()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.title("📚 Smart Library")
    st.caption("Management System")

    st.divider()

    user = st.session_state.get("user", {})

    st.success("Database Connected")
    st.info(
        f"Logged in as: {user.get('username', 'User')}"
    )

    st.caption(
        f"Role: {user.get('role', 'Unknown')}"
    )

    st.divider()

    st.markdown("### M.Tech DBMS Project")
    st.caption("PostgreSQL + Python + Streamlit")


# --------------------------------------------------
# MAIN DASHBOARD
# --------------------------------------------------

st.title("📚 Library Management Dashboard")

st.caption(
    "Monitor books, members, circulation and library performance."
)

st.divider()

# --------------------------------------------------
# FETCH DASHBOARD METRICS
# --------------------------------------------------

total_books = fetch_data("""
    SELECT COUNT(*) FROM library.books
""")

total_copies = fetch_data("""
    SELECT COUNT(*) FROM library.book_copies
""")

available_copies = fetch_data("""
    SELECT COUNT(*)
    FROM library.book_copies
    WHERE status = 'available'
""")

active_members = fetch_data("""
    SELECT COUNT(*)
    FROM library.members
    WHERE membership_status = 'active'
""")

active_issues = fetch_data("""
    SELECT COUNT(*)
    FROM library.issue_records
    WHERE status = 'issued'
""")

overdue_books = fetch_data("""
    SELECT COUNT(*)
    FROM library.issue_records
    WHERE status = 'issued'
      AND due_date < CURRENT_DATE
""")

# --------------------------------------------------
# METRIC CARDS
# --------------------------------------------------

def get_count(result):
    if result and result[0]:
        return result[0][0]
    return 0


st.subheader("📊 Library Overview")

c1, c2, c3 = st.columns(3)

c1.metric("📚 Total Titles", get_count(total_books))
c2.metric("📦 Total Copies", get_count(total_copies))
c3.metric("👥 Active Members", get_count(active_members))

c4, c5, c6 = st.columns(3)

c4.metric("✅ Available Copies", get_count(available_copies))
c5.metric("📖 Active Issues", get_count(active_issues))
c6.metric("⚠️ Overdue Books", get_count(overdue_books))

st.divider()

# --------------------------------------------------
# BOOK INVENTORY BY CATEGORY
# --------------------------------------------------

st.subheader("📊 Book Inventory by Category")

category_data = fetch_data("""
    SELECT
        cat.category_name,
        COUNT(bc.copy_id) AS total_copies
    FROM library.categories cat
    LEFT JOIN library.books b
        ON cat.category_id = b.category_id
    LEFT JOIN library.book_copies bc
        ON b.book_id = bc.book_id
    GROUP BY cat.category_id, cat.category_name
    ORDER BY total_copies DESC
""")

if category_data:

    df_category = pd.DataFrame(
        category_data,
        columns=["Category", "Total Copies"]
    )

    fig = px.bar(
        df_category,
        x="Category",
        y="Total Copies",
        title="Physical Copies Across Categories",
        text="Total Copies"
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Book Category",
        yaxis_title="Number of Copies"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:
    st.info("No category inventory data available.")

st.divider()

# --------------------------------------------------
# RECENT ISSUE TRANSACTIONS
# --------------------------------------------------

st.subheader("📖 Recent Issue Transactions")

recent_issues = fetch_data("""
    SELECT
        i.issue_id,
        b.title,
        m.full_name,
        i.issue_date,
        i.due_date,
        i.status
    FROM library.issue_records i
    JOIN library.book_copies bc
        ON i.copy_id = bc.copy_id
    JOIN library.books b
        ON bc.book_id = b.book_id
    JOIN library.members m
        ON i.member_id = m.member_id
    ORDER BY i.issue_id DESC
    LIMIT 10
""")

if recent_issues:

    df_issues = pd.DataFrame(
        recent_issues,
        columns=[
            "Issue ID",
            "Book Title",
            "Member",
            "Issue Date",
            "Due Date",
            "Status"
        ]
    )

    st.dataframe(
        df_issues,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("No issue transactions available.")

st.divider()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div style="text-align:center; padding:20px;">
        <h4>📚 Smart Library Management System</h4>
        <p>M.Tech DBMS Project | PostgreSQL Database</p>
        <p>Developed using Python and Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)
