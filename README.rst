directory_to_sql
======================

Get a SQLite database of a directory tree.

- Get file sizes and modification date.
- Get folder sizes and file counts.
- Get recursive (including sub-folders) folder sizes and file counts.

To create the database and execute some example queries
listing largest files and folders::

  from directory_to_sql import get_db, top_10
  conn = get_db('db.db')
  top_10(conn)
