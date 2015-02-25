:mod:`datetime2` --- New date and time classes
==============================================

.. module:: datetime2
   :synopsis: Date and time types with broader calendar coverage.
.. moduleauthor:: Francesco Ricciardi <francescor2010@yahoo.it>

.. testsetup:: test_date

   from datetime2 import Date

.. testsetup:: test_time

   from datetime2 import Time

The :mod:`datetime2` module provides classes to manipulate date and time
like the :mod:`datetime` module does, with these objectives in mind:

* decoupling between operations on date and time objects and their
  representation;
* access to different calendars, for input parsing and output formatting;
* access to different time representations, also for input and output;
* ability to dynamically register new formatting classes;
* internationalization;
* implementation of the part of the Unicode Locale Database concerned with
  dates and times;
* interface with other Python modules or inclusion of their
  functionalities in submodules.

These objectives are very long term ones, which I am setting because it is
important to establish a direction for the project. Do not expect to see them
implemented in initial versions of the module, even if you will be able to see
traces of them early.

.. toctree::
   :hidden:

   calendars
   timeofday

Overview
--------

The driving idea in the :mod:`datetime2`is to detach how date or time are
handled from the representation in different cultures. Indeed, a day in
history is the same independently from the way it is represented, and
the same is true also for time, even if much fewer time representation
systems are used.

The four core classes implemented in the :mod:`datetime2` module
(:class:`Date`, :class:`Time`, :class:`DateTime`, :class:`TimeDelta`) have
close resemblance to those of the original :mod:`datetime` module. By
themselves, they provide a generic service, not bound to any particular
calendar or time representation.


============================
These  class names use the CapitalizedWords
convention, required by :pep:`8`, not used in the old module.  The :class:`DateTime` classe will be implemented
in a future version. The :class:`TimeDelta` class is currently a stub.

.. class:: Date
   :noindex:

   An idealized date, with no notion of time or time zone. A date is stored
   counting the number of days elapsed from what would have been January 1st
   of year 1 on the Gregorian calendar. The only attribute of this class is:
   :attr:`day_count`.


.. class:: Time
   :noindex:

   An indication of time, independent of any particular day. There might be a
   time correction, e.g. due to time zone or daylight saving time. Time is
   stored as a fraction of a day, using a Python :class:`fractions.Fraction`.
   Attributes of this class are: :attr:`day_frac`, :attr:`correction`.


.. class:: TimeDelta
   :noindex:

   A duration expressing the difference between two :class:`Date`,
   :class:`Time`, or :class:`DateTime` instances. This difference is stored
   in a single Python :class:`fractions.Fraction`. The only attribute of
   this class is: :attr:`days`.


These core classes are of little use as defined above. Indeed,
:mod:`datetime2` is able to interface with different calendars and time
representations. The syntax to access these calendars and representations is
through the attribute paradigm. E.g.: the core classes and their instances will
be able to access class methods, constructors and instances of the specific
calendar as class or instance attributes. For example:

.. doctest:: test_date

  >>> d = Date.gregorian(2012, 2, 27)
  >>> print(d)
  R.D. 734560
  >>> print(d.gregorian)
  2012-02-27
  >>> d.iso.week
  9

.. _list-of-calendars :

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
is day number 2, and so on. This calendar ideally extends indefinitely.

There are two ways of creating a :class:`Date` instance:

.. class:: Date(day_count)

   Return an object that represent a date which is ``day_count - 1`` days
   after January 1 of year 1 in the current Gregorian calendar. The argument
   is required and must be an integer or an object that has the
   ``to_rata_die`` method, and this method returns an integer. There is no
   restriction on its numeric value.


.. classmethod:: Date.today()

   Return a :class:`Date` object that represents the current local date.

:class:`Date` instances are immutable, so they can be used as dictionary keys.
They can also be pickled and unpickled. In boolean contexts, all :class:`Date`
instances are considered to be true. :class:`Date` instances have one attribute:

.. attribute:: date.day_count

   The number of days between the given date and January 1\ :sup:`st`, year 1.
   This attribute is read-only: an :exc:`AttributeError` exception is raised
   when trying to change it.


Supported operations
^^^^^^^^^^^^^^^^^^^^

