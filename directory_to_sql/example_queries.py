"""Example queries to find large folders and files."""
import sqlite3
import pandas as pd


def top_10(conn):
    """Print various top 10s from tables."""
    c = conn.cursor()

    # Count files
    print('File Count')
    sql =  '''
        SELECT COUNT(*)
        FROM files
        '''
    c.execute(sql)
    print(c.fetchone())

    # Top 10 files by size
    print('Top 10 files by size')
    sql = '''
        SELECT files.*, path
        FROM (
            SELECT * 
            FROM files
            ORDER BY size DESC
            LIMIT 10
        ) as files
        INNER JOIN folders ON files.parent_folder = folders.folder_id
        ORDER BY size DESC
    '''
    c.execute(sql)
    for r in c.fetchall():
        print(r)

    sql = '''
        SELECT path, folder_size
        FROM folders
        ORDER BY folder_size DESC
        LIMIT 10
    '''
    c.execute(sql)
    print('Folders by size')
    print(pd.read_sql(sql, conn))

    sql = '''
        SELECT path, folder_size_r
        FROM folders
        ORDER BY folder_size_r DESC
        LIMIT 10
    '''
    c.execute(sql)
    print('Folders by size r')
    print(pd.read_sql(sql, conn))

    sql = '''
        SELECT path, subfolder_count_r
        FROM folders
        ORDER BY subfolder_count_r DESC
        LIMIT 10
    '''
    c.execute(sql)
    print('Folders by subfolder ct r')
    print(pd.read_sql(sql, conn))
