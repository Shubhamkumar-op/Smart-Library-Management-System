# Smart Library Management System — SQL scripts

These scripts were split from the supplied PostgreSQL 18.6 plain dump.

## Files and execution order

Run them in this order, using a PostgreSQL administrator:

1. `01_schema.sql` — creates the `library` schema.
2. `02_tables_sequences.sql` — creates all 13 tables and identity sequences.
3. `03_functions.sql` — creates the six PL/pgSQL functions.
4. `04_views.sql` — creates the three views.
5. `05_sample_data.sql` — inserts safe demo catalog data only.
6. `06_constraints_foreign_keys.sql` — adds primary keys, unique/check constraints and foreign keys.
7. `07_indexes.sql` — creates indexes.
8. `08_triggers.sql` — creates triggers.
9. `09_create_roles.sql` — creates the NOLOGIN permission roles.
10. `10_permissions.sql` — applies grants.

Create the database first, for example `library_management`.

## Important notes

- `05_sample_data.sql` intentionally excludes personal member contact details, user password hashes, audit history, issue history, fines, payments and reservations. It is suitable as starter data for a public GitHub repository.
- The complete `library_database.sql` dump you exported contains actual database records and bcrypt password hashes. Keep that full dump private; do not commit it to a public repository.
- The dump references `library_app`, which is a LOGIN role. Create it separately on each machine with a new password, then grant it membership in the permission roles as required by your application. Do not reuse or publish database passwords.
- The original dump includes grants for roles that must exist before `10_permissions.sql` runs.
- These scripts reproduce the database objects represented in the supplied dump. The original complete plain dump remains the most direct way to reproduce all original records privately.
- Execute the scripts with `psql -d library_management -f <filename>` or through pgAdmin's Query Tool where supported. For the sample-data file, `COPY ... FROM stdin` is a psql dump mechanism; run it with `psql`, not by pasting individual statements into Query Tool.
