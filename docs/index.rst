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

A moment in history is independent from the way it is represented in different
cultures. There are indeed many calendars in which the same day is represented
in different ways. The :mod:`datetime2` module detaches operations on time or
date objects from their representation, and also allows to add other
representations at run time. The module does all this in an efficient and
syntactically clear way.

A very simple internal representation has been chosen so that it becomes easy
to convert this internal representation to the many different calendars. The
idea, inspired by the excellent book "Calendrical Calculations"[#book]_, is to
identify each day by simply counting the days starting with 1 for January
1\ :sup:`st` of year 1, 2 for January 2\ :sup:`nd` is day 2, and so on. Using
the the :mod:`datetime2` module we write:

.. doctest::

   >>> d1 = Date(1)       # January 1st, 1
   >>> d2 = Date(737109)  # February 19th, 2019

However entering dates in this way is nearly useless, but the module comes in
help. E.g. we can use the Gregorian calendar or the ISO calendar:

.. doctest::

   >>> d3 = Date.gregorian(1965, 3, 1)  # Gregorian: 1965-03-01
   >>> d4 = Date.iso(2011, 1, 1)        # ISO: 2011-W01-1

Similarly, each :class:`Date` object can be printed with the internal
representation:

.. doctest::

   >>> print(d3)
   717396
   >>> print(d4)
   734140

And again, this way of using the day is nearly useless. But you can use
attributes also on :class:`Date` objects to access different representations:

.. doctest::

   >>> print(d1.gregorian)
   0001-01-01
   >>> print(d2.gregorian)
   2019-02-19
   >>> print(d4.gregorian)
   2011-01-03
   >>> print(d1.iso)
   0001-W01-1
   >>> print(d2.iso)
   2019-W08-2
   >>> print(d3.iso)
   1965-W09-1

As you can see, it is not required to use the same calendar with which an
object has been created. Each calendar also presents different attributes
that can be accessed as usual. These may be components of the date, like in:

.. doctest::

   >>> print(d2.gregorian.year)
   2019
   >>> print(d3.iso.week)
   9

But also other date attributes:

.. doctest::

   >>> print(d3.gregorian.weekday())
   1
   >>> print(d3.gregorian.day_of_year())
   60

Finally, :class:`Date` objects can often be created with other constructors:

.. doctest::

   >>> print(Date.gregorian.year_day(2020, 120).gregorian)  # the 120th day of 2020
   2020-04-29

Although there exist much less time representations, the :mod:`datetime2`
module uses the same reasoning to represent the time of the day: a moment of
the day is represented as a fraction of the day, starting from midnight. In
the following examples we use the Decimal Time, a subdivision of days in 10
hours of 100 minutes, each minute being 100 seconds.

.. doctest::

   >>> t1 = Time((7, 10))
   >>> print(t1.western)
   16:48:00
   >>> print(t1.decimal)
   7:00:00

As with dates, also time can be entered and printed with different
representations, and also the time of day representations have attributes,
methods and alternate constructors:

.. doctest::

   >>> t2 = Time.western(15, 47, 16)
   >>> t3 = Time.decimal(4, 83, 18)
   >>> print(t2.decimal)
   6:55:06
   >>> print(t3.western)
   11:35:46
   >>> print(t3.western.minute)
   35
   >>> print(t3.western.to_hours())
   Fraction(72477, 6250)
   >>> t4 = Time.western.in_minutes(1000)
   >>> print(t4)
   25/36 of a day
   >>> print(t4.western)
   16:40:00
   >>> print(t4.decimal)
   6:94:44

The reference between time objects can be either implicit time, i.e. depending
on implementation (it usually is the local time,but can also be UTC). It is
also possible to have an explicit reference to UTC, passed as an additional
parameter to the object constructor. In the first case the  :class:`Time`
object is said to be "naive", in the second case it is said to be "aware".

As in dates and time classes, also the time to UTC is indicated by a
culturally independent value, i.e. a fraction of a day. Additional time
representations can support naive references, or are implicitly aware.

.. doctest::

   >>> t5 = Time('2/3', to_utc=(1, 12))
   >>> print(t8)
   2/3 of a day, 1/12 of a day to UTC
   >>> print(t5.western)
   16:00:00+02
   >>> t6 = Time.internet(456)
   >>> print(t6.western)
   10:56:03+01

The :ref:`Internet time <internet-time>` is by definition on Basel time zone.
This is equivalent to central Europe time zone, but doesnt have daylight
saving time.

Other prominent features of the :mod:`datetime2` module are the ability to
add other representations at run time and the fact that representations do
not consume memory unless they are effectively used (this is especially
important for calendars, where many representation exists [#many]_ ).

Currently (version |release|) the following calendars and time representations
are available:

+-------------------+-----------------------------------------+----------------------------------------------------+
| Module            | Calendar(s)                             | Time representation(s)                             |
+===================+=========================================+====================================================+
| datetime2.western | :ref:`Gregorian <gregorian-calendar>`   | :ref:`Western <western-time>`                      |
+-------------------+-----------------------------------------+----------------------------------------------------+
| datetime2.modern  | :ref:`ISO <iso-calendar>`               | :ref:`Internet <internet-time>`                    |
+-------------------+-----------------------------------------+----------------------------------------------------+


.. [#many] Well, this should be read as "will exist", since current version
           (|release|) only has two of them.

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

