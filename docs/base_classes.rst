Base classes
============

.. testsetup::

   from datetime2 import Time
   from fractions import Fraction
   from datetime2 import Date


The heart of the :mod:`datetime2` module is made of four base classes,
each having a very simple definition. All base classes implement
operations for date and time independently of the way they are created.

:mod:`datetime2` class names use the CapitalizedWords convention required by
:pep:`8`, so they differ from the names of their similar counterparts in
:mod:`datetime` module.



:class:`Date` objects
---------------------

A :class:`Date` object represents a specific date. To do so it uses an
idealized calendar, in which it counts the days elapsed from Gregorian Dec
31\ :sup:`st` of year 0, i.e. January 1\ :sup:`st` of year 1 is day number 1,
January 2\ :sup:`nd` of year 1 is day number 2, and so on. This calendar
ideally extends indefinitely in both directions.

There are two ways of creating a :class:`Date` instance:

.. class:: Date(day_count)

   Return an object that represent a date which is ``day_count`` days
   after December 31\ :sup:`st` of year 0 in an ideal Gregorian calendar that
   has no limit. The argument ``day_count``  is required and it must be an
   integer, otherwise a :exc:`TypeError` exception is raised. There is no
   restriction on its numeric value.

.. classmethod:: Date.today()

   Return a :class:`Date` object that represents the current local date.

:class:`Date` instances are immutable, so they can be used as dictionary keys.
They can also be pickled and unpickled. In boolean contexts, all :class:`Date`
instances are considered to be true.

:class:`Date` instances have one attribute:

.. attribute:: Date.day_count

   An integer that represents the number of days between the given date and
   January 1\ :sup:`st`, year 1. This attribute is read-only: an
   :exc:`AttributeError` exception is raised when trying to change it.

:class:`Date` has one instance method:

.. method:: Date.__str__()

   Return ``R.D.`` followed by the day count. ``R.D.`` stands for Rata Die, the
   Latin for "fixed date".


Available calendars
^^^^^^^^^^^^^^^^^^^

The following table lists all available calendars and the attributes by which
they are reachable:

+--------------+------------------+----------------------------------------------------------+-------------------+
| Calendar     | Access attribute | Calendar class                                           | Module            |
+==============+==================+==========================================================+===================+
| Gregorian    | ``gregorian``    | :ref:`GregorianCalendar <gregorian-calendar>`            | datetime2.western |
+--------------+------------------+----------------------------------------------------------+-------------------+
| ISO          | ``iso``          | :ref:`IsoCalendar <iso-calendar>`                        | datetime2.modern  |
+--------------+------------------+----------------------------------------------------------+-------------------+



Supported operations
^^^^^^^^^^^^^^^^^^^^

+-------------------------------+----------------------------------------------+
| Operation                     | Result                                       |
+===============================+==============================================+
| ``date2 = date1 + timedelta`` | *date2* is ``timedelta`` days after          |
|                               | *date1*. Reverse addition (``timedelta +     |
|                               | date1``) is allowed. (1) (2)                 |
+-------------------------------+----------------------------------------------+
| ``date2 = date1 - timedelta`` | *date2* is ``timedelta`` days before         |
|                               | *date1*. (1) (3)                             |
+-------------------------------+----------------------------------------------+
| ``timedelta = date1 - date2`` | A :class:`TimeDelta` object is returned      |
|                               | representing the number of days              |
|                               | between *date1* and *date2*. (4)             |
+-------------------------------+----------------------------------------------+
| ``date1 < date2``             | *date1* is less than *date2* when it         |
|                               | represents a day earlier that that of        |
|                               | *date2*. (5) (6)                             |
+-------------------------------+----------------------------------------------+


Notes:

(1)
   A :exc:`ValueError` exception is raised if *timedelta* is not an integral
   number of days. *timedelta* object with non-integral number of days must be
   added or subtracted from :class:`DateTime` instances.

(2)
   If *timedelta* is negative, ``date2`` will be before ``date1``.

(3)
   If *timedelta* is negative, ``date2`` will be after ``date1``.

(4)
   The *timedelta* instance created when subtracting :class:`Date` instances
   will always have an integral number of days, positive if ``date1`` is later
   than ``date2``, negative otherwise.

