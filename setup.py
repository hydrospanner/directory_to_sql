from setuptools import setup


with open('README.rst', 'r') as file:
    long_description = file.read()

setup(name='directory_to_sql',
      version='0.1.1',
      description='Get a SQL database of file directory data.',
      long_description=long_description,
      url='http://github.com/hydrospanner/directory_to_sql',
      author='John Tucker',
      license='MIT',
      packages=['directory_to_sql'],
      install_requires=[
          'pandas',
      ],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
      )