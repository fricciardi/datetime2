.. datetime2 documentation master file, created by
   sphinx-quickstart on Tue Jan 15 17:29:11 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. module:: datetime2
   :synopsis: New date and time types
.. moduleauthor:: Francesco Ricciardi <francescor2010@yahoo.it>

.. testsetup::

   from datetime2 import Time
   from fractions import Fraction
   from datetime2 import Date

Overview
========

The definition of a moment in history is independent from the way it is
represented in different cultures. There are indeed many calendars in which
the same day is represented in different ways. The :mod:`datetime2` module
detaches operations on date and time objects from their representation, and
also allows to add other representations at run time. The module does all
this in an efficient and syntactically clear way.

We can create a date object by calling the relevant access attribute of the
base class :class:`Date`:

.. doctest::

   >>> d1 = Date.gregorian(1965, 3, 1)  # Gregorian: 1965-03-01
   >>> d2 = Date.iso(2011, 23, 4)      # ISO: 2011-W23-4

Each of these date objects can be printed and has its own attributes and
methods:

.. doctest::

   >>> print(d1.gregorian)
   1965-03-01
   >>> print(d1.gregorian.month)
   3
   >>> print(d1.gregorian.weekday())
   1
   >>> print(d2.iso)
   2011-W23-4
   >>> print(d2.iso.week)
   23
   >>> print(d2.iso.day_of_year())
   158

What makes :mod:`datetime2` powerful is that we can mix these attributes,
independently from how they were built:

.. doctest::

   >>> print(d1.iso)
   1965-W09-1
   >>> print(d1.iso.week)
   9
   >>> print(d1.iso.day_of_year())
   57
   >>> print(d2.gregorian)
   2011-06-09
   >>> print(d2.gregorian.month)
   6
   >>> print(d2.gregorian.weekday())
   4

Currently (version |release|) the calendars listed below are available.
Custom representations can be added at run time.

+-------------------+---------------------+-----------------------------------------+
| Module            | Access attribute    | Calendar                                |
+===================+=====================+=========================================+
| datetime2.western | `gregorian`         | :ref:`Gregorian <gregorian-calendar>`   |
+-------------------+---------------------+-----------------------------------------+
| datetime2.modern  | `iso`               | :ref:`ISO <iso-calendar>`               |
+-------------------+---------------------+-----------------------------------------+


Similarly, we can have different representations also for time. They can be
mixed like in dates:

.. doctest::

   >>> t1 = Time.western(15, 47, 16)
   >>> t2 = Time.internet(895)
   >>> print(t1.western)
   15:47:16
   >>> print(t1.internet)
   @657
   >>> print(t2.western)
   21:28:48
   >>> print(t2.western.minute)
   28

Currently (version |release|) the time of day listed below are available.
Again, custom time of day can be added at run time.

+-------------------+---------------------+-----------------------------------------+
| Module            | Access attribute    | Time of day                             |
+===================+=====================+=========================================+
| datetime2.western | `western`           | :ref:`Western <western-time>`           |
+-------------------+---------------------+-----------------------------------------+
| datetime2.modern  | `internet`          | :ref:`Internet <internet-time>`         |
+-------------------+---------------------+-----------------------------------------+


Internal representation
=======================

In order to be able to convert between the different calendars and between
the different times of day, a generic and culturally independent way of
internally representing them has been chosen. For calendars, the idea,
inspired by the excellent book "Calendrical Calculations"[#book]_, is to
identify each day by simply counting the days starting with 1 for January
1\ :sup:`st` of year 1, 2 for January 2\ :sup:`nd` is day 2, and so on. Using
the :mod:`datetime2` module we write:

.. doctest::

   >>> d3 = Date(1)
   >>> d4 = Date(737109)

These dates can then be handled like above:

.. doctest::

   >>> print(d3.gregorian)
   0001-01-01
   >>> print(d3.iso)
   0001-W01-1
   >>> print(d4.gregorian)
   2019-02-19
   >>> print(d4.iso)
   2019-W08-2

Similarly, each :class:`Date` object can be printed with the internal
representation (even if it is of little use):

.. doctest::

   >>> print(d1)
   R.D. 717396
   >>> print(d2)
   R.D. 734297

Where ``R.D.`` stands for Rata Die, the Latin for "fixed date".

There is also a generic time of day internal representation: a moment of the
day is represented as a fraction of the day, starting from midnight.

.. doctest::

   >>> t3 = Time(7, 10)
   >>> t4 = Time(0.796875)
   >>> print(t3.western)
   16:48:00
   >>> print(t3.internet)
   @700
   >>> print(t4.western)
   19:07:30
   >>> print(t4.internet)
   @796

And again we can print the internal time of day:

.. doctest::

   >>> print(t1)
   14209/21600 of a day
   >>> print(t2)
   179/200 of a day, 1/24 of a day from UTC

(Remember that ``t2`` was created from Internet time, and Internet time
objects are always aware

UTC offset
==========

The reference between time objects can be either implicit time, i.e.
depending on implementation (it usually is the local time, but can also be
UTC). In the :mod:`datetime2` module, it is also possible to have an explicit
reference to UTC, passed as an additional parameter to :class:`Time` and
:class:`DateTime` object constructors. An instance that has been created with
this explicit reference is said to be "aware",  without the object is said to
be "naive".

In some of the time of day representations of this module, the UTC offset is
implicit. E.g., :ref:`Internet time <internet-time>` is by definition on
Basel time zone, e.g. UTC+1. This means that only aware :class:`Time` objects
can have such time representations.


.. [#book] "Calendrical Calculations: The Ultimate Edition",  E. M. Reingold, N. Dershowitz, Cambridge University
           Press, 2018, and all its previous versions


.. seealso::

   Module :mod:`datetime`
      Basic date and time types.

   Module :mod:`calendar`
      General calendar related functions.

   Module :mod:`time`
      Time access and conversions.


Indices and tables
==================

.. toctree::

   base_classes
   calendars
   timeofday
   interface


* :ref:`genindex`

