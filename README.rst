datetime2
=========

.. image:: https://readthedocs.org/projects/datetime2/badge/?version=stable
   :target: https://datetime2.readthedocs.io/en/stable/?badge=stable

.. image:: https://img.shields.io/pypi/v/datetime2.svg
   :target: https://pypi.org/project/datetime2/

.. image:: https://img.shields.io/pypi/status/datetime2.svg
   :target: https://pypi.org/project/datetime2/

.. image:: https://img.shields.io/pypi/pyversions/datetime2.svg
   :target: https://pypi.org/project/datetime2/

.. image:: https://github.com/fricciardi/datetime2/actions/workflows/push-workflow.yml/badge.svg
   :target: https://github.com/fricciardi/datetime2/actions/workflows/push-workflow.yml
   :alt: Build Status

.. image:: https://img.shields.io/pypi/l/datetime2.svg
   :target: https://opensource.org/licenses/BSD-3-Clause


The `datetime2 <http://pypi.org/project/datetime2>`_ module provides similar
features to those given by the standard
`datetime <https://docs.python.org/3/library/datetime.html>`_ module,
adding the capability of constructing and representing date and time in many
formats. Additionally, it removes a few limits that the original package has.

*datetime2* is a one-man, free-time work. Project is hosted at GitHub, please
follow the source code link on the right to see the latest version of this
page (e.g. for an updated release map).

Current and future releases
===========================

Current:

* 0.9.4: Implementation of WesternTimeDelta

Planned:

* 1.0: Implementation of DateTime, first production release
* 1.1: Implementation of Julian and Hebrew calendars

Project objectives
==================

* Decoupling between operations on date and time objects and their
  representation.
* Access to different calendars, for input parsing and output formatting.
* Access to different time representations, also for input and output.
* Infinite precision in converting between different time representations.
* Ability to dynamically register new formatting classes.
* Internationalization.
* Implementation of the part of the Unicode Locale Database concerned with
  dates and times.
* Interface with other Python modules or inclusion of their
  functionalities in submodules.

These objectives are very long term ones, which I am setting because I think it is
important to establish a direction for the project.

License
=======

Datetime2 is distributed under the terms of the new BSD license. You are free
to use it for commercial or non-commercial projects with little or no
restriction, all I ask is that:

* Redistributions of the code, in whole or part, retain the original
  copyright notice and license text.
* You do not claim my endorsement of any derived product.

For a complete text of the license see the LICENSE.txt file in the source distribution.
