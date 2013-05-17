# datetime2 package test

# Copyright (c) 2011-2012 Francesco Ricciardi
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


import decimal
import fractions
import pickle
import unittest
from fractions import Fraction
from datetime2 import Date, TimeDelta
from calendars.gregorian import GregorianCalendar
from calendars.iso import IsoCalendar


INF = float("inf")
NAN = float("nan")

date_test_data = (-2, -1, 0, 1, 2, -1000, 1000, -123456789, 123456789, -999999999, 999999999, -1000000000, 1000000000)


#############################################################################
# Date tests
#
class TestDate(unittest.TestCase):
    def test_000_valid_parameter_types(self):
        for day_count in date_test_data:
            self.assertEqual(Date(day_count).day_count, day_count, msg = 'day_count = {}'.format(day_count))

    def test_010_invalid_parameter_types(self):
        # exception with no or two parameters
        self.assertRaises(TypeError, Date)
        self.assertRaises(TypeError, Date, 1, 2)
        # exception with non-numeric types
        for par in ("1", (1,), [1], {1:1}, (), [], {}, None):
            self.assertRaises(TypeError, Date, par)
            # exception with invalid numeric types
        for par in (1.0, Fraction(1, 1), decimal.Decimal(1), 1j):
            self.assertRaises(TypeError, Date, par)

    def test_020_today(self):
        # for the time being, let's use the good old datetime module :-)
        import datetime
        
        # we need to ensure that we are not testing across date change
        for dummy in range(3):
            today_before = datetime.date.today()
            date_today = Date.today()
            today_after = datetime.date.today()
            if today_before == today_after:
                break
        self.assertEqual(date_today.day_count, today_before.toordinal())

    def test_100_write_attribute(self):
        d = Date(1)
        self.assertRaises(AttributeError, setattr, d, 'day_count', 3)

    def test_110_get_unknown_attribute(self):
        # I want to do this, because Date will have attributes added at runtime
        # let's test this both on class and instance
        self.assertRaises(AttributeError, getattr, Date, 'unknown')
        d = Date(1)
        self.assertRaises(AttributeError, getattr, d, 'unknown')

    def test_120_create_from_attr(self):
        for day_count in date_test_data:
            d = Date(day_count)
            self.assertEqual(d, Date(d.day_count), msg = 'Create from attribute, dya_count = {}'.format(day_count))

    def test_300_operations(self):
        a = Date(0)
        b = Date(-3)
        c = Date(5)
        zero = TimeDelta(0)
        one = TimeDelta(1)
        minusone = TimeDelta(-1)
        
        # Addition between Date and TimeDelta, reverse is not defined
        self.assertEqual(a + zero, Date(0), msg = 'a + zero')
        self.assertEqual(a + one, Date(1), msg = 'a + one')
        self.assertEqual(a + minusone, Date(-1), msg = 'a + minusone')
        self.assertEqual(b + zero, Date(-3), msg = 'b + zero')
        self.assertEqual(b + one, Date(-2), msg = 'b + one')
        self.assertEqual(b + minusone, Date(-4), msg = 'b + minusone')
        self.assertEqual(c + zero, Date(5), msg = 'c + zero')
        self.assertEqual(c + one, Date(6), msg = 'c + one')
        self.assertEqual(c + minusone, Date(4), msg = 'c + minusone')

        # subtraction between Date and TimeDelta, reverse is not defined        
        self.assertEqual(a - zero, Date(0), msg = 'a - zero')
        self.assertEqual(a - one, Date(-1), msg = 'a - one')
        self.assertEqual(a - minusone, Date(1), msg = 'a - minusone')
        self.assertEqual(b - zero, Date(-3), msg = 'b - zero')
        self.assertEqual(b - one, Date(-4), msg = 'b - one')
        self.assertEqual(b - minusone, Date(-2), msg = 'b - minusone')
        self.assertEqual(c - zero, Date(5), msg = 'c - zero')
        self.assertEqual(c - one, Date(4), msg = 'c - one')
        self.assertEqual(c - minusone, Date(6), msg = 'c - minusone')
        
        
    def test_310_disallowed_operations(self):
        import operator

        a = Date(42)
        b = Date(24)

        # Add/sub int, float, string, complex, specials and containers should be illegal
        for obj in (10, 34.5, "abc", 1 + 2j, INF, NAN, {}, [], ()):
            self.assertRaises(TypeError, operator.add, a, obj)
            self.assertRaises(TypeError, operator.sub, a, obj)
            self.assertRaises(TypeError, operator.add, obj, a)
            self.assertRaises(TypeError, operator.sub, obj, a)

        # These operations make no sense for Date objects
        self.assertRaises(TypeError, operator.add, TimeDelta(2), a)  # reverse is valid
        self.assertRaises(TypeError, operator.sub, TimeDelta(2), a)  # reverse is valid
        
        self.assertRaises(TypeError, operator.mul, a, 1)
        self.assertRaises(TypeError, operator.mul, 1, a)
        self.assertRaises(TypeError, operator.mul, 1.1, a)
        self.assertRaises(TypeError, operator.mul, a, 1.1)
        self.assertRaises(TypeError, operator.truediv, a, 1.1)
        self.assertRaises(TypeError, operator.truediv, a, 1)
        self.assertRaises(TypeError, operator.truediv, 1, a)
        self.assertRaises(TypeError, operator.truediv, 1.1, a)
        self.assertRaises(TypeError, operator.floordiv, a, 1.1)
        self.assertRaises(TypeError, operator.floordiv, a, 1)
        self.assertRaises(TypeError, operator.floordiv, 1, a)
        self.assertRaises(TypeError, operator.floordiv, 1.1, a)
        self.assertRaises(TypeError, pow, a, 1, 3)
        self.assertRaises(TypeError, pow, 1, a, 3)
        self.assertRaises(TypeError, pow, a, 1.1, 3)
        self.assertRaises(TypeError, pow, 1.1, a, 3)
        self.assertRaises(TypeError, operator.pow, a, 1)
        self.assertRaises(TypeError, operator.pow, 1, a)
        self.assertRaises(TypeError, operator.pow, 1.1, a)
        self.assertRaises(TypeError, operator.pow, a, 1.1)
        self.assertRaises(TypeError, operator.pow, a, b)
        self.assertRaises(TypeError, operator.lshift, a, 1)
        self.assertRaises(TypeError, operator.lshift, 1, a)
        self.assertRaises(TypeError, operator.lshift, a, 1.1)
        self.assertRaises(TypeError, operator.lshift, 1.1, a)
        self.assertRaises(TypeError, operator.lshift, a, b)
        self.assertRaises(TypeError, operator.rshift, a, 1)
        self.assertRaises(TypeError, operator.rshift, 1, a)
        self.assertRaises(TypeError, operator.rshift, a, 1.1)
        self.assertRaises(TypeError, operator.rshift, 1.1, a)
        self.assertRaises(TypeError, operator.rshift, a, b)

    def test_320_compare(self):
        d1 = Date(42)
        d2 = Date(42)
        self.assertEqual(d1, d2)
        self.assertTrue(d1 <= d2)
        self.assertTrue(d1 >= d2)
        self.assertFalse(d1 != d2)
        self.assertFalse(d1 < d2)
        self.assertFalse(d1 > d2)

        d2 = Date(4242)   # this is larger than d1
        self.assertTrue(d1 < d2)
        self.assertTrue(d2 > d1)
        self.assertTrue(d1 <= d2)
        self.assertTrue(d2 >= d1)
        self.assertTrue(d1 != d2)
        self.assertTrue(d2 != d1)
        self.assertFalse(d1 == d2)
        self.assertFalse(d2 == d1)
        self.assertFalse(d1 > d2)
        self.assertFalse(d2 < d1)
        self.assertFalse(d1 >= d2)
        self.assertFalse(d2 <= d1)

    def test_330_compare_invalid_types(self):
        import operator

        class SomeClass:
            pass

        d = Date(1)

        # exception with non-numeric types
        for par in ("1", (1,), [1], {1:1}, (), [], {}, None):
            self.assertFalse(d == par)
            self.assertTrue(d != par)
            self.assertRaises(TypeError, operator.lt, d, par)
            self.assertRaises(TypeError, operator.gt, d, par)
            self.assertRaises(TypeError, operator.le, d, par)
            self.assertRaises(TypeError, operator.ge, d, par)
        # exception with numeric types (all invalid) and other objects
        for par in (1, 1.0, fractions.Fraction(1, 1), decimal.Decimal(1), 1j, 1 + 1j, INF, NAN, SomeClass()):
            self.assertFalse(d == par)
            self.assertTrue(d != par)
            self.assertRaises(TypeError, operator.lt, d, par)
            self.assertRaises(TypeError, operator.gt, d, par)
            self.assertRaises(TypeError, operator.le, d, par)
            self.assertRaises(TypeError, operator.ge, d, par)

    def test_340_hash_equality(self):
        d1 = Date(42)
        # same thing
        d2 = Date(42)
        self.assertEqual(hash(d1), hash(d2))

        dic = {d1: 1}
        dic[d2] = 2
        self.assertEqual(len(dic), 1)
        self.assertEqual(dic[d1], 2)
        self.assertEqual(dic[d2], 2)

        d1 = Date(42)
        # same thing
        d2 = Date(42)
        self.assertEqual(hash(d1), hash(d2))

        dic = {d1: 1}
        dic[d2] = 2
        self.assertEqual(len(dic), 1)
        self.assertEqual(dic[d1], 2)
        self.assertEqual(dic[d2], 2)

    def test_350_bool(self):
        for day_count in date_test_data:
            self.assertTrue(bool(Date(day_count)), msg = 'bool, day_count = {}'.format(day_count))

    def test_500_repr(self):
        import datetime2

        for day_count in date_test_data:
            d = Date(day_count)
            date_repr = repr(d)
            names, args = date_repr.split('(')
            self.assertEqual(names.split('.'), ['datetime2', 'Date'], msg='Repr test 1 for day count {}'.format(day_count))
            args = args[:-1] # drop ')'
            self.assertEqual(int(args), day_count, msg='Repr test 2 for day count {}'.format(day_count))
            self.assertEqual(d, eval(repr(d)), msg='Repr test 3 for day count {}'.format(day_count))

    def test_520_str(self):
        for day_count in date_test_data:
            d = Date(day_count)
            self.assertEqual(int(str(d)[5:]), day_count, msg='Str test for day count {}'.format(day_count))

    def test_900_pickling(self):
        for day_count in date_test_data:
            d = Date(day_count)
            for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
                pickled = pickle.dumps(d, protocol)
                derived = pickle.loads(pickled)
                self.assertEqual(d, derived)

    def test_920_subclass(self):

        class D(Date):
            theAnswer = 42

            def __init__(self, *args, **kws):
                temp = kws.copy()
                self.extra = temp.pop('extra')
                Date.__init__(self, *args, **temp)

            def newmeth(self, start):
                return start + (self.day_count * 3) // 2

        d1 = Date(2013)
        d2 = D(2013, extra = 7)

        self.assertEqual(d2.theAnswer, 42)
        self.assertEqual(d2.extra, 7)
        self.assertEqual(d1.day_count, d2.day_count)
        self.assertEqual(d2.newmeth(-7), (d1.day_count * 3) // 2 - 7)

class ExampleTestCalendar:  # probably one of the simplest form, it is also used in documentation as example
    def __init__(self, week, day):
        self.week = week
        self.day = day
    @classmethod
    def from_rata_die(cls, rata_die):
        return cls((rata_die - 1) // 7 + 1, (rata_die - 1) % 7 + 1)
    def to_rata_die(self):
        return 7 * (self.week - 1) + self.day

class TestCalendarInterface(unittest.TestCase):
    def tearDown(self):
        for name in [name for name in Date.__dict__.keys() if name.startswith('test_')]:
            delattr(Date, name)

    def test_000_register_new_calendar(self):
        assert not hasattr(Date, 'test_1')
        Date.register_new_calendar('test_1', ExampleTestCalendar)
        self.assertTrue(hasattr(Date, 'test_1'))

    def test_010_register_new_calendar_existing_calendar_or_attribute(self):
        self.assertRaises(AttributeError, Date.register_new_calendar, 'gregorian', ExampleTestCalendar)
        self.assertRaises(AttributeError, Date.register_new_calendar, 'day_count', ExampleTestCalendar)

    def test_020_register_new_calendar_invalid_attribute_name(self):
        self.assertRaises(ValueError, Date.register_new_calendar, '', ExampleTestCalendar)
        self.assertRaises(ValueError, Date.register_new_calendar, '123new', ExampleTestCalendar)
        self.assertRaises(ValueError, Date.register_new_calendar, 123, ExampleTestCalendar)

    def test_030_register_new_calendar_invalid_calendar_class(self):
        class NoFromCalendar:  # without from_rata_die
            def __init__(self, week, day):
                self.week = week
                self.day = day
            def to_rata_die(self):
                return 7 * (self.week - 1) + self.day

        self.assertRaises(TypeError, Date.register_new_calendar, 'test_1', NoFromCalendar)

        class NoToCalendar:  # without to_rata_die
            def __init__(self, week, day):
                self.week = week
                self.day = day
            @classmethod
            def from_rata_die(cls, rata_die):
                return cls((rata_die - 1) // 7 + 1, (rata_die - 1) % 7 + 1)

        self.assertRaises(TypeError, Date.register_new_calendar, 'test_2', NoToCalendar)

    def test_040_registered_attribute_simple_class(self):
        Date.register_new_calendar('test_1', ExampleTestCalendar)

        # Date attribute type and metaclass are correct
        self.assertEqual(Date.test_1.__name__, 'ExampleTestCalendarInDate', msg='Name of first test calendar (found {}).'.format(Date.test_1.__name__))
        self.assertEqual(type(Date.test_1).__name__, 'ModifiedClass', msg='Metaclass name of first test calendar (found {}).'.format(type(Date.test_1).__name__))
        self.assertTrue(issubclass(Date.test_1, ExampleTestCalendar), msg='Type of first test calendar.')

        # constructed date type and value are is correct
        d1a = Date.test_1(100, 4)
        self.assertEqual(type(d1a), Date, msg='Type of created instance with first test calendar.')
        self.assertEqual(d1a.day_count, 697, msg='Value of first test date is correct and recoverable.')

        # new attribute on date instance, type and value are correct
        d1b = Date(1000)
        self.assertIsInstance(d1b.test_1, ExampleTestCalendar, msg='Type of first test calendar (2).')
        self.assertEqual(type(d1b.test_1).__name__, 'ExampleTestCalendarInDate', msg='Metaclass name of first test calendar (2)(found {}).'.format(type(d1b.test_1).__name__))
        self.assertEqual(type(d1b.test_1.__class__).__name__, 'ModifiedClass', msg='Name of first test calendar (2) (found {}).'.format(type(d1b.test_1.__class__).__name__))
        self.assertEqual(d1b.test_1.week, 143, msg='Value of first test date attribute (1) is correct and recoverable.')
        self.assertEqual(d1b.test_1.day, 6, msg='Value of first test date attribute (2) is correct and recoverable.')

        # new attribute on date instance build by another calendar, type and value are correct
        d1c = Date.gregorian(100, 2, 3)
        self.assertIsInstance(d1c.test_1, ExampleTestCalendar, msg='Type of first test calendar (3).')
        self.assertEqual(type(d1c.test_1).__name__, 'ExampleTestCalendarInDate', msg='Metaclass name of first test calendar (3)(found {}).'.format(type(d1c.test_1).__name__))
        self.assertEqual(type(d1c.test_1.__class__).__name__, 'ModifiedClass', msg='Name of first test calendar (3) (found {}).'.format(type(d1b.test_1.__class__).__name__))
        self.assertEqual(d1c.test_1.week, 5171, msg='Value of first test date attribute (1) via gregorian is correct and recoverable.')
        self.assertEqual(d1c.test_1.day, 3, msg='Value of first test date attribute (2) via gregorian is correct and recoverable.')


    def test_043_registered_attribute_class_with_other_constructors(self):
        class ExampleTestCalendar2(ExampleTestCalendar):
            @classmethod
            def with_thousands(cls, thousands, week, day):
                return cls(1000 * thousands + week, day)

        Date.register_new_calendar('test_2', ExampleTestCalendar2)
        
        # Date attribute type and metaclass are correct
        self.assertEqual(Date.test_2.__name__, 'ExampleTestCalendar2InDate', msg='Name of second test calendar (found {}).'.format(Date.test_2.__name__))
        self.assertEqual(type(Date.test_2).__name__, 'ModifiedClass', msg='Metaclass name of second test calendar (found {}).'.format(type(Date.test_2).__name__))
        self.assertTrue(issubclass(Date.test_2, ExampleTestCalendar2), msg='Type of second test calendar.')

        # constructed date type and value are is correct
        d2a = Date.test_2(100, 4)
        self.assertEqual(type(d2a), Date, msg='Type of created instance with second test calendar.')
        self.assertEqual(d2a.day_count, 697, msg='Value of second test date is correct and recoverable.')
        d2d = Date.test_2.with_thousands(2, 3, 4)
        self.assertEqual(type(d2d), Date, msg='Type of created instance via non-default constructor with second test calendar.')
        self.assertEqual(d2d.day_count, 14018, msg='Value of second test date (non-default constructor) is correct and recoverable.')

        # new attribute on date instance, type and value are correct
        d2b = Date(1000)
        self.assertIsInstance(d2b.test_2, ExampleTestCalendar2, msg='Type of second test calendar (2).')
        self.assertEqual(type(d2b.test_2).__name__, 'ExampleTestCalendar2InDate', msg='Metaclass name of second test calendar (2)(found {}).'.format(type(d2b.test_2).__name__))
        self.assertEqual(type(d2b.test_2.__class__).__name__, 'ModifiedClass', msg='Name of second test calendar (2) (found {}).'.format(type(d2b.test_2.__class__).__name__))
        self.assertEqual(d2b.test_2.week, 143, msg='Value of second test date attribute (1) is correct and recoverable.')
        self.assertEqual(d2b.test_2.day, 6, msg='Value of second test date attribute (2) is correct and recoverable.')

        # new attribute on date instance build by another calendar, type and value are correct
        d2c = Date.gregorian(100, 2, 3)
        self.assertIsInstance(d2c.test_2, ExampleTestCalendar2, msg='Type of second test calendar (3).')
        self.assertEqual(type(d2c.test_2).__name__, 'ExampleTestCalendar2InDate', msg='Metaclass name of second test calendar (3)(found {}).'.format(type(d2c.test_2).__name__))
        self.assertEqual(type(d2c.test_2.__class__).__name__, 'ModifiedClass', msg='Name of second test calendar (3) (found {}).'.format(type(d2b.test_2.__class__).__name__))
        self.assertEqual(d2c.test_2.week, 5171, msg='Value of second test date attribute (1) via gregorian is correct and recoverable.')
        self.assertEqual(d2c.test_2.day, 3, msg='Value of second test date attribute (2) via gregorian is correct and recoverable.')

    def test_046_registered_attribute_class_with_static_methods(self):
        class ExampleTestCalendar3(ExampleTestCalendar):
            @staticmethod
            def is_odd(number):
                return (number % 2) == 1

        Date.register_new_calendar('test_3', ExampleTestCalendar3)

        # Date attribute type and metaclass are correct
        self.assertEqual(Date.test_3.__name__, 'ExampleTestCalendar3InDate', msg='Name of first test calendar (found {}).'.format(Date.test_3.__name__))
        self.assertEqual(type(Date.test_3).__name__, 'ModifiedClass', msg='Metaclass name of first test calendar (found {}).'.format(type(Date.test_3).__name__))
        self.assertTrue(issubclass(Date.test_3, ExampleTestCalendar3), msg='Type of first test calendar.')

        # constructed date type and value are is correct
        d3a = Date.test_3(100, 4)
        self.assertEqual(type(d3a), Date, msg='Type of created instance with first test calendar.')
        self.assertEqual(d3a.day_count, 697, msg='Value of first test date is correct and recoverable.')

        # new attribute on date instance, type and value are correct
        d3b = Date(1000)
        self.assertIsInstance(d3b.test_3, ExampleTestCalendar3, msg='Type of first test calendar (2).')
        self.assertEqual(type(d3b.test_3).__name__, 'ExampleTestCalendar3InDate', msg='Metaclass name of first test calendar (2)(found {}).'.format(type(d3b.test_3).__name__))
        self.assertEqual(type(d3b.test_3.__class__).__name__, 'ModifiedClass', msg='Name of first test calendar (2) (found {}).'.format(type(d3b.test_3.__class__).__name__))
        self.assertEqual(d3b.test_3.week, 143, msg='Value of first test date attribute (1) is correct and recoverable.')
        self.assertEqual(d3b.test_3.day, 6, msg='Value of first test date attribute (2) is correct and recoverable.')

        # new attribute on date instance build by another calendar, type and value are correct
        d3c = Date.gregorian(100, 2, 3)
        self.assertIsInstance(d3c.test_3, ExampleTestCalendar3, msg='Type of first test calendar (3).')
        self.assertEqual(type(d3c.test_3).__name__, 'ExampleTestCalendar3InDate', msg='Metaclass name of first test calendar (3)(found {}).'.format(type(d3c.test_3).__name__))
        self.assertEqual(type(d3c.test_3.__class__).__name__, 'ModifiedClass', msg='Name of first test calendar (3) (found {}).'.format(type(d3b.test_3.__class__).__name__))
        self.assertEqual(d3c.test_3.week, 5171, msg='Value of first test date attribute (1) via gregorian is correct and recoverable.')
        self.assertEqual(d3c.test_3.day, 3, msg='Value of first test date attribute (2) via gregorian is correct and recoverable.')

        # static method can be reached on the class and on all types of instance 
        self.assertTrue(Date.test_3.is_odd(3))
        self.assertFalse(Date.test_3.is_odd(4))
        self.assertTrue(d3a.test_3.is_odd(3))
        self.assertFalse(d3a.test_3.is_odd(4))
        self.assertTrue(d3b.test_3.is_odd(3))
        self.assertFalse(d3b.test_3.is_odd(4))
        self.assertTrue(d3c.test_3.is_odd(3))
        self.assertFalse(d3c.test_3.is_odd(4))

    def test_100_date_has_attributes_instance_not(self):
        # the date class aways has a registered attribute
        self.assertTrue(hasattr(Date, 'gregorian'), msg='Date class has attribute')
        # an instance created with another calendar or by Date does not have
        #   the attribute; it is instead is reachable via the Date class
        d1 = Date(4)
        self.assertRaises(AttributeError, getattr, d1.__dict__, 'gregorian')
        self.assertTrue(hasattr(d1, 'gregorian'), msg='Date instance has attribute via the class (1)')
        d2 = Date.iso(3, 4, 5)
        self.assertRaises(AttributeError, getattr, d2.__dict__, 'gregorian')
        self.assertTrue(hasattr(d2, 'gregorian'), msg='Date instance has attribute via the class (2)')
        # a Date instance created via the calendar does have the attribute
        d3 = Date.gregorian(3, 4, 5)
        self.assertTrue(hasattr(d3, 'gregorian'), msg='Date instance has attribute via the class (3)')

    def test_900_avoid_date_override(self):
        d = Date.gregorian(1, 1, 1)
        # I do not want an instance of Date created through a Gregorian to have its static methods
        # One of the implementation I used had this error and I want to avoid it
        self.assertRaises(AttributeError, getattr, d, 'is_leap_year')