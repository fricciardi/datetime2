Time of day
===========

.. testsetup:: western

   from timeofday.western import WesternTime

.. testsetup:: internet

   from timeofday.other import InternetTime

This chapter lists the time representations classes defined in the
:mod:`datetime2` package. These classes are not depending on the
:class:`~datetime2.Time` class.

.. TODO: if we will be keeping all time representations on a page, a ToC here will be useful

All time representations listed here define the six standard comparison operators:
``<``, ``>``, ``==``, ``>=``, ``<=``, and ``!=``, which return a meaningful
result when comparing time representation objects of the same type. When comparing a
time representation object with an object of a different type, the ``==`` and ``!=``
operators *always* consider them to be unequal, while the ``<``, ``>``, ``>=``
and ``<=`` operators raise a :exc:`TypeError`. In the following we will call a Python
number any Python integer, float, Fraction or Decimal number.

Note that these time representations do not have any notion of time correction
like daylight saving time or time zone.

Also, all time representations listed here conform to the rules listed in
:ref:`customization`.

.. _western-time:

Western time
^^^^^^^^^^^^

An instance of the :class:`WesternTime` class represents a moment of a day as
generally done in western countries, dividing each day in 24 hours, each hour
in 60 minutes and each minute in 60 seconds.

There are five constructors for a western time. The default one is:

.. class:: WesternTime(hour, minute, second)

   Return an object that represents the moment of a day in hour, minute and
   second. This representation does not take into account the possibility of
   one or two additional seconds that sometimes are added in specific dates
   to compensate earth rotation. All arguments are required and must satisfy
   the following requirements:

   * ``hour`` must be an integer and ``0 <= month <= 23``
   * ``minute`` must be an integer and ``0 <= minute <= 59``
   * ``second`` must be a Python number; its value must be ``0 <= second < 60``

   If an argument is not of the accepted type, a :exc:`TypeError` exception
   is raised. If an argument is outside its accepted range, a :exc:`ValueError`
   exception is raised.

The other four constructors are:

.. class:: WesternTime.in_hours(hour)

   Return an object that represents the moment of the day specified as a
   multiple, possibly with decimals, of an hour. The argument must be a Python
   number, otherwise a :exc:`TypeError` exception is generated. Its value must
   be equal or greater than 0 and less than 24, otherwise a :exc:`ValueError`
   exception is raised.

.. class:: WesternTime.in_minutes(minute)

   Return an object that represents the moment of the day specified as a
   multiple, possibly with decimals, of a minute. The argument must be a Python
   number, otherwise a :exc:`TypeError` exception is generated. Its value must
   be equal or greater than 0 and less than 1440, otherwise a :exc:`ValueError`
   exception is raised.

.. class:: WesternTime.in_seconds(second)

   Return an object that represents the moment of the day specified as a
   multiple, possibly with decimals, of a second. The argument must be a Python
   number, otherwise a :exc:`TypeError` exception is generated. Its value must
   be equal or greater than 0 and less than 86400, otherwise a :exc:`ValueError`
   exception is raised.

.. class:: WesternTime.from_day_frac(day_frac)

   Return an object that represents the fraction of the day in hours,
   minutes and seconds. The ``day_frac`` argument is required and must be
   a Python number, otherwise a :exc:`TypeError` exception is generated. Its
   value must be equal or greater than 0 and less than 1, otherwise a
   :exc:`ValueError` exception is raised. Note that the only accepted integer
   value is ``0``.

A :class:`WesternTime` object has three attributes:

.. attribute:: western.hour

.. attribute:: western.minute

.. attribute:: western.second

   These attributes are read-only numbers. The first two are integers; the
   last one is a Python Fraction. The three attributes will respect the
   value requirements of the main constructor.

An instance of the :class:`WesternTime` class has the following methods:

.. method:: western.as_hours()

   Return a Python Fraction representing the moment of the day in hours.
   Thus the returned value will be equal or greater than 0, and less
   than 24.

.. method:: western.as_minutes()

   Return a Python Fraction representing the moment of the day in minutes.
   Thus the returned value will be equal or greater than 0, and less
   than 1440.

.. method:: western.as_seconds()

   Return a Python Fraction representing the moment of the day in seconds.
   Thus the returned value will be equal or greater than 0, and less
   than 86400.

