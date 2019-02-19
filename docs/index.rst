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


Development of the :mod:`datetime2` module starts from the idea that a
day in history or in future is the same independently from the way it
is represented in different cultures. The module, indeed, detaches
operations on dates from their representation, chosing for the base class
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
representations. However, the simple definitions create an additional effort
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
representation in which it was created. Any available representation can be
used to create a new object, or to show the date or time with a precise
representation. There are a few representations already available, listed below.

Another feature of the :mod:`datetime2` module is the ability to add other
representations at run time. Representations do not consume memory
unless they are effectively used. This is especially important for
calendars, where many representation exists [#many]_ .

Currently (version |release|) the following calendars and time representations
are available.

Calendars:

.. hlist::

  * :ref:`gregorian-calendar`
  * :ref:`iso-calendar`

Time representation:

.. hlist::

  * :ref:`western-time`
  * :ref:`internet-time`

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
* :ref:`modindex`

