datetime2
=========

[![Documentation Status](https://readthedocs.org/projects/datetime2/badge/?version=stable)](https://datetime2.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://github.com/fricciardi/datetime2/actions/workflows/publish-workflow.yml/badge.svg)](https://github.com/fricciardi/datetime2/actions/workflows/publish-workflow.yml)
[![License](https://img.shields.io/badge/License-BSD-green.svg)](https://opensource.org/licenses/BSD-3-Clause)


The *datetime2* module implements the same features the standard
[datetime](https://docs.python.org/3/library/datetime.html) module, and adds the 
capability of constructing and representing date and time in many formats. 
Additionally, it removes a few limits that the original package has.


*datetime2* is a one-man, free-time work.  

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
