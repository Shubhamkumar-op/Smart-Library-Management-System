
import streamlit as st
import pandas as pd
from datetime import date
from database.connection import get_connection

st.set_page_config(
    page_title="Member Management",
    page_icon="👥",
    layout="wide"
)

st.title("👥 Member Management")
st.caption("Manage library members and membership status.")

def fetch_data(query, params=None):
    conn = get_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            return cur.fetchall()
    finally:
        conn.close()


def execute_query(query, params=None):
    conn = get_connection()
    if not conn:
        return False, "Database connection failed."

    try:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
        conn.commit()
        return True, "Operation completed successfully."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()


# Dashboard metrics
col1, col2, col3 = st.columns(3)

total = fetch_data("SELECT COUNT(*) FROM members")
active = fetch_data(
    "SELECT COUNT(*) FROM members WHERE membership_status = 'active'"
)
inactive = fetch_data(
    "SELECT COUNT(*) FROM members WHERE membership_status = 'inactive'"
)

col1.metric("Total Members", total[0][0] if total else 0)
col2.metric("Active Members", active[0][0] if active else 0)
col3.metric("Inactive Members", inactive[0][0] if inactive else 0)

st.divider()

tab1, tab2, tab3 = st.tabs([
    "➕ Add Member",
    "📋 View / Search Members",
    "✏️ Update Membership"
])


# ADD MEMBER
with tab1:
    st.subheader("Register New Member")

    with st.form("add_member_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        department = st.text_input("Department")

        membership_date = st.date_input(
            "Membership Date",
            value=date.today()
        )

        submitted = st.form_submit_button(
            "Add Member",
            use_container_width=True
        )

        if submitted:
            if not name.strip() or not email.strip():
                st.error("Name and email are required.")
            else:
                query = """
                    INSERT INTO members
                    (full_name, email, phone, department,
                     membership_date, membership_status)
                    VALUES (%s, %s, %s, %s, %s, 'active')
                """

                success, message = execute_query(
                    query,
                    (
                        name.strip(),
                        email.strip(),
                        phone.strip() or None,
                        department.strip() or None,
                        membership_date
                    )
                )

                if success:
                    st.success("Member added successfully!")
                    st.rerun()
                else:
                    st.error(message)


# VIEW MEMBERS
with tab2:
    st.subheader("All Library Members")

    search = st.text_input(
        "Search by name, email or department"
    )

    query = """
        SELECT member_id, full_name, email, phone,
               department, membership_date, membership_status
        FROM members
        WHERE full_name ILIKE %s
           OR email ILIKE %s
           OR COALESCE(department, '') ILIKE %s
        ORDER BY member_id
    """

    term = f"%{search}%"
    members = fetch_data(query, (term, term, term))

    if members:
        columns = [
            "Member ID", "Full Name", "Email",
            "Phone", "Department", "Membership Date",
            "Status"
        ]

        df = pd.DataFrame(members, columns=columns)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"Showing {len(df)} member(s).")
    else:
        st.info("No members found.")


# UPDATE MEMBERSHIP
with tab3:
    st.subheader("Update Membership Status")

    members = fetch_data("""
        SELECT member_id, full_name, membership_status
        FROM members
        ORDER BY member_id
    """)

    if members:
        member_options = {
            f"{m[0]} - {m[1]} ({m[2] or 'unknown'})": m[0]
            for m in members
        }

        selected = st.selectbox(
            "Select Member",
            list(member_options.keys())
        )

        new_status = st.selectbox(
            "New Membership Status",
            ["active", "inactive"]
        )

        if st.button("Update Status", use_container_width=True):
            member_id = member_options[selected]

            success, message = execute_query(
                """
                UPDATE members
                SET membership_status = %s
                WHERE member_id = %s
                """,
                (new_status, member_id)
            )

            if success:
                st.success("Membership status updated!")
                st.rerun()
            else:
                st.error(message)
    else:
        st.info("No members available.")