.. method:: western.to_day_frac()

   Return a Python Fraction representing the moment of the day in days.
   Thus the returned value will be equal or greater than 0, and less
   than 1. For example,
   ``WesternTime(14, 45, 0).to_day_fraction() == fractions.Fraction(45, 96)``.

.. method:: western.replace(hour, minute, second)

   Returns a new :class:`WesternTime` object with the same value, except
   for those parameters given new values by whichever keyword arguments are
   specified. All values are optional; if used, they must respect the
   requirements of the main constructor, otherwise a :exc:`TypeError` or
   :exc:`ValueError` exception is raised. For example:

.. doctest:: western

      >>> my_time = WesternTime(19, 6, 29)
      >>> print(my_time.replace(minute=38))
      06:38:29
      >>> my_time.replace(hour=24)
      Traceback (most recent call last):
        |
      ValueError: Hour must be between 0 and 23, while it is 24.

.. method:: western_time.__str__()

   Return a string representing the time with the 'HH:MM:SS' format. Any
   decimal will be truncated from the number of seconds. For example:

.. doctest:: western

      >>> str(WesternTime(12, 44, 14.8))
      '12:44:14'

.. method:: western_time.cformat(format)

   Return a string representing the time, controlled by an explicit format
   string. The formatting directives are a subset of those accepted by
   :meth:`datetime.date.strftime`, and their meaning does not depend on the
   underlying C library (i.e. there are no platform variations). The table
   below lists the accepted formatting directives, all other character are not
   interpreted.

   +-----------+-------------------------------------------+-------+
   | Directive | Meaning                                   | Notes |
   +===========+===========================================+=======+
   | ``%H``    | Hour (24-hour clock) as a                 |       |
   |           | zero-padded decimal number [00, 23].      |       |
   +-----------+-------------------------------------------+-------+
   | ``%I``    | Hour (12-hour clock) as a                 |       |
   |           | zero-padded decimal number [00, 11].      |       |
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
   | ``%%``    | A literal ``'%'`` character.              |       |
   +-----------+-------------------------------------------+-------+

Notes:

(1)
   The ``%p`` directive returns a localized string in Standard C++.
   This is not true for :mod:`datetime2`, which only returns the
   English string.


.. _internet-time:

Internet time
^^^^^^^^^^^^^

The Internet Time (or beat time) is a decimal time concept introduced in 1998,
marketed by a large Swiss watch company, and divides the day in 1000 parts,
called "beats". A beat is equivalent to 1 minute and 26.4 seconds. A `Wikipedia
article <http://en.wikipedia.org/wiki/Swatch_Internet_Time>`_ well describes
the Internet time.

There are two constructors for the Internet time representation. The default
one is :

.. class:: InternetTime(beat)

   Return an object that represents the time in thousandths of a day. The
   ``beat`` argument is required and must be Python number; its value must
   be:

   * ``0 <= beat < 1000``

   If an argument is a Python number, a :exc:`TypeError` exception is raised.
   If an argument is outside its accepted range, a :exc:`ValueError`
   exception is raised.

The other constructor is:

.. class:: InternetTime.from_day_frac(day_frac)

   Return an object that represents the fraction of the day in thousandths
   of a day. The ``day_frac`` argument is required and must be a Python number,
   otherwise a :exc:`TypeError` exception is generated. Its value must be
   equal or greater than 0 and less than 1, otherwise a :exc:`ValueError`
   exception is raised. Note that the only accepted integer value is ``0``.

An :class:`InternetTime` object has one attribute:

.. attribute:: internet_time.beat

   This attribute is a read-only Python Fraction greater than or equal 0 and
   less than 1000.

and the following methods:

.. method:: internet_time.__str__()

   Return a string representing the moment of the day in beats, '@BBB' format.
   For example:

.. doctest:: internet

      >>> str(InternetTime(345.8))
      '@345'

.. method:: internet_time.to_day_frac()

   Returns a the moment of the day as a Python :class:`fractions.Fraction`. For
   example,
   ``InternetTime(125).to_day_fraction() == fractions.Fraction(1, 8)``.

.. method:: internet_time.cformat(format)

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
