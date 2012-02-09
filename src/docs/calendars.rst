Calendars
=========

This chapter lists the calendars defined in the :mod:`datetime2` module. As
described :ref:`here <register-classes>`, it is possible to add calendars to
the *datetime2* module at run time.

.. _gregorian-calendar:

Gregorian calendar
^^^^^^^^^^^^^^^^^^

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
   (either 365 or 366), otherwise a :exc:`ValueError` exception is raised.

There are two classmethods:

.. classmethod:: Date.gregorian.is_leap_year(year)

   Return ``True`` if *year* is a leap year in the Gregorian calendar.
   ``False`` otherwise. For example, ``Date.gregorian.is_leap_year(2008) == True``.

.. classmethod:: Date.gregorian.days_in_year(year)

   Return 366 if *year* is a leap year in the Gregorian calendar, 365
   otherwise. For example, ``Date.gregorian.days_in_year(2100) == 365``.

   .. versionadded:: 0.3.2
      :meth:`days_in_year` will be added in version 0.3.2.


The Gregorian representation of a :class:`Date` instance has three attributes:

.. attribute:: date.gregorian.year

.. attribute:: date.gregorian.month

.. attribute:: date.gregorian.day

   These attributes are read-only integer numbers. Month will be between 1 and 12, day
   will be between 1 and the number of days in the corresponding month.

The Gregorian representation of a :class:`Date` object has the following
methods:

.. method:: date.gregorian.weekday()

   Return the day of the week as an integer, where Sunday is 0 and Saturday is
   6. For example, ``Date.gregorian(2002, 12, 4).weekday() == 3``, a Wednesday.
   Note that this is *not* the convention used by :meth:`date.weekday`, where
   Monday is 0 and Sunday is 6.

   .. versionadded:: 0.3.2
      :meth:`days_in_year` will be added in version 0.3.2.


.. method:: date.gregorian.day_of_year()

   Return the day of the year as an integer, from 1 to 365 or 366 (in leap years).
   For example, ``Date.gregorian(2008, 3, 1).day_of_year() == 61``.

   .. versionadded:: 0.3.2
      :meth:`day_of_year` will be added in version 0.3.2.


.. method:: date.gregorian.replace(year, month, day)

   Returns a new :class:`Date` object with the same value, except for those members
   given new values by whichever keyword arguments are specified. All values are optional; if used, they must be
   integers. If any argument is outside its validity range, a :exc:`ValueError`
   exception is raised. For example, if ``d == Date.gregorian(2002, 12, 31)``, then
   ``d.replace(day=26) == Date.gregorian(2002, 12, 26)``.

   .. versionadded:: 0.3.2
      :meth:`replace` will be added in version 0.3.2.


.. method:: date.gregorian.week_and_day(week_start = 0)

   Return a tuple representing the week number in the year the date belongs to,
   and the day within this week. Week number 1 starts on the first weekday
   ``week_start`` (0 for Sunday, 6 for Saturday). Days preceding the first
   ``week_start`` day are in week 0.
   For example, ``Date.gregorian(2010, 5, 8).day_of_year(week_start = 0) == 18``.

   .. versionadded:: 0.3.2
      :meth:`week_and_day` will be added in version 0.3.2.


.. method:: date.gregorian.__str__()

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

   .. versionadded:: 0.3.2
      :meth:`__str__` will be added in version 0.3.2.


.. method:: date.gregorian.cformat(format)

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

   .. versionadded:: 0.3.2
      :meth:`cformat` will be added in version 0.3.2.

