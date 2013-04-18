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
from datetime2 import Date, TimeDelta
from datetime2.calendars.gregorian import GregorianCalendar
from fractions import Fraction

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



class TestDateCalendarInterface(unittest.TestCase):
    # these tests are using the Gregorian and ISO calendars, but could have
    # been done with other calendars
    # TODO: understand if interface tests can have calendars as parameters
    def test_000_constructors(self):
        # constructors return a Date
        self.assertIsInstance(Date.gregorian(2, 1, 1), Date, msg="Date.gregorian creates a Date")
        self.assertIsInstance(Date.gregorian.year_day(1, 1), Date, msg="Date.gregorian.year_day creates a Date")
        # constructed calendar is always the same
        d1 = Date(2)
        d1_id = id(d1.gregorian)
        self.assertEqual(id(d1.gregorian), d1_id, msg = 'constructed caledar instance is always the same')

    def test_050_calendar_attributes(self):
        # a Date instance does not have a calendar in __dict__, but the class definition has it
        d = Date(4)
        self.assertRaises(AttributeError, getattr, d.__dict__, 'gregorian')
        self.assertTrue(hasattr(d, 'gregorian'))

    def test_100_calendar_type_is_correct(self):
        # instance created with Date
        d1 = Date(2)
        self.assertIsInstance(d1.gregorian, GregorianCalendar, msg="Calendar type is correct with instance created with Date")
        # instance created with GregorianCalendar
        d2 = Date.gregorian(2, 2, 2)
        self.assertIsInstance(d2.gregorian, GregorianCalendar, msg="Calendar type is correct with instance created with GregorianCalendar")
        # instance created with IsoCalendar
        # TODO: uncomment when iso calendar has been done
#        d3 = Date.iso(2, 2, 2)
#        self.assertIsInstance(d3.gregorian, GregorianCalendar, msg="Calendar type is correct with instance created with IsoCalendar")

    def test_200_static_method_always_accessible(self):
        self.assertTrue(Date.gregorian.is_leap_year(2000), msg="Static method through class")
        # instance created with Date
        d1 = Date(2)
        self.assertTrue(d1.gregorian.is_leap_year(2000), msg="Static method through instance created with Date")
        # instance created with GregorianCalendar
        d2 = Date.gregorian(2, 2, 2)
        self.assertTrue(d2.gregorian.is_leap_year(2000), msg="Static method through instance created with GregorianCalendar")
        # instance created with IsoCalendar
        # TODO: uncomment when iso calendar has been done
#        d3 = Date.iso(2, 2, 2)
#        self.assertTrue(d3.gregorian.is_leap_year(2000), msg="Static method through instance created with IsoCalendar")

    def test_900_avoid_date_override(self):
        d = Date.gregorian(1, 1, 1)
        # I do not want an instance of Date created through a Gregorian to have its static methods
        # One of the implementation I used had this error and I want to avoid it
        self.assertRaises(AttributeError, getattr, d, 'is_leap_year')