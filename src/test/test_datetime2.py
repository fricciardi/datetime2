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
import pickle
import unittest
from datetime2 import Date, TimeDelta
from datetime2.calendars.gregorian import GregorianCalendar
from fractions import Fraction

INF = float("inf")
NAN = float("nan")

# contains all pickle protocols
pickle_choices = [(pickle, pickle, proto)
                  for proto in range(pickle.HIGHEST_PROTOCOL + 1)]
assert len(pickle_choices) == pickle.HIGHEST_PROTOCOL + 1


#############################################################################
# Date tests
#
class TestDate(unittest.TestCase):
    def test_000_valid_parameter_types(self):
        for par in (-2, -1, 0, 1, 2, -1000, 1000, -123456789, 123456789, -999999999, 999999999, -1000000000, 1000000000):
            self.assertEqual(Date(par).day_count, par, msg = 'par = {}'.format(par))
        cal_obj = GregorianCalendar(1, 1, 1)
        self.assertEqual(Date(cal_obj).day_count, 1, "Object with to_rata_die")

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
            # exception when to_rata_die method does not return an integer
        class Test:
            def to_rata_die(self):
                return 1.1
        self.assertRaises(TypeError, Date, Test())

    def test_020_today(self):
        # for the time being, let's use the good old datetime module :-)
        import datetime
        
        # we need to ensure that we are not testing across date change
        for dummy in range(3):
            today = Date.today()
            # let's use the good old date module
            day_count = datetime.date.today().toordinal()
            if day_count != today.day_count:
                break
        self.assertEqual(today.day_count, day_count)

    def test_030_write_attribute(self):
        d = Date(1)
        self.assertRaises(AttributeError, setattr, d, 'day_count', 3)

    def test_040_get_unknown_attribute(self):
        self.assertRaises(AttributeError, getattr, Date, 'unknown')
        d = Date(1)
        self.assertRaises(AttributeError, getattr, d, 'unknown')

    def test_100_computations(self):
        eq = self.assertEqual

        a = Date(0)
        b = Date(-3)
        c = Date(5)
        zero = TimeDelta(0)
        one = TimeDelta(1)
        minusone = TimeDelta(-1)
        
        # Addition between Date and TimeDelta, reverse is not defined
        eq(a + zero, Date(0), msg = 'a + zero')
        eq(a + one, Date(1), msg = 'a + one')
        eq(a + minusone, Date(-1), msg = 'a + minusone')
        eq(b + zero, Date(-3), msg = 'b + zero')
        eq(b + one, Date(-2), msg = 'b + one')
        eq(b + minusone, Date(-4), msg = 'b + minusone')
        eq(c + zero, Date(5), msg = 'c + zero')
        eq(c + one, Date(6), msg = 'c + one')
        eq(c + minusone, Date(4), msg = 'c + minusone')

        # subtraction between Date and TimeDelta, reverse is not defined        
        eq(a - zero, Date(0), msg = 'a - zero')
        eq(a - one, Date(-1), msg = 'a - one')
        eq(a - minusone, Date(1), msg = 'a - minusone')
        eq(b - zero, Date(-3), msg = 'b - zero')
        eq(b - one, Date(-4), msg = 'b - one')
        eq(b - minusone, Date(-2), msg = 'b - minusone')
        eq(c - zero, Date(5), msg = 'c - zero')
        eq(c - one, Date(4), msg = 'c - one')
        eq(c - minusone, Date(6), msg = 'c - minusone')
        
        
    def test_110_disallowed_computations(self):
        a = Date(42)
        b = Date(24)

        # Add/sub int, float, string, complex, specials and containers should be illegal
        for obj in (10, 34.5, "abc", 1 + 2j, INF, NAN, {}, [], ()):
            self.assertRaises(TypeError, lambda: a + obj)
            self.assertRaises(TypeError, lambda: a - obj)
            self.assertRaises(TypeError, lambda: obj + a)
            self.assertRaises(TypeError, lambda: obj - a)

        # These operations make no sense for Date objects
        self.assertRaises(TypeError, lambda: TimeDelta(2) + a)  # reverse is valid
        self.assertRaises(TypeError, lambda: TimeDelta(2) - a)  # reverse is valid
        
        self.assertRaises(TypeError, lambda: a * 1)
        self.assertRaises(TypeError, lambda: 1 * a)
        self.assertRaises(TypeError, lambda: 1.1 * a)
        self.assertRaises(TypeError, lambda: a * 1.1)
        self.assertRaises(TypeError, lambda: a / 1.1)
        self.assertRaises(TypeError, lambda: a / 1)
        self.assertRaises(TypeError, lambda: 1 / a)
        self.assertRaises(TypeError, lambda: 1.1 / a)
        self.assertRaises(TypeError, lambda: a // 1.1)
        self.assertRaises(TypeError, lambda: a // 1)
        self.assertRaises(TypeError, lambda: 1 // a)
        self.assertRaises(TypeError, lambda: 1.1 // a)
        self.assertRaises(TypeError, pow, a, 1)
        self.assertRaises(TypeError, pow, 1, a)
        self.assertRaises(TypeError, pow, a, 1.1)
        self.assertRaises(TypeError, pow, 1.1, a)
        self.assertRaises(TypeError, lambda: a ** 1)
        self.assertRaises(TypeError, lambda: 1 ** a)
        self.assertRaises(TypeError, lambda: 1.1 ** a)
        self.assertRaises(TypeError, lambda: a ** 1.1)
        self.assertRaises(TypeError, lambda: a ** b)
        self.assertRaises(TypeError, lambda: a << 1)
        self.assertRaises(TypeError, lambda: 1 << a)
        self.assertRaises(TypeError, lambda: a << 1.1)
        # self.assertRaises(TypeError, lambda: 1.1 << a) not applicable to float
        self.assertRaises(TypeError, lambda: a << b)
        self.assertRaises(TypeError, lambda: a >> 1)
        self.assertRaises(TypeError, lambda: 1 >> a)
        self.assertRaises(TypeError, lambda: a >> 1.1)
        # self.assertRaises(TypeError, lambda: 1.1 >> a) not applicable to float
        self.assertRaises(TypeError, lambda: a >> b)
        

    def test_120_compare(self):
        d1 = Date(42)
        d2 = Date(24)
        d3 = Date(42)
        self.assertEqual(d1, d3)
        self.assertNotEqual(d2, d3)
        self.assertGreaterEqual(d1, d3)
        self.assertLessEqual(d1, d3)
        self.assertGreater(d1, d2)
        self.assertLess(d2, d1)

        for badarg in (10, 34.5, "abc", 1 + 2j, INF, NAN, {}, [], ()):
            self.assertFalse(d1 == badarg)
            self.assertTrue(d1 != badarg)
            self.assertFalse(badarg == d1)
            self.assertTrue(badarg != d1)

            self.assertRaises(TypeError, lambda: d1 <= badarg)
            self.assertRaises(TypeError, lambda: d1 < badarg)
            self.assertRaises(TypeError, lambda: d1 > badarg)
            self.assertRaises(TypeError, lambda: d1 >= badarg)
            self.assertRaises(TypeError, lambda: badarg <= d1)
            self.assertRaises(TypeError, lambda: badarg < d1)
            self.assertRaises(TypeError, lambda: badarg > d1)
            self.assertRaises(TypeError, lambda: badarg >= d1)

    def test_130_bool(self):
        self.assertTrue(Date(3))
        self.assertTrue(Date(0))
        self.assertTrue(Date(-3))

    def test_140_str(self):
        for count in (0, -1, 1, -1000, 1000, 99999999, 99999999):
            self.assertEqual(str(Date(count)), 'R.D. {}'.format(count))

    def test_150_roundtrip(self):
        for count in (0, -1, 1, -1000, 1000, 99999999, 99999999):
            # Verify date -> string -> date identity.
            d1 = Date(count)
            s = repr(d1)
            d2 = eval(s)
            self.assertEqual(d1, d2)

    # TODO: add tests for subclassing Date

    def test_210_hash_equality(self):
        d1 = Date(42)
        d2 = Date(32) + TimeDelta(10)
        self.assertEqual(hash(d1), hash(d2))

        d = {d1: 1, d2: 2}
        self.assertEqual(len(d), 1)
        self.assertEqual(d[d1], 2)

    def test_220_pickling(self):
        orig = Date(3141592)
        for pickler, unpickler, proto in pickle_choices:
            green = pickler.dumps(orig, proto)
            derived = unpickler.loads(green)
            self.assertEqual(orig, derived)


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