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

There are two ways of creating a :class:`Date` instance:

.. class:: Date(day_count)

   Return an object that represent a date which is ``day_count - 1`` days
   after January 1 of year 1 in the current Gregorian calendar. The argument
   is requiried and must be an integer. There is no restriction on its value.


.. classmethod:: Date.today()

   Return a :class:`Date` object that represents the current local date.

:class:`Date` objects are immutable, so they can be used as dictionary keys.
They can also be pickled and unpickled. In Boolean contexts, all :class:`Date`
instances are considered to be true.

:class:`Date` instances have a read-only attribute:

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
   date2.day_count``. All other comparison operators behave similarly.
   
(4)
   Comparison between a :class:`Date` object and an object of another class
   return a :exc:`NotImplemented` exception, except for the equality and inequality
   operators, which respectively return *False* and *True*.


There's one instance method:

.. method:: Date.__str__()

   Return ``R.D.`` followed by the day count. ``R.D.`` stands for Rata Die, the Latin
   for "fixed date".


Other constructors and representations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As shown above, :class:`Date` objects have little use. The intended purpose
of the :mod:`datetime2` module is indeed that to provide access to a number
of different calendars. In detail, there will be a number of constructors
reachable with dotted notation to class :class:`Date`. Similarly, there will
access to representation attributes and/or methods.

