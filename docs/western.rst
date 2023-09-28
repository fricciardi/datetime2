:mod:`datetime2.western` - Gregorian calendar and western time
==============================================================

.. module:: datetime2.western
    :synopsis: Gregorian calendar and western time
.. moduleauthor:: Francesco Ricciardi <francescor2010@yahoo.it>

.. testsetup::

   from datetime2.western import GregorianCalendar

This module implements the calendar and time representation used in the
western world:

*  The :ref:`Gregorian calendar <gregorian-calendar>`
*  The :ref:`western time representation <western-time>` in hours, minutes and
   seconds.

Of course, they all conform to the requirements for interface classes listed
in :ref:`customization`.


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

   Return the number of days elapsed since January 1\ :sup:`st`. The result
   is a number from 1 to 365 or 366 (in leap years). For example,
   ``GregorianCalendar(2008, 3, 1).day_of_year() == 61``.


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


.. _western-time:

Western time
^^^^^^^^^^^^

An instance of the :class:`WesternTime` class represents a moment of a day as
generally done in western countries, dividing each day in 24 hours, each hour
in 60 minutes and each minute in 60 seconds.

The default western time constructor is:

.. class:: WesternTime(hour, minute, second, timezone=None)

   Return an object that represents the moment of a day in hour, minute and
   second elapsed from midnight. This representation does not take into
   account the possibility of one or two additional seconds that sometimes
   are added in specific dates to compensate earth rotation. All arguments
   except ``timezone`` are required. The following requirements must be
   satisfied:

   * ``hour`` must be an integer and ``0 <= hour < 24``
   * ``minute`` must be an integer and ``0 <= minute < 60``
   * ``second`` must be a rational number and its value must be
     ``0 <= second < 60``
   * ``timezone``, if present, must be a rational number and its value must be
     ``-24 <= timezone <= 24``

   Here a *rational number* is anything that can be passed to the
   :class:`fractions.Fraction` constructor, i.e. an integer, a float, another
   Fraction, a Decimal number or a string representing an integer, a float or
   a fraction.

   If an argument is not of the accepted type, a :exc:`TypeError` exception
   is raised. If an argument is outside its accepted range, a
   :exc:`ValueError` exception is raised.

   The ``timezone`` argument, if present, makes the object aware and defines
   the number of hours that must be added to UTC to get local time.

.. note::

   The ``timezone`` parameter is likely to change its values in future.

A :class:`WesternTime` object has four attributes, all of which are read-only
numbers: an attempt to change them will raise an :exc:`AttributeError`
exception. These attributes store the corresponding values in the constructor:

.. attribute:: WesternTime.hour

   An integer with values between ``0`` and ``23``.

.. attribute:: WesternTime.minute

   An integer with values between ``0`` and ``59``.

.. attribute:: WesternTime.second

   A Python Fraction with value grater or equal to ``0`` and less than ``60``.

.. attribute:: WesternTime.timezone

   If this attribute is not ``None``, it a Python Fraction with values
   between -24 and 24.


An instance of the :class:`WesternTime` class has the following methods:

.. method:: WesternTime.replace(hour, minute, second, *, timezone)

   Returns a new :class:`WesternTime` object with the same value, except
   for those parameters given new values by whichever keyword arguments are
   specified. The value, if given, they must respect the same requirements
   of the default constructor, otherwise a :exc:`TypeError` or
   :exc:`ValueError` exception is raised. ``timezone`` parameter can be
   replaced only for aware instances. For example:

.. doctest::

      >>> my_time = WesternTime(19, 6, 29)
      >>> print(my_time.replace(minute=38))
      19:38:29
      >>> my_time.replace(hour=24)
      Traceback (most recent call last):
        |
      ValueError: Hour must be between 0 and 23, while it is 24.
      >>> my_time.replace(timezone=1)
      Traceback (most recent call last):
        |
      TypeError: Can replace timezone only in aware instances.

.. method:: WesternTime.__str__()

   For a naive instance, return a string representing the time with the
   'HH:MM:SS' format. For an aware instance, the format is
   'HH:MM:SS+HH:MM'. The number of seconds in the time part and the number of
   minutes in the timezone part will be truncated. For example:

.. doctest::

      >>> str(WesternTime(12, 44, 14.8))
      '12:44:14'
      >>> str(WesternTime(12, 34, 56.7, timezone=12.256))
      '12:34:56+12:15'

.. method:: WesternTime.cformat(format)

   Return a string representing the time, controlled by an explicit format
   string. The formatting directives are a subset of those accepted by
   :meth:`datetime.date.strftime`, and their meaning does not depend on the
   underlying C library (i.e. there are no platform variations). The table
   below lists the accepted formatting directives, all other characters are
   not interpreted.

   +-----------+-------------------------------------------+-------+
   | Directive | Meaning                                   | Notes |
   +===========+===========================================+=======+
   | ``%H``    | Hour (24-hour clock) as a                 |       |
   |           | zero-padded decimal number [00, 23].      |       |
   +-----------+-------------------------------------------+-------+
   | ``%I``    | Hour (12-hour clock) as a                 |       |
   |           | zero-padded decimal number [01, 12].      |       |
   +-----------+-------------------------------------------+-------+
   | ``%p``    | Returns 'AM' if hour is between 0 and 11, |       |
   |           | 'PM' if hour is between 12 and 23.        | \(1)  |
   +-----------+-------------------------------------------+-------+
   | ``%M``    | Minute as a zero-padded decimal number    |       |
   |           | [00, 59].                                 |       |
   +-----------+-------------------------------------------+-------+
   | ``%S``    | Second as a zero-padded decimal number    |       |
   |           | [00, 59].                                 |       |
   +-----------+-------------------------------------------+-------+
   | ``%f``    | Microsecond as a decimal number,          |       |
   |           | zero-padded on the left [000000, 999999]. |       |
   +-----------+-------------------------------------------+-------+
   | ``%z``    | UTC offset in the form ±HHMM[SS[.ffffff]] |       |
   |           | (empty string if the object is naive).    |       |
   +-----------+-------------------------------------------+-------+
   | ``%%``    | A literal ``'%'`` character.              |       |
   +-----------+-------------------------------------------+-------+

