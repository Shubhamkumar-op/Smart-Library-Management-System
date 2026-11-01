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
└
