
import os
import streamlit as st
import psycopg
from dotenv import load_dotenv

load_dotenv()

ROLE_MAPPING = {
    "admin": "library_admin",
    "librarian": "library_librarian"
}


def get_db_setting(key):

    try:
        value = st.secrets.get(key)
        if value:
            return value
    except Exception:
        pass

    return os.getenv(key)


def get_auth_connection():

    return psycopg.connect(
        host=get_db_setting("DB_HOST"),
        port=get_db_setting("DB_PORT"),
        dbname=get_db_setting("DB_NAME"),
        user=get_db_setting("DB_USER"),
        password=get_db_setting("DB_PASSWORD"),
        options="-c search_path=library,public"
    )


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
            host=get_db_setting("DB_HOST"),
            port=get_db_setting("DB_PORT"),
            dbname=get_db_setting("DB_NAME"),
            user=get_db_setting("DB_USER"),
            password=get_db_setting("DB_PASSWORD"),
            options="-c search_path=library,public"
        )

        with conn.cursor() as cur:
            cur.execute(f"SET ROLE {db_role}")

        return conn

    except Exception as e:

        if conn:
            conn.close()

        print("Database connection error:", e)
        return None
