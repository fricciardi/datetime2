:mod:`datetime2` --- New date and time classes
==============================================

.. module:: datetime2
   :synopsis: Date and time types with broader calendar coverage.
.. moduleauthor:: Francesco Ricciardi <francescor2010@yahoo.it>

.. testsetup:: *

   from datetime2 import Date

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
   adding

Overview
--------

The :mod:`datetime2` module implements four core classes, corresponding to the
four classes implemented in the original :mod:`datetime` module. These are
:class:`Date`, :class:`Time`, :class:`DateTime`,
:class:`TimeDelta`. These  class names use the CapitalizedWords
convention, required by :pep:`8`, not used in the old module. The classes
provide generic service, not bound to any particular calendar or time
representation. The :class:`Date` and :class:`Time` classes will be implemented
in a future version. The :class:`TimeDelta` class is currently a stub.

.. class:: Date
   :noindex:

   An idealized date, with no notion of time or time zone. A date is stored
   counting the number of days elapsed from what would have been January 1st
   of year 1 on the Gregorian calendar. The only attribute of this class is:
   :attr:`day_count`.


.. class:: TimeDelta
   :noindex:

   A duration expressing the difference between two :class:`Date`,
   :class:`Time`,    or :class:`DateTime` instances. This difference is stored
   in a single Python    :class:`fractions.Fraction`. The only attribute of
   this class is: :attr:`days`.


These core classes are of little use as defined above. Indeed,
:mod:`datetime2` is able to interface with different calendars and time
representations. The syntax to access these calendars and representations is
through the attribute paradigm. E.g.: the core classes and their instances will
be able to access class methods, constructors and instances of the specific
calendar as class or instance attributes. For example:

.. doctest::

  >>> d = Date.gregorian(2012, 2, 27)
  >>> print(d)
  R.D. 734560
  >>> print(d.gregorian)
  2012-02-27
  >>> d.iso.week
  9

.. _list-of-calendars :

Currently (version |release|) the following calendars are available:

.. hlist::

  * :ref:`gregorian-calendar`
  * :ref:`iso-calendar`

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
   This attribute is read-only: an :exc:`AttributeException` is raised when
   trying to change it.


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
module provides access to many calendars, through class and instance methods.
For example, the ``gregorian`` attribute allows to see the date instance as an
instance of the :class:`GregorianCalendar` class, as follows:

.. doctest::

   >>> d = Date.gregorian(2013, 4, 18)
   >>> d
   datetime2.Date(734976)

Note that the ``Date.gregorian`` constructor returns a :class:`Date`
instance, not a :class:`GregorianCalendar` one. Through the attribute, it is
also possible to access other constructors, as seen below, always returning a
date:

.. doctest::

   >>> d = Date.gregorian.year_day(2012, 366)
   >>> d
   datetime2.Date(734868)

Similarly, we can access static methods:

.. doctest::

   >>> Date.gregorian.is_leap_year(2012)
   True

Through the same attribute, we can see date instances as calendar instances,
thus accessing calendar methods. For example:

.. doctest::

   >>> d = Date(734977)
   >>> str(d.gregorian)
   '2013-04-19'
   >>> d.gregorian.weekday()
   5

Special attention is given to methods that normally return a new calendar
instance: these methods, when accessed through a :class:`Date` attribute,
return an instance of :class:`Date` and not one of the calendar. E.g.:

.. doctest::

   >>> d1 = Date(734977)
   >>> d2 = d1.gregorian.replace(month = 6)
   >>> str(d.gregorian)
   '2013-04-19'

The real power of this paradigm is when different calendars are used. The
methods can be easily mixed transparently to the user::

   >>> d = Date.gregorian(2013, 4, 22)
   >>> d.iso.week
   17

The calendars available in the datetime2 distribution are
:ref:`listed here <list-of-calendars>`. The manual section
:ref:`Adding a new calendar to the Date class <adding-a-new-calendar>` explains
how a custom calendar can be added to :class:`Date`, together with an
explanation of the inner working of this mechanism. To add a new calendar,
just call this function:

.. function:: register_new_calendar(calendar_attribute, CalendarClass)

   Register the class ``CalendarClass`` to be used as a calendar in the
   :mod:`datetime2` module, accessing it with the ``calendar_attribute``
   attribute. If the ``calendar_attribute`` attribute is already defined, an
   :exc:`AttributeError` exception is generated. If ``calendar_attribute`` is
   not a valid identifier, a :exc:`ValueError` exception is generated.

   The ``CalendarClass`` class must satisfy the requirements listed in
   :ref:`Adding a new calendar to the Date class <adding-a-new-calendar>`. If
   it does not, a :exc:`TypeError` exception is generated.