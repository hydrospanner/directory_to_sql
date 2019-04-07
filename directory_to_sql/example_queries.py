"""Example queries to find large folders and files."""
import sqlite3
import pandas as pd


def top_10(conn):
    """Get various top 10s from tables."""
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


def idk():
    # Update folder value by value of sum agg files table.
    sql = '''
        UPDATE 
            folders
        SET
        folders.folder_size = (
            SELECT SUM(size) as size
            FROM files
            WHERE files.parent_folder = folders.folder_id
            GROUP BY parent_folder
        )
        WHERE
            EXISTS (
                SELECT * 
                FROM files
                WHERE files.parent_folder = folders.folder_id
            );
    '''
    c.execute(sql)


if __name__ == '__main__':
    conn = sqlite3.connect('db.db')
    top_10(conn)
