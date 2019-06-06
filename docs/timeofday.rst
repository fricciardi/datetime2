.. _all-time-representations:

Time of day
===========

.. testsetup::

   from datetime2.western import WesternTime
   from datetime2.modern import InternetTime

This chapter lists the time representations classes available in the
:mod:`datetime2` package. They all conform to the rules listed
in :ref:`customization`. Note that these time representations do not
have any notion of time correction like daylight saving time or time
zone.

As such, they all have the six standard comparison operators: ``<``, ``>``, ``==``,
``>=``, ``<=``, and ``!=``, which return a meaningful result when comparing
calendar objects of the same type. When comparing a calendar object with an
object of a different type, the ``==`` and ``!=`` operators *always* consider
them to be unequal, while the ``<``, ``>``, ``>=`` and ``<=`` operators raise
a :exc:`TypeError` exception.

Similarly all classes implement the ``from_day_frac`` contructor and the
``to_day_frac`` method.

Description of the comparison operators and interface methods is then omitted
from the calendar class descriptions below.

.. TODO: if we will be keeping all time representations on a page, a ToC here will be useful

In the following we will call a rational number anything that can be
passed to the :class:`fractions.Fraction` constructor, i.e. an integer, a
float, another Fraction, a Decimal number or a string representing an integer,
a float or a fraction. In addition, it is also possible to use a 2-value tuple
with integer values. This tuple represents the numerator and denominator of a
fraction that will be passed to the :class:`fractions.Fraction` constructor.

.. _western-time:

Western time
^^^^^^^^^^^^

An instance of the :class:`WesternTime` class represents a moment of a day as
generally done in western countries, dividing each day in 24 hours, each hour
in 60 minutes and each minute in 60 seconds.

There are four constructors for a western time. The default one is:

.. class:: western.WesternTime(hour, minute, second, to_utc=None)

   Return an object that represents the moment of a day in hour, minute and
   second elapsed from midnight. This representation does not take into
   account the possibility of one or two additional seconds that sometimes
   are added in specific dates to compensate earth rotation. All arguments
   are required and must satisfy the following requirements:

   * ``hour`` must be an integer and ``0 <= month <= 23``
   * ``minute`` must be an integer and ``0 <= minute <= 59``
   * ``second`` must be a rational number and its value must be
     ``0 <= second < 60``
   * ``to_utc``, if present, must be a rational number and its value must be
     ``-24 <= to_utc <= 24``

   If an argument is not of the accepted type, a :exc:`TypeError` exception
   is raised. If an argument is outside its accepted range, a
   :exc:`ValueError` exception is raised.

   The ``to_utc`` argument, if present, makes the object aware and defines the
   number of hours that must be added to it to get UTC time.

The other three constructors are:

.. class:: WesternTime.in_hours(hour, to_utc=None)

   Return an object that represents the moment of the day specified in
   hours, possibly fractional, elapsed from midnight. The argument must be a
   rational number, otherwise a :exc:`TypeError` exception is raised. Its
   value must be greater or equal to 0 and less than 24, otherwise a
   :exc:`ValueError` exception is raised.

   The ``to_utc`` argument, if present, makes the object aware and defines the
   number of hours that must be added to it to get UTC time. It must be a
   rational number and its value must be ``-24 <= to_utc <= 24``

.. class:: WesternTime.in_minutes(minute, to_utc=None)

   Return an object that represents the moment of the day specified in
   minutes, possibly fractional, elapsed from midnight. The argument must be
   a rational number, otherwise a :exc:`TypeError` exception is raised. Its
   value must be greater or equal to 0 and less than 1440, otherwise a
   :exc:`ValueError` exception is raised.

   The ``to_utc`` argument, if present, makes the object aware and defines the
   number of hours that must be added to it to get UTC time. It must be a
   rational number and its value must be ``-24 <= to_utc <= 24``

.. class:: WesternTime.in_seconds(second, to_utc=None)

   Return an object that represents the moment of the day specified in
   seconds, possibly fractional, elapsed from midnight. The argument must be
   a rational number, otherwise a :exc:`TypeError` exception is raised. Its
   value must be greater or equal to 0 and less than 86400, otherwise a
   :exc:`ValueError` exception is raised.

   The ``to_utc`` argument, if present, makes the object aware and defines the
   number of hours that must be added to it to get UTC time. It must be a
   rational number and its value must be ``-24 <= to_utc <= 24``


A :class:`WesternTime` object has four attributes:

.. attribute:: western.hour

.. attribute:: western.minute

.. attribute:: western.second

   These attributes are read-only numbers. The first two are integers; the
   last one is a Python Fraction. The three attributes will respect the
   value requirements listed in the default constructor description.

.. attribute:: western.to_utc

   If this attribute is not ``None``, it is the number of hours that must be
   added the object's time to it to get UTC time


An instance of the :class:`WesternTime` class has the following methods:

.. method:: western.to_hours()

   Return a Python Fraction representing the moment of the day in hours.
   Thus the returned value will be equal or greater than 0, and less
   than 24.

.. method:: western.to_minutes()

   Return a Python Fraction representing the moment of the day in minutes.
   Thus the returned value will be equal or greater than 0, and less
   than 1440.

.. method:: western.to_seconds()

   Return a Python Fraction representing the moment of the day in seconds.
   Thus the returned value will be equal or greater than 0, and less
   than 86400.

.. method:: western.replace(hour, minute, second)

   Returns a new :class:`WesternTime` object with the same value, except
   for those parameters given new values by whichever keyword arguments are
   specified. All values are optional; if used, they must respect the
   requirements of the default constructor, otherwise a :exc:`TypeError` or
   :exc:`ValueError` exception is raised. For example:

.. doctest::

      >>> my_time = WesternTime(19, 6, 29)
      >>> print(my_time.replace(minute=38))
      19:38:29
      >>> my_time.replace(hour=24)
      Traceback (most recent call last):
        |
      ValueError: Hour must be between 0 and 23, while it is 24.

.. method:: western_time.__str__()

   Return a string representing the time with the 'HH:MM:SS' format. Any
   decimal will be truncated from the number of seconds. For example:

.. doctest::

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

The default constructor for Internet time is:

.. class:: InternetTime(beat)

   Return an object that represents the time in thousandths of a day. The
   ``beat`` argument is required and must be a rational number; its value must
   be equal or greater than 0 and less than 1000. If the argument is not a
   Python number, a :exc:`TypeError` exception is raised. If the argument
   is outside its accepted range, a :exc:`ValueError` exception is raised.

An :class:`InternetTime` object has one attribute:

.. attribute:: internet_time.beat

   This attribute is a read-only Python Fraction greater than or equal 0 and
   less than 1000.

and the following methods:

.. method:: internet_time.__str__()

   Return a string representing the moment of the day in beats, '@BBB' format.
   For example:

.. doctest::

      >>> str(InternetTime(345.25))
      '@345'

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
