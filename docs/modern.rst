:mod:`datetime2.modern` - ISO calendar and Internet time
==============================================================

.. module:: datetime2.modern
    :synopsis: ISO calendar and Internet time
.. moduleauthor:: Francesco Ricciardi <francescor2010@yahoo.it>

.. testsetup::

   from datetime2.modern import IsoCalendar

This module implements a calendar and a time representation that have been
defined in the recent years:

*  The :ref:`ISO calendar <iso-calendar>`
*  The :ref:`internet time representation <internet-time>` where a day is divided in 1000 parts.

Of course, they all conform to the requirements for interface classes listed
in :ref:`customization`.


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


.. _internet-time:

Internet time
^^^^^^^^^^^^^

The Internet Time (or beat time) is a decimal time concept introduced in 1998,
marketed by a large Swiss watch company, and divides the day in 1000 parts,
called "beats". A beat is equivalent to 1 minute and 26.4 seconds. A `Wikipedia
article <http://en.wikipedia.org/wiki/Swatch_Internet_Time>`_ describes
the Internet time. The Internet time is aware by definition.

The default constructor for Internet time is:

.. class:: InternetTime(beat)

   Return an object that represents the time in thousandths of a day. The
   ``beat`` argument is required and must be a anything that can be passed to
   the :class:`fractions.Fraction` constructor, i.e. an integer, a float,
   another Fraction, a Decimal number or a string representing an integer, a
   float or a fraction. Its value must be equal or greater than 0 and less
   than 1000. If the argument is not of one of the possible types, a
   :exc:`TypeError` exception is raised. If the argument is outside its
   accepted range, a :exc:`ValueError` exception is raised.

An :class:`InternetTime` object has one attribute:

.. attribute:: InternetTime.beat

   This attribute is a read-only Python Fraction greater than or equal to 0
   and less than 1000.

and the following methods:

.. method:: InternetTime.__str__()

   Return a string representing the moment of the day in beats, '@BBB' format.
   For example:

.. doctest::

      >>> str(InternetTime(345.25))
      '@345'

.. method:: InternetTime.cformat(format)

   Return a string representing the Internet time, controlled by an explicit
   format string with formatting directives close to that used in C. The table
   below lists the accepted formatting directives, all other character are not
   interpreted.

   +-----------+--------------------------------------+-------+
   | Directive | Meaning                              | Notes |
   +===========+======================================+=======+
   | ``%b``    | Integer number of beats [000, 999].  |       |
   +-----------+--------------------------------------+-------+
   | ``%f``    | Thousandths of a beat,               | \(1)  |
   |           | zero-padded on the left [000, 999].  |       |
   +-----------+--------------------------------------+-------+

Notes:

(1)
   One thousandth of a beat is a millionth of a day, i.e. 86.4 milliseconds.
