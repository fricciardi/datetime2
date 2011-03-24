.. toctree::

:mod:`datetime2` --- New date and time classes
==============================================

.. module:: datetime2
   :synopsis: Date and time types with broader calendar coverage.
.. moduleauthor:: Francesco Ricciardi <francescor2010@yahoo.it>

The :mod:`datetime2` module provides classes to manipulate date and time
like the :mod:`datetime` module does, with these objectives in mind:

* decoupling between operations on date and time objects and their
  representation;
* access to different calendars, for input parsing and output formatting;
* access to different time representation systems, also for input and output;
* ability to dynamically load new formatting classes;
* internationalization;
* implementation of the part of the Unicode Locale Database concerned with
  dates and times;
* interface with other Python modules or inclusion of their
  functionalities in its submodules.

These are long term objective and will not be available immediately.

Available calendars and time representation systems will be discovered at
import time. Additionally, registering new systems at run time is also
possible.

Available Classes
-----------------

There are four base classes in :mod:`datetime2`. These base classes do not
provide input parsing or output formatting. 
Additional representation classes 
provide calendar and time system representation, and also will be capable
of parsing strings to generate dates and time instances.

The class names used in :mod:`datetime2` are distinguished from
those of :mod:`datetime` because they use the CapitalizedWords convention, 
required by :pep:`8`, not used in the old module.

.. class:: Date
   :noindex:

   An idealized date, with no notion of time or time zone. A date is stored
   counting the number of days elapsed from what would have been January 1st
   of year 1 on the Gregorian calendar. The only attribute of this class is:
   :attr:`day_count`.


.. class:: Time
   :noindex:

   An indication of time, independent of any particular day. There might be a
   time correction, e.g. due to time zone or daylight saving time. Time is
   stored as a fraction of a day, using a Python :class:`fractions.Fraction`.
   Attributes of this class are: :attr:`day_frac`, :attr:`correction`.


.. class:: DateTime
   :noindex:

   A combination of a date and a time. As with :class:`Time`, there might be a
   correction of time. Date and time are stored together in a single Python
   :class:`fractions.Fraction`. Attributes of this class are: :attr:`days`,
   :attr:`correction`.


.. class:: TimeDelta
   :noindex:

   A duration expressing the difference between two :class:`Date`, :class:`Time`,
   or :class:`DateTime` instances. This difference is stored in a single Python
   :class:`fractions.Fraction`. The only attribute of this class is: :attr:`days`.



.. seealso::

   Module :mod:`datetime`
      Basic date and time types.

   Module :mod:`calendar`
      General calendar related functions.

   Module :mod:`time`
      Time access and conversions.


.. _datetime-date:

:class:`Date` Objects
---------------------

A :class:`Date` object represents a date in an idealized calendar, the
current Gregorian calendar indefinitely extended in both directions.
January 1 of year 1 is called day number 1, January 2 of year 1 is called
day number 2, and so on. This matches the definition of the "proleptic
Gregorian" calendar in Dershowitz and Reingold's book Calendrical
Calculations, where it's the base calendar for all computations. See the
book for algorithms for converting between proleptic Gregorian ordinals
and many other calendar systems.

Contructors
^^^^^^^^^^^

.. class:: Date(day_count)

   The argument is required and must be an integer. It represents the
   nummber    of days from January 1 of year 1 of the current Gregorian
   calendar. There is no restriction on its value, i.e. zero and all
   positive and negative values are accepted.


.. classmethod:: Date.today()

   A class method that represents the current local date.

:class:`Date` objects are immutable, so they can be used as dictionary keys.
They can also be pickled and unpickled. In Boolean contexts, all :class:`Date`
instances are considered to be true.

Instance attributes (read-only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. attribute:: Date.day_count

   The number of days between the given date and January 1, year 1. An
   :exc:`AttributeException` is raised when trying to change this attribute.


Supported operations
^^^^^^^^^^^^^^^^^^^^

+-------------------------------+----------------------------------------------+
| Operation                     | Result                                       |
+===============================+==============================================+
| ``date2 = date1 + timedelta`` | *date2* is ``timedelta`` days after          |
|                               | *date1*. (1)                                 |
+-------------------------------+----------------------------------------------+
| ``date2 = date1 - timedelta`` | *date2* is ``timedelta`` days before         |
|                               | *date1*. (1)                                 |
+-------------------------------+----------------------------------------------+
| ``timedelta = date1 - date2`` | A :class:`TimeDelta` object is returned      |
|                               | representing the number of days              |
|                               | between *date1* and *date2*. (2)             |
+-------------------------------+----------------------------------------------+
| ``date1 < date2``             | *date1* is less than *date2* when its day    |
|                               | count is less that that of *date2*. (3) (4)  |
+-------------------------------+----------------------------------------------+

Notes:

(1)
   A :exc:`ValueError` exception is raised if *timedelta* is not integer. If you
   deal with non-integer date differences, you need to use :class:`DateTime` 
   instances. If *timedelta* is negative, ``date2`` will be before ``date1``.

(2)
   An integer *timedelta* is always created when subtracting :class:`Date`
   instances.

(3)
   In other words, ``date1 < date2`` if and only if ``date1.day_count <
   date2.day_count``. All other comparison operators between dates are defined.
   
(4)
   Comparison between a :class:`Date` object and an object of another class
   return a :exc:`NotImplemented` exception, except for the equality and inequality
   operators, which respectively return *False* and *True*.


Instance methods
^^^^^^^^^^^^^^^^

.. method:: date.__str__()

   Return ``R.D.`` followed by the day count.