+-------------------------------+----------------------------------------------+
| Operation                     | Result                                       |
+===============================+==============================================+
| ``date2 = date1 + timedelta`` | *date2* is ``timedelta`` days after          |
|                               | *date1*. (1)                                 |
+-------------------------------+----------------------------------------------+
| ``date2 = date1 - timedelta`` | *date2* is ``timedelta`` days before         |
|                               | *date1*. (1)                                 |
+-------------------------------+----------------------------------------------+
| ``timedelta = date1 - date2`` | A :class:`TimeDelta` object is returned      |
|                               | representing the number of days              |
|                               | between *date1* and *date2*. (2)             |
+-------------------------------+----------------------------------------------+
| ``date1 < date2``             | *date1* is less than *date2* when its day    |
|                               | count is less that that of *date2*. (3) (4)  |
+-------------------------------+----------------------------------------------+

TODO: When Timedelta will be defined properly, use a better definition that
"integer" in note 1 and 2

Notes:

(1)
   A :exc:`ValueError` exception is raised if *timedelta* is not integer. If you
   deal with non-integer date differences, you need to use :class:`DateTime` 
   instances. If *timedelta* is negative, ``date2`` will be before ``date1``.

(2)
   An integer *timedelta* is always created when subtracting :class:`Date`
   instances.

(3)
   In other words, ``date1 < date2`` if and only if ``date1.day_count <
   date2.day_count``. All other comparison operators behave similarly.
   
(4)
   Comparison between a :class:`Date` object and an object of another class
   return a :exc:`NotImplemented` exception, except for the equality and inequality
   operators, which respectively return *False* and *True*.


There's one instance method:

.. method:: date.__str__()

   Return ``R.D.`` followed by the day count. ``R.D.`` stands for Rata Die, the Latin
   for "fixed date".


Calendar interface
^^^^^^^^^^^^^^^^^^

An instance of the :class:`Date` class, as described above, is of little use
as it is: even if it stands out for its simplicity, rata die is not a common
way of representing dates in the real world. Indeed, the :mod:`datetime2`
module provides access to many calendars, via the attribute paradigm.


For example, the ``gregorian`` attribute allows to see the date instance as an
instance of the :class:`GregorianCalendar` class, as follows:

.. doctest:: test_date

   >>> d1 = Date.gregorian(2013, 4, 18)
   >>> d1
   datetime2.Date(734976)
   >>> d2 = Date(1)
   >>> d2.gregorian
   calendars.gregorian.GregorianCalendarInDate(1, 1, 1)
   >>> d2.gregorian.month
   1

Above there are examples of two kinds of accesses: first of all, we can
construct a :class:`Date` instance using the default constructor of a calendar
(below there are examples of using non-default constructors). Note that the
``Date.gregorian`` constructor returns a :class:`Date` instance, not a
:class:`GregorianCalendar` one.

Additionally, we can see a :class:`Date` instance, whichever way it was
constructed, as an instance of a Gregorian calendar. As such, it is possible
to access all attributes and methods of the calendar:

.. doctest:: test_date

   >>> d = Date(734977)
   >>> str(d.gregorian)
   '2013-04-19'
   >>> d.gregorian.weekday()
   5

Special attention is given to calendar methods that normally return a new
calendar instance: these methods, when accessed through a :class:`Date`
attribute, return an instance of :class:`Date` and not one of the calendar.
E.g.:

.. doctest:: test_date

   >>> d1 = Date(734977)
   >>> d2 = d1.gregorian.replace(month = 6)
   >>> d2
   datetime2.Date(735038)
   >>> str(d2.gregorian)
   '2013-06-19'

When accessed through the attribute, also other calendar constructors, return
a date:

.. doctest:: test_date

   >>> d = Date.gregorian.year_day(2012, 366)
   >>> d
   datetime2.Date(734868)
   >>> d.gregorian
   calendars.gregorian.GregorianCalendarInDate(2012, 12, 31)

As expected, calendar static methods are unchanged:

.. doctest:: test_date

   >>> Date.gregorian.is_leap_year(2012)
   True

The real power of this paradigm is when different calendars are used. Indeed a
:class:`Date` instance is not limited to handling a single calendar: using the
corresponding attributes, all calendars are reachable:

