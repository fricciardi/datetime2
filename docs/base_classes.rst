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


:class:`Date` instances have one attribute:

.. attribute:: Date.day_count

   An integer that represents the number of days between the given date and
   January 1\ :sup:`st`, year 1. This attribute is read-only: an
   :exc:`AttributeError` exception is raised when trying to change it.


:class:`Date` instances are immutable, so they can be used as dictionary keys.
When two aware instances indicate the same time, even if they have different
UTC offsets, the have the same hash. The hash function takes into consideration also that They can also be pickled and unpickled.
In boolean contexts, all :class:`Date` instances are considered to be true.


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
   attribute, if the operator is equality (``==``) or inequality (``!=``), the
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
   integer, a float or a fraction. The ``day_frac`` argument only can also be
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
UTC offset in aware instances is always taken into account. When both
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
   the ``day_frac`` attribute. UTC offset, if present, is represented as well:

.. doctest::

   >>> t1 = Time(4, 12)
   >>> print(t1)
   1/3 of a day
   >>> t2 = Time(3, 24, utcoffset="-4/24")
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
|                               | UTC offset, if present, is taken into        |
|                               | consideration. (5) (6) (7)                   |
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
   The *timedelta* object created when subtracting two :class:`Time`
   instances will always represent a fractional part of a day, with the
   ``days`` attribute value greater than -0.5 and less or equal to 0.5.
   ``time1`` and ``time2`` must have the same naivety; if they don't, a
   :exc:`ValueError` exception is raised. If they are aware, UTC offset of
   both instances will be taken into account to generate the result.

(5)
   All other comparison operators (``<=``, ``>``, ``>=``, ``==`` and ``!=``)
   behave similarly.

(6)
   If both objects to be compared are :class:`Time` instances, they must have
   the same naivety; if they don't, a :exc:`ValueError` exception is raised.

(7)
   When comparing a :class:`Time` object and an object of another class, if
   the latter has a ``day_frac`` attribute, ``NotImplemented`` is returned.
   This allows a Time-like instance to perform reflected comparison if it is
   the second operator. In this case, the second object is responsible for
   checking naivety. If the second object doesn't have a ``day_frac``
   attribute, if the operator is equality (``==``) or inequality (``!=``),
   the value returned is always :const:`False` and :const:`True` respectively.
   If the operator is one of the other four (``<=``, ``>``, ``>=`` or
   ``==``), a :exc:`TypeError` exception is raised.


.. note::
   Given the rules above it, if ``time1`` and ``time2`` are aware instances,
   ``time1 + (time2 - time1)`` compares equal to ``time2``, but it will have
   the same ``day_frac`` value only if the UTC offsets of ``time1`` and
   ``time2`` are equal.


:class:`TimeDelta` objects
--------------------------

An interval of time, expressed in fractional days.

There are two :class:`TimeDelta` constructors:

.. class:: TimeDelta(fractional_days)
.. class:: TimeDelta(numerator, denominator)

   Return an object that represents a time interval in fractional days, given
   in the ``fractional_days`` argument. This value will be greater than 1 to
   indicate an interval longer than 1 day.

   The ``fractional_days`` argument can be anything that can be passed to the
   :class:`fractions.Fraction` constructor, i.e. an integer, a float, another
   Fraction, a Decimal number or a string representing an integer, a float or
   a fraction. The argument can also be passed with two values that represent
   numerator and denominator of the fraction. A :exc:`TypeError` exception is
   raised if the type of any argument is not one of the accepted types. A
   :exc:`ZeroDivisionError` exception is raised if the denominator is 0.
   There are no limits on the value of ``fractional_days``.


The read-only attribute ``fractional_days`` stores the value, always as a
Python Fraction object. An attempt to directly set the values of this
attribute will raise an :exc:`AttributeError` exception. It is also possible
to access the integral and fractional parts of ``fractional_days`` with two
calculated attributes: ``int_part`` and ``frac_part``. If the time interval
is negative, both ``int_part`` and ``frac_part`` are negative. Given any
:class:`TimeDelta` instance ``td``, it is always:
``td.fractional_days == td.int_part() + td.frac_part()``

.. doctest::

   >>> td1 = Timedelta(16, 3)
   >>> td1.int_part
   5
   >>> td1.frac_part
   Fraction(1, 3)
   >>> td2 = TimeDelta(-7.625)
   >>> td2.int_part
   -7
   >>> td2.frac_part
   Fraction(-5, 8)


:class:`TimeDelta` objects support comparison, where *timedelta1* is
considered greater than *timedelta2* when the former represents a time
interval longer than the latter. When comparing a :class:`TimeDelta` object
and an object of another class, if the latter has the ``fractional_days``
attribute, ``NotImplemented`` is returned. This allows a TimeDelta-like
instance to perform reflected comparison if it is the second operator.


:class:`TimeDelta` instances are immutable, so they can be used as dictionary
keys. They can also be pickled and unpickled.

In boolean contexts, a :class:`TimeDelta` instance is considered to be true
if and only if it isn’t equal to ``TimeDelta(0)``.


Instance methods:

