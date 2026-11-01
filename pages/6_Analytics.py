
import streamlit as st
import pandas as pd
import plotly.express as px

from database.connection import get_connection
from utils.helpers import require_role

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Library Analytics",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# ADMIN-ONLY ACCESS
# ==========================================

require_role(["admin"])

# ==========================================
# DATABASE FUNCTION
# ==========================================

def fetch_data(query, params=None):

    conn = get_connection()

    if not conn:
        return None

    try:
        with conn.cursor() as cur:

            cur.execute(query, params or ())

            rows = cur.fetchall()

            columns = [
                description[0]
                for description in cur.description
            ]

        return pd.DataFrame(rows, columns=columns)

    except Exception as e:

        st.error(f"Database Error: {e}")

        return None

    finally:
        conn.close()


# ==========================================
# PAGE HEADER
# ==========================================

st.title("📊 Library Analytics Dashboard")

st.caption(
    "Admin-only analytics and library performance reports."
)

st.divider()


# ==========================================
# SUMMARY METRICS
# ==========================================

summary = fetch_data("""
    SELECT
        (SELECT COUNT(*) FROM library.books)
            AS total_books,

        (SELECT COUNT(*) FROM library.members)
            AS total_members,

        (SELECT COUNT(*) FROM library.issue_records
         WHERE status = 'issued')
            AS active_issues,

        (SELECT COUNT(*) FROM library.issue_records
         WHERE status = 'issued'
         AND due_date < CURRENT_DATE)
            AS overdue_books
""")

if summary is not None and not summary.empty:

    row = summary.iloc[0]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "📚 Total Books",
        int(row["total_books"])
    )

    c2.metric(
        "👥 Total Members",
        int(row["total_members"])
    )

    c3.metric(
        "📖 Active Issues",
        int(row["active_issues"])
    )

    c4.metric(
        "⚠️ Overdue Books",
        int(row["overdue_books"])
    )

st.divider()


# ==========================================
# MONTHLY ISSUE TREND
# ==========================================

st.subheader("📈 Monthly Book Issue Trend")

monthly = fetch_data("""
    SELECT
        DATE_TRUNC('month', issue_date) AS month,
        COUNT(*) AS total_issues
    FROM library.issue_records
    GROUP BY DATE_TRUNC('month', issue_date)
    ORDER BY month
""")

if monthly is not None and not monthly.empty:

    fig = px.line(
        monthly,
        x="month",
        y="total_issues",
        markers=True,
        title="Books Issued Per Month"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info("No monthly issue data available.")


st.divider()


# ==========================================
# MOST BORROWED BOOKS
# ==========================================

st.subheader("🏆 Most Borrowed Books")

popular = fetch_data("""
    SELECT
        b.title,
        COUNT(i.issue_id) AS borrow_count
    FROM library.issue_records i
    JOIN library.book_copies c
        ON i.copy_id = c.copy_id
    JOIN library.books b
        ON c.book_id = b.book_id
    GROUP BY b.book_id, b.title
    ORDER BY borrow_count DESC
    LIMIT 10
""")

if popular is not None and not popular.empty:

    fig = px.bar(
        popular,
        x="borrow_count",
        y="title",
        orientation="h",
        title="Top 10 Most Borrowed Books"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info("No borrowing data available.")


st.divider()


# ==========================================
# MOST ACTIVE MEMBERS
# ==========================================

st.subheader("👥 Most Active Members")

member_activity = fetch_data("""
    SELECT
        m.full_name,
        COUNT(i.issue_id) AS total_borrowed
    FROM library.members m
    JOIN library.issue_records i
        ON m.member_id = i.member_id
    GROUP BY m.member_id, m.full_name
    ORDER BY total_borrowed DESC
    LIMIT 10
""")

if member_activity is not None and not member_activity.empty:

    fig = px.bar(
        member_activity,
        x="full_name",
        y="total_borrowed",
        title="Top 10 Active Members"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info("No member activity available.")


st.divider()


# ==========================================
# FINE COLLECTION REPORT
# ==========================================

st.subheader("💰 Fine Collection Report")

fine_data = fetch_data("""
    SELECT
        COALESCE(SUM(f.fine_amount), 0) AS total_fines,
        COALESCE(SUM(p.paid_total), 0) AS collected
    FROM library.fines f
    LEFT JOIN (
        SELECT fine_id, SUM(amount) AS paid_total
        FROM library.payments
        GROUP BY fine_id
    ) p ON f.fine_id = p.fine_id
""")

if fine_data is not None and not fine_data.empty:

    total_fines = float(
        fine_data.iloc[0]["total_fines"]
    )

    collected = float(
        fine_data.iloc[0]["collected"]
    )

    outstanding = total_fines - collected

    fine_chart = pd.DataFrame({
        "Category": ["Collected", "Outstanding"],
        "Amount": [collected, outstanding]
    })

    fig = px.pie(
        fine_chart,
        names="Category",
        values="Amount",
        hole=0.4,
        title="Fine Collection Status"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Fines", f"₹{total_fines:.2f}")
    c2.metric("Collected", f"₹{collected:.2f}")
    c3.metric("Outstanding", f"₹{outstanding:.2f}")


st.divider()


# ==========================================
# OVERDUE BOOK REPORT
# ==========================================

st.subheader("⚠️ Overdue Books Report")

overdue = fetch_data("""
    SELECT
        i.issue_id,
        b.title,
        m.full_name,
        m.email,
        i.due_date,
        CURRENT_DATE - i.due_date AS days_overdue
    FROM library.issue_records i
    JOIN library.book_copies c
        ON i.copy_id = c.copy_id
    JOIN library.books b
        ON c.book_id = b.book_id
    JOIN library.members m
        ON i.member_id = m.member_id
    WHERE i.status = 'issued'
      AND i.due_date < CURRENT_DATE
    ORDER BY i.due_date
""")

if overdue is not None and not overdue.empty:

    st.dataframe(
        overdue,
        use_container_width=True,
        hide_index=True
    )

else:

    st.success("No overdue books currently!")


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "Smart Library Management System | "
    "Admin Analytics Panel"
)
