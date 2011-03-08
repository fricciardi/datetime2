.. toctree::

:mod:`datetime2` --- New date and time classes
==============================================

.. module:: datetime2
   :synopsis: Date and time types with broader calendar coverage.
.. moduleauthor:: Francesco Ricciardi <francescor2010@yahoo.it>

The :mod:`datetime2` module provides classes to manipulate date and time
like the :mod:`datetime` module does. However, its aim is to provide a
flexible framework in order to provide:

* decoupling between operations on date and time objects and their
  representation;
* access to different calendars, for input parsing and output formatting;
* access to different time representation systems, also for input and output;
* internationalization;
* implementation of the part of the Unicode Locale Database concerned with
  dates and times;
* interface with other Python modules or inclusion of their
  functionalities in its submodules.

However, the above objectives are long term ones, so stay tuned for
improvement!

Available calendars and time representation systems will be discovered at
import time. Additionally, registering new systems at run time is also
possible.

Available Classes
-----------------

There are four base classes in :mod:`datetime2`. These classes provide the
computation abilities of date and time handling, while giving a very basic
formatting, and no string parsing. Addtional classes (TODO: add link)
provide calendar and time system representation, and also will be capable
of parsing strings to generate dates and time.

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
   stored as a fraction of a day, using a Python :class:`Fraction`.
   Attributes of this class are: :attr:`day_frac`, :attr:`correction`.


.. class:: DateTime
   :noindex:

   A combination of a date and a time. As with :class:`Time`, there might be a
   correction of time. Date and time are stored together in a single Python
   :class:`Fraction`. Attributes of this class are: :attr:`days`,
   :attr:`correction`.


.. class:: TimeDelta
   :noindex:

   A duration expressing the difference between two :class:`Date`, :class:`Time`,
   or :class:`DateTime` instances. This difference is stored in a single Python
   :class:`Fraction`. The only attribute of this class is: :attr:`days`.


Objects of these types are immutable, so they can be used as dictionary key.


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

A :class:`Date` object represents a date in an idealized calendar which only
counts days from January 1 of year 1 of the current Gregorian calendar
indefinitely extended in both directions.  This matches the definition of the
"proleptic 
Gregorian" calendar in Dershowitz and Reingold's book Calendrical Calculations,
where it's the base calendar for all computations.


.. class:: Date(day_count)

   The argument is required and must be an integer. There is no restriction
   on its value.


Other constructors, all class methods:

.. classmethod:: Date.today()

   Return the current local date.


Instance attributes (read-only):

.. attribute:: Date.day_count

   The number of days between the given date and Janary 1, year 1.


Supported operations:

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
|                               | between *date2* and *date1*.                 |
+-------------------------------+----------------------------------------------+
| ``date1 < date2``             | *date1* is less than *date2* when its day    |
|                               | count is less that that of *date2*. (2)      |
+-------------------------------+----------------------------------------------+

Notes:

(1)
   Only the integer part of *timedelta* is taken into account. Definition is for
   positive *timedelta*; negative *timedelta* result in opposite behavior.

(2)
   In other words, ``date1 < date2`` if and only if ``date1.day_count <
   date2.day_count``. All other comparison operators between dates are defined.
   Comparison between a :class:`Date` object and an object of another class
   return a :exc:`NotImplemented` exception.

Dates can be used as dictionary keys. In Boolean contexts, all :class:`Date`
objects are considered to be true.

Instance methods:

.. method:: date.__str__()

   Return ``R.D.`` followed by the day count.