.. doctest:: test_date

   >>> d = Date.gregorian(2013, 4, 22)
   >>> d.iso.week
   17

The following table lists the available calendars:

+--------------+----------------------------------------------------------+------------------+
| Calendar     | Calendar class                                           | Attribute        |
+==============+==========================================================+==================+
| Gregorian    | :ref:`GregorianCalendar <gregorian-calendar>`            | ``gregorian``    |
+--------------+----------------------------------------------------------+------------------+
| ISO          | :ref:`IsoCalendar <iso-calendar>`                        | ``iso``          |
+--------------+----------------------------------------------------------+------------------+

.. _custom-calendars:

Custom calendars
""""""""""""""""

Not only the :mod:`datetime2` module has a variety of calendars, but it is also
possible to add custom calendars to class :class:`Date`, by calling the
following function:

.. function:: register_new_calendar(calendar_attribute, CalendarClass)

   Register the class ``CalendarClass`` to be used as a calendar in the
   :mod:`datetime2` module, accessing it with the ``calendar_attribute``
   attribute. If the ``calendar_attribute`` attribute is already defined, an
   :exc:`AttributeError` exception is generated. If ``calendar_attribute`` is
   not a valid identifier, a :exc:`ValueError` exception is generated.

   The ``CalendarClass`` must have the non-default constructor
   ``from_rata_die`` and the method ``to_rata_die`` that convert the calendar
   to and from the rata die count. A :exc:`TypeError` exception is generated if
   either method does not exist. Additionally, for the import mechanism to
   work, all non-default constructors and methods that return a calendar
   instance (e.g. :ref:`gregorian.replace <gregorian-replace>`) should
   construct objects of the calendar class just calling the calendar class
   (like in ``GregorianCalendar(1, 2, 3)``).

As a very simple example, let's define a new calendar that defines each day by
indicating the week number and the week day, counting the week of January
1\ :sup:`st` of year 1 as week 1 and so on. In addition, this new calendar has
a constructor using also thousands of weeks:

.. doctest:: test_date

   >>> class SimpleWeekCalendar():
   ...     def __init__(self, week, day):
   ...         self.week = week
   ...         self.day = day
   ...     @classmethod
   ...     def from_rata_die(cls, rata_die):
   ...         return cls((rata_die - 1) // 7 + 1, (rata_die - 1) % 7 + 1)
   ...     def to_rata_die(self):
   ...         return 7 * (self.week - 1) + self.day
   ...     def __repr__(self):
   ...         return '{}({}, {})'.format(self.__class__.__name__,self.week, self.day)
   ...     @classmethod
   ...     def with_thousands(cls, thousands, week, day):
   ...         return cls(1000 * thousands + week, day)
   ...
   >>> Date.register_new_calendar('week_count', SimpleWeekCalendar)
   >>> d1 = Date.week_count(1, 1)
   >>> d1.gregorian
   calendars.gregorian.GregorianCalendarInDate(1, 1, 1)
   >>> d2 = Date.gregorian(2013, 4, 26)
   >>> d2.week_count
   SimpleWeekCalendarInDate(104998, 5)

To avoid computing all calendars at initialization time, calendar attributes
in a :class:`Date` instance are evaluated when retrieved for the first time;
they are then stored as attributes of the instance.

To obtain this, the standard attribute lookup mechanisms is exploited:

* if the instance has the attribute, this is retrieved normally; however, this
  is not an instance of the original calendar, but a subclass of it such that
  methods that originally return a calendar instance now return a :class:`Date`
  instance (e.g. the :meth:`~calendars.gregorian.GregorianCalendar.replace`
  method of the :class:`~calendars.gregorian.GregorianCalendar` class);
* if the instance does not have the attribute, the attribute lookup mechanism
  looks for it in the corresponding :class:`Date` class definition, where it is
  found; the code thus called creates the attribute in the instance (by monkey
  patching), so the next time it is returned as indicated above;
* if the attribute is retrieved directly from the class, as in
  ``Date.week_count(1, 1)`` above, a hybrid date/calendar constructor is
  returned: this constructor returns a :class:`Date` instance, initializing it
  with the ``day_count`` corresponding to the invoked calendar, and adds the
  corresponding calendar attribute (it has already been computed, so this does
  not require more computations).

The last two points seems conflicting: depending on the context (i.e. whether
the attribute is retrieved from the class or from the instance) a different
content is returned. This is obtained implementing a context-dependent
attribute retrieval, well described in `Descriptor HowTo Guide
<http://docs.python.org/3.3/howto/descriptor.html>`_).

This quite complex implementation has a few advantages:

* :class:`Date` instances do not store calendars unless they are retrieved;
* hybrid calendar classes are built at registration time, which happens only
  once per program invocation;
* the registration mechanism works unchanged for built-in and custom calendars;
* the calendar classes are completely independent from each other and from
  their use in the :class:`Date` class.


:class:`Time` Objects
---------------------

An indication of time, independent of any particular day. There might be a
time correction, e.g. due to time zone or daylight saving time. Attributes
of this class are: :attr:`day_frac`, :attr:`correction`. ``day_frac`` is
a Python :class:`fractions.Fraction` and contains the time as as a
fraction of a day. If present, ``correction`` indicates then number of
*hours* to be added or subtracted from the time to provide knowledge about
its location. Using the same definition used in :mod:`datetime`, such
an object is said to be "aware". An aware object is used to represent a
specific moment in time that is not open to interpretation. An object
whose ``correction`` attribute is ``None is said to be "naive".
Interpretation of what a naive object represents is left to the program.

Consequently, aware object can only be compared with aware objects and
naive object with naive objects.

There are two ways of creating a :class:`Time` instance:

.. class:: Time(day_frac, correction = None)

   Return an object that represent a moment in a day as a fraction of the
   whole day, given in the ``day_frac`` argument. If needed, a correction to
   this time, for whatever political, algorithmic or geographic need (e.g.
   time zone) can be given in hours and stored in the ``correction``
   argument.

   In version 0.5, time correction is not implemented, although the
   constructor interface supports it.

   The ``day_frac`` argument can be the integer ``0``, a float or a
   Python Fraction or Decimal, whose value is equal or greater than 0 and
   less than 1. A :exc:`TypeError` exception is raised if the argument type
   is not one of the accepted types. A :exc:`ValueError` exception is raised
   in the argument value is outside the accepted range.

.. classmethod:: Time.now(correction = None)

   Return a :class:`Time` object that represents the current moment in the
   day. It is possible to add a correction to this time.

   In version 0.5, time correction is not implemented, although the
   constructor interface supports it.

:class:`Time` instances are immutable, so they can be used as dictionary keys.
They can also be pickled and unpickled. In boolean contexts, all :class:`Time`
instances are considered to be true. :class:`Time` instances have two
attributes:

.. attribute:: time.day_frac

   The fraction of the day that represent the moment store in the object.
   This attribute is a Python Fraction and is read-only: an
   :exc:`AttributeError` exception is raised when trying to change it.

.. attribute:: time.correction

   When not ``None``, this attribute indicates a correction to the time that
   must be used to compare the time object with other time objects that have
   a correction.

   In version 0.5, time correction is not implemented, although the
   constructor interface supports it.


Supported operations
^^^^^^^^^^^^^^^^^^^^

+-------------------------------+----------------------------------------------+
| Operation                     | Result                                       |
+===============================+==============================================+
| ``time2 = time1 + timedelta`` | *time2* is ``timedelta`` time after          |
|                               | *time1*. If ``time1`` has a correction, this |
|                               | will be copied to ``time2``. (1) (2)         |
+-------------------------------+----------------------------------------------+
| ``time2 = time1 - timedelta`` | *time2* is ``timedelta`` time before         |
|                               | *time1*. If ``time1`` has a correction, this |
|                               | will be copied to ``time2``. (1) (2)         |
+-------------------------------+----------------------------------------------+
| ``timedelta = time1 - time2`` | A :class:`TimeDelta` object is returned      |
|                               | representing the day fraction                |
|                               | between *time1* and *time2*. (3) (4)         |
+-------------------------------+----------------------------------------------+
| ``time1 < time2``             | *time1* is less than *time2* when the former |
|                               | represents a moment earlier than the latter. |
|                               | (4) (5) (6)                                  |
+-------------------------------+----------------------------------------------+

Notes:

(1)
   A :exc:`ValueError` exception is raised if *timedelta* is not less than a
   day. If want to handle time differences greater than a day, you need to
   use :class:`DateTime` instances. If *timedelta* is negative, ``time2``
   will be before ``time1``.

(2)
   The result of adding a TimeDelta object to a Time object will always be
   valid: if overflow or underflow occur, the integer day part will be
   truncated so that only the fractional part will remain.

(3)
   The *timedelta* object created when subtracting two :class:`Time`
   instances will always represent a fractional part of a day, either
   positive or negative.

(4)
   ``time1`` and ``time2`` must be both naive or aware. Of they are aware
   time correction will be taken into account to generate the result.

(5)
   All other comparison operators behave similarly.

(6)
   Comparison between a :class:`Time` object and an object of another class
   return a :exc:`NotImplemented` exception, except for the equality and inequality
   operators, which respectively return *False* and *True*.


There are two instance methods:

.. method:: time.to_midnight()

   Return the time missing to midnight of the same day. if the initisl time
   has a correction, this will be copied into the result. Mathematically it
   is equivalent to:

.. doctest:: test_time

   >>> t1 = Time(0.25)
   >>> to_midnight = Time(1 - t1.day_frac, correction = t1.correction)
   >>> to_midnight.day_frac
   0.75
   >>> to_midnight.correction
   None


Time interface
^^^^^^^^^^^^^^^^^^

As with the :class:`Date` class, day fraction is not usable as a way to
indicate time. :class:`Time` objects also provide access to various time
representations, via the attribute paradigm.

For example, the ``western`` attribute allows to see the time instance as an
instance of the :class:`WesternTime` class, as follows:

.. doctest:: test_time

   >>> t1 = Time.western(19, 16, 55)
   >>> t1
   datetime2.Time(fractions.Fraction(13883, 17280))
   >>> t2 = Time(0.25)
   >>> t2.western
   timeofday.western.WesternTimeInTime(6, 0, 0)
   >>> d2.gregorian.month
   1

Above there are examples of two kinds of accesses: first of all, we can
construct a :class:`Date` instance using the default constructor of a calendar
(below there are examples of using non-default constructors). Note that the
``Date.gregorian`` constructor returns a :class:`Date` instance, not a
:class:`GregorianCalendar` one.

Additionally, we can see a :class:`Date` instance, whichever way it was
constructed, as an instance of a Gregorian calendar. As such, it is possible
to access all attributes and methods of the calendar:

.. doctest::

   >>> d = Date(734977)
   >>> str(d.gregorian)
   '2013-04-19'
   >>> d.gregorian.weekday()
   5

Special attention is given to calendar methods that normally return a new
calendar instance: these methods, when accessed through a :class:`Date`
attribute, return an instance of :class:`Date` and not one of the calendar.
E.g.:

.. doctest::

   >>> d1 = Date(734977)
   >>> d2 = d1.gregorian.replace(month = 6)
   >>> d2
   datetime2.Date(735038)
   >>> str(d2.gregorian)
   '2013-06-19'

When accessed through the attribute, also other calendar constructors, return
a date:

.. doctest::

   >>> d = Date.gregorian.year_day(2012, 366)
   >>> d
   datetime2.Date(734868)
   >>> d.gregorian
   calendars.gregorian.GregorianCalendarInDate(2012, 12, 31)

As expected, calendar static methods are unchanged:

.. doctest::

   >>> Date.gregorian.is_leap_year(2012)
   True

The real power of this paradigm is when different calendars are used. Indeed a
:class:`Date` instance is not limited to handling a single calendar: using the
corresponding attributes, all calendars are reachable:

.. doctest::

   >>> d = Date.gregorian(2013, 4, 22)
   >>> d.iso.week
   17

The following table lists the available calendars:

+--------------+----------------------------------------------------------+------------------+
| Calendar     | Calendar class                                           | Attribute        |
+==============+==========================================================+==================+
| Gregorian    | :ref:`GregorianCalendar <gregorian-calendar>`            | ``gregorian``    |
+--------------+----------------------------------------------------------+------------------+
| ISO          | :ref:`IsoCalendar <iso-calendar>`                        | ``iso``          |
+--------------+----------------------------------------------------------+------------------+

.. _custom-time-representations:

Custom time representations
"""""""""""""""""""""""""""


