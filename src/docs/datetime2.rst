.. toctree::

:mod:`datetime2` --- New date and time classes
==============================================

.. module:: datetime2
   :synopsis: Date and time types with broader calendar coverage.
.. moduleauthor:: Francesco Ricciardi <francescor2010@yahoo.it>

The :mod:`datetime2` module provides classes to manipulate date and time
like the :mod:`datetime` module does. However, its aim is to provide a
flexible framework in order to provide:

* decoupling between operations on date and time objects and their
  representation;
* access to different calendars, for input parsing and output formatting;
* access to different time measurement systems, also for input and output;
* internationalization;
* implementation of the part of the Unicode Locale Database concerned with
  dates and times;
* interface with other Python modules or inclusion of their
  functionalities in its submodules.

However, the above objectives are long term ones, so stay tuned for
improvement!

Available calendars and time measuring systems will be discovered at
import time. Additionally, registering new systems at run time is also
possible.


.. seealso::

   Module :mod:`datetime`
      Basic date and time types.

   Module :mod:`calendar`
      General calendar related functions.

   Module :mod:`time`
      Time access and conversions.


