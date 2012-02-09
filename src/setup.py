from distutils.core import setup

setup(
    name='datetime2',
    version='0.3.1',
    packages=['datetime2'],
    author='Francesco Ricciardi',
    author_email='francescor2010 at yahoo dot it',
    license='BSD License',
    description='New date and time classes',
    long_description=open('README.txt').read(),
    url='http://pypi.python.org/pypi/datetime',
    classifiers=[
          'Development Status :: 3 - Alpha',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.2',
          'Topic :: Scientific/Engineering',
          'Topic :: Software Development :: Libraries'
          ],
    platforms=['Platform independent']
    )
