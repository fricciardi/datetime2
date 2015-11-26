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
available (see to :ref:`Available date and time representations<list-of-calendars>`), but others can be
ref:`added at run time<interface>`.

Each representation can be reached via the attribute paradigm, e.g.:

.. doctest::

   >>> d = Date(765432)
   >>> print(d.gregorian)
   2096-09-05
   >>> print(d.iso)
   2096-W36-3
   >>> t = Time(0.25)
   >>> print(t.western)
   06:00:00
   >>> print(t.internet)
   @250

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
the same is true also for time. Indeed, all base classes have a very simple definition of day and time.

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
   Attributes of this class are: :attr:`day_frac`, :attr:`correction`.


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
   this class is: :attr:`days`.

:mod:`datetime2` class names use the CapitalizedWords convention required by :pep:`8`, so they
differ from the names of their similar counterparts in :mod:`datetime` module.



.. _list-of-calendars:

Currently (version |release|) the following calendars and time representation are available:

.. hlist::

  * :ref:`gregorian-calendar`
  * :ref:`iso-calendar`

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
   after January 1 of year 1 in the current Gregorian calendar. The argument
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

In addition, the following calendars are reachable via the listed access attributes:

+------------------+--------------+----------------------------------------------------------+-------------------+
| Access attribute | Calendar     | Calendar class                                           | Module            |
+==================+==============+==========================================================+===================+
| ``gregorian``    | Gregorian    | :ref:`GregorianCalendar <gregorian-calendar>`            | datetime2.western |
+------------------+--------------+----------------------------------------------------------+-------------------+
| ``iso``          | ISO          | :ref:`IsoCalendar <iso-calendar>`                        | datetime2.modern  |
+------------------+--------------+----------------------------------------------------------+-------------------+



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
time correction, e.g. due to time zone or daylight saving time. ``correction``.
This correction will be implemented in a future release, although it is still
included in all :class:`Time` signatures. If a :class:`Time` object has a
correction, it is said to be "aware" and is used to represent a precise moment
in time. An object without correction is said to be "naive", and ist
interpretation is left to the program that uses it.

There are two ways of creating a :class:`Time` instance:

.. class:: Time(day_frac, *, correction=None)

   Return an object that represent a moment in a day as a fraction of the
   whole day, given in the ``day_frac`` argument. If needed, a correction to
   this time, for whatever political, algorithmic or geographic need (e.g.
   time zone) can be given in hours and stored in the ``correction``
   argument, which must be explicitly named.

   In version 0.6, time correction is not implemented, although the
   constructor accepts it it.

   The ``day_frac`` argument can be anything that can be passed to the
   :class:`fractions.Fraction` constructor, i.e. an integer, a float,
   another Fraction, a Decimal number or a string representing an integer,
   a float or a fraction. It is also possible to use a 2-value tuple with
   integer values. This tuple represent the numerator and denominator of a
   fraction that will be passed to the :class:`fractions.Fraction`
   constructor. In any case, the resulting value for ``day_frac`` must be
   equal or greater than 0 and less than 1. A :exc:`TypeError` exception
   is raised if the argument type is not one of the accepted types. A
   :exc:`ZeroDivisionError` exception is raised if denominator is 0. A
   :exc:`ValueError` exception is raised in the argument value is outside
   the accepted range.

.. classmethod:: Time.now(correction = None)

   Return a :class:`Time` object that represents the current moment in the
   day. It is possible to add a correction to this time.

   In version 0.6, time correction is not implemented, although the
   constructor accepts it.

:class:`Time` instances are immutable, so they can be used as dictionary keys.
They can also be pickled and unpickled. In boolean contexts, all :class:`Time`
instances are considered to be true.

:class:`Time` instances have two attributes:

.. attribute:: Time.day_frac

   A  Python :class:`fractions.Fraction` that represents the part of the day
   after midnight. This attribute is read-only: an :exc:`AttributeError`
   exception is raised when trying to change it.

.. attribute:: Time.correction

   A correction to the time of the day, in order to indicate a location and/or
   daylight saving time. In version 0.6, correction is not implemented,
   although the class accepts it.

:class:`Time` has one instance method:

.. method:: time.__str__()

   Return the string ``<fraction> of a day``, where *fraction* is the value of the
   ``day_frac`` attribute.

   String representation of time correction will be defined in a future version.

In addition, the following time representation are reachable via the listed access attributes:

+----------------+----------------+------------------------------------------------+--------------------+
| Attribute      | Representation | Time representation class                      | Module             |
+================+================+================================================+====================+
| ``western``    | Western        | :ref:`WesternTime <western-time>`              | datetime2.western  |
+----------------+----------------+------------------------------------------------+--------------------+
| ``internet``   | Internet       | :ref:`InternetTime <internet-time>`            | datetime2.modern   |
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
|                               | (5) (6)                                      |
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
   both instances will be taken into account to generate the result.

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

