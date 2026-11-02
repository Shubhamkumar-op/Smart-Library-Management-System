
import streamlit as st
import pandas as pd

from database.connection import get_connection
from utils.helpers import require_role


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Book Management",
    page_icon="📚",
    layout="wide"
)

require_role(["admin", "librarian"])


# ==========================================
# DATABASE FUNCTIONS
# ==========================================

def fetch_data(query, params=None):

    conn = get_connection()

    if conn is None:
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


def get_or_create_id(cur, table, id_column, name_column, name):

    name = name.strip()

    if not name:
        raise ValueError(f"{name_column} cannot be empty.")

    cur.execute(
        f"""
        SELECT {id_column}
        FROM library.{table}
        WHERE LOWER(TRIM({name_column})) = LOWER(TRIM(%s))
        LIMIT 1
        """,
        (name,)
    )

    result = cur.fetchone()

    if result:
        return result[0]

    cur.execute(
        f"""
        INSERT INTO library.{table} ({name_column})
        VALUES (%s)
        RETURNING {id_column}
        """,
        (name,)
    )

    return cur.fetchone()[0]


# ==========================================
# PAGE HEADER
# ==========================================

st.title("📚 Book Management")
st.caption("Add, search, view and manage library inventory.")

st.divider()


# ==========================================
# DASHBOARD METRICS
# ==========================================

total = fetch_data("""
    SELECT COUNT(*)
    FROM library.books
    WHERE is_active = TRUE
""")

copies = fetch_data("""
    SELECT COUNT(*)
    FROM library.book_copies bc
    JOIN library.books b
        ON b.book_id = bc.book_id
    WHERE b.is_active = TRUE
""")

available = fetch_data("""
    SELECT COUNT(*)
    FROM library.book_copies bc
    JOIN library.books b
        ON b.book_id = bc.book_id
    WHERE b.is_active = TRUE
    AND bc.status = 'available'
""")

c1, c2, c3 = st.columns(3)

if total is not None:
    c1.metric("Active Titles", int(total.iloc[0, 0]))

if copies is not None:
    c2.metric("Total Copies", int(copies.iloc[0, 0]))

if available is not None:
    c3.metric("Available Copies", int(available.iloc[0, 0]))

st.divider()


# ==========================================
# ADD NEW BOOK
# ==========================================

st.subheader("➕ Add New Book")

with st.form("add_book_form"):

    title = st.text_input(
        "Book Title",
        placeholder="Enter book title"
    )

    isbn = st.text_input(
        "ISBN",
        placeholder="Enter ISBN"
    )

    st.markdown("### Author Information")

    author = st.text_input(
        "Author Name",
        placeholder="Enter author name"
    )

    st.markdown("### Category Information")

    category = st.text_input(
        "Category Name",
        placeholder="Enter category name"
    )

    st.markdown("### Publisher Information")

    publisher = st.text_input(
        "Publisher Name",
        placeholder="Enter publisher name"
    )

    st.markdown("### Additional Information")

    publication_year = st.number_input(
        "Publication Year",
        min_value=1000,
        max_value=2100,
        value=2026
    )

    edition = st.text_input(
        "Edition",
        placeholder="Enter edition"
    )

    language = st.text_input(
        "Language",
        value="English"
    )

    number_of_copies = st.number_input(
        "Number of Copies",
        min_value=1,
        max_value=100,
        value=1
    )

    submitted = st.form_submit_button(
        "Add Book",
        use_container_width=True
    )

    if submitted:

        if not title.strip():
            st.error("Book title is required.")

        elif not isbn.strip():
            st.error("ISBN is required.")

        elif not author.strip():
            st.error("Author name is required.")

        elif not category.strip():
            st.error("Category name is required.")

        elif not publisher.strip():
            st.error("Publisher name is required.")

        else:

            conn = get_connection()

            if conn is None:
                st.error("Database connection failed.")

            else:

                try:

                    with conn.cursor() as cur:

                        # Check duplicate ISBN

                        cur.execute("""
                            SELECT book_id
                            FROM library.books
                            WHERE isbn = %s
                        """, (isbn.strip(),))

                        existing = cur.fetchone()

                        if existing:
                            raise ValueError(
                                "A book with this ISBN already exists."
                            )

                        # Create or reuse Author

                        author_id = get_or_create_id(
                            cur,
                            "authors",
                            "author_id",
                            "author_name",
                            author
                        )

                        # Create or reuse Category

                        category_id = get_or_create_id(
                            cur,
                            "categories",
                            "category_id",
                            "category_name",
                            category
                        )

                        # Create or reuse Publisher

                        publisher_id = get_or_create_id(
                            cur,
                            "publishers",
                            "publisher_id",
                            "publisher_name",
                            publisher
                        )

                        # Insert Book

                        cur.execute("""
                            INSERT INTO library.books
                            (
                                title,
                                isbn,
                                category_id,
                                publisher_id,
                                publication_year,
                                edition,
                                language,
                                is_active
                            )
                            VALUES (
                                %s, %s, %s, %s, %s, %s, %s, TRUE
                            )
                            RETURNING book_id
                        """, (
                            title.strip(),
                            isbn.strip(),
                            category_id,
                            publisher_id,
                            publication_year,
                            edition.strip() or None,
                            language.strip() or None
                        ))

                        book_id = cur.fetchone()[0]

                        # Insert Author Relationship

                        cur.execute("""
                            INSERT INTO library.book_authors
                            (book_id, author_id)
                            VALUES (%s, %s)
                        """, (
                            book_id,
                            author_id
                        ))

                        # Insert Book Copies

                        for i in range(number_of_copies):

                            accession = f"{isbn.strip()}-{i + 1}"

                            cur.execute("""
                                INSERT INTO library.book_copies
                                (
                                    book_id,
                                    accession_number,
                                    status,
                                    acquired_date
                                )
                                VALUES (
                                    %s, %s, 'available', CURRENT_DATE
                                )
                            """, (
                                book_id,
                                accession
                            ))

                    conn.commit()

                    st.success("Book added successfully!")
                    st.rerun()

                except Exception as e:

                    conn.rollback()
                    st.error(f"Unable to add book: {e}")

                finally:
                    conn.close()


