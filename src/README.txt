=========
datetime2
=========

The `datetime2 <http://pypi.python.org/pypi/datetime2>`_ module
provides new classes date and time classes.

This module will provide date and time classes, as the original 
`datetime <http://docs.python.org/py3k/library/datetime.html>`_ module does.
However, the new classes on the one hand will separate date and time handling from
their representation, on the other hand they will provide new calendars and
time measurement systems.

Code is hosted at `GitHub <http://github.com/fricciardi/datetime2>`_: see
that page for development information.

Project objectives
==================

* Decoupling between operations on date and time objects and their
  representation.
* Access to different calendars, for input parsing and output formatting.
* Access to different time representation systems, also for input and output.
* Ability to dynamically load new formatting classes.
* Internationalization.
* Implementation of the part of the Unicode Locale Database concerned with
  dates and times.
* Interface with other Python modules or inclusion of their
  functionalities in its submodules.

License
=======

Datetime2 is distributed under the terms of the new BSD license. You are free
to use it for commercial or non-commercial projects with little or no
restriction, all we ask is that:

    Redistributions of the code, in whole or part, retain the original
    copyright notice and license text. You do not claim our endorsement
    of any derived product.

For a complete text of the license see the LICENSE.txt file in the source distribution.


