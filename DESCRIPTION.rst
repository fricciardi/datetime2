datetime2
=========

.. image:: https://travis-ci.org/fricciardi/datetime2.svg?branch=master
   :target: https://travis-ci.org/fricciardi/datetime2

.. image:: https://readthedocs.org/projects/datetime2/badge/?version=stable
   :target: https://datetime2.readthedocs.io/en/stable/?badge=stable

.. image:: https://img.shields.io/badge/License-BSD-green.svg
   :target: https://opensource.org/licenses/BSD-3-Clause

The [datetime2](http://pypi.org/project/datetime2) module provides date
and time classes to Python.

It will enhance the standard [datetime](https://docs.python.org/3.7/library/datetime.html)
module, adding the capability of constructing and representing date and time in
many formats and removing a few limits that the original package has.

Documentation is hosted at [ReadtheDocs](https://datetime2.readthedocs.io/en/stable/?badge=stable).

Code is hosted at [GitHub](http://github.com/fricciardi/datetime2): the
[wiki pages](https://github.com/fricciardi/datetime2/wiki) host development
discussions. *datetime2* is a one-man, free-time work. Although I am deeply
committed in completing the project, do not expect regular updates (and indeed
there weren't for two years!)

Project objectives
==================

* Decoupling between operations on date and time objects and their
  representation.
* Access to different calendars, for input parsing and output formatting.
* Access to different time representations, also for input and output.
* Infinite precision in converting between different time representations.
* Ability to dynamically register new formatting classes.
* Internationalization.
* Implementation of the part of the Unicode Locale Database concerned with
  dates and times.
* Interface with other Python modules or inclusion of their
  functionalities in submodules.

These objectives are very long term ones, which I am setting because I think it is
important to establish a direction for the project. Do not expect to see them
implemented in initial versions of the module, even if you will be able to see
traces of them early.

License
=======

Datetime2 is distributed under the terms of the new BSD license. You are free
to use it for commercial or non-commercial projects with little or no
restriction, all I ask is that:

> Redistributions of the code, in whole or part, retain the original
> copyright notice and license text. You do not claim my endorsement
> of any derived product.

For a complete text of the license see the LICENSE.txt file in the source distribution.