(5)
   In other words, ``date1 < date2`` if and only if ``date1.day_count <
   date2.day_count``. All other comparison operators (``<=``, ``>``, ``>=``,
   ``==`` and ``!=``) behave similarly.

(6)
   When comparing a :class:`Date` object and an object of another class, if
   the latter has a ``day_count`` attribute, ``NotImplemented`` is returned.
   This allows a Date-like instance to perform reflected comparison if it is
   the second operator. When the second object doesn't have a ``day_count``
   attribute, if the operator is equality(``==``) or inequality(``!=``), the
   value returned is always :const:`False` and :const:`True` respectively.
   If the operator is one of the other four (``<=``, ``>``, ``>=`` or
   ``==``), a :exc:`TypeError` exception is raised.




:class:`Time` objects
---------------------

An indication of time, independent of any particular day, expressed as a
fraction of day. There might be an indication of time difference from UTC,
e.g. due to time zone or daylight saving time. This time difference is
expressed as fraction of a day and represents the time to be added to local
time to get UTC. If there is this indication, the :class:`Time` object is
said to be "aware" and it is used to represent a precise moment (regardless
of the day). An object without indication is said to be "naive", and its
interpretation is left to the program that uses it.

There are five :class:`Time` constructors:

.. class:: Time(day_frac, *, utcoffset=None)
.. class:: Time(numerator, denominator, *, utcoffset=None)

   Return an object that represents a moment in a day as a fraction of the
   whole day, given in the ``day_frac`` argument. If needed, it is possible
   to assign to the instance an indication of the time offset from UTC, for
   whatever political, algorithmic or geographic need (e.g. time zone), using
   the ``utcoffset`` argument, which must be explicitly named.

   The ``day_frac`` and ``utcoffset`` arguments can be anything that can
   be passed to the :class:`fractions.Fraction` constructor, i.e. an integer, a
   float, another Fraction, a Decimal number or a string representing an
   integer, a float or a fraction. The ``day_frac`` arguments only can also be
   passed with two values that represent numerator and denominator of the
   fraction. A :exc:`TypeError` exception is raised if the type of any
   argument is not one of the accepted types. A :exc:`ZeroDivisionError`
   exception is raised if the denominator is 0.

   The value for ``day_frac`` must be equal or greater than 0 and less than 1.
   The value for ``utcoffset`` in aware objects must be equal or greater than
   -1 and less or equal to 1. A :exc:`ValueError` exception is raised if
   values are outside these ranges.

.. classmethod:: Time.now(utcoffset=None)

   Return an aware :class:`Time` object that represents the current time.
   Without argument, the time represented in ``day_frac`` will be local
   standard time and ``utcoffset`` will be set to the difference between
   local standard time and UTC.

   If ``utcoffset`` is given, the returned object will be the current time
   at the given time difference from UTC. ``utcoffset`` follows the same
   requirements of the default constructor.

.. classmethod:: Time.localnow()

   Return a naive :class:`Time` object that represents the current local
   standard time.

.. classmethod:: Time.utcnow()

   Return a naive :class:`Time` object that represents the current standard
   UTC.

Two read-only attributes store the ``day_frac`` and ``utcoffset`` arguments.
The former is always a Fraction object, the latter is either a Fraction
object or ``None``, for naive time. An attempt to directly set the values of
these two attributes will raise an :exc:`AttributeError` exception.

:class:`Time` objects support comparison, where *time1* is considered less
than *time2* when the former represents a moment earlier than the latter.
Time correction in aware instances is always taken into account. When both
objects are :class:`Time` instances they must have the same naivety,
otherwise :exc:`TypeError` is raised if an order comparison is attempted,
while for equality comparisons, naive instances are never equal to aware
instances.

When comparing a :class:`Time` object and an object of another class, if the
latter has the ``day_frac``  and ``utcoffset`` attributes, ``NotImplemented``
is returned. This allows a Time-like instance to perform reflected comparison
if it is the second operator. In this case, the second object is responsible
for checking naivety.

