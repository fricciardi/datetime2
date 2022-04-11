`datetime2` customization
=========================

.. testsetup:: 

   from datetime2 import Date
   from datetime2 import Time
   from fractions import Fraction

.. _interface:

Interface
^^^^^^^^^
Base classes of the :mod:`datetime2` module have little if no practical
use as they natively are: even if it stands out for its simplicity,
rata die is not a common way of representing dates in the real world.
Same consideration can be done about time as a fraction of a day.

A mechanism based on attributes, here called "access" attributes, has been
implemented to give access to a wide variety of calendars and time
representations.

When used on the base class, the attribute behaves as a constructor of the
base class, but with the arguments of the specific representation:

.. doctest::

   >>> d = Date.gregorian(2013, 4, 18)
   >>> d
   datetime2.Date(734976)
   >>> t = Time.western(17, 16, 28)
   >>> t
   datetime2.Time('15547/21600')

When used on a base class instance, the attribute allows to see the instance
using a specific representation, or to call methods defined for that
specific representation:

.. doctest::

   >>> d = Date(1)
   >>> str(d.gregorian)
   '0001-01-01'
   >>> d.gregorian.month
   1
   >>> d.gregorian.weekday()
   1
   >>> t = Time(Fraction(697, 1440))
   >>> str(t.western)
   '11:37:00'
   >>> t.western.minute
   37

The attribute gives access to what is called an "interface class". The
interface class is the one that manages converting a specific representation
(e.g. the Gregorian calendar) to the base class. The :ref:`all-calendars`
chapter lists all available interface classes for calendars. The
:ref:`all-time-representations` chapter lists all available interface
classes for time.

The real power of this paradigm is that we can create a base class instance
with an access attribute and see its value with another access attribute,
or use different access attributes on the same base class instance. In this
way, the base class object is unchanged, but it can bee seen in many
different ways.

.. doctest::

   >>> d = Date.gregorian(2013, 4, 22)
   >>> d.iso.week
   17
   >>> t = Time(0.5)
   >>> str(t.western)
   '12:00:00'
   >>> t.internet.beat
   Fraction(500, 1)

An intended feature of :mod:`datetime2` is that any representations is computed
only once, when first accessed, then remains available to the base class.

Interface class may have, as it is normal, additional constructors. E.g. the
:class:`GregorianCalendar` class has the :meth:`GregorianCalendar.year_day` and
:meth:`GregorianCalendar.replace` methods that return a
:class:`GregorianCalendar` instance. However, thanks to some magic explained
later, when such constructors are accessed via the attribute mechanisms on the
base class or an instance of it, constructors of the interface class return
instances of the base class instead, as shown in this example:

.. doctest::

   >>> greg = GregorianCalendar.year_day(2012, 366)
   >>> greg
   GregorianCalendar(2012, 12, 31)
   >>> d1 = Date.gregorian.year_day(2012, 366)
   >>> d1
   datetime2.Date(734868)
   >>> str(d1.gregorian)
   '2012-12-31'
   >>> d2 = d1.gregorian.replace(year = 2013, month = 7)
   >>> d2
   datetime2.Date(735080)
   >>> str(d2.gregorian)
   '2013-07-31'

And, as expected, static methods of the interface classes are
unchanged even when invoked via access attribute:

.. doctest::

   >>> Date.gregorian.is_leap_year(2012)
   True

.. _customization:

Customization
^^^^^^^^^^^^^

Base classes provide a mechanism to register new interface classes at run-time.
The same mechanism is indeed used to register already available interface
classes at module import time. The interface class must respect a few simple
requirements shown later.

Before examining these requisites in detail, let's have a look at a simple
example: we want to define a new calendar that defines each day by
indicating the week number and the week day, counting the week of January
1\ :sup:`st` of year 1 as week 1 and so on. In addition, this new calendar
has a non-default constructor that takes as argument also thousands of weeks:

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
   ...     def __str__(self):
   ...         return 'W{}-{}'.format(self.week, self.day)
   ...     @classmethod
   ...     def with_thousands(cls, thousands, week, day):
   ...         return cls(1000 * thousands + week, day)
   ...
   >>> Date.register_new_calendar('week_count', SimpleWeekCalendar)
   >>> d1 = Date.week_count(1, 1)
   >>> d1
   datetime2.Date(1)
   >>> str(d1.gregorian)
   '0001-01-01'
   >>> d2 = Date.gregorian(2013, 4, 26)
   >>> str(d2.week_count)
   'W104998-5'
   >>> d3 = Date.week_count.with_thousands(104, 998, 5)
   >>> d2 == d3
   True

As can be seen in the example, the new interface class completely ignores the
way a base class instance works. The requirements for an interface class to be
used by the registration module are:

* Have a non-default forward constructor, that creates an instance of the
  interface class using the base class attribute.
* Have a backward method that returns the base class attribute corresponding to
  the interface class value.