Notes:

(1)
   The ``%p`` directive returns a localized string in Standard C++. This is
   not true for :mod:`datetime2`, which only returns the English string.


.. _western-timedelta:

Western time interval
^^^^^^^^^^^^^^^^^^^^^

An instance of the :class:`WesternTimeDelta` class represents a time interval
given in days, hours, minutes and seconds.

The default constructor is:

.. class:: WesternTimeDelta(days, hours, minutes, seconds)

   Return an object that represents a time interval in hours, minutes and
   seconds. All arguments are required. ``hours``, ``minutes`` and
   ``seconds`` must have the same sign of ``days``. The types and absolute
   values of each parameter are listed below:

   * ``days`` must be an integer of any value
   * ``hours`` must be an integer and its absolute value must be
     ``0 <= hours <= 23``
   * ``minutes`` must be an integer and its absolute value must be
     ``0 <= minutes <= 59``
   * ``seconds`` must be a rational number and its absolute value must be
     ``0 <= second < 60``

   Here a *rational number* is anything that can be passed to the
   :class:`fractions.Fraction` constructor, i.e. an integer, a float, another
   Fraction, a Decimal number or a string representing an integer, a float or
   a fraction.

   If an argument is not of the accepted type, a :exc:`TypeError` exception
   is raised. If an argument is outside its accepted range or all parameter
   haven't the same sign, a :exc:`ValueError` exception is raised.


A :class:`WesternTimeDelta` object has four attributes, all of which are
read-only numbers: an attempt to change them will raise an
:exc:`AttributeError` exception. These attributes store the corresponding
values in the constructor:

.. attribute:: WesternTimeDelta.days

   An integer of any value.

.. attribute:: WesternTimeDelta.hours

   An integer of the same sign as ``days`` and with absolute value between
   ``0`` and ``23``.

.. attribute:: WesternTimeDelta.minutes

   An integer of the same sign as ``days`` and with absolute value between
   ``0`` and ``59``.

.. attribute:: WesternTimeDelta.seconds

   A Python Fraction of the same sign as ``days`` and with absolute value
   grater or equal to ``0`` and less than ``60``.

An instance of the :class:`WesternTimeDelta` class has the following methods:

.. method:: WesternTimeDelta.replace(days, hours, minutes, seconds)

   Returns a new :class:`WesternTimeDelta` object with the same value, except
   for those parameters given new values by whichever keyword arguments are
   specified. The value, if given, they must respect the same requirements
   of the default constructor, otherwise a :exc:`TypeError` or
   :exc:`ValueError` exception is raised. For example:

.. doctest::

      >>> my_td = WesternTimeDelta(1, 23, 45, 6)
      >>> print(my_td.replace(minutes=0))
      1 day, 23 hours and 6 seconds
      >>> my_td.replace(hours=24)
      Traceback (most recent call last):
        |
      ValueError: Hours must be between 0 and 23, while it is 24.
      >>> my_time.replace(secondsì'33')
      Traceback (most recent call last):
        |
      ValueError: Seconds must be of the same sign of 'days'.

.. method:: WesternTimeDelta.__str__()

   Return a string representing the time interval. When a component of the
   interval is zero, it is not printed. The number of seconds will be
   truncated. For example:

.. doctest::

      >>> str(WesternTimeDelta(9, 8, 7, 6.5))
      '9 days, 8 hours, 7 minutes and 6 seconds'
      >>> str(WesternTimeDelta(0, 0, -5, -2))
      '-5 minutes and -2 seconds'

.. method:: WesternTimeDelta.cformat(format)

   Return a string representing the time, controlled by an explicit format
   string. The formatting directives are a subset of those accepted by
   :meth:`datetime.date.strftime`, and their meaning does not depend on the
   underlying C library (i.e. there are no platform variations). The table
   below lists the accepted formatting directives, all other characters are
   not interpreted.

   +-----------+-------------------------------------------+
   | Directive | Meaning                                   |
   +===========+===========================================+
   | ``%d``    | Full days as a decimal number.            |
   +-----------+-------------------------------------------+
   | ``%H``    | Hours as a zero-padded decimal number     |
   |           | [00, 23].                                 |
   +-----------+-------------------------------------------+
   | ``%M``    | Minutes as a zero-padded decimal number   |
   |           | [00, 59].                                 |
   +-----------+-------------------------------------------+
   | ``%S``    | Seconds as a zero-padded decimal number   |
   |           | [00, 59].                                 |
   +-----------+-------------------------------------------+
   | ``%f``    | Microseconds as a zero-padded decimal     |
   |           | number [000000, 999999].                  |
   +-----------+-------------------------------------------+
   | ``%%``    | A literal ``'%'`` character.              |
   +-----------+-------------------------------------------+