Not only the :mod:`datetime2` module has a variety of calendars, but it is also
possible to add custom calendars to class :class:`Date`, by calling the
following function:

.. function:: register_new_calendar(calendar_attribute, CalendarClass)

   Register the class ``CalendarClass`` to be used as a calendar in the
   :mod:`datetime2` module, accessing it with the ``calendar_attribute``
   attribute. If the ``calendar_attribute`` attribute is already defined, an
   :exc:`AttributeError` exception is generated. If ``calendar_attribute`` is
   not a valid identifier, a :exc:`ValueError` exception is generated.

   The ``CalendarClass`` must have the non-default constructor
   ``from_rata_die`` and the method ``to_rata_die`` that convert the calendar
   to and from the rata die count. A :exc:`TypeError` exception is generated if
   either method does not exist. Additionally, for the import mechanism to
   work, all non-default constructors and methods that return a calendar
   instance (e.g. :ref:`gregorian.replace <gregorian-replace>`) should
   construct objects of the calendar class just calling the calendar class
   (like in ``GregorianCalendar(1, 2, 3)``).

As a very simple example, let's define a new calendar that defines each day by
indicating the week number and the week day, counting the week of January
1\ :sup:`st` of year 1 as week 1 and so on. In addition, this new calendar has
a constructor using also thousands of weeks:

