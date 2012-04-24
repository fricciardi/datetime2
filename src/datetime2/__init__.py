# datetime2 package main file

# Copyright (c) 2011 Francesco Ricciardi
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, 
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name(s) of the copyright holders nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AS IS AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL THE COPYRIGHT HOLDERS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, 
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

__author__ = 'Francesco Ricciardi <francescor2010 at yahoo.it>'


from math import floor
from functools import total_ordering

import datetime2.osinterface
import datetime2.gregorian


__all__ = ['Date', 'TimeDelta']


##############################################################################
# support classes and functions
#
def constructor_wrapper(meth, wrapping_class, attr_to_set, method_to_call):
    def new_method(*args):
        ret_obj = meth(*args)
        if hasattr(ret_obj, method_to_call):
            wrapping_obj = wrapping_class(getattr(ret_obj, method_to_call)())
            setattr(wrapping_obj, attr_to_set, ret_obj)
            return wrapping_obj
        else:
            return ret_obj
    return new_method

class DynamicAttributeProxy:
    def __init__(self, proxying_class, attr_to_set, proxied_class, meth_to_call):
        self.proxying_class = proxying_class
        self.attr_to_set = attr_to_set
        self.proxied_class = proxied_class
        self.meth_to_call = meth_to_call

    def __call__(self, *args, **kwargs):
        retobj = self.proxied_class(*args, **kwargs)
        proxying_obj = self.proxying_class(getattr(retobj, self.meth_to_call)())
        setattr(proxying_obj, self.attr_to_set, retobj)
        return proxying_obj

    def __getattr__(self, name):
        attr_obj = getattr(self.proxied_class, name)
        if callable(attr_obj):
            return constructor_wrapper(attr_obj, self.proxying_class, self.attr_to_set, self.meth_to_call)
        else:
            return attr_obj

class DynamicAtributeMeta(type):
    """ We need a metaclass because we want to redefine how core classes will
    find the calendars or time representations they need using the attribute
    notation.
    """
    def __new__(mcs, name, bases, classdict):
        """Check at creation time that class defines the following
        attributes:
          - dynamic_attrs : the dictionary that contains or will contain the
            dynamic class constructors and methods
          - method_to_call : name of the method that has to be called to
            retrieve the value to be set in the proxing cls
        """
        #TODO add check that values are identifiers
        if ("dynamic_attrs" in classdict and
            "method_to_call" in classdict):
            return type.__new__(mcs, name, bases, classdict)
        else:
            raise NotImplementedError("Classes of DynamicDatetimeMeta type should have two attributes.")

    def __getattr__(cls, name):
        if name in cls.dynamic_attrs:
            return DynamicAttributeProxy(cls, name, cls.dynamic_attrs[name], cls.method_to_call)
        else:
            raise AttributeError("type object '{}' has no attribute '{}'".format(cls.__name__, name))

class DynamicAttrsCls:
    def __getattr__(self, name):
        if name in self.dynamic_attrs:
            attr_obj = self.dynamic_attrs[name].from_rata_die(self.day_count)
            setattr(self, name, attr_obj)
            return attr_obj
        else:
            raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, name))

class CalendarObjectProxy:
    def __init__(self, calendar_obj):
        self.calendar_obj = calendar_obj


class CalendarClassMethodProxy:
    def __init__(self, method, proxying_class, calendar_class, attr_name):
        self.method = method
        self.proxying_class = proxying_class
        self.calendar_class = calendar_class
        self.attr_name = attr_name

    def __call__(self, *args, **kwargs):
        return_obj = self.method(*args, **kwargs)
        if isinstance(return_obj, self.calendar_class):
            proxying_obj = self.proxying_class.from_rata_die(return_obj.to_rata_die())
            setattr(proxying_obj, self.attr_name, CalendarObjectProxy(return_obj, self.proxying_class))
            return proxying_obj
        else:
            return return_obj


