.. datetime2 documentation master file, created by
   sphinx-quickstart on Tue Jan 15 17:29:11 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

:mod:`datetime2` --- New date and time classes
==============================================

.. module:: datetime2
   :synopsis: Second generation date and time types
.. moduleauthor:: Francesco Ricciardi <francescor2010@yahoo.it>

.. testsetup::

   from datetime2 import Time
   from fractions import Fraction
   from datetime2 import Date

.. toctree::
   :hidden:

   calendars
   timeofday
   interface


Development of the :mod:`datetime2` module starts from the idea that a
day in history or in future is the same independently from the way it
is represented in different cultures. The module, indeed, detaches
operations on dates from the representation, chosing for the base class
a very simple definition. In the example below a :class:`Date` object
is created, and it is then printed in two different representations:

.. doctest::

   >>> d = Date(765432)
   >>> print(d.gregorian)
   2096-09-05
   >>> print(d.iso)
   2096-W36-3

The example shows how different representations are accessed as
attributes of the object. Dates are defined counting the days:
January 1\ :sup:`st`, year 1 is day 1, January 2\ :sup:`nd` is
day 2 and so on.

Similar thinking can be done for time:

.. doctest::

   >>> t = Time(0.25)
   >>> print(t.western)
   06:00:00
   >>> print(t.internet)
   @250

Also for time, object attributes allow to access different representations
(Internet time just divides a day in 1,000 parts, called "beats"). Time is
given as a fraction of the day (the example uses ``0.25`` as a perfect
fraction).

Using very simple definitions helps implementing precise operations on date
or time objects and makes it easy to convert between the different
representations. However, the simple defiitions create an additional effort
when creating an object, because conversion from "normal" dates to day count
or "normal" time to day fraction would be required.

Not surprisingly, the :mod:`datetime2` module makes it possbile to create
date or time objects in a more comprehensible way:

.. doctest::

   >>> d = Date.gregorian(2013, 4, 22)
   >>> print(d.gregorian)
   2013-04-22
   >>> print(d.iso)
   2013-W17-1
   >>> t = Time.western(16, 15, 0)
   >>> print(t.western)
   16:15:00
   >>> print(t.internet)
   @677

Note also that users are not restricted in accessing an object with the same
representation in which it was created.

Any available representation can be used to create a new object, or
to show the date or time with a precise representation. There are a
few representations already available, listed below.

Another feature of the :mod:`datetime2` module is the ability to add other
representations at run time. Representations do not consume memory
unless they are effectively used. This is especially important for
calendars, where many representation exists [#many]_ .

Currently (version |release|) the following calendars and time representation
are available.

Calendars:

.. hlist::

  * :ref:`gregorian-calendar`
  * :ref:`iso-calendar`

Time representation:

.. hlist::

  * :ref:`western-time`
  * :ref:`internet-time`



.. seealso::

   Module :mod:`datetime`
      Basic date and time types.

   Module :mod:`calendar`
      General calendar related functions.

   Module :mod:`time`
      Time access and conversions.


Base classes
============

The heart of the :mod:`datetime2` module is made of four base classes,
each having a very simple definition. All base classes implement
operations for date and time independently of the way they are created.

:mod:`datetime2` class names use the CapitalizedWords convention required by
:pep:`8`, so they differ from the names of their similar counterparts in
:mod:`datetime` module.



:class:`Date` Objects
---------------------

A :class:`Date` object represents a date in an idealized calendar, just
counting the days elapsed from Gregorian Dec 31\ :sup:`st` of year 0, i.e.
January 1\ :sup:`st` of year 1 is day number 1, January 2\ :sup:`nd` of year 1
is day number 2, and so on. This calendar ideally extends indefinitely in both
directions.

There are two ways of creating a :class:`Date` instance:

.. class:: Date(day_count)

   Return an object that represent a date which is ``day_count - 1`` days
   after January 1:sup:`st` of year 1 of the current Gregorian calendar.
   The argument  is required and must be an integer; there is no
   restriction on its numeric value. Using any other type of parameter, a
   :exc:`TypeError` exception is raised.

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
   Comparison between a :class:`Date` object and an object of another class
   raises a :exc:`TypeError` exception, unless the other object has a
   ``day_count`` attribute, in which case ``NotImplemented`` is returned. This
   allows a Date-like instance to implement reflected comparison, if wanted.
   When the comparison is equality or inequality operator, the value returned
   is always :const:`False` and :const:`True` respectively.


:class:`Time` Objects
---------------------

.. warning:: This version of the documentation already includes time correction.
             However, this part of the documentation is not stable and may change at any time.
             Additionally, no implementation nor test code has been written for it.

An indication of time, independent of any particular day, expressed as a
fraction of day. There might be an indication of time difference to UTC, e.g.
due to time zone or daylight saving time. Also this indication is expressed as
fraction of a day and represents the time to be added to local time to get UTC.
If there is this indication, the :class:`Time` object is said to be "aware" and
it is used to represent a precise moment (regardless of the day). An object
without indication is said to be "naive", and its interpretation is left to the
program that uses it.

There are four :class:`Time` constructors:

.. class:: Time(day_frac, *, time_to_utc=None)

   Return an object that represents a moment in a day as a fraction of the
   whole day, given in the ``day_frac`` argument. If needed, it is possible
   to assign to the instance an indication of the time to be added to get UTC,
   for whatever political, algorithmic or geographic need (e.g. time zone).
   This indication is given in the ``time_to_utc`` argument, which must be
   explicitly named.

   The ``day_frac`` and ``time_to_utc`` arguments can be anything that can
   be passed to the :class:`fractions.Fraction` constructor, i.e. an integer, a
   float, another Fraction, a Decimal number or a string representing an
   integer, a float or a fraction. In addition, it is also possible to use a
   2-value tuple with integer values. This tuple represents the numerator and
   denominator of a fraction that will be passed to the
   :class:`fractions.Fraction` constructor.

   The ``day_frac`` argument is stored in a read-only attribute with the same
   name. In addition to the types listed above, the ``time_to_utc`` argument
   can also be an object that has a ``time_to_utc`` method returning a
   :class:`fractions.Fraction` value.

   When a :class:`Time` instance is created giving an indication of time to
   UTC, one of the two following cases can happen:

   - ``time_to_utc`` is a fractional value, expressed in one of the
     possibilities above. This value is stored in the ``to_utc`` attribute. The
     ``to_utc_obj`` attribute is set to ``None``.

   - ``time_to_utc`` is an object that has a ``time_to_utc`` method. This
     method is called and its value is stored in the ``to_utc`` read-only
     attribute. The object itself is stored in the ``to_utc_obj`` attribute for
     further reference. Note that the value is read only once. This mechanism
     is such that e.g. a time zone object can be stored with the :class:`Time`
     instance.

   In any case, the resulting value for ``day_frac`` must be equal or greater
   than 0 and less than 1. The resulting value for ``to_utc`` must be greater
   than -1 and less than 1. A :exc:`ValueError` exception is raised if the
   resulting value are outside these ranges. A :exc:`TypeError` exception is
   raised if the argument type is not one of the accepted types or the tuple
   argument does not have two values. A :exc:`ZeroDivisionError` exception is
   raised if the second value (denominator) of a tuple argument is 0.

.. classmethod:: Time.now(time_to_utc = None)

   Return an aware :class:`Time` object that represents the current time.
   Without argument, the time represented in ``day_frac`` will be local
   standard time, ``to_utc`` will be set to the difference between UTC and
   local standard time, and ``to_utc_obj`` will be set to ``None``.

   If ``time_to_utc`` is given, the returned object will be the current time
   at the given time difference from UTC. ``time_to_utc`` will be treated as
   in the default constructor.

.. classmethod:: Time.localnow()

   Return a naive :class:`Time` object that represents the current local
   standard time.

.. classmethod:: Time.utcnow()

   Return a naive :class:`Time` object that represents the current standard
   UTC.


:class:`Time` instances are immutable, so they can be used as dictionary keys.
They can also be pickled (provided the ``to_utc_obj`` attribute is a pickable
object) and unpickled. In boolean contexts, all :class:`Time` instances are
considered to be true.

:class:`Time` instances have three read-only attributes: an
:exc:`AttributeError` exception is raised when trying to change any of them.

.. attribute:: Time.day_frac

   A Python :class:`fractions.Fraction` that represents the part of the day
   after midnight. The value is given as a fraction of a day.

.. attribute:: Time.to_utc

   If not ``None``, this attribute is a Python :class:`fractions.Fraction` that
   represents the fraction of a day that must be added to current time to get
   UTC. The value is given as a fraction of a day.

.. attribute:: Time.to_utc_obj

   This attribute is used to store the object passed as ``time_to_utc`` in any
   of the relevant constructors. This object does not contribute to the
   semantics of the :class:`Time` object.


:class:`Time` has two instance methods:

.. method:: time.__str__()

   Return the string ``<fraction> of a day``, where *fraction* is the value of
   the ``day_frac`` attribute. Time correction, if present, is represented as
   well:

.. doctest::

   >>> t1 = Time((4, 12))
   >>> print(t1)
   1/3 of a day
   >>> t2 = Time((3, 24), time_to_utc=(-4, 24))
   >>> print(t2)
   1/8 of a day, -1/6 of a day to UTC

.. method:: time.at_to_utc(new_time_to_utc)

   Applicable only to aware instances, return another :class:`Time` instance
   that identifies the same time, with the new indication of temporal distance
   from UTC passed in ``new_time_to_utc``. This argument is treated as in the
   default creator. If called on a naive instance, a :exc:`TypeError` exception
   is raised. Example:

.. doctest::

   >>> t1 = Time(0.25, time_to_utc=-0.5)
   >>> print(t1)
   1/4 of a day, -1/2 to UTC
   >>> t2 = t1.at_to_utc(0.25)
   >>> print(t2)
   0/1 of a day, 1/4 to UTC

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
   only the fractional part will remain. Naivety is maintained: if ``time1``
   has a correction, this will be copied to ``time2``, including, if populated,
   the ``to_utc_obj`` object.

(2)
   If *timedelta* is negative, ``time2`` will be before ``time1``.

(3)
   If *timedelta* is negative, ``time2`` will be after ``time1``.

(4)
   The *timedelta* object created when subtracting two :class:`Time` instances
   will always represent a fractional part of a day, either positive or
   negative. ``time1`` and ``time2`` must have the same naivety; if they don't,
   a :exc:`ValueError` exception is raised. If they are aware, correction of
   both instances will be taken into account to generate the result. Result
   will be more than -1 and less than 0 if ``time1`` is after than ``time2``,
   or between 0 and 1 if ``time1`` is before than ``time2``.

(5)
   All other comparison operators (``<=``, ``>``, ``>=``, ``==`` and ``!=``)
   behave similarly. Both operand must have the same naivety; if they don't, a
   :exc:`ValueError` exception is raised.

(6)
   Comparison between a :class:`Time` object and an object of another class
   raises a :exc:`TypeError` exception, unless the  :class:`Time` instances is
   naive and the other object has a ``day_frac`` attribute, or the
   :class:`Time` instances is aware and the other object has both ``day_frac``
   and ``to_utc`` attributes, in which case ``NotImplemented`` is returned.
   This allows a Time-like instance to perform reflected comparison if it is
   the second operator. When the comparison is equality or inequality
   operators, the value returned is always :const:`False` and :const:`True`
   respectively.


.. rubric:: Footnotes

.. [#many] Well, this should be read as "will exist", since current version
           (|release|) only has two of them.



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
