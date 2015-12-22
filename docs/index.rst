:mod:`datetime2` --- New date and time classes
==============================================

.. module:: datetime2
   :synopsis: Second generation date and time types
.. moduleauthor:: Francesco Ricciardi <francescor2010@yahoo.it>

.. testsetup::

   from datetime2 import Time
   from fractions import Fraction
   from datetime2 import Date


The :mod:`datetime2` module is intended to be a replacement of the :mod:`datetime` module. Its most visible feature is
the ability to have multiple representation of the same date or time object. There are a few representations already
available (see :ref:`Available date and time representations<list-of-calendars>`), but others can be
ref:`added at run time<interface>`.

Each representation can be reached via the attribute paradigm, e.g.:

.. doctest::

   >>> d = Date(765432)
   >>> print(d.gregorian)
   2096-09-05
   >>> print(d.iso)
   2096-W36-3
   >>> t1 = Time(0.25)
   >>> print(t1.western)
   06:00:00
   >>> print(t1.internet)
   @250
   >>> t2 = Time(0.75, time_to_utc=-Fraction(1, 6))
   >>> print(t2.western)
   18:00:00 -04
   >>> print(t2.internet)
   @583

Representations do not consume memory unless they are effectively used. This is
especially important for calendars, where many representation exists [#many]_ .

Some long term objectives of the :mod:`datetime2` module are:
 * internationalization;
 * implementation of the part of the Unicode Locale Database concerned with dates and times;
 * interface with other Python modules or inclusion of their functionalities in submodules.


.. toctree::
   :hidden:

   interface
   calendars
   timeofday

Overview
--------

The driving idea in the :mod:`datetime2` is to detach operations on date or time from their representation
in different cultures. After all, a day in history, or in future, is the same independently from the way it is represented, and
the same is true also for time. Indeed, the four base classes of :mod:`datetime2` have a very simple definition of day and time.

This is a brief description of these four classes:

.. class:: Date
   :noindex:

   An idealized date, with no notion of time or time zone. A date is defined
   counting the number of days elapsed from what would have been January 1st
   of year 1 on the Gregorian calendar. The only attribute of this class is:
   :attr:`day_count`.


.. class:: Time
   :noindex:

   An indication of time, independent of any particular day. There might be a
   time correction, e.g. due to time zone or daylight saving time. Time and correction
   are stored as fraction of a day, using a Python :class:`fractions.Fraction`.
   Attributes of this class are: :attr:`day_frac`, :attr:`time_to_utc`.


.. class:: DateTime
   :noindex:

   A precise moment in time. There might be a time correction, e.g. due to time zone or daylight saving time. This
   class has not been implemented yet, but will interface with calendars and time representations used by the two
   classes above.



.. class:: TimeDelta
   :noindex:

   A duration expressing the difference between two :class:`Date`,
   :class:`Time`, or :class:`DateTime` instances. This difference is stored
   in a single Python :class:`fractions.Fraction`. The only attribute of
   this class is: :attr:`days`. The current implementation of this class is just a stub.

:mod:`datetime2` class names use the CapitalizedWords convention required by :pep:`8`, so they
differ from the names of their similar counterparts in :mod:`datetime` module.



.. _list-of-calendars:

Currently (version |release|) the following calendars and time representation are available.

Calendars:

.. hlist::

  * :ref:`gregorian-calendar`
  * :ref:`iso-calendar`

Tiem representation:

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


:class:`Date` Objects
---------------------

A :class:`Date` object represents a date in an idealized calendar, just
counting the days elapsed from Gregorian Dec 31\ :sup:`st` of year 0, i.e.
January 1\ :sup:`st` of year 1 is day number 1, January 2\ :sup:`nd` of year 1
is day number 2, and so on. This calendar ideally extends indefinitely in both
directions. A :class:`Date` object is printed as ``R.D.`` followed by the day
count. ``R.D.`` stands for Rata Die, the Latin for "fixed date".

There are two ways of creating a :class:`Date` instance:

.. class:: Date(day_count)

   Return an object that represent a date which is ``day_count - 1`` days
   after January 1 of year 1 of the current Gregorian calendar. The argument
   is required and must be an integer. There is no restriction on its
   numeric value.

.. classmethod:: Date.today()

   Return a :class:`Date` object that represents the current local date.

:class:`Date` instances are immutable, so they can be used as dictionary keys.
They can also be pickled and unpickled. In boolean contexts, all :class:`Date`
instances are considered to be true.

:class:`Date` instances have one attribute:

.. attribute:: Date.day_count

   An integer that represents the number of days between the given date and January
   1\ :sup:`st`, year 1. This attribute is read-only: an :exc:`AttributeError` exception is raised
   when trying to change it.

:class:`Date` has one instance method:

.. method:: Date.__str__()

   Return ``R.D.`` followed by the day count. ``R.D.`` stands for Rata Die, the Latin
   for "fixed date".

The following table lists all available calendars and the attributes by which they are reachable:

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
|                               | *date1*. (1) (2)                             |
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
   A :exc:`ValueError` exception is raised if *timedelta* is not an integral number of days.
   *timedelta* object with non-integral number of days must be added or subtracted from
   :class:`DateTime` instances.

(2)
   If *timedelta* is negative, ``date2`` will be before ``date1``.

(3)
   If *timedelta* is negative, ``date2`` will be after ``date1``.

(4)
   A *timedelta* instance with with an integral number of dyas is always created when
   subtracting :class:`Date` instances.

(5)
   In other words, ``date1 < date2`` if and only if ``date1.day_count < date2.day_count``.
   All other comparison operators (``<=``, ``>``, ``>=``, ``==`` and ``!=``)
   behave similarly.
   
(6)
   Comparison between a :class:`Date` object and an object of another class
   return a :exc:`NotImplemented` exception, except for the equality and inequality
   operators, which respectively return *False* and *True*.


:class:`Time` Objects
---------------------

An indication of time, independent of any particular day. There might be a
time correction, e.g. due to time zone or daylight saving time. This
correction is expressed in fraction of a day and represent the time to be
added to local time to get UTC. If there is a correction, the :class:`Time`
object is said to be "aware" and it is used to represent a precise moment in
time. An object without correction is said to be "naive", and its
interpretation is left to the program that uses it.

There are two ways of creating a :class:`Time` instance:

.. class:: Time(day_frac, *, time_to_utc=None)

   Return an object that represent a moment in a day as a fraction of the
   whole day, given in the ``day_frac`` argument. If needed, a correction to
   this time, for whatever political, algorithmic or geographic need (e.g.
   time zone) can be given (again as a fraction of a day) and stored in the
   ``time_to_utc`` argument, which must be explicitly named.

   The ``day_frac`` and ``time_to_utc`` arguments can be anything that can
   be passed to the :class:`fractions.Fraction` constructor, i.e. an
   integer, a float, another Fraction, a Decimal number or a string
   representing an integer, a float or a fraction. It is also possible to
   use a 2-value tuple with integer values. This tuple represents the
   numerator and denominator of a fraction that will be passed to the
   :class:`fractions.Fraction` constructor. ``time_to_utc`` can also be
   any object that has a ``time_to_utc`` method that returns a
   :class:`fractions.Fraction` representing the correction.

   The resulting value for ``day_frac`` must be equal or greater than 0 and
   less than 1. The resulting value for ``time_to_utc`` must be greater than
   -1 and less than 1. A :exc:`ValueError` exception is raised if the
   resulting value is outside these ranges. A :exc:`TypeError` exception
   is raised if the argument type is not one of the accepted types or the
   tuple argument does not have two values. A :exc:`ZeroDivisionError`
   exception is raised if denominator is 0.

.. classmethod:: Time.now(time_to_utc = None)

   Return a :class:`Time` object that represents the current moment in the
   day. It is possible to add a correction to this time.

   See default creator for accepted values of the ``time_to_utc`` argument.

:class:`Time` instances are immutable, so they can be used as dictionary keys.
They can also be pickled and unpickled. In boolean contexts, all :class:`Time`
instances are considered to be true.

:class:`Time` instances have two attributes:

.. attribute:: Time.day_frac

   A  Python :class:`fractions.Fraction` that represents the part of the day
   after midnight. This attribute is read-only: an :exc:`AttributeError`
   exception is raised when trying to change it.

.. attribute:: Time.time_to_utc

   If not ``None``, this attribute is a Python :class:`fractions.Fraction`
   that represents the fraction of a day that must be added to current time
   to get UTC. This attribute is read-only: an :exc:`AttributeError`
   exception is raised when trying to change it.

:class:`Time` has two instance methods:

.. method:: time.__str__()

   Return the string ``<fraction> of a day``, where *fraction* is the value of the
   ``day_frac`` attribute. Time correction, if present, is represented as well:

.. doctest::

   >>> t1 = Time((4, 12))
   >>> print(t1)
   1/3 of a day
   >>> t2 = Time((3, 24), time_to_utc=(-4, 24))
   >>> print(t2)
   1/8 of a day, -1/6 of a day to UTC

.. method:: time.move(new_time_to_utc)

   Applicable only to aware instances, return another :class:`Time` instance
   that identifies the same time but has the new correction
   ``new_time_to_utc``. If called on a naive instance, a :exc:`TypeError`
   exception is raised. Example:

.. doctest::

   >>> t1 = Time(0.25, time_to_utc=-0.5)
   >>> print(t1)
   1/4 of a day, -1/2 to UTC
   >>> t2 = t1.move(0.25)
   >>> print(t2)
   0/1 of a day, 1/4 to UTC

The following table lists all available time representations and the attributes by which they are reachable:

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
|                               | *time1*. (1) (2)                             |
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
   only the fractional part will remain. If ``time1`` has a correction, this
   will be copied to ``time2``, so naivety is maintained.

(2)
   If *timedelta* is negative, ``time2`` will be before ``time1``.

(3)
   If *timedelta* is negative, ``time2`` will be after ``time1``.

(4)
   The *timedelta* object created when subtracting two :class:`Time` instances
   will always represent a fractional part of a day, either positive or
   negative. ``time1`` and ``time2`` must have the same naivety; if they don't, a
   :exc:`ValueError` exception is raised. If they are aware, correction of
   both instances will be taken into account to generate the result. Result
   will always be more than -1 and less than 1.

(5)
   All other comparison operators (``<=``, ``>``, ``>=``, ``==`` and ``!=``)
   behave similarly. Both operand must have the same naivety; if they don't, a
   :exc:`ValueError` exception is raised.

(6)
   Comparison between a :class:`Time` object and an object of another class
   return a :exc:`NotImplemented` exception, except for the equality and inequality
   operators, which respectively return *False* and *True*.


.. rubric:: Footnotes

.. [#many] Well, this should be read as "will exist", since current version(|release|) only has two of them.

