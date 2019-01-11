import setuptools
from os import environ, path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst')) as f:
    long_description = f.read()

setuptools.setup(
    name='datetime2',
    version=environ['TRAVIS_TAG'],

    description='New date and time classes',
    long_description=long_description,
    long_description_content_type="text/x-rst",

    url='https://github.com/fricciardi/datetime2',

    author='Francesco Ricciardi',
    author_email='francescor2010@yahoo.it',
    license='BSD License',

    keywords='date time datetime calendar',

    classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.6',
          'Topic :: Scientific/Engineering',
          'Topic :: Software Development :: Libraries :: Python Modules'
          ],

    packages=setuptools.find_packages(exclude=['docs*']),

    platforms=['Platform independent']
    )
