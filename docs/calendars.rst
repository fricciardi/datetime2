Calendars
=========

.. testsetup::

   from datetime2.western import GregorianCalendar
   from datetime2.modern import IsoCalendar

This chapter lists the calendars classes available in the :mod:`datetime2` package.
Of course, they all conform to the rules listed in :ref:`customization`.

As such, they all have the six standard comparison operators: ``<``, ``>``, ``==``,
``>=``, ``<=``, and ``!=``, which return a meaningful result when comparing
calendar objects of the same type. When comparing a calendar object with an
object of a different type, the ``==`` and ``!=`` operators *always* consider
them to be unequal, while the ``<``, ``>``, ``>=`` and ``<=`` operators raise
a :exc:`TypeError` exception.

Similarly all classes implement the ``from_rata_die`` contructor and the
``to_rata_die`` method.

Description of the comparison operators and interface methods is then omitted
from the calendar class descriptions below.

.. TODO: if we will be keeping all calendars on a page, a ToC here will be useful



.. _gregorian-calendar:

Gregorian calendar
^^^^^^^^^^^^^^^^^^

An instance of the :class:`GregorianCalendar` class represents a day in the
calendar as generally done in western countries. It is a solar calendar dividing
day count in years of 365 or 366 days, each year is then divided in 12 months
of 28 (or 29), 30 and 31 days.

The default constructor for a Gregorian day is:

.. class:: GregorianCalendar(year, month, day)

   Return an object that represents the date given with Gregorian year, month
   and day. Month is entered as a number, not as a string. All arguments are
   required and must be integers. Values for ``month`` and ``day`` must lie in
   the following ranges:

   * ``1 <= month <= 12``
   * ``1 <= day <= number of days in the given month and year``

   If an argument is outside those ranges, a :exc:`ValueError` exception is
   raised.

Another constructor can be used if the day in the year is known:

.. classmethod:: GregorianCalendar.year_day(year, day_of_year)

   Return an object that represents the day specified by a Gregorian year and
   the day in that year. Both arguments are required and must be integers.
   Value for ``day_of_year`` must be between 1 and the number of days in the year
   (either 365 or 366), otherwise a :exc:`ValueError` exception is raised.


A :class:`GregorianCalendar` object has three attributes:

.. attribute:: GregorianCalendar.year

.. attribute:: GregorianCalendar.month

.. attribute:: GregorianCalendar.day

   These attributes are read-only integer numbers. There is no restriction on the
   value of the year. Month will be between 1 and 12. Day will be between 1 and
   the number of days in the corresponding month. These attributes are read-only:
   an :exc:`AttributeError` exception is raised when trying to change any of them.

Two static method have been implemented to return details of a Gregorian year:

.. staticmethod:: GregorianCalendar.is_leap_year(year)

   Return ``True`` if *year* is a leap year in the Gregorian calendar.
   ``False`` otherwise. For example,
   ``GregorianCalendar.is_leap_year(2008) == True``.

.. staticmethod:: GregorianCalendar.days_in_year(year)

   Return 366 if *year* is a leap year in the Gregorian calendar, 365
   otherwise. For example, ``GregorianCalendar.days_in_year(2100) == 365``.

An instance of the :class:`GregorianCalendar` class has the following
methods:

.. method:: GregorianCalendar.weekday()

   Return the day of the week as an integer, where Monday is 1 and Sunday is 7.
   For example, ``GregorianCalendar(2002, 12, 4).weekday() == 3``, a Wednesday.
   Note that this is the ISO convention for weekdays, *not* the one used by
   :meth:`datetime.date.weekday`, where Monday is 0 and Sunday is 6.

.. method:: GregorianCalendar.day_of_year()

   Return the day of the year as an integer, from 1 to 365 or 366 (in leap years).
   For example, ``GregorianCalendar(2008, 3, 1).day_of_year() == 61``.

.. method:: GregorianCalendar.replace(year, month, day)

   Returns a new :class:`GregorianCalendar` object with the same value, except
   for those parameters given new values by whichever keyword arguments are
   specified. All values are optional; if used, they must be integers. If any
   argument is outside its validity range or would create an invalid Gregorian
   date, a :exc:`ValueError` exception is raised. For example:

