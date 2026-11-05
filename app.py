
import streamlit as st
import pandas as pd
import plotly.express as px

from database.connection import get_connection
from utils.helpers import require_login


st.set_page_config(
    page_title="Smart Library Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }

    [data-testid="stSidebar"] {
        background-color: #0e1117;
    }

    [data-testid="stSidebar"] * {
        color: #ffffff;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    [data-testid="stMetric"] {
        background-color: #1c212b;
        padding: 18px;
        border-radius: 10px;
        border: 1px solid #303641;
    }

    [data-testid="stMetricLabel"] {
        color: #c5cbd5;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff;
    }

    h1, h2, h3 {
        color: #ffffff !important;
    }

    p, label {
        color: #d0d4dc;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #303641;
        border-radius: 8px;
    }

    div.stButton > button {
        border-radius: 7px;
    }

    hr {
        border-color: #303641;
    }
</style>
""", unsafe_allow_html=True)


require_login()


def fetch_data(query, params=None):

    conn = get_connection()

    if not conn:
        st.error("Database connection failed.")
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


def get_count(result):

    if result and result[0]:
        return result[0][0]

    return 0


with st.sidebar:

    st.title("📚 Smart Library")
    st.caption("Library Management System")

    st.divider()

    user = st.session_state.get("user", {})

    st.success("Database Connected")

    st.write(
        "**User:**",
        user.get(
            "username",
            st.session_state.get("username", "User")
        )
    )

    st.write(
        "**Role:**",
        user.get(
            "role",
            st.session_state.get("role", "Unknown")
        )
    )

    st.divider()

    st.caption("Manage books, members and library records.")


st.title("📚 Library Dashboard")

st.caption(
    "Here's an overview of the library's current activity."
)


if st.button("🔄 Refresh Dashboard"):
    st.rerun()


st.divider()


total_books = fetch_data("""
    SELECT COUNT(*)
    FROM library.books
    WHERE is_active = TRUE
""")


total_copies = fetch_data("""
    SELECT COUNT(*)
    FROM library.book_copies bc
    JOIN library.books b
        ON bc.book_id = b.book_id
    WHERE b.is_active = TRUE
""")


available_copies = fetch_data("""
    SELECT COUNT(*)
    FROM library.book_copies bc
    JOIN library.books b
        ON bc.book_id = b.book_id
    WHERE bc.status = 'available'
    AND b.is_active = TRUE
""")


active_members = fetch_data("""
    SELECT COUNT(*)
    FROM library.members
    WHERE membership_status = 'active'
""")


active_issues = fetch_data("""
    SELECT COUNT(*)
    FROM library.issue_records i
    JOIN library.book_copies bc
        ON i.copy_id = bc.copy_id
    JOIN library.books b
        ON bc.book_id = b.book_id
    WHERE i.status = 'issued'
    AND b.is_active = TRUE
""")


overdue_books = fetch_data("""
    SELECT COUNT(*)
    FROM library.issue_records i
    JOIN library.book_copies bc
        ON i.copy_id = bc.copy_id
    JOIN library.books b
        ON bc.book_id = b.book_id
    WHERE i.status = 'issued'
    AND i.due_date < CURRENT_DATE
    AND b.is_active = TRUE
""")


st.subheader("Library Overview")


c1, c2, c3 = st.columns(3)

c1.metric(
    "📚 Active Titles",
    get_count(total_books)
)

c2.metric(
    "📦 Total Copies",
    get_count(total_copies)
)

c3.metric(
    "👥 Active Members",
    get_count(active_members)
)


c4, c5, c6 = st.columns(3)

c4.metric(
    "✅ Available Copies",
    get_count(available_copies)
)

c5.metric(
    "📖 Active Issues",
    get_count(active_issues)
)

c6.metric(
    "⚠️ Overdue Books",
    get_count(overdue_books)
)


st.divider()


st.subheader("Book Inventory by Category")


category_data = fetch_data("""
    SELECT
        cat.category_name,
        COUNT(bc.copy_id) AS total_copies
    FROM library.categories cat
    LEFT JOIN library.books b
        ON cat.category_id = b.category_id
        AND b.is_active = TRUE
    LEFT JOIN library.book_copies bc
        ON b.book_id = bc.book_id
    GROUP BY
        cat.category_id,
        cat.category_name
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
        text="Total Copies"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        font_color="#ffffff",
        xaxis_title="Category",
        yaxis_title="Number of Copies",
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info("No category inventory data available.")


st.divider()


st.subheader("Recently Added Books")


recent_books = fetch_data("""
    SELECT
        book_id,
        title,
        isbn,
        publication_year,
        created_at
    FROM library.books
    WHERE is_active = TRUE
    ORDER BY created_at DESC, book_id DESC
    LIMIT 5
""")


if recent_books:

    df_books = pd.DataFrame(
        recent_books,
        columns=[
            "Book ID",
            "Book Title",
            "ISBN",
            "Publication Year",
            "Date Added"
        ]
    )

    st.dataframe(
        df_books,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No recent books available.")


st.divider()


st.subheader("Recent Issue Transactions")


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


st.markdown(
    """
    <div style="text-align:center; padding:15px; color:gray;">
        📚 Smart Library Management System
    </div>
    """,
    unsafe_allow_html=True
)
