import setuptools
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

# TODO: All setup arguments need to be revised, also check for those to give more info on PyPI page
setuptools.setup(
    name='datetime2',
    version='0.8.0',

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
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Topic :: Scientific/Engineering',
          'Topic :: Software Development :: Libraries :: Python Modules'
          ],

    packages=setuptools.find_packages(exclude=['docs*']),

    platforms=['Platform independent'],

    project_urls={"Issue Tracker": "https://github.com/fricciardi/datetime2/issues"}
    )