.. doctest::

      >>> greg = GregorianCalendar(2002, 12, 31)
      >>> print(greg.replace(day=26))
      2002-12-26
      >>> greg.replace(month=11)         # November has 30 days
      Traceback (most recent call last):
        |
      ValueError: Day must be between 1 and number of days in month, while it is 31.

.. method:: GregorianCalendar.__str__()

   Return a string representing the date with the 'YYYY-MM-DD' format. Years
   above 9999 are represented adding necessary figures. Negative years are
   represented prepending the minus sign. For example:

.. doctest::

      >>> str(GregorianCalendar(2002, 12, 4))
      '2002-12-04'
      >>> str(GregorianCalendar(-1, 1, 1))
      '-0001-01-01'


.. method:: GregorianCalendar.cformat(format)

   Return a string representing the date, controlled by an explicit format
   string. The formatting directives are a subset of those accepted by
   :meth:`datetime.date.strftime`, and their meaning does not depend on the
   underlying C library (i.e. there are no platform variations). The table
   below lists the accepted formatting directives, all other character are not
   interpreted.

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
   |           | number [01, 31].               |       |
   +-----------+--------------------------------+-------+
   | ``%j``    | Day of the year as a decimal   |       |
   |           | number [001, 366].             |       |
   +-----------+--------------------------------+-------+
   | ``%m``    | Month as a decimal number      |       |
   |           | [01, 12].                      |       |
   +-----------+--------------------------------+-------+
   | ``%U``    | Week number of the year        |       |
   |           | (Sunday as the first day of    |       |
   |           | the week) as a decimal number  |       |
   |           | [00, 53].  All days in a new   |       |
   |           | year preceding the first       |       |
   |           | Sunday are considered to be in |       |
   |           | week 0.                        |       |
   +-----------+--------------------------------+-------+
   | ``%w``    | Weekday as a decimal number    |       |
   |           | [1 (Monday), 7 (Sunday)].      |       |
   +-----------+--------------------------------+-------+
   | ``%W``    | Week number of the year        |       |
   |           | (Monday as the first day of    |       |
   |           | the week) as a decimal number  |       |
   |           | [00, 53].  All days in a new   |       |
   |           | year preceding the first       |       |
   |           | Monday are considered to be in |       |
   |           | week 0.                        |       |
   +-----------+--------------------------------+-------+
   | ``%y``    | Year without century as a      | \(2)  |
   |           | decimal number [00, 99].       |       |
   +-----------+--------------------------------+-------+
   | ``%Y``    | Year with century as a decimal | \(3)  |
   |           | number. At least four figures  |       |
   |           | will be returned.              |       |
   +-----------+--------------------------------+-------+
   | ``%%``    | A literal ``'%'`` character.   |       |
   +-----------+--------------------------------+-------+

Notes:

(1)
   The ``%a``, ``%A``, ``%b`` and ``%B`` directives return a localized name in
   Standard C++. This is not true for :mod:`datetime2`, which only returns
   English names.

(2)
   Since this is a truncated representation, **negative years will not have a sign**.

(3)
   Negative years will have a trailing ``'-'``.


.. _iso-calendar:

ISO calendar
^^^^^^^^^^^^

The ISO calendar divides the days into weeks, from Monday to Sunday, and groups
52 or 53 whole weeks into a year. The first calendar week of a year is the one
that includes the first Thursday of the corresponding Gregorian year. This
definition can be seen also as: the first calendar weeks of a ISO year
is the week including January, 4\ :sup:`th` Gregorian.

A good discussion of the ISO calendar can be read at `The Mathematics of the
ISO 8601 Calendar
<http://www.staff.science.uu.nl/~gent0113/calendar/isocalendar.htm>`_.

The constructor of an ISO calendar is:

.. currentmodule:: datetime2.modern

.. class:: IsoCalendar(year, week, day)

   Return an object that represents the date given with ISO year, week number
   and day. All arguments are required and must be integers. Values for
   ``week`` and ``day`` must lie in the following ranges:

   * ``1 <= week <= number of weeks in the given year``
   * ``1 <= day <= 7``

   If an argument is outside those ranges, a :exc:`ValueError` exception is
   raised. They day number goes from 1 (Monday) to 7 (Sunday).


