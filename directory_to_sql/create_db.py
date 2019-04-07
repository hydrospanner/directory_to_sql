"""Create the database tables."""
import sqlite3
import os


def create_db(database=':memory:'):
    """Create the database tables."""
    if os.path.isfile(database):
        os.remove(database)
    conn = sqlite3.connect(database)
    c = conn.cursor()

    sql = '''
        CREATE TABLE folders
        (folder_id INTEGER PRIMARY KEY,
        name text,
        path text,
        subfolder_count INTEGER DEFAULT 0,
        subfolder_count_r INTEGER DEFAULT 0,
        folder_size INTEGER DEFAULT 0,
        folder_size_r INTEGER DEFAULT 0
        )
        '''
    c.execute(sql)
    sql = '''
        CREATE UNIQUE INDEX inx_path ON folders (path)
        '''
    c.execute(sql)
    sql = '''
        CREATE TABLE folder_x_folder
        (parent_id INTEGER,
        child_id INTEGER,
        FOREIGN KEY(parent_id) REFERENCES folders(folder_id),
        FOREIGN KEY(child_id) REFERENCES folders(folder_id)
        )
        '''
    c.execute(sql)
    sql = 'CREATE INDEX inx_parent_id ON folder_x_folder (parent_id)'
    c.execute(sql)
    sql = 'CREATE INDEX inx_child_id ON folder_x_folder (child_id)'
    c.execute(sql)

    sql = '''
        CREATE TABLE files
        (file_name text,
        size INTEGER,
        parent_folder INTEGER,
        mod_date INTEGER,
        FOREIGN KEY(parent_folder) REFERENCES folders(folder_id)
        )
        '''
    c.execute(sql)
    conn.commit()
    return conn
