
import os
import streamlit as st
import psycopg
from dotenv import load_dotenv

load_dotenv()

# Application roles and their PostgreSQL roles
ROLE_MAPPING = {
    "admin": "library_admin",
    "librarian": "library_librarian"
}


# ==========================================
# AUTHENTICATION CONNECTION
# ==========================================

def get_auth_connection():
    """
    Used only for login verification.
    Connects as library_app.
    """

    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        options="-c search_path=library,public"
    )


# ==========================================
# ROLE-BASED DATABASE CONNECTION
# ==========================================

def get_connection():

    conn = None

    try:
        user = st.session_state.get("user")

        if not user:
            return None

        app_role = user.get("role", "").strip().lower()

        db_role = ROLE_MAPPING.get(app_role)

        if not db_role:
            raise ValueError("Invalid application role.")

        conn = psycopg.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            options="-c search_path=library,public"
        )

        # Activate the appropriate PostgreSQL role
        with conn.cursor() as cur:
            cur.execute(f"SET ROLE {db_role}")

        return conn

    except Exception as e:

        if conn:
            conn.close()

        print("Database connection error:", e)

        return None


# ==========================================
# TEST CONNECTION
# ==========================================

def test_connection():

    conn = get_auth_connection()

    try:
        with conn.cursor() as cur:

            cur.execute("""
                SELECT
                    current_database(),
                    current_user,
                    session_user;
            """)

            print("Authentication connection successful!")
            print(cur.fetchone())

    finally:
        conn.close()


if __name__ == "__main__":
    test_connection()
