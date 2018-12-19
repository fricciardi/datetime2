datetime2
=========

[![Build Status](https://travis-ci.org/fricciardi/datetime2.svg?branch=master)](https://travis-ci.org/fricciardi/datetime2)
[![Documentation Status](https://readthedocs.org/projects/datetime2/badge/?version=latest)](https://datetime2.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/badge/License-BSD-green.svg)](https://opensource.org/licenses/BSD-3-Clause)


The *datetime2* module provides date and time classes to Python. It will enhance the 
standard [datetime](http://docs.python.org/py3k/library/datetime.html) module, 
adding the capability of constructing and representing date and time in many formats
and removing a few limits that the original package has.

*datetime2* is a one-man, free-time work. Although I am deeply committed in completing 
the project, do not expect regular updates on it. However, I am now using an "agile" 
development style, so you can expect more releases. Any tagged commit will be a meaningful 
release, and I am thinking of deploying all these releases to PyPI as well.  

If you are looking for more information, check the following:

* [Official documentation](https://datetime2.readthedocs.io/en/latest/?badge=latest), now
  hosted at ReadTheDocs

* [datetime2 PyPI page](http://pypi.org/project/datetime2), where versions are 
  uploaded;

* [wiki pages](https://github.com/fricciardi/datetime2/wiki), for further
  information on development and documentation.
  
Please note that Python 2.x is not supproted because it does not have keyword only arguments,
which instead are used in a few functions and methods.