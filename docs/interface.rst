`datetime2` customization
=========================

.. testsetup:: test_date

   from datetime2 import Date

.. testsetup:: test_time

   from datetime2 import Time
   from fractions import Fraction

.. _interface:

Interface
^^^^^^^^^
Base classes of the :mod:`datetime2` module have all little if no practical
use as they natively are. E.g.: even if it stands out for its simplicity,
rata die is not a common way of representing dates in the real world.

A mechanism based on attributes, here called "access" attributes, has been
implemented to give access to a wide variety of calendars and time
representations. A table in the description of each base class lists all
currently available access attributes.

The access attribute can be used both on the base class and on a base class
instance:

* if called on the base class it creates a new instance of the base class
  using the values provided by the interface class:

.. doctest:: test_date test_time

   >>> d1 = Date.gregorian(2013, 4, 18)
   >>> d1
   datetime2.Date(734976)
   >>> t1 = Time.western(17, 16, 28)
   >>> t1
   datetime2.Time(Fraction(15547, 21600))

* if called on a base class instance, it allows to see the instance using
  attributes and methods of the corresponding interface class:

.. doctest:: test_date test_time

   >>> d2 = Date(1)
   >>> str(d2.gregorian)
   '0001-01-01'
   >>> d2.gregorian.month
   1
   >>> d2.gregorian.weekday()
   1
   >>> t2 = Time(Fraction(697, 1440))
   >>> str(t2.western)
   '11:37:00'
   >>> t2.western.minute
   37

The real power of this paradigm is that we can create a base class instance
with an access attribute and see its value with another access attribute,
or use different access attributes on the same base class instance. In this
way, the base class object is unchanged, but it can bee seen in many
different ways.

.. doctest:: test_date test_time

   >>> d = Date.gregorian(2013, 4, 22)
   >>> d.iso.week
   17
   >>> t = Time(0.5)
   >>> str(t.western)
   '12:00:00'
   >>> t.internet.beat
   500

A feature of :mod:`datetime2` is that all representations are
computed only once, when first accessed.

Special attention is given when a methods referenced via an access
attribute would normally return a new instance: examples are non-default
constructors and *replace*-like methods. When these methods are invoked via
an access attribute, the returned value is not an instance of the
referenced class, but one of the base class. E.g.
:meth:`GregorianCalendar.replace` returns a :class:`GregorianCalendar`
instance, but when used via the :class:`Date` class this becomes a
:class:`Date` instance:

.. doctest:: test_date test_time

   >>> d1 = Date.gregorian.year_day(2012, 366)
   >>> d1
   datetime2.Date(734868)
   >>> str(d1.gregorian)
   '2012-12-31'
   >>> d2 = d1.gregorian.replace(year = 2013, month = 6)
   >>> d2
   datetime2.Date(735050)
   >>> str(d2.gregorian)
   '2013-06-19'

As expected, static methods are unchanged even when invoked via access
attribute:

.. doctest:: test_date

   >>> Date.gregorian.is_leap_year(2012)
   True

.. _customization:

Customization
"""""""""""""

It is possible to add new calendars and/or time representations at run time,
by calling a method of the base class and providing the new access attribute
name and the new interface class. This new class must satisfy three simple
requirements in order to be used as such.

Before examining these requisites in detail, let's have a look at a simple
example: we want to define a new calendar that defines each day by
indicating the week number and the week day, counting the week of January
1\ :sup:`st` of year 1 as week 1 and so on. In addition, this new calendar
has a non-default constructor that takes as argument also thousands of weeks:

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
   ...     def __str__(self):
   ...         return 'W{}-{}'.format(self.week, self.day)
   ...     @classmethod
   ...     def with_thousands(cls, thousands, week, day):
   ...         return cls(1000 * thousands + week, day)
   ...
   >>> Date.register_new_calendar('week_count', SimpleWeekCalendar)
   >>> d1 = Date.week_count(1, 1)
   >>> str(d1.gregorian)
   '0001-01-01'
   >>> d2 = Date.gregorian(2013, 4, 26)
   >>> str(d2.week_count)
   'W104998-5'
   >>> d3 = Date.week_count.with_thousands(104, 998, 5)
   >>> d2 == d3
   True