Gregorian
"""""""""

The Gregorian representation uses the calendar generally used in western
countries. It is a solar calendar dividing day count in years of 365 or 366
days, each year is then divided in 12 months of 30, 31 and 28 or 29 days.

The default constructor for Gregorian dates is:

.. class:: Date.gregorian(year, month, day)

   Return a :class:`Date` object that represents the date given with Gregorian
   year, month and day. Month is entered as a number, not as a string. All
   arguments are required and must be integers. Values for ``month`` and ``day``
   must lie in the following ranges:

   * ``1 <= month <= 12``
   * ``1 <= day <= number of days in the given month and year``

   If an argument outside those ranges is given, :exc:`ValueError` is raised.

Another constructor:

.. class:: Date.gregorian.year_day(year, day_of_year)

   Returns a :class:`Date` object that represents the date given with Gregorian
   year, and day in year. Both arguments are required and must be integers.
   Value for ``day_of_year`` must be between 1 and the number of days in the year
   (either 365 or 366):

   * ``1 <= month <= 12``
   * ``1 <= day <= number of days in the given month and year``

   If an argument outside those ranges is given, :exc:`ValueError` is raised.

There are classmethods:

.. classmethod:: Date.gregorian.is_leap_year(year)

   Return ``True`` if *year* is a leap year in the Gregorian calendar.
   ``False`` otherwise. For example, ``Date.gregorian.is_leap_year(2008) == True``.

.. classmethod:: Date.gregorian.days_in_year(year)

   Return 366 if *year* is a leap year in the Gregorian calendar, 365
   otherwise. For example, ``Date.gregorian.days_in_year(2100) == 365``.

The Gregorian representation of a :class:`Date` instance has three attributes:

.. attribute:: Date.gregorian.year

.. attribute:: Date.gregorian.month

.. attribute:: Date.gregorian.day

   These attributes are read-only integer numbers. Month will be between 1 and 12, day
   will be between 1 and the number of days in the corresponding month.

The Gregorian representation of a :class:`Date` object has the following methods:

.. method:: Date.gregorian.weekday()

   Return the day of the week as an integer, where Sunday is 0 and Saturday is 6.
   For example, ``Date.gregorian(2002, 12, 4).weekday() == 3``, a Wednesday.
   Note that this is *not* the convention used by :meth:`date.weekday`, where
   Monday is 0 and Sunday is 6.

.. method:: Date.gregorian.day_of_year()

   Return the day of the year as an integer, from 1 to 365 or 366 (in leap years).
   For example, ``Date.gregorian(2008, 3, 1).day_of_year() == 61``.

.. method:: Date.gregorian.replace(year, month, day)

   Returns a new :class:`Date` object with the same value, except for those members
   given new values by whichever keyword arguments are specified. All values must be
   integers. If any argument is outside its validity range, a :exc:`ValueError`
   exception is raised. For example, if ``d == Date.gregorian(2002, 12, 31)``, then
   ``d.replace(day=26) == Date.gregorian(2002, 12, 26)``.


.. method:: Date.gregorian.week_and_day(week_start = 0)

   Return a tuple representing the week number in the year the date belongs to,
   and the day within this week. Week number 1 starts on the first weekday
   ``week_start`` (0 for Sunday, 6 for Saturday). Days preceding the first
   ``week_start`` day are in week 0.
   For example, ``Date.gregorian(2010, 5, 8).day_of_year(week_start = 0) == 18``.

.. method:: Date.gregorian.__str__()

   Return a string representing the date in ISO 8601 format 'YYYY-MM-DD'
   (*Extended format* of paragraph 4.1.2.2 of the Standard, "Complete representation"). For
   negative years and for years above 9999, the representation 's_Y_YYYY-MM-DD'
   (*Extended format* of paragraph 4.1.2.4, "Expanded representations") will
   be used, where s is either '+' or '-' and is mandatory and _Y_ is one or
   more figures. For example::

      >>> d1 = Date.gregorian(2002, 12, 4)
      >>> str(d1)
      'R.D. 731188'
      >>> str(d1.gregorian)
      '2002-12-04'
      >>> d2 = Date.gregorian(-1, 1, 1)
      >>> str(d2.gregorian)
      '-00001-01-01'

.. method:: Date.gregorian.cformat(format)

   Return a string representing the date, controlled by an explicit format string.
   The formatting characters are the same as :meth:`date.strftime`, except that
   their meaning does not depend on the underlying C library (i.e. there are no
   platform variations). Also, formatting characters not valid for dates are not
   interpreted.

   The table below lists the interpreted formatting codes for ``Date.gregorian``
   objects.

   +-----------+--------------------------------+-------+
   | Directive | Meaning                        | Notes |
   +===========+================================+=======+
   | ``%a``    | Abbreviated weekday name.      | \(1)  |
   +-----------+--------------------------------+-------+
   | ``%A``    | Full weekday name.             | \(1)  |
   +-----------+--------------------------------+-------+
   | ``%b``    | Abbreviated month name.        | \(1)  |
   +-----------+--------------------------------+-------+
   | ``%B``    | Full month name.               | \(1)  |
   +-----------+--------------------------------+-------+
   | ``%d``    | Day of the month as a decimal  |       |
   |           | number [01,31].                |       |
   +-----------+--------------------------------+-------+
   | ``%j``    | Day of the year as a decimal   |       |
   |           | number [001,366].              |       |
   +-----------+--------------------------------+-------+
   | ``%m``    | Month as a decimal number      |       |
   |           | [01,12].                       |       |
   +-----------+--------------------------------+-------+
   | ``%U``    | Week number of the year        |       |
   |           | (Sunday as the first day of    |       |
   |           | the week) as a decimal number  |       |
   |           | [00,53].  All days in a new    |       |
   |           | year preceding the first       |       |
   |           | Sunday are considered to be in |       |
   |           | week 0.                        |       |
   +-----------+--------------------------------+-------+
   | ``%w``    | Weekday as a decimal number    |       |
   |           | [0 (Sunday),6 (Saturday)].     |       |
   +-----------+--------------------------------+-------+
   | ``%W``    | Week number of the year        |       |
   |           | (Monday as the first day of    |       |
   |           | the week) as a decimal number  |       |
   |           | [00,53].  All days in a new    |       |
   |           | year preceding the first       |       |
   |           | Monday are considered to be in |       |
   |           | week 0.                        |       |
   +-----------+--------------------------------+-------+
   | ``%y``    | Year without century as a      | \(2)  |
   |           | decimal number [00,99].        |       |
   +-----------+--------------------------------+-------+
   | ``%Y``    | Year with century as a decimal | \(3)  |
   |           | number.                        |       |
   +-----------+--------------------------------+-------+
   | ``%%``    | A literal ``'%'`` character.   |       |
   +-----------+--------------------------------+-------+

Notes:

(1)
   The ``%a``, ``%A``, ``%b`` and ``%B`` directives return a localized name in
   Standard C++. This is not true for :mod:`datetime2`, which only returns
   English names.

(2)
   Since this is a truncated representation, negative years will not have a sign.

(3)
   Negative years will have a trailing ``'-'``.