.. method:: TimeDelta.int()
.. method:: TimeDelta.frac()

   The first method return the same instance with only the integer part. The
   last method returns the same instance with only the fractional part. All
   methods return a negative value if the time interval is negative. In this
   way, given any :class:`TimeDelta` instance ``td``, it is always:
   ``td == td.int() + td.frac()``

.. doctest::

   >>> td1 = Timedelta(16, 3)
   >>> td1.int()
   TimeDelta(Fraction(5, 1))
   >>> td1.frac()
   TimeDelta(Fraction(1, 3))
   >>> td2 = TimeDelta(-7.625)
   >>> int(td2)
   TimeDelta(Fraction(-7, 1))
   >>> td2.frac()
   TimeDelta(Fraction(-5, 8))




.. method:: TimeDelta.is_integer()

   Returns ``True`` if the time interval is made of an integer number of days.

.. doctest::

   >>> td1 = Timedelta("3/4")
   >>> td1.is_integer()
   False
   >>> td2 = TimeDelta(-1)
   >>> td2.is_integer()
   True


.. method:: TimeDelta.__str__()

   Returns a string indicating the number of days and the remaining fraction
   of a day. Note that whilst in :class:`datetime.timedelta` the fractional
   part is always positive, in :class:`TimeDelta` the fractional part has the
   same sign of the integer part.

.. doctest::

   >>> td1 = Timedelta("1/12")
   >>> print(td1)
   1/12 of a day
   >>> td2 = TimeDelta(3)
   >>> print(td2)
   3 days
   >>> td3 = TimeDelta(11, -7)
   >>> print(td3)
   -1 day and -4/7 of a day


Available time interval representations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following table lists the available time representations interval and the
attributes by which they are reachable:

+----------------+----------------+------------------------------------------------+--------------------+
| Representation | Attribute      | Time representation class                      | Module             |
+================+================+================================================+====================+
| Western        | ``western``    | :ref:`WesternTimeDelta <western-timedelta>`    | datetime2.western  |
+----------------+----------------+------------------------------------------------+--------------------+

.. note::
   Not available in version 0.9.0.


Supported operations
^^^^^^^^^^^^^^^^^^^^

+----------------------------------------------+----------------------------------------------+
| Operation                                    | Result                                       |
+==============================================+==============================================+
| ``timedelta1 = timedelta2 + timedelta3``     | Sum of two time intervals.                   |
+----------------------------------------------+----------------------------------------------+
| ``timedelta1 = timedelta2 - timedelta3``     | Difference of two time intervals.            |
+----------------------------------------------+----------------------------------------------+
| ``timedelta1 = timedelta2 * number`` or      | Multiplication of a time interval by a       |
| ``timedelta1 = number * timedelta2``         | number. (1)                                  |
+----------------------------------------------+----------------------------------------------+
| ``timedelta1 = timedelta2 / number``         | Division of a time interval by a number. (1) |
+----------------------------------------------+----------------------------------------------+
| ``number = timedelta1 / timedelta2``         | Returns a fraction which is the ratio        |
|                                              | between the two time intervals.              |
+----------------------------------------------+----------------------------------------------+
| ``timedelta1 = timedelta2 // number``        | Floor division. Returns a time interval with |
|                                              | an integer number of days. If dividend and   |
|                                              | divisor are of different sign, the result is |
|                                              | negative and, if not integer, it is more     |
|                                              | negative than the true result.               |
+----------------------------------------------+----------------------------------------------+
| ``number = timedelta1 // timedelta2``        | Integer number of times ``timedelta2`` is    |
|                                              | contained in ``timedelta1``. If dividend and |
|                                              | divisor are of different sign, the result is |
|                                              | negative and, if not integer, it is more     |
|                                              | negative than the true result.               |
+----------------------------------------------+----------------------------------------------+
| ``timedelta1 = timedelta2 % divisor``        | Remainder of the division. This result       |
|                                              | always has the same sign of the divisor.     |
+----------------------------------------------+----------------------------------------------+
| ``divmod(timedelta, divisor)``               | Return a tuple made of the integral quotient |
|                                              | and remainder of ``timedelta`` divided by    |
|                                              | *dividend*. (2)                              |
+----------------------------------------------+----------------------------------------------+
| ``timedelta1 < timedelta2``                  | *timedelta1* is less than *timedelta2* when  |
|                                              | the former represents an interval shorter    |
|                                              | than the latter. (3)                         |
+----------------------------------------------+----------------------------------------------+


The table above does not include mixed type operations between ``TimeDelta``
and ``Date``, ``Time`` or ``DateTime``. For more information, see the
*Supported operations* chapter of each of these classes.

Class :class:`TimeDelta` also upports unary arithmetic operators ``+``, ``-``
and ``abs()``.


Notes:

(1)
   The number is first converted to a fraction, then multiplication or
   division takes place. As such, if *number* is a float, float to Fraction
   conversion error may happen, and result may not be exact.

(2)
   If dividend is a number, see note (1).

(3)
   All other comparison operators (``<=``, ``>``, ``>=``, ``==`` and ``!=``)
   behave similarly.


