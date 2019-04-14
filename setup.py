from setuptools import setup

setup(name='directory_to_sql',
      version='0.1',
      description='Get a SQL database of file directory data.',
      url='http://github.com/hydrospanner/directory_to_sql',
      author='John Tucker',
      license='MIT',
      packages=['directory_to_sql'],
      install_requires=[
          'db-sqlite3',
      ],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
      )