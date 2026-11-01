
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


def get_options(table, id_column, name_column):

    return fetch_data(
        f"""
        SELECT {id_column}, {name_column}
        FROM library.{table}
        ORDER BY {name_column}
        """
    )


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

authors = get_options(
    "authors",
    "author_id",
    "author_name"
)

categories = get_options(
    "categories",
    "category_id",
    "category_name"
)

publishers = get_options(
    "publishers",
    "publisher_id",
    "publisher_name"
)

if all(
    df is not None and not df.empty
    for df in [authors, categories, publishers]
):

    with st.form("add_book_form"):

        title = st.text_input("Book Title")

        isbn = st.text_input("ISBN")

        author = st.selectbox(
            "Author",
            authors.to_dict("records"),
            format_func=lambda x: x["author_name"]
        )

        category = st.selectbox(
            "Category",
            categories.to_dict("records"),
            format_func=lambda x: x["category_name"]
        )

        publisher = st.selectbox(
            "Publisher",
            publishers.to_dict("records"),
            format_func=lambda x: x["publisher_name"]
        )

        publication_year = st.number_input(
            "Publication Year",
            min_value=1000,
            max_value=2100,
            value=2026
        )

        edition = st.text_input("Edition")

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

            if not title.strip() or not isbn.strip():
                st.error("Title and ISBN are required.")

            else:

                conn = get_connection()

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

                        # Insert book

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
                            category["category_id"],
                            publisher["publisher_id"],
                            publication_year,
                            edition.strip() or None,
                            language.strip() or None
                        ))

                        book_id = cur.fetchone()[0]

                        # Insert author relationship

                        cur.execute("""
                            INSERT INTO library.book_authors
                            (book_id, author_id)
                            VALUES (%s, %s)
                        """, (
                            book_id,
                            author["author_id"]
                        ))

                        # Insert book copies

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

else:

    st.warning(
        "Please add authors, categories and publishers "
        "before adding a book."
    )


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

        try:
            with conn.cursor() as cur:

                # Lock book record

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

                    # Check issued copies

                    cur.execute("""
                        SELECT COUNT(*)
                        FROM library.book_copies
                        WHERE book_id = %s
                        AND status = 'issued'
                    """, (selected_book["book_id"],))

                    issued = cur.fetchone()[0]

                    # Check pending reservations

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

                        # Soft delete

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