* All other non-default constructors and all methods returning an interface
  class instance must use the interface class default constructor.

Once the new interface class is ready, the call of a registration method of the
base class does the magic.

Each :mod:`datetime2` base class has a specific registration function.
Required methods also have names depending on the base class they are
registered to. The following table lists all these names:

+-------------------------+---------------------------+---------------------------+---------------------------+---------------------------+
|                         | Base Classes                                                                                                  |
+-------------------------+---------------------------+---------------------------+---------------------------+---------------------------+
|                         | :class:`Date`             | :class:`Time`             | :class:`DateTime`         | :class:`TimeDelta`        |
+=========================+===========================+===========================+===========================+===========================+
| Registration function   | ``register_new_calendar`` | ``register_new_time``     | TBD                       | TBD                       |
+-------------------------+---------------------------+---------------------------+---------------------------+---------------------------+
| Non-default constructor | ``from_rata_die``         | ``from_time_pair``        | TBD                       | TBD                       |
+-------------------------+---------------------------+---------------------------+---------------------------+---------------------------+
| Conversion method       | ``to_rata_die``           | ``to_time_pair``          | TBD                       | TBD                       |
+-------------------------+---------------------------+---------------------------+---------------------------+---------------------------+

These methods are detailed below:

.. classmethod:: Date.register_new_calendar(access_attribute, CalendarInterface)

   Register the ``CalendarInterface`` class to the :class:`Date` class, using
   the ``access_attribute`` identifier to access it. If ``access_attribute`` is
   already defined, an :exc:`AttributeError` exception is raised. If
   ``access_attribute`` isn't a valid identifier, a :exc:`ValueError` exception
   is raised.

   ``CalendarInterface`` must obey the requirements for the :mod:`datetime2`
   interface classes, otherwise a :exc:`TypeError` exception is raised.

.. classmethod:: Time.register_new_time(access_attribute, TimeInterface)

   Register the ``TimeInterface`` class to the :class:`Time` class, using
   the ``access_attribute`` identifier to access it. If ``access_attribute`` is
   already defined, an :exc:`AttributeError` exception is raised. If
   ``access_attribute`` isn't a valid identifier, a :exc:`ValueError` exception
   is raised.

   ``TimeInterface`` must obey the requirements for the :mod:`datetime2`
   interface classes, otherwise a :exc:`TypeError` exception is raised.

.. classmethod:: calendar_class.from_rata_die(day_count)

   Return a calendar object that corresponds to the day identified by the
   given day count.

.. method:: calendar_obj.to_rata_die()

   Return a rata die value that corresponds to the day represented by the
   calendar instance.

.. classmethod:: time_of_day_class.from_time_pair(day_frac, utcoffset)

   Return a time of day object that corresponds to the moment identified by
   the given day fraction, possibly with reference to the given UTC distance.

.. method:: time_of_day_obj.to_time_pair()

   Return a tuple of two values: the first one is the day fraction
   corresponding to the moment of the day identified by the time object, the
   second is null for naive time objects, or is a fraction of day to be added
   to UTC to get the time of day object.


Inner workings
^^^^^^^^^^^^^^

At registration time, some magic needs to be performed to obtain the wanted
results:

* A new class is created on the fly, inheriting from the interface class.
  The new class changes the default constructor so it returns a base
  class instance when called. Since all other constructors use the default
  one (see the requirements above), all constructors of the new class return
  a base class instance.
* A new attribute is added to the base class. This attribute is special
  because its semantic depend on whether it is called on the base class or
  on a base class instance. In the former case, it creates a new base class
  instance. In the latter case, it uses the methods corresponding to the
  registered interface class.

The latter is obtained by exploiting the standard attribute lookup
mechanisms, implementing a context-dependent attribute retrieval. This is
well described in `Descriptor HowTo Guide <http://docs.python.org/3.4/howto/descriptor.html>`_:

* If the attribute is retrieved directly from the class (e.g. as in
  ``Date.week_count(1, 1)``), the modified interface class (contained in
  ``Date.week_count``) is returned, so that when invoked with the interface
  class signature, it returns a base class instance. The modified interface
  class was created at registration time, so no additional time is required
  to create it.
* If the attribute is retrieved from a base class instance, there are two
  cases:

  * The instance does not have the attribute: the attribute lookup mechanism
    looks for it in the corresponding :class:`Date` class definition, where
    it is found since it was created at registration time. The attribute is
    created and added to the instance by monkey patching, so the next time
    the interface class instance is returned as indicated below.
  * The instance already has the attribute, which is retrieved normally.
    Note that this attribute is an instance of the modified interface class,
    not of the original one.

This quite complex implementation has a few advantages:

* Base class instances do not store access attributes unless they are
  retrieved.
* Modified interface classes are built at registration time, which happens
  only once per program invocation.
* The registration mechanism is common to built-in and custom calendars.
* Interface classes are completely independent from each other and from
  their use in base classes.

