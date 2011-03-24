# datetime2 test modules

"""Test the datetime2 module.

"""


import decimal
import pickle
import unittest

from datetime2 import Date, TimeDelta
from fractions import Fraction


INF = float("inf")
NAN = float("nan")

# contains all pickle protocols
pickle_choices = [(pickle, pickle, proto)
                  for proto in range(pickle.HIGHEST_PROTOCOL + 1)]
assert len(pickle_choices) == pickle.HIGHEST_PROTOCOL + 1


#############################################################################
# Date tests

class TestDate(unittest.TestCase):
    def test_000_valid_parameter_types(self):
        for par in (-2, -1, 0, 1, 2, -1000, 1000, -123456789, 123456789, -999999999, 999999999, -1000000000, 1000000000):
            self.assertEqual(Date(par).day_count, par)

    def test_010_invalid_parameter_types(self):
        # exception with no or two parameters
        self.assertRaises(TypeError, Date)
        self.assertRaises(TypeError, Date, 1, 2)
        # exception with non-numeric types
        for par in ("1", (1), [1], {1:1}, (), [], {}, None, True, False):
            self.assertRaises(TypeError, Date, par)
        # exception with invalid numeric types
        for par in (1.0, Fraction(1, 1), decimal.Decimal(1), 1j):
            self.assertRaises(TypeError, Date, par)

    def test_020_today(self):
        # let's use the good old datetime module :-)
        import datetime
        
        # we need to ensure that we are not testing across date change
        for dummy in range(3):
            today = Date.today()
            # let's use the good old date module
            t = datetime.date.today()
            # compute number of days from january 1st, 1
            days_before_year = 365 * (t.year - 1) + (t.year - 1) // 4 - (t.year - 1) // 100 + (t.year - 1) // 400
            days_before_month = sum([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30][:(t.month - 1)])
            leap_day =  0 if (t.month <= 2 or t.year % 4 != 0 or (t.year % 100 == 0 and t.year % 400 != 0)) else 1
            t_day_count = days_before_year + days_before_month + leap_day + t.day
            if t_day_count != today.day_count:
                break
        self.assertEqual(today.day_count, t_day_count)

    def test_030_write_attribute(self):
        d = Date(1)
        self.assertRaise(AttributeError, setattr, d, 'day_count', 3)
        self.assertRaise(AttributeError, setattr, d, 'dummy', 3)
        self.assertRaise(AttributeError, getattr, d, 'dummy')

    def test_100_computations(self):
        eq = self.assertEqual

        a = Date(0)
        b = Date(-3)
        c = Date(5)
        zero = TimeDelta(0)
        one = TimeDelta(1)
        minusone = TimeDelta(-1)
        
        # Addition between Date and TimeDelta, reverse is not defined
        eq(a + zero, Date(0))
        eq(a + one, Date(1))
        eq(a + minusone, Date(-1))
        eq(b + zero, Date(-3))
        eq(b + one, Date(-2))
        eq(b + minusone, Date(-4))
        eq(c + zero, Date(5))
        eq(c + one, Date(6))
        eq(c + minusone, Date(4))

        # subtraction between Date and TimeDelta, reverse is not defined        
        eq(a - zero, Date(0))
        eq(a - one, Date(-1))
        eq(a - minusone, Date(1))
        eq(b - zero, Date(-3))
        eq(b - one, Date(-4))
        eq(b - minusone, Date(-2))
        eq(c - zero, Date(5))
        eq(c - one, Date(4))
        eq(c - minusone, Date(6))
        
        
    def test_110_disallowed_computations(self):
        a = Date(42)
        b = Date(24)

        # Add/sub int, float, string, complex, specials and containers should be illegal
        for obj in (10, 34.5, "abc", 1 + 2j, INF, NAN, {}, [], ()):
            self.assertRaises(TypeError, lambda: a + obj)
            self.assertRaises(TypeError, lambda: a - obj)
            self.assertRaises(TypeError, lambda: obj + a)
            self.assertRaises(TypeError, lambda: obj - a)

        # These opertations make no sense for Date objects
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
        self.assertRaises(TypeError, lambda: 1.1 << a)
        self.assertRaises(TypeError, lambda: a << b)
        self.assertRaises(TypeError, lambda: a >> 1)
        self.assertRaises(TypeError, lambda: 1 >> a)
        self.assertRaises(TypeError, lambda: a >> 1.1)
        self.assertRaises(TypeError, lambda: 1.1 >> a)
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

        d = {d1: 1}
        d[d2] = 2
        self.assertEqual(len(d), 1)
        self.assertEqual(d[d1], 2)

    def test_220_pickling(self):
        orig = Date(3141592)
        for pickler, unpickler, proto in pickle_choices:
            green = pickler.dumps(orig, proto)
            derived = unpickler.loads(green)
            self.assertEqual(orig, derived)


if __name__ == "__main__":
    date_tests = unittest.TestLoader().loadTestsFromTestCase(TestDate)
    all_tests = unittest.TestSuite([date_tests])
    unittest.TextTestRunner().run(all_tests)
