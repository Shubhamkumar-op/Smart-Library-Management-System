# 📚 Smart Library Management System

A database-driven Library Management System built using **Python, Streamlit, and PostgreSQL**. The project is designed to simplify library operations such as book management, member management, book issuing, returns, fine calculation, reservations, and analytics.

## 🚀 Project Overview

The Smart Library Management System provides a centralized platform to manage library resources and daily operations. PostgreSQL handles structured data storage, relationships, transactions, constraints, and database-level business logic, while Streamlit provides an interactive user interface.

## ✨ Features

- **Book Management:** Manage book records, authors, publishers, and categories.
- **Member Management:** Register and manage library members.
- **Issue & Return:** Issue books and process returns.
- **Fine Management:** Calculate late return fines and record payments.
- **Book Reservations:** Allow members to reserve books.
- **Analytics Dashboard:** View library inventory and operational statistics.
- **Authentication:** User login with password hashing.
- **Role-Based Access Control:** Separate administrative, librarian, and analyst permissions.
- **Audit Logging:** Track changes to important database records.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | User interface |
| PostgreSQL | Relational database |
| psycopg | Python-PostgreSQL connectivity |
| Pandas | Data handling |
| Plotly | Data visualization |
| bcrypt | Password hashing |

## 📂 Project Structure

```text
Smart-Library-Management-System/
│
├── database/
│   ├── __init__.py
│   └── connection.py
│
├── pages/
│   ├── 1_Book_Management.py
│   ├── 2_Member_Management.py
│   ├── 3_Issue_Return.py
│   ├── 4_Fine_Management.py
│   ├── 5_Reservations.py
│   └── 6_Analytics.py
│
├── utils/
│   ├── __init__.py
│   └── helpers.py
│
├── assets/
│
├── sql/
│   ├── 01_schema.sql
│   ├── 02_tables_sequences.sql
│   ├── 03_functions.sql
│   ├── 04_views.sql
│   ├── 05_sample_data.sql
│   ├── 06_constraints_foreign_keys.sql
│   ├── 07_indexes.sql
│   ├── 08_triggers.sql
│   ├── 09_create_roles.sql
│   ├── 10_permissions.sql
│   └── README_SQL.md
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Smart-Library-Management-System.git
cd Smart-Library-Management-System
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

- Install PostgreSQL.
- Create a database named `library_management`.
- Configure the database connection details in your `.env` file.
- Create the required database roles and permissions.

### 5. Configure Environment Variables

Create a `.env` file in the project root using `.env.example` as a template.

Example:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=library_management
DB_USER=library_app
DB_PASSWORD=your_password
DB_SCHEMA=library
```

Never upload your actual `.env` file to GitHub.

### 6. Set Up the Database

Execute the SQL scripts in the following order:

1. `01_schema.sql`
2. `02_tables_sequences.sql`
3. `03_functions.sql`
4. `04_views.sql`
5. `05_sample_data.sql`
6. `06_constraints_foreign_keys.sql`
7. `07_indexes.sql`
8. `08_triggers.sql`
9. `09_create_roles.sql`
10. `10_permissions.sql`

**Note:** Run `05_sample_data.sql` using `psql` because it contains PostgreSQL COPY data blocks. Review role permissions and configure the local application login before running the application.

### 7. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🗄️ Database Design

The database uses a relational structure with the following main tables:

- users
- members
- authors
- categories
- publishers
- books
- book_authors
- book_copies
- issue_records
- fines
- payments
- reservations
- audit_logs

It also includes database functions, views, triggers, indexes, constraints, and role-based permissions.

## 🔐 Security

- Environment variables are used for database credentials.
- Passwords are stored using bcrypt hashing.
- PostgreSQL roles control database access.
- Foreign keys and constraints maintain data integrity.
- Audit logs help track changes to important records.

## 🎯 Project Objective

The objective of this project is to develop a reliable and structured library management solution using relational database concepts, SQL programming, transaction management, and a Python-based interface.

## 👨‍💻 Author

**Shubham Kumar Singh**

## 📄 License

This project is available for educational and academic purposes.
