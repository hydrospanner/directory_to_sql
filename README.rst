directory_to_sql
======================

Get a SQLite database of a directory tree.

.. image:: https://travis-ci.com/hydrospanner/directory_to_sql.svg?branch=master

The data retrived includes:

- File sizes and modification date.
- Folder sizes and file counts.
- Recursive (including sub-folders) folder sizes and file counts.

To create the database and execute some example queries
listing largest files and folders::

  from directory_to_sql import get_db, top_10
  conn = get_db('\\', 'db.db')
  top_10(conn)

Where to get it
------------------
The latest released version is available on the `Python Package Index
   <https://pypi.org/project/directory-to-sql/>`_.

::

  pip install directory_to_sql
