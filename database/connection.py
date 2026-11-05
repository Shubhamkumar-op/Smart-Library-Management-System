
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
        if value is not None and str(value).strip():
            return str(value)
    except Exception:
        pass

    return os.getenv(key)


def get_connection_parameters():
    required_keys = [
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD"
    ]

    config = {}

    for key in required_keys:
        value = get_db_setting(key)

        if value is None or not str(value).strip():
            raise ValueError(
                f"Missing database configuration: {key}"
            )

        config[key] = value

    return {
        "host": config["DB_HOST"],
        "port": int(config["DB_PORT"]),
        "dbname": config["DB_NAME"],
        "user": config["DB_USER"],
        "password": config["DB_PASSWORD"],
        "options": "-c search_path=library,public",
        "connect_timeout": 15
    }


def get_auth_connection():
    try:
        return psycopg.connect(
            **get_connection_parameters()
        )
    except Exception as e:
        st.error(
            f"Authentication database error: "
            f"{type(e).__name__}: {e}"
        )
        return None


def get_connection():
    conn = None

    try:
        user = st.session_state.get("user")

        if not user:
            return None

        app_role = user.get("role", "").strip().lower()
        db_role = ROLE_MAPPING.get(app_role)

        if not db_role:
            raise ValueError(
                f"Invalid application role: {app_role}"
            )

        conn = psycopg.connect(
            **get_connection_parameters()
        )

        with conn.cursor() as cur:
            cur.execute(f'SET ROLE "{db_role}"')

        return conn

    except Exception as e:
        if conn is not None:
            conn.close()

        st.error(
            f"Database connection error: "
            f"{type(e).__name__}: {e}"
        )

        return None
