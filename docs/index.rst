.. datetime2 documentation master file, created by
   sphinx-quickstart on Tue Jan 15 17:29:11 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

##############################################
:mod:`datetime2` --- New date and time classes
##############################################

.. module:: datetime2
   :synopsis: Second generation date and time types
.. moduleauthor:: Francesco Ricciardi <francescor2010@yahoo.it>

.. testsetup::

   from datetime2 import Time
   from fractions import Fraction
   from datetime2 import Date

Overview
========

The key idea behind the :mod:`datetime2` module is the fact that a moment in
history is independent from the way it is represented in different cultures.
The module, indeed, detaches operations on time or date objects from their
representation. Indeed, dates are defined counting the elapsed days: January
1\ :sup:`st`, year 1 is day 1, January 2\ :sup:`nd` is day 2 and so on. E.g.:

.. doctest::

   >>> d1 = Date(1)  # January 1st, AD 1
   >>> d2 = Date(737109)  # February 19th, 2019

We can then print those dates with different representations. These
representations are accessed as attributes of the :class:`Date` object:

.. doctest::

   >>> d1 = Date(1)  # January 1st, AD 1
   >>> d2 = Date(737109)  # February 19th, 2019
   >>> print(d1.gregorian)
   0001-01-01
   >>> print(d1.iso)
   0001-W01-1
   >>> print(d2.gregorian)
   2019-02-19
   >>> print(d2.iso)
   2019-W08-2

Date representation can be used also in the opposite direction, i.e. to create
the date object:

.. doctest::

   >>> d3 = Date.gregorian(1965, 3, 1)  # Gregorian: 1965-03-01
   >>> d4 = Date.iso(2001, 1, 1)  # ISO: 2001-W01-1

And also objects created in this way can be used with different
representations:

.. doctest::

   >>> d3 = Date.gregorian(1965, 3, 1)  # Gregorian: 1965-03-01
   >>> d4 = Date.iso(2011, 1, 1)  # ISO: 2001-W01-1
   >>> print(d3.iso)
   1965-W09-1
   >>> print(d4.gregorian)
   2011-01-03

The same thinking can be applied to the time of the day: any moment in a day
can be seen as a fraction of one day, starting from midnight. This holds even
if the number of time representations is smaller than that of calendars.

.. doctest::

   >>> t1 = Time(0.25)
   >>> print(t1.western)
   06:00:00
   >>> print(t1.internet)
   @250

The second time representation you see above is name "Internet Time" and
divides the day in 1,000 units, called "beats".

The :class:`Time` class allows entering the fraction of a day in many different
ways, provided they express the value of a day fraction. Other examples:

.. doctest::

   >>> t2 = Time("1/8")
   >>> t3 = Time((3, 24))
   >>> t4 = Time(Fraction(7, 10))

As with dates, also time can be entered with different represetations:

.. doctest::

   >>> t5 = Time.western(15, 47, 16)
   >>> t6 = Time.internet(163)
   >>> print(t5.internet)
   @657
   >>> print(t6.western)
   03:54:43

.. warning::

   The documentation for the to_utc attribute of the Time class is under
   development. Its content will not be aligned to code until this warning is
   removed.

With time objects, there may be an implicit time reference, assumed by program
implementation, or an explict one, passed as an additional parameter to the
:class:`Time` object. In the first case the object is said to be "naive", in
the second case it is said to be "aware". The reference time may be UTC, but
this is not mandatory.

.. doctest::

   >>> t8 = Time('2/3', to_ref=(1, 12))
   >>> print(t8)
   2/3 of a day, 1/12 of a day to ref
   >>> print(t8.western)
   16:00:00+02

.. TODO:: The following may change in the future

With western time representation, the time reference is UTC.

Another feature of the :mod:`datetime2` module is the ability to add other
representations at run time. Representations do not consume memory
unless they are effectively used. This is especially important for
calendars, where many representation exists [#many]_ .

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

