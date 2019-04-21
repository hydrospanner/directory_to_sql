"""Unit tests"""
import unittest
import os
import shutil

from directory_to_sql import get_db


PARENT_PATH = os.path.dirname(__file__)
TEST_PATH = os.path.join(PARENT_PATH, 'test_data')


def create_file(file_path, size_bytes):
    """Create a file of a specific size.

    size_bytes (int): size in bytes to make the file.
    """
    txt = ''.join('1' for _ in range(size_bytes))
    with open(file_path, 'w') as f:
        f.write(txt)


class CreateFileSizeTest(unittest.TestCase):
    """Test the create file size function."""

    def setUp(self):
        """Make the directory."""
        os.mkdir(TEST_PATH)

    def test_file_sizes(self):
        """Create files of different sizes and test against actual size."""
        sizes = [1, 10, 100, 1000]
        for file_size in sizes:
            file_path = os.path.join(PARENT_PATH, 'test.txt')
            create_file(file_path, file_size)
            actual_size = os.path.getsize(file_path)
            os.remove(file_path)
            self.assertEqual(file_size, actual_size)

    def tearDown(self):
        """Delete the directory."""
        os.rmdir(TEST_PATH)

class DirDBTest(unittest.TestCase):
    top_file_tree = os.path.join(TEST_PATH, '1')

    def setUp(self):
        """Create a directory tree."""
        create_path = os.path.join(TEST_PATH, '1/2/3')
        os.makedirs(create_path)
        create_path = os.path.join(TEST_PATH, '1/4')
        os.mkdir(create_path)
        file_path = os.path.join(TEST_PATH, '1/2/10.txt')
        create_file(file_path, 10)
        file_path = os.path.join(TEST_PATH, '1/1.txt')
        create_file(file_path, 1)
        file_path = os.path.join(TEST_PATH, '1/2/3/3.txt')
        create_file(file_path, 4)

    def test_file_count(self):
        """Count files"""
        db = get_db(self.top_file_tree)
        c = db.cursor()
        sql =  '''
            SELECT COUNT(*)
            FROM files
            '''
        c.execute(sql)
        count = c.fetchone()[0]
        self.assertEqual(count, 3)


    def test_r_folder_sizes(self):
        """Check recursive folder sizes."""
        db = get_db(self.top_file_tree)
        c = db.cursor()
        sql =  '''
            SELECT folder_size_r
            FROM folders
            WHERE name = ?
            '''
        folder_r_sizes = [
            ('1', 15),
            ('2', 14),
            ('3', 4),
            ('4', 0)
        ]
        for folder_name, folder_r_size_answer in folder_r_sizes:
            c.execute(sql, [folder_name])
            size_query = c.fetchone()[0]
            self.assertEqual(size_query, folder_r_size_answer)


    def tearDown(self):
        """Delete the directory tree."""
        create_path = os.path.join(TEST_PATH, '1')
        shutil.rmtree(create_path)
