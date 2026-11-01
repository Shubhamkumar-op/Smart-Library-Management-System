
import streamlit as st
import bcrypt

from database.connection import (
    get_auth_connection
)


# ==========================================
# 1. VERIFY LOGIN
# ==========================================

def verify_login(username, password):

    conn = None

    try:
        conn = get_auth_connection()

        with conn.cursor() as cur:

            cur.execute("""
                SELECT
                    user_id,
                    username,
                    password_hash,
                    role
                FROM library.users
                WHERE username = %s
                  AND is_active = TRUE
            """, (username,))

            user = cur.fetchone()

        if not user:
            return None

        stored_hash = user[2].encode("utf-8")

        password_valid = bcrypt.checkpw(
            password.encode("utf-8"),
            stored_hash
        )

        if password_valid:

            return {
                "user_id": user[0],
                "username": user[1],
                "role": str(user[3]).strip().lower()
            }

        return None

    except Exception as e:

        st.error(f"Login Error: {e}")

        return None

    finally:

        if conn:
            conn.close()


# ==========================================
# 2. LOGIN SCREEN
# ==========================================

def login_screen():

    st.markdown(
        "<h1 style='text-align:center;'>"
        "📚 Smart Library Management"
        "</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>"
        "Login to access your dashboard"
        "</p>",
        unsafe_allow_html=True
    )

    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.subheader("🔐 User Login")

        with st.form("login_form"):

            username = st.text_input("Username")

            password = st.text_input(
                "Password",
                type="password"
            )

            submitted = st.form_submit_button(
                "Login",
                use_container_width=True
            )

            if submitted:

                if not username.strip() or not password:

                    st.warning(
                        "Please enter username and password."
                    )

                else:

                    user = verify_login(
                        username.strip(),
                        password
                    )

                    if user:

                        st.session_state["authenticated"] = True

                        st.session_state["user"] = user

                        st.success("Login successful!")

                        st.rerun()

                    else:

                        st.error(
                            "Invalid username or password."
                        )


# ==========================================
# 3. LOGOUT
# ==========================================

def logout():

    st.session_state.clear()

    st.rerun()


# ==========================================
# 4. REQUIRE LOGIN
# ==========================================

def require_login():

    if not st.session_state.get(
        "authenticated",
        False
    ):

        login_screen()

        st.stop()

    user = st.session_state.get("user")

    if not user:

        st.session_state.clear()

        st.rerun()

    with st.sidebar:

        st.divider()

        st.subheader("👤 User Profile")

        st.write(
            f"Username: **{user['username']}**"
        )

        st.write(
            f"Role: **{user['role'].title()}**"
        )

        st.success("Authenticated")

        st.divider()

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            logout()


# ==========================================
# 5. ROLE-BASED ACCESS CONTROL
# ==========================================

def require_role(allowed_roles):

    require_login()

    user = st.session_state.get("user", {})

    user_role = user.get(
        "role",
        ""
    ).strip().lower()

    allowed_roles = [
        role.lower() for role in allowed_roles
    ]

    if user_role not in allowed_roles:

        st.error("⛔ Access Denied!")

        st.warning(
            "You do not have permission to access this page."
        )

        st.info(
            f"Your current role is: {user_role.title()}"
        )

        st.stop()
