.. _adding-a-new-calendar:

.. testsetup:: *

   import datetime2
   from datetime2 import Date


Adding a new calendar to the Date class
=======================================

It is easy to define new classes to be used as calendar in the
:class:`~datetime2.Date` class. Any class that complies with the requirements
below can be used as a calendar. Once the class satisfies the requirements, a
simple call to :func:`~datetime2.register_new_calendar` solves the problem::

   >>> datetime2.register_new_calendar('my_new_calendar', MyNewCalendar)

After this, the new calendar is integrated into :mod:`datetime2`::

   >>> d = Date.my_new_calendar(....)
   >>> str(d)
   'R.D. .......'
   >>> d.gregorian.year
   1234

The new calendar class must define the ``from_rata_die`` constructor and the
``to_rata_die`` method. In addition, for the interface to work with the other
methods of the new calendar, it must list the following special methods in some
class variables, as listed in the following table:

.. _class-attributes-to-fill:

+------------------------------------------+---------------------------------+
| Methods to list                          | In class variable               |
+==========================================+=================================+
| All static methods.                      | ``_static_methods``             |
+------------------------------------------+---------------------------------+
| All classmethods that return an instance | ``_classmethods``               |
| of the calendar class, including the     |                                 |
| other non-default constructors.          |                                 |
+------------------------------------------+---------------------------------+
| All methods that return an instance of   | ``_special_methods``            |
| the calendar class.                      |                                 |
+------------------------------------------+---------------------------------+

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
   ...         return 'SimpleWeekCalendar({}, {}}'.format(self.week, self.day)
   ...     @classmethod
   ...     def with_thousands(cls, thousands, week, day):
   ...         return cls(1000 * thousands + week, day)
   ...     _classmethods = [with_thousands]
   ...
   >>> datetime2.register_new_calendar('week_count', SimpleWeekCalendar)
   >>> d1 = Date.week_count(1, 1)
   >>> d1.gregorian
   GregorianCalendarInDate(1, 1, 1)
   >>> d2 = Date.gregorian(2013, 4, 26)
   >>> d2.week_count
   SimpleWeekCalendarInDate(104998, 5)

Under the hood, this simple implementation hides some magic. First of all,
the Date attribute becomes a context-dependent attribute, i.e. an attribute
that returns a different content when retrieved from a class or from an
instance. To see how this is implemented, a good starting point is python.org's
`Descriptor HowTo Guide <http://docs.python.org/3.3/howto/descriptor.html>`_.

The call to :func:`~datetime2.register_new_calendar` adds to the
:class:`~datetime2.Date` class an instance of the following class:

.. class:: CalendarAttribute(attribute_name, CalendarClass)

   Return an object able to implement a context dependent attribute for the
   :class:`~datetime2.Date` class, such that:

   *  When called in class context, the attribute returns a
      :class:`~datetime2.Date` instance with an attribute of the same name
      populated with a subclass of ``CalendarClass`` described below.
   *  When called in instance context:

      *  if the instance has the requested calendar attribute, it is returned;
      *  if the instance does not have the requested attribute and it is one
         of the registered calendars, a new attribute is generated, with a
         subclass of the corresponding calendar class;
      *  if the instance does not have the requested attribute and it is not
         one of the registered calendars, an :exc:`AttrbuteError` exception is
         generated.

When a :class:`~datetime2.Date` instance has an attribute that corresponds to a
registered calendar, its type is a subclass of the original calendar class.
This subclass is such that all methods originally generating a calendar
instance (including the constructors) now return a :class:`~datetime2.Date`
instance.

This subclass is generated dynamically at registration time. To accomplish
this, the only requirement is that the class attributes :ref:`listed above
<class-attributes-to-fill>` must be populated. They can be left out only if
they are empty.

