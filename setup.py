from setuptools import setup, find_packages # Always prefer setuptools over distutils
from codecs import open # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'PYPI_DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='datetime2',
    version='0.6.6',

    description='New date and time classes',
    long_description=long_description,
    url='http://pypi.python.org/pypi/datetime2',

    author='Francesco Ricciardi',
    author_email='francescor2010 at yahoo dot it',
    license='BSD License',

    keywords='date time datetime calendar',

    classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.4',
          'Topic :: Scientific/Engineering',
          'Topic :: Software Development :: Libraries'
          ],

    packages=find_packages(exclude=['docs*', 'tests*']),

    platforms=['Platform independent']
    )