The requirements that must be satisfied to define a custom :class:`Date`
calendar are:

* The new calendar class must define the non-default constructor
  ``from_rata_die``, that creates a calendar instance using the day count
  defined in the :class:`Date` class as argument.
* The new calendar class must have the method ``to_rata_die`` to convert the
  given calendar instance to rata die.
* All other non-default constructors and all methods returning a calendar
  instance must use the default constructor to return the new calendar
  instance.

The following tables lists the name required for each base class:

+-------------------------+---------------------------+---------------------------+---------------------------+---------------------------+
|                         | :class:`Date`             | :class:`Time`             | :class:`DateTime`         | :class:`TimeDelta`        |
+=========================+===========================+===========================+===========================+===========================+
| Registration function   | ``register_new_calendar`` | ``register_new_time``     | TBD                       | TBD                       |
+-------------------------+---------------------------+---------------------------+---------------------------+---------------------------+
| Non-default constructor | ``from_rata_die``         | ``from_day_frac``         | TBD                       | TBD                       |
+-------------------------+---------------------------+---------------------------+---------------------------+---------------------------+
| Conversion method       | ``to_rata_die``           | ``to_day_frac``           | TBD                       | TBD                       |
+-------------------------+---------------------------+---------------------------+---------------------------+---------------------------+

All registration methods have the same structure:

.. function:: registration_method(access_attribute, InterfaceClass)

   Register the class ``InterfaceClass`` to the corresponding
   :mod:`datetime2` base class, accessing it with the ``access_attribute``
   attribute. If ``access_attribute`` is already defined, an
   :exc:`AttributeError` exception is generated. If ``access_attribute`` is
   not a valid identifier, a :exc:`ValueError` exception is generated.

   ``InterfaceClass`` must have the non-default constructor and conversion
   method listed above, otherwise a :exc:`TypeError` exception is generated.


Inner workings
""""""""""""""

In order to obtain this mechanism, two operations are performed when an
interface class is registered to a base class:

* A new class in created on the fly, so that the new class returns a base
  class instance when constructor is called, and not an interface class
  instance. This new class inherits from the interface class, but returns
  base class instances.
* A new attribute is added to the base class. This attribute is special:
  depending on whether it is called on the base class or on a base class
  instance, it returns or creates the modified interface class instance.

This is an exploit of the standard attribute lookup mechanisms, obtained
implementing a context-dependent attribute retrieval, well described in
`Descriptor HowTo Guide <http://docs.python.org/3.4/howto/descriptor.html>`_:

* If the attribute is retrieved directly from the class (e.g. as in
  ``Date.week_count(1, 1)``), the modified interface class (contained in
  ``Date.week_count``) is returned, so that when invoked with the interface
  class signature, it returns a base class instance. The modified interface
  class was created at registration time, so no additional time is required
  to create it.
* If the attribute is retrieved from a base class instance, there are two
  cases:

  * The instance already has the attribute, which is retrieved normally.
    Note that this attribute is an instance of the modified interface class,
    not of the original one.
  * The instance does not have the attribute: the attribute lookup mechanism
    looks for it in the corresponding :class:`Date` class definition, where
    it is found since it was created at registration time. The attribute is
    created and added to the instance by monkey patching, so the next time
    it is returned as indicated above.

This quite complex implementation has a few advantages:

* Base cass instances do not store access attributes unless they are
  retrieved.
* Modified interface classes are built at registration time, which happens
  only once per program invocation.
* The registration mechanism is common to built-in and custom calendars.
* Interface classes are completely independent from each other and from
  their use in base classes.