.. doctest::

   >>> class SimpleWeekCalendar():
   ...     def __init__(self, week, day):
   ...         self.week = week
   ...         self.day = day
   ...     @classmethod
   ...     def from_rata_die(cls, rata_die):
   ...         return cls((rata_die - 1) // 7 + 1, (rata_die - 1) % 7 + 1)
   ...     def to_rata_die(self):
   ...         return 7 * (self.week - 1) + self.day
   ...     def __repr__(self):
   ...         return '{}({}, {})'.format(self.__class__.__name__,self.week, self.day)
   ...     @classmethod
   ...     def with_thousands(cls, thousands, week, day):
   ...         return cls(1000 * thousands + week, day)
   ...
   >>> Date.register_new_calendar('week_count', SimpleWeekCalendar)
   >>> d1 = Date.week_count(1, 1)
   >>> d1.gregorian
   calendars.gregorian.GregorianCalendarInDate(1, 1, 1)
   >>> d2 = Date.gregorian(2013, 4, 26)
   >>> d2.week_count
   SimpleWeekCalendarInDate(104998, 5)

To avoid computing all calendars at initialization time, calendar attributes
in a :class:`Date` instance are evaluated when retrieved for the first time;
they are then stored as attributes of the instance.

To obtain this, the standard attribute lookup mechanisms is exploited:

* if the instance has the attribute, this is retrieved normally; however, this
  is not an instance of the original calendar, but a subclass of it such that
  methods that originally return a calendar instance now return a :class:`Date`
  instance (e.g. the :meth:`~calendars.gregorian.GregorianCalendar.replace`
  method of the :class:`~calendars.gregorian.GregorianCalendar` class);
* if the instance does not have the attribute, the attribute lookup mechanism
  looks for it in the corresponding :class:`Date` class definition, where it is
  found; the code thus called creates the attribute in the instance (by monkey
  patching), so the next time it is returned as indicated above;
* if the attribute is retrieved directly from the class, as in
  ``Date.week_count(1, 1)`` above, a hybrid date/calendar constructor is
  returned: this constructor returns a :class:`Date` instance, initializing it
  with the ``day_count`` corresponding to the invoked calendar, and adds the
  corresponding calendar attribute (it has already been computed, so this does
  not require more computations).

The last two points seems conflicting: depending on the context (i.e. whether
the attribute is retrieved from the class or from the instance) a different
content is returned. This is obtained implementing a context-dependent
attribute retrieval, well described in `Descriptor HowTo Guide
<http://docs.python.org/3.3/howto/descriptor.html>`_).

This quite complex implementation has a few advantages:

* :class:`Date` instances do not store calendars unless they are retrieved;
* hybrid calendar classes are built at registration time, which happens only
  once per program invocation;
* the registration mechanism works unchanged for built-in and custom calendars;
* the calendar classes are completely independent from each other and from
  their use in the :class:`Date` class.


