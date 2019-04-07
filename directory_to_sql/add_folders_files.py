"""Populate database with file directory information."""
import os

from .create_db import create_db


def get_db(search_path, database=':memory:'):
    """Create database with directory tree data. Return a database connection.

    Args:
        search_path (str): parent folder path to start directory tree.
        database (str): path-like-object of database file
    """
    if not os.isdir(search_path):
        raise ValueError('The search path "%s" does not exist.' % search_path)
    conn = create_db(database)
    c = conn.cursor()

    walk_inserts(c)
    add_folder_sizes(c)
    add_recursive_folder_sizes(c)
    add_folder_counts(c)
    add_folder_counts_recursive(c)
    conn.commit()
    return conn


def walk_inserts(c):
    """OS walk through folders and files and insert them to database."""
    insert_folders = '''
        INSERT INTO folders
        (folder_id, name, path)
        VALUES (?, ?, ?)
        '''
    # Insert the parent path.
    parent_folder_name = os.path.basename(search_path)
    folder_id = 1
    c.execute(insert_folders, (folder_id, parent_folder_name, search_path))

    folder_x_folder = '''
        INSERT INTO folder_x_folder
        (parent_id, child_id)
        VALUES (?, ?)
        '''
    for dirpath, dirnames, filenames in os.walk(search_path):
        parent_folder_id = get_folder_id(dirpath, c)
        for subfolder in dirnames:
            # Insert into folders table.
            folder_id += 1
            subfolder_path = os.path.join(dirpath, subfolder)
            c.execute(insert_folders, (folder_id, subfolder, subfolder_path))

            # Insert into folder_x_folder table.
            c.execute(folder_x_folder, (parent_folder_id, folder_id))
            
        insert_files(filenames, dirpath, c, parent_folder_id)

        if folder_id % 10 == 0:
            print('\rProcessed %s folders.' % folder_id, end='\r')
    print()


def insert_files(filenames, dirpath, c, parent_folder_id):
    """Get file attributes and insert to database."""
    insert_file = '''
        INSERT INTO files
        (file_name, parent_folder, size, mod_date)
        VALUES (?, ?, ?, ?)
    '''
    file_data = []
    for file_name in filenames:
        file_path = os.path.join(dirpath, file_name)
        size = get_file_size(file_path)
        mod_date = get_file_modification_dt(file_path)
        file_data.append((file_name, parent_folder_id, size, mod_date))
    c.executemany(insert_file, file_data)


def add_folder_counts(c):
    """Aggregate subfolder counts from folder_x_folder."""
    sql = '''
        SELECT COUNT(*) as count, parent_id
        FROM folder_x_folder
        GROUP BY parent_id
    '''
    c.execute(sql)
    data = c.fetchall()
    sql = '''
        UPDATE folders
        SET subfolder_count = ?
        WHERE folder_id = ?
    '''
    c.executemany(sql, data)


def add_folder_counts_recursive(c):
    """Aggregate subfolder counts from folder_x_folder."""
    sql = '''
        WITH RECURSIVE descendants AS
            ( 
                SELECT parent_id, child_id, 1 as level
                FROM folder_x_folder
            UNION ALL
                SELECT d.parent_id, s.child_id, d.level + 1
                FROM descendants AS d
                JOIN folder_x_folder s
                ON d.child_id = s.parent_id
            )
        SELECT count(child_id) as count, parent_id
        FROM descendants
        INNER JOIN folders ON descendants.parent_id = folders.folder_id
        GROUP BY parent_id
    '''
    c.execute(sql)
    data = c.fetchall()
    sql = '''
        UPDATE folders
        SET subfolder_count_r = ?
        WHERE folder_id = ?
    '''
    c.executemany(sql, data)


def add_folder_sizes(c):
    """Aggregate folder size from file sizes and set folder value."""
    sql = '''
        SELECT SUM(size) as size, parent_folder
        FROM files
        GROUP BY parent_folder
    '''
    c.execute(sql)
    sizes = c.fetchall()
    sql = '''
        UPDATE folders
        SET folder_size = ?
        WHERE folder_id = ?
    '''
    c.executemany(sql, sizes)


def add_recursive_folder_sizes(c):
    """Aggregate folder size from file sizes and set folder value."""
    # Recursive SQL query to get the sizes of all children folders.
    sql = '''
        WITH RECURSIVE descendants AS
            ( 
                SELECT parent_id, child_id, 1 as level
                FROM folder_x_folder
            UNION ALL
                SELECT d.parent_id, s.child_id, d.level + 1
                FROM descendants AS d
                JOIN folder_x_folder s
                ON d.child_id = s.parent_id
            )
        SELECT SUM(folder_size) as size, parent_id
        FROM descendants
        INNER JOIN folders ON descendants.child_id = folders.folder_id
        GROUP BY parent_id
    '''
    c.execute(sql)
    sizes = c.fetchall()
    sql = '''
        UPDATE folders
        SET folder_size_r = ?
        WHERE folder_id = ?
    '''
    c.executemany(sql, sizes)
    """Add the children size to the non-recusrive size to include files in
    the parent folder."""
    sql = '''
        UPDATE folders
        SET folder_size_r = folder_size_r + folder_size
    '''
    c.execute(sql)


def get_folder_id(path, c):
    """Query the folder id of the directory."""
    sql = '''
        SELECT folder_id
        FROM folders
        WHERE path = ?
        '''
    c.execute(sql, (path, ))
    return c.fetchone()[0]


def get_file_size(file_path):
    """Return file size in bytes."""
    try:
        return os.path.getsize(file_path)
    except (PermissionError, OSError):
        return


def get_file_modification_dt(file_path):
    """Return file modification datetime in UNIX timestamp."""
    try:
       return os.path.getmtime(file_path)
    except (PermissionError, OSError):
        return


if __name__ == '__main__':
    search_path = '\\'
    get_db(search_path, 'db.db')
