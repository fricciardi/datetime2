=========
datetime2
=========

The `datetime2 <http://pypi.python.org/pypi/datetime2>`_ module provides date
and time classes to Python.

It will enhance the standard `datetime <http://docs.python.org/py3k/library/datetime.html>`_
module, adding the capability of constructing and representing date and time in
many formats and removing a few limits that the original package has.

Code is hosted at `GitHub <http://github.com/fricciardi/datetime2>`_: the
`wiki pages <https://github.com/fricciardi/datetime2/wiki>`_ host development
discussions. *datetime2* is a one-man, free-time work. Although I am deeply
committed in completing the project, do not expect regular updates.

Project objectives
==================

* Decoupling between operations on date and time objects and their
  representation.
* Access to different calendars, for input parsing and output formatting.
* Access to different time representations, also for input and output.
* Ability to dynamically register new formatting classes.
* Internationalization.
* Implementation of the part of the Unicode Locale Database concerned with
  dates and times.
* Interface with other Python modules or inclusion of their
  functionalities in its submodules.

These objectives are very long term ones, which I am setting because it is
important to establish a direction for the project. Do not expect to see them
implemented in initial versions of the module, even if you will be able to see
traces of them early.

License
=======

Datetime2 is distributed under the terms of the new BSD license. You are free
to use it for commercial or non-commercial projects with little or no
restriction, all we ask is that:

    Redistributions of the code, in whole or part, retain the original
    copyright notice and license text. You do not claim our endorsement
    of any derived product.

For a complete text of the license see the LICENSE.txt file in the source distribution.