An :class:`IsoCalendar` object has three attributes:

.. attribute:: IsoCalendar.year

.. attribute:: IsoCalendar.week

.. attribute:: IsoCalendar.day

   These attributes are read-only integer numbers. Week will be between 1 and
   the number of weeks in the ISO year (52 or 53), day will be between 1 and 7.

Two static method have been implmented to give details of an ISO year:

.. classmethod:: IsoCalendar.is_long_year(year)

   Return ``True`` if *year* is a long year, i.e. a year with 53 weeks, in the
   ISO calendar, ``False`` otherwise. For example,
   ``IsoCalendar.is_leap_year(2004) == True``.

.. classmethod:: IsoCalendar.weeks_in_year(year)

   Return the number of weeks in a ISO year, either 52 or 53. For example,
   ``IsoCalendar.weeks_in_year(2009) == 53``.


An instance of the :class:`IsoCalendar` class has the following methods:

.. method:: IsoCalendar.day_of_year()

   Return the day of the year as an integer, from 1 to 364 (in short years) or
   371 (in long years). For example, ``IsoCalendar(2008, 3, 1).day_of_year() ==
   62``.

.. method:: IsoCalendar.replace(year, week, day)

   Returns a new :class:`IsoCalendar` object with the same value, except for
   those parameters given new values by whichever keyword arguments are
   specified. All values are optional; if used, they must be integers. If any
   argument is outside its validity range or would create an invalid Gregorian
   date, a :exc:`ValueError` exception is raised. For example:

.. doctest::

      >>> iso = IsoCalendar(2004, 53, 3)
      >>> print(iso.replace(week=26))
      2004-W26-3
      >>> iso.replace(year=2003)  # 2003 has 52 weeks
      Traceback (most recent call last):
        |
      ValueError: Week must be between 1 and number of weeks in year, while it is 53.

.. method:: IsoCalendar.__str__()

   Return a string representing the date with the 'YYYY-**W**\ WW-DD' format.
   Years above 9999 are represented adding necessary figures. Negative years
   are represented prepending the minus sign. For example:

.. doctest::

      >>> str(IsoCalendar(2002, 12, 4))
      '2002-W12-4'
      >>> str(IsoCalendar(-1, 1, 1))
      '-0001-W01-1'


.. method:: IsoCalendar.cformat(format)

   Return a string representing the ISO date, controlled by an explicit format
   string. The formatting directives are a subset of those accepted by
   :meth:`datetime.date.strftime`, and their meaning does not depend on the
   underlying C library (i.e. there are no platform variations). The table
   below lists the accepted formatting directives, all other character are not
   interpreted.

   +-----------+--------------------------------+-------+
   | Directive | Meaning                        | Notes |
   +===========+================================+=======+
   | ``%a``    | Abbreviated weekday name.      | \(1)  |
   +-----------+--------------------------------+-------+
   | ``%A``    | Full weekday name.             | \(1)  |
   +-----------+--------------------------------+-------+
   | ``%j``    | Day of the year as a decimal   |       |
   |           | number [001,371].              |       |
   +-----------+--------------------------------+-------+
   | ``%w``    | Weekday as a decimal number    |       |
   |           | [1 (Monday), 7 (Sunday)].      |       |
   +-----------+--------------------------------+-------+
   | ``%W``    | Week number in the ISO year    |       |
   |           | as a decimal number [01, 53].  |       |
   +-----------+--------------------------------+-------+
   | ``%y``    | ISO year without century as a  | \(2)  |
   |           | decimal number [00, 99].       |       |
   +-----------+--------------------------------+-------+
   | ``%Y``    | ISO year with century as a     | \(3)  |
   |           | decimal number. At least four  |       |
   |           | figures will be returned.      |       |
   +-----------+--------------------------------+-------+
   | ``%%``    | A literal ``'%'`` character.   |       |
   +-----------+--------------------------------+-------+

Notes:

(1)
   The ``%a`` and ``%A`` directives return a localized name in Standard C++.
   This is not true for :mod:`datetime2`, which only returns English names.

(2)
   Since this is a truncated representation, **negative years will not have a
   sign**.

(3)
   Negative years will have a trailing ``'-'``.