st.divider()


# ==========================================
# SEARCH AND VIEW BOOKS
# ==========================================

st.subheader("📖 All Library Books")

search = st.text_input(
    "🔍 Search by title or ISBN"
)

books = fetch_data("""
    SELECT
        b.book_id,
        b.title,
        b.isbn,
        b.publication_year,
        b.edition,
        b.language,

        COUNT(bc.copy_id) AS total_copies,

        COUNT(bc.copy_id) FILTER (
            WHERE bc.status = 'available'
        ) AS available_copies

    FROM library.books b

    LEFT JOIN library.book_copies bc
        ON b.book_id = bc.book_id

    WHERE b.is_active = TRUE

    GROUP BY
        b.book_id,
        b.title,
        b.isbn,
        b.publication_year,
        b.edition,
        b.language

    ORDER BY b.book_id DESC
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

    st.caption(
        f"Total books displayed: {len(books)}"
    )

else:

    st.error("Unable to load books.")


st.divider()


# ==========================================
# REMOVE BOOK - SOFT DELETE
# ==========================================

st.subheader("🗑️ Remove Book")

st.info(
    "The book will be marked inactive. "
    "Its historical issue records will be preserved."
)

remove_data = fetch_data("""
    SELECT
        book_id,
        title,
        isbn
    FROM library.books
    WHERE is_active = TRUE
    ORDER BY title
""")

if remove_data is not None and not remove_data.empty:

    selected_book = st.selectbox(
        "Select book to remove",
        remove_data.to_dict("records"),
        format_func=lambda x:
            f'{x["title"]} | {x["isbn"]}'
    )

    confirm = st.checkbox(
        "I confirm that I want to remove this book."
    )

    if st.button(
        "Remove Selected Book",
        disabled=not confirm,
        type="primary"
    ):

        conn = get_connection()

        if conn is None:
            st.error("Database connection failed.")

        else:

            try:

                with conn.cursor() as cur:

                    # Lock Book Record

                    cur.execute("""
                        SELECT book_id
                        FROM library.books
                        WHERE book_id = %s
                        AND is_active = TRUE
                        FOR UPDATE
                    """, (selected_book["book_id"],))

                    book = cur.fetchone()

                    if not book:

                        st.error(
                            "Book not found or already inactive."
                        )

                    else:

                        # Check Issued Copies

                        cur.execute("""
                            SELECT COUNT(*)
                            FROM library.book_copies
                            WHERE book_id = %s
                            AND status = 'issued'
                        """, (selected_book["book_id"],))

                        issued = cur.fetchone()[0]

                        # Check Pending Reservations

                        cur.execute("""
                            SELECT COUNT(*)
                            FROM library.reservations
                            WHERE book_id = %s
                            AND status = 'pending'
                        """, (selected_book["book_id"],))

                        reservations = cur.fetchone()[0]

                        if issued > 0:

                            st.error(
                                "Cannot remove book. "
                                "Some copies are currently issued."
                            )

                        elif reservations > 0:

                            st.error(
                                "Cannot remove book. "
                                "Active reservations exist."
                            )

                        else:

                            # Soft Delete

                            cur.execute("""
                                UPDATE library.books
                                SET is_active = FALSE
                                WHERE book_id = %s
                            """, (selected_book["book_id"],))

                            conn.commit()

                            st.success(
                                "Book removed from active inventory!"
                            )

                            st.rerun()

            except Exception as e:

                conn.rollback()
                st.error(f"Unable to remove book: {e}")

            finally:
                conn.close()

else:

    st.info("No active books available to remove.")