class CalendarClassProxy:
    def __init__(self, proxying_class, calendar_class, attr_name):
        self.proxying_class = proxying_class
        self.calendar_cls = calendar_class
        self.attr_name = attr_name

    def __call__(self, *args, **kwargs):
        calendar_obj = self.calendar_cls(*args, **kwargs)
        proxying_obj = self.proxying_class.from_rata_die(calendar_obj.to_rata_die())
        setattr(proxying_obj, self.attr_name, CalendarObjectProxy(calendar_obj, self.proxying_class))
        return proxying_obj

    def __getattr__(self, name):
        return CalendarClassMethodProxy(getattr(self.calendar_cls, name), self.proxying_class, self.calendar_cls)

class ContextDependentCalendarAttribute:
    def __init__(self, name, calendar_cls):
        self.name = '_' + name
        self.calendar_cls = calendar_cls

    def __get__(self, obj, cls):
        if obj == None:
            return CalendarClassProxy(cls, self.calendar_cls, self.name)
        else:
            return getattr(obj, self.name)


##############################################################################
# calendar classes for Date objects
#
#class GregorianCalendarToDate(datetime2.gregorian.GregorianCalendar):
#    def replace(self, ):
#
#        pass


##############################################################################
# interface with calendars and time representations
#
_identifier_name_re = re.compile("[a-zA-Z][_a-zA-Z]*")

def register_calendar(name, calendar):
    if not _identifier_restricted_re.match(name):
        raise RuntimeError("Calendar must have a valid name.")
    if not hasattr(calendar, 'to_rata_die') or not callable(getattr(calendar, 'to_rata_die')):
        raise RuntimeError("Calendar must have a callable 'to_rata_die' function.")
    if not hasattr(calendar, 'from_rata_die') or not callable(getattr(calendar, 'from_rata_die')):
        raise RuntimeError("Calendar must have a callable 'to_rata_die' function.")
    setattr(datetime2.Date, name, obj)

#TODO: generalize registration process, so that other classes can use it
#TODO: add code to manage the calendars (list, check if present, etc)

#register_calendar('gregorian', datetime2.gregorian.GregorianCalendar)


##############################################################################
# Core classes
#

class TimeDelta:
    # This is a stub in version 0.2
    def __init__(self, days):
        self._days = days
        
    def __repr__(self):
        return "TimeDelta({})".format(self.days)
    
    @property
    def days(self):
        return self._days
    
    def __add__(self, other):
        raise TypeError   # required to let Date tests pass

@total_ordering
class Date(DynamicAttrsCls, metaclass=DynamicAtributeMeta):
    dynamic_attrs = _datetime2_calendars
    method_to_call = "to_rata_die"

    def __init__(self, day_count):
        if isinstance(day_count, int):
            self._day_count = day_count
        else:
            raise TypeError("an integer is required")

    @classmethod
    def today(cls):
        return cls(floor(datetime2.osinterface.get_moment()))

    @property
    def day_count(self):
        return self._day_count
    
    def __repr__(self):
        return "Date({})".format(self.day_count)
    
    def __str__(self):
        return "R.D. {}".format(self.day_count)
    
    def __add__(self, other):
        if isinstance(other, TimeDelta):
            return Date(self.day_count + other.days)
        else:
            return NotImplemented
        
    def __radd__(self, other):
        return self + other
    
    def __sub__(self, other):
        if isinstance(other, Date):
            return TimeDelta(self.day_count - other.day_count)
        elif isinstance(other, TimeDelta):
            return Date(self.day_count - other.days)
        else:
            return NotImplemented
        
    # TODO: undestand if we want to use total ordering
    def __eq__(self, other):
        return isinstance(other, Date) and self.day_count == other.day_count

    def __lt__(self, other):
        if isinstance(other, Date):
            return self.day_count < other.day_count
        else:
            return NotImplemented
        
    def __hash__(self):
        return hash(self._day_count)