:class:`Time` instances are immutable, so they can be used as dictionary keys.
They can also be pickled and unpickled. In boolean contexts, all :class:`Time`
instances are considered to be true.

Instance method:

.. method:: Time.__str__()

   Return the string ``<fraction> of a day``, where *fraction* is the value of
   the ``day_frac`` attribute. Time correction, if present, is represented as
   well:

.. doctest::

   >>> t1 = Time(4, 12)
   >>> print(t1)
   1/3 of a day
   >>> t2 = Time(3, 24, utcoffset=(-4, 24))
   >>> print(t2)
   1/8 of a day, -1/6 of a day from UTC


Available time representations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following table lists all available time representations and the attributes
by which they are reachable:

+----------------+----------------+------------------------------------------------+--------------------+
| Representation | Attribute      | Time representation class                      | Module             |
+================+================+================================================+====================+
| Western        | ``western``    | :ref:`WesternTime <western-time>`              | datetime2.western  |
+----------------+----------------+------------------------------------------------+--------------------+
| Internet       | ``internet``   | :ref:`InternetTime <internet-time>`            | datetime2.modern   |
+----------------+----------------+------------------------------------------------+--------------------+

Supported operations
^^^^^^^^^^^^^^^^^^^^

+-------------------------------+----------------------------------------------+
| Operation                     | Result                                       |
+===============================+==============================================+
| ``time2 = time1 + timedelta`` | *time2* is ``timedelta`` time after          |
|                               | *time1*. Reverse addition (``timedelta +     |
|                               | time1``) is allowed. (1) (2)                 |
+-------------------------------+----------------------------------------------+
| ``time2 = time1 - timedelta`` | *time2* is ``timedelta`` time before         |
|                               | *time1*. (1) (3)                             |
+-------------------------------+----------------------------------------------+
| ``timedelta = time1 - time2`` | A :class:`TimeDelta` object is returned      |
|                               | representing the day fraction                |
|                               | between *time1* and *time2*. (4)             |
+-------------------------------+----------------------------------------------+
| ``time1 < time2``             | *time1* is less than *time2* when the former |
|                               | represents a moment earlier than the latter. |
|                               | Time correction, if present, is taken into   |
|                               | consideration. (5) (6)                       |
+-------------------------------+----------------------------------------------+


Notes:

(1)
   The result of this operation will always be a valid :class:`Time` instance.
   If overflow or underflow occur, the full day part will be truncated so that
   only the fractional part will remain. Naivety is preserved: if ``time1``
   has a UTC offset, this will be copied to ``time2``.

(2)
   If *timedelta* is negative, ``time2`` will be before ``time1``.

(3)
   If *timedelta* is negative, ``time2`` will be after ``time1``.

(4)
   The *timedelta* object created when subtracting two :class:`Time` instances
   will always represent a fractional part of a day, either positive or
   negative. ``time1`` and ``time2`` must have the same naivety; if they don't,
   a :exc:`ValueError` exception is raised. If they are aware, UTC offset of
   both instances will be taken into account to generate the result. Result
   will always be equal or greater to -0.5 and less than 0.5.

(5)
   All other comparison operators (``<=``, ``>``, ``>=``, ``==`` and ``!=``)
   behave similarly.

(6)
   If both objects to be compared are :class:`Time` instances, they must have
   the same naivety; if they don't, a :exc:`ValueError` exception is raised.
   When comparing a :class:`Time` object and an object of another class, if
   the latter has a ``day_frac`` attribute, ``NotImplemented`` is returned.
   This allows a Time-like instance to perform reflected comparison if it is
   the second operator. In this case, the second object is responsible for
   checking naivety. When the second object doesn't have a ``day_frac``
   attribute, if the operator is equality(``==``) or inequality(``!=``), the
   value returned is always :const:`False` and :const:`True` respectively.
   If the operator is one of the other four (``<=``, ``>``, ``>=`` or
   ``==``), a :exc:`TypeError` exception is raised.


.. note::
   Given the rules above it, if ``time1`` and ``time2`` are aware instances,
   ``time1 + (time2 - time1)`` compares equal to ``time2``, but it will have
   the same ``day_frac`` value only if the UTC offsets of ``time1`` and
   ``time2``are equal.