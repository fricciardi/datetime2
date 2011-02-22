"""Test the datetime2 module.

"""


import decimal
import pickle
import unittest

from datetime2 import TimeDelta, WesternTD, BasicTD
from fractions import Fraction


INF = float("inf")
NAN = float("nan")

# contains all pickle protocols
pickle_choices = [(pickle, pickle, proto)
                  for proto in range(pickle.HIGHEST_PROTOCOL + 1)]
assert len(pickle_choices) == pickle.HIGHEST_PROTOCOL + 1


#############################################################################
# module tests
# None for the moment being  TODO: remove if not needed


#############################################################################
# TimeDelta tests
# The TimeDelta class is tested with the BasicTD class. It's better to do so,
# to ease testing the interface used by the other subclasses

class TestTimeDelta(unittest.TestCase):
    def test_000_valid_parameter_types(self):
        self.assertEqual(BasicTD("1").days, 1)
        self.assertEqual(BasicTD("1.0").days, 1)
        self.assertEqual(BasicTD("1.1").days, 1.1)
        self.assertEqual(BasicTD(1.0).days, 1)
        self.assertEqual(BasicTD(1.1).days, 1.1)
        self.assertEqual(BasicTD(decimal.Decimal("1")).days, 1)
        self.assertEqual(BasicTD(decimal.Decimal("1.1")).days, 1.1)
        self.assertEqual(BasicTD(1).days, 1)
        self.assertEqual(BasicTD(Fraction("1")).days, 1)
        self.assertEqual(BasicTD(Fraction("1.0")).days, 1)
        self.assertEqual(BasicTD(Fraction("1.1")).days, 1.1)

    def test_010_invalid_parameter_types(self):
        self.assertRaises(TypeError, BasicTD, BasicTD(1))
        self.assertRaises(TypeError, BasicTD, 1 + 2j)
        self.assertRaises(ValueError, BasicTD, INF)
        self.assertRaises(ValueError, BasicTD, NAN)

    def test_100_computations(self):
        eq = self.assertEqual
        td = BasicTD

        a = td(1) # One day
        b = td(10) # Ten days
        c = td("1/10") # One tenth of a day
        
        # Addition, subtraction, unary minus
        eq(a + b + c, td(11.1))
        eq(a + b, td(11))
        eq(a + c, td(1.1))
        eq(b + c, td(10.1))
        eq(a - b, td(-9))
        eq(b - a, td(9))
        eq(a - c, td(0.9))
        eq(c - a, td(-0.9))
        eq(b - c, td(9.9))
        eq(c - b, td(-9.9))
        eq(-a, td(-1))
        eq(-b, td(-10))
        eq(-c, td(-0.1))
        
        # absolute value
        eq(abs(a), a)
        eq(abs(-a), a)
        eq(abs(b), b)
        eq(abs(-b), b)
        eq(abs(c), c)
        eq(abs(-c), c)
        
        # Multiplication by integer or float, positive or negative
        eq(a*10, td(10))
        eq(a*10, 10*a)
        eq(a*1.2, td(1.2))
        eq(a*1.2, 1.2*a)
        eq(a*-10, td(-10))
        eq(a*-10, -a*10)
        eq(a*-1.2, td(-1.2))
        eq(a*-1.2, -a*1.2)
        eq(b*10, td(100))
        eq(b*10, 10*b)
        eq(b*1.2, td(12))
        eq(b*1.2, 1.2*b)
        eq(b*-10, td(-100))
        eq(b*-10, -b*10)
        eq(b*-1.2, td(-12))
        eq(b*-1.2, -b*1.2)
        eq(c*10, td(1))
        eq(c*10, 10*c)
        eq(c*1.2, td(0.12))
        eq(c*1.2, 1.2*c)
        eq(c*-10, td(-1))
        eq(c*-10, -c*10)
        eq(c*-1.2, td(-0.12))
        eq(c*-1.2, -c*1.2)

        # True division by integer or float, positive or negative
        eq(a/10, td(0.1))
        eq(a/1.25, td(0.8))
        eq(a/-10, td(-0.1))
        eq(a/-1.25, td(-0.8))
        eq(b/10, td(1))
        eq(b/1.25, td(8))
        eq(b/-10, td(-1))
        eq(b/-1.25, td(-8))
        eq(c/10, td(0.01))
        eq(c/1.25, td(0.08))
        eq(c/-10, td(-0.01))
        eq(c/-1.25, td(-0.08))

        # True division by TimeDelta (inverse of the tests above)
        eq(a/td(0.1), 10)
        eq(a/td(0.8), 1.25)
        eq(a/td(-0.1), -10)
        eq(a/td(-0.8), -1.25)
        eq(b/td(1), 10)
        eq(b/td(8), 1.25)
        eq(b/td(-1), -10)
        eq(b/td(-8), -1.25)
        eq(c/td(0.01), 10)
        eq(c/td(0.08), 1.25)
        eq(c/td(-0.01), -10)
        eq(c/td(-0.08), -1.25)

        # TODO: add tests for floor division, mod and divmod
        
        # TODO: add tests for __ceil__, __floor__ and __trunc__ .

    def test_110_disallowed_computations(self):
        a = BasicTD(42)
        b = BasicTD(24)
        z = BasicTD(0)

        # Add/sub int, float, string, complex, specials and containers should be illegal
        for obj in (10, 34.5, "abc", 1 + 2j, INF, NAN, {}, [], ()):
            self.assertRaises(TypeError, lambda: a + obj)
            self.assertRaises(TypeError, lambda: a - obj)
            self.assertRaises(TypeError, lambda: obj + a)
            self.assertRaises(TypeError, lambda: obj - a)

        # These opertations are not defined for TimeDelta
        self.assertRaises(TypeError, lambda: pow(a, 1))
        self.assertRaises(TypeError, lambda: pow(1, a))
        self.assertRaises(TypeError, lambda: pow(a, 1.1))
        self.assertRaises(TypeError, lambda: pow(1.1, a))
        self.assertRaises(TypeError, lambda: pow(a, b))
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
        
        # Division of integer or float by TimeDelta doesn't make sense.
        self.assertRaises(TypeError, lambda: 1 // a)
        self.assertRaises(TypeError, lambda: 1.1 // a)
        
        # Multiplication and divion of TimeDelta by string, complex, specials or 
        # containers should be illegal
        for obj in ("abc", 1 + 2j, INF, NAN, (), [], {}):
            self.assertRaises(TypeError, lambda: a * obj)
            self.assertRaises(TypeError, lambda: obj * a)
            self.assertRaises(TypeError, lambda: a / obj)
            self.assertRaises(TypeError, lambda: obj / a)
            
        # Division by zero doesn't make sense.
        self.assertRaises(ZeroDivisionError, lambda: a / 0)
        self.assertRaises(ZeroDivisionError, lambda: a / 0.0)
        self.assertRaises(ZeroDivisionError, lambda: a / z)

    def test_130_compare(self):
        t1 = BasicTD("2")
        t2 = BasicTD(2.0)
        self.assertEqual(t1, t2)
        self.assertTrue(t1 <= t2)
        self.assertTrue(t1 >= t2)
        self.assertTrue(not t1 != t2)
        self.assertTrue(not t1 < t2)
        self.assertTrue(not t1 > t2)

        # positive values
        t3 = BasicTD(3)   # this is larger than t1
        self.assertTrue(t1 < t3)
        self.assertTrue(t3 > t1)
        self.assertTrue(t1 <= t3)
        self.assertTrue(t3 >= t1)
        self.assertTrue(t1 != t3)
        self.assertTrue(t3 != t1)
        self.assertFalse(t1 == t3)
        self.assertFalse(t3 == t1)
        self.assertFalse(t1 > t3)
        self.assertFalse(t3 < t1)
        self.assertFalse(t1 >= t3)
        self.assertFalse(t3 <= t1)

        # negative values
        t_1 = BasicTD(-2)
        t_3 = BasicTD(-3)   # this is higher than t1
        self.assertTrue(t_1 < t_3)
        self.assertTrue(t_3 > t_1)
        self.assertTrue(t_1 <= t_3)
        self.assertTrue(t_3 >= t_1)
        self.assertTrue(t_1 != t_3)
        self.assertTrue(t_3 != t_1)
        self.assertFalse(t_1 == t_3)
        self.assertFalse(t_3 == t_1)
        self.assertFalse(t_1 > t_3)
        self.assertFalse(t_3 < t_1)
        self.assertFalse(t_1 >= t_3)
        self.assertFalse(t_3 <= t_1)

        for badarg in (10, 34.5, "abc", 1 + 2j, INF, NAN, {}, [], ()):
            self.assertEqual(t1 == badarg, False)
            self.assertEqual(t1 != badarg, True)
            self.assertEqual(badarg == t1, False)
            self.assertEqual(badarg != t1, True)

            self.assertRaises(TypeError, lambda: t1 <= badarg)
            self.assertRaises(TypeError, lambda: t1 < badarg)
            self.assertRaises(TypeError, lambda: t1 > badarg)
            self.assertRaises(TypeError, lambda: t1 >= badarg)
            self.assertRaises(TypeError, lambda: badarg <= t1)
            self.assertRaises(TypeError, lambda: badarg < t1)
            self.assertRaises(TypeError, lambda: badarg > t1)
            self.assertRaises(TypeError, lambda: badarg >= t1)

    def test_140_bool(self):
        self.assertTrue(BasicTD(1))
        self.assertTrue(BasicTD(0.0001))
        self.assertFalse(BasicTD())
        self.assertFalse(BasicTD(0))

    def test_200_roundtrip(self):
        for td in (BasicTD(days=1),
                   BasicTD(days=9999998),
                   BasicTD(days=-9999989),
                   BasicTD(days=0.0000000001),
                   BasicTD(days=-0.0000000001),
                   BasicTD()):

            # Verify td -> string -> td identity.
            s = repr(td)
            td2 = eval(s)
            self.assertEqual(td, td2)

    def test_210_hash_equality(self):
        t1 = BasicTD(days=0)
        t2 = BasicTD()
        self.assertEqual(hash(t1), hash(t2))

        t1 += BasicTD(6)
        t2 += 3 * BasicTD(2)
        self.assertEqual(t1, t2)
        self.assertEqual(hash(t1), hash(t2))

        d = {t1: 1}
        d[t2] = 2
        self.assertEqual(len(d), 1)
        self.assertEqual(d[t1], 2)

    def test_220_pickling(self):
        orig = BasicTD(3.141592)
        for pickler, unpickler, proto in pickle_choices:
            green = pickler.dumps(orig, proto)
            derived = unpickler.loads(green)
            self.assertEqual(orig, derived)


# TODO: for each timedelta interface, we need to test that unknown attributes generate an exception

class TestWesternTD(unittest.TestCase):

    theclass = TimeDelta

    @unittest.skip("old test function")
    def test_000_constructor(self):
        eq = self.assertEqual
        td = TimeDelta

        # Check keyword arguments to constructor
        eq(td(), td(weeks=0, days=0, hours=0, minutes=0, seconds=0,
                    milliseconds=0, microseconds=0))
        eq(td(1), td(days=1))
        eq(td(0, 1), td(seconds=1))
        eq(td(0, 0, 1), td(nanoseconds=1))
        eq(td(weeks=1), td(days=7))
        eq(td(days=1), td(hours=24))
        eq(td(hours=1), td(minutes=60))
        eq(td(minutes=1), td(seconds=60))
        eq(td(seconds=1), td(milliseconds=1000))
        eq(td(milliseconds=1), td(microseconds=1000))
        eq(td(microseconds=1), td(nanoseconds=1000))
        
        # Check negative arguments to constructor
        eq(td(hours=-1), td(days=-1, hours=23))
        eq(td(minutes=-1), td(days=-1, hours=23, minutes=59))
        eq(td(seconds=-1), td(days=-1, hours=23, minutes=59, seconds=59))
        eq(td(milliseconds=-1), td(days=-1, hours=23, minutes=59, seconds=59, 
                                   milliseconds=999))
        eq(td(microseconds=-1), td(days=-1, hours=23, minutes=59, seconds=59, 
                                   milliseconds=999, microseconds=999))
        eq(td(nanoseconds=-1), td(days=-1, hours=23, minutes=59, seconds=59, 
                                  milliseconds=999, microseconds=999, nanoseconds = 999))

        # Check float arguments to constructor
        eq(td(weeks=1.0/7), td(days=1))
        eq(td(days=1.0/24), td(hours=1))
        eq(td(hours=1.0/60), td(minutes=1))
        eq(td(minutes=1.0/60), td(seconds=1))
        eq(td(seconds=0.001), td(milliseconds=1))
        eq(td(milliseconds=0.001), td(microseconds=1))
        eq(td(microseconds=0.001), td(nanoseconds=1))
        eq(td(weeks=1.5),td(days=10, hours=12))
        eq(td(days=1.5), td(days=1, hours=12))
        eq(td(days=1.1), td(days=1, hours=2, minutes=24))
        eq(td(hours=1.5), td(seconds=5400))
        eq(td(hours=1.1), td(seconds=3960))
        eq(td(minutes=1.5), td(seconds=90))
        eq(td(minutes=1.1), td(seconds=66))
        eq(td(seconds=1.5), td(seconds=1, microseconds=500000))
        eq(td(seconds=1.1), td(seconds=1, microseconds=100000))
        
        # Check normalization in constructor
        eq(td(hours=25), td(days=1, hours=1))
        eq(td(milliseconds=2500), td(seconds=2, milliseconds=500))
        eq(td(1, 24*3600), td(2))
        eq(td(0, 0, 60*1000000000), td(minutes=1))
        
        # Check normalization with float arguments

    def test_001_default_constructor_western(self):
        eq = self.assertEqual
        td = TimeDelta

        # Check keyword arguments to constructor
        eq(td(), td(weeks=0, days=0, hours=0, minutes=0, seconds=0))
        eq(td(1), td(days=1))
        eq(td(0, 1), td(hours=1))
        eq(td(0, 0, 1), td(minutes=1))
        eq(td(0, 0, 0, 1), td(seconds=1))
        eq(td(0, 0, 0, 0, 1), td(weeks=1))
        eq(td(weeks=1), td(days=7))
        eq(td(days=1), td(hours=24))
        eq(td(hours=1), td(minutes=60))
        eq(td(minutes=1), td(seconds=60))
        
        # Check negative arguments to constructor
        eq(td(weeks=-1), td(days=-7))
        eq(td(hours=-1), td(days=-1, hours=23))
        eq(td(minutes=-1), td(days=-1, hours=23, minutes=59))
        eq(td(seconds=-1), td(days=-1, hours=23, minutes=59, seconds=59))

        # Check float arguments to constructor
        eq(td(weeks=1.0/7), td(days=1))
        eq(td(days=1.0/24), td(hours=1))
        eq(td(hours=1.0/60), td(minutes=1))
        eq(td(minutes=1.0/60), td(seconds=1))
        eq(td(weeks=1.5),td(days=10, hours=12))
        eq(td(days=1.5), td(days=1, hours=12))
        eq(td(days=1.1), td(days=1, hours=2, minutes=24))
        eq(td(hours=1.5), td(seconds=5400))
        eq(td(hours=1.1), td(seconds=3960))
        eq(td(minutes=1.5), td(seconds=90))
        eq(td(minutes=1.1), td(seconds=66))
        
        # Check normalization in constructor
        eq(td(hours=25), td(days=1, hours=1))
        eq(td(minutes=66), td(hours=1, minutes=6))
        eq(td(seconds=66), td(minutes=1, seconds=6))
        eq(td(days=1, hours=24), td(days=2))
        eq(td(hours=1, minutes=60), td(hours=2))
        eq(td(minutes=1, seconds=60), td(minutes=2))
        eq(td(days=1, minutes=1440), td(days=2))
        eq(td(hours=1, seconds=3600), td(hours=2))
        eq(td(days=1, seconds=86400), td(days=2))
        
        # TODO: Check normalization with float arguments
        
        # TODO: mix positive and negative, integer and float arguments

    def test_041_basic_attributes_western(self):
        days, hours, minutes, seconds = 11, 13, 17, 19.5
        td = TimeDelta(days, hours, minutes, seconds)    # using WesternTD default
        self.assertEqual(td.days, days)
        self.assertEqual(td.hours, hours)
        self.assertEqual(td.minutes, minutes)
        self.assertEqual(td.seconds, seconds)

    def test_050_as_seconds(self):
        td = TimeDelta(days=365)
        self.assertEqual(td.as_seconds(), 31536000)
        for total_seconds in [123456.789012, -123456.789012, 0.123456, 0, 1e6]:
            td = TimeDelta(seconds=total_seconds)
            self.assertEqual(td.as_seconds(), total_seconds)
        # Issue8644: Test that td.total_seconds() has the same
        # accuracy as td / TimeDelta(seconds=1).
        for us in [-1, -2, -123]:
            td = TimeDelta(microseconds=us)
            self.assertEqual(td.as_seconds(), td / TimeDelta(seconds=1))
        # do this also for nanoseconds
        for ns in [-1, -2, -123]:
            td = TimeDelta(nanoseconds=ns)
            self.assertEqual(td.as_seconds(), td / TimeDelta(seconds=1))

    def test_060_carries(self):
        t1 = TimeDelta(days=100,
                       weeks=-7,
                       hours=-24*(100-49),
                       minutes=-3,
                       seconds=12,
                       nanoseconds=(3*60 - 12) * 1000000000 + 1)
        t2 = TimeDelta(nanoseconds=1)
        self.assertEqual(t1, t2)

    def test_070_hash_equality(self):
        t1 = TimeDelta(days=100,
                       weeks=-7,
                       hours=-24*(100-49),
                       minutes=-3,
                       seconds=12,
                       nanoseconds=(3*60 - 12) * 1000000000)
        t2 = TimeDelta()
        self.assertEqual(hash(t1), hash(t2))

        t1 += TimeDelta(weeks=7)
        t2 += TimeDelta(days=7*7)
        self.assertEqual(t1, t2)
        self.assertEqual(hash(t1), hash(t2))

        d = {t1: 1}
        d[t2] = 2
        self.assertEqual(len(d), 1)
        self.assertEqual(d[t1], 2)

    def test_080_pickling(self):
        orig = TimeDelta(12, 34, 56)
        for pickler, unpickler, proto in pickle_choices:
            green = pickler.dumps(orig, proto)
            derived = unpickler.loads(green)
            self.assertEqual(orig, derived)

    def test_090_compare(self):
        t1 = TimeDelta(2, 3, 4)
        t2 = TimeDelta(2, 3, 4)
        self.assertEqual(t1, t2)
        self.assertTrue(t1 <= t2)
        self.assertTrue(t1 >= t2)
        self.assertTrue(not t1 != t2)
        self.assertTrue(not t1 < t2)
        self.assertTrue(not t1 > t2)

        for args in (3, 3, 3), (2, 4, 4), (2, 3, 5):
            t3 = TimeDelta(*args)   # this is larger than t1
            self.assertTrue(t1 < t3)
            self.assertTrue(t3 > t1)
            self.assertTrue(t1 <= t3)
            self.assertTrue(t3 >= t1)
            self.assertTrue(t1 != t3)
            self.assertTrue(t3 != t1)
            self.assertTrue(not t1 == t3)
            self.assertTrue(not t3 == t1)
            self.assertTrue(not t1 > t3)
            self.assertTrue(not t3 < t1)
            self.assertTrue(not t1 >= t3)
            self.assertTrue(not t3 <= t1)

        t_1 = TimeDelta(-2, -3, -4)
        for args in (-2, -3, -3), (-2, -2, -4), (-1, -3, -4):
            t_3 = TimeDelta(*args)   # this is higher than t1
            self.assertTrue(t_1 < t_3)
            self.assertTrue(t_3 > t_1)
            self.assertTrue(t_1 <= t_3)
            self.assertTrue(t_3 >= t_1)
            self.assertTrue(t_1 != t_3)
            self.assertTrue(t_3 != t_1)
            self.assertTrue(not t_1 == t_3)
            self.assertTrue(not t_3 == t_1)
            self.assertTrue(not t_1 > t_3)
            self.assertTrue(not t_3 < t_1)
            self.assertTrue(not t_1 >= t_3)
            self.assertTrue(not t_3 <= t_1)

        for badarg in (10, 34.5, "abc", {}, [], ()):
            self.assertEqual(t1 == badarg, False)
            self.assertEqual(t1 != badarg, True)
            self.assertEqual(badarg == t1, False)
            self.assertEqual(badarg != t1, True)

            self.assertRaises(TypeError, lambda: t1 <= badarg)
            self.assertRaises(TypeError, lambda: t1 < badarg)
            self.assertRaises(TypeError, lambda: t1 > badarg)
            self.assertRaises(TypeError, lambda: t1 >= badarg)
            self.assertRaises(TypeError, lambda: badarg <= t1)
            self.assertRaises(TypeError, lambda: badarg < t1)
            self.assertRaises(TypeError, lambda: badarg > t1)
            self.assertRaises(TypeError, lambda: badarg >= t1)

    def test_100_nanosecond_rounding(self):
        td = TimeDelta
        eq = self.assertEqual

        # Single-field rounding.
        eq(td(milliseconds=0.4/1000000), td(0))    # rounds to 0
        eq(td(milliseconds=-0.4/1000000), td(0))    # rounds to 0
        eq(td(milliseconds=0.6/1000000), td(nanoseconds=1))
        eq(td(milliseconds=-0.6/1000000), td(nanoseconds=-1))
        eq(td(microseconds=0.4/1000), td(0))    # rounds to 0
        eq(td(microseconds=-0.4/1000), td(0))    # rounds to 0
        eq(td(microseconds=0.6/1000), td(nanoseconds=1))
        eq(td(microseconds=-0.6/1000), td(nanoseconds=-1))

        # Rounding due to contributions from more than one field.
        ns_per_hour = 3600000000000
        ns_per_day = ns_per_hour * 24
        eq(td(days=.4/ns_per_day), td(0))
        eq(td(hours=.2/ns_per_hour), td(0))
        eq(td(days=.4/ns_per_day, hours=.2/ns_per_hour), td(nanoseconds=1))

        eq(td(days=-.4/ns_per_day), td(0))
        eq(td(hours=-.2/ns_per_hour), td(0))
        eq(td(days=-.4/ns_per_day, hours=-.2/ns_per_hour), td(nanoseconds=-1))

    def test_110_bool(self):
        self.assertTrue(TimeDelta(1))
        self.assertTrue(TimeDelta(0, 1))
        self.assertTrue(TimeDelta(0, 0, 1))
        self.assertTrue(TimeDelta(microseconds=1))
        self.assertFalse(TimeDelta())
        self.assertFalse(TimeDelta(0))
        self.assertFalse(TimeDelta(0, 0))
        self.assertFalse(TimeDelta(0, 0, 0))

    def test_120_subclass_TimeDelta(self):

        class T(TimeDelta):
            @staticmethod
            def from_td(td):
                return T(td.days, td.seconds, td.nanoseconds)

            def as_hours(self):
                sum = (self.days * 24 +
                       self.seconds / 3600.0 +
                       self.nanoseconds / 3600000000000)
                return round(sum)

        t1 = T(days=1)
        self.assertTrue(isinstance(t1, TimeDelta))
        self.assertFalse(type(t1) is TimeDelta)
        self.assertEqual(t1.as_hours(), 24)

        t2 = T(days=-1, seconds=-3600)
        self.assertEqual(t2.as_hours(), -25)

        t3 = t1 + t2
        self.assertTrue(type(t3) is T)
        self.assertTrue(isinstance(t3, TimeDelta))
        td4 = TimeDelta(hours=-1)
        self.assertEqual(t3, td4)
        t5 = T.from_td(td4)
        self.assertTrue(type(t5) is T)
        self.assertEqual(t3, t5)
        self.assertEqual(t5.as_hours(), -1)

    def test_130_division(self):
        t1 = TimeDelta(3, 85750, microseconds=317460)
        self.assertEqual(t1 / 3.14, TimeDelta(1, 23456, milliseconds=789))
        self.assertEqual(t1 / TimeDelta(1, 23456, milliseconds=789), 3.14)
        
        t2 = TimeDelta(1)
        self.assertEqual(t2 / 1024, TimeDelta(seconds=84, milliseconds=375))
        self.assertEqual(t2 / TimeDelta(seconds=1024), 84.375)

        t3 = TimeDelta(minutes=2, seconds=30)
        self.assertEqual(t3 / TimeDelta(minutes=1), 2.5)
        self.assertEqual(t3 / 60, TimeDelta(seconds=2, milliseconds=500))

    def test_140_repr(self):
        td = TimeDelta
        name = 'datetime2.' + self.theclass.__name__
        self.assertEqual(repr(td()), "{}()".format(name))
        self.assertEqual(repr(td(0)), "{}()".format(name))
        self.assertEqual(repr(td(0, 0)), "{}()".format(name))
        self.assertEqual(repr(td(0, 0, 0)), "{}()".format(name))
        self.assertEqual(repr(td(1)), "{}(1)".format(name))
        self.assertEqual(repr(td(-1)), "{}(-1)".format(name))
        self.assertEqual(repr(td(seconds=1)), "{}(0, 1)".format(name))
        self.assertEqual(repr(td(nanoseconds=1)), "{}(0, 0, 1)".format(name))

    def test_150_roundtrip(self):
        for td in (TimeDelta(days=9999, hours=23, minutes=59,
                             seconds=59, nanoseconds=999999999),
                   TimeDelta(days=-9999),
                   TimeDelta(days=-9999, seconds=1),
                   TimeDelta(days=1, seconds=2, microseconds=3),
                   TimeDelta()):

            # Verify td -> string -> td identity.
            s = repr(td)
            self.assertTrue(s.startswith('datetime2.'))
            s = s[10:]
            td2 = eval(s)
            self.assertEqual(td, td2)

    def test_str(self):
        td = TimeDelta
        eq = self.assertEqual

        eq(str(td(1)), "1 day, 0:00:00")
        eq(str(td(-1)), "-1 day, 0:00:00")
        eq(str(td(2)), "2 days, 0:00:00")
        eq(str(td(-2)), "-2 days, 0:00:00")

        eq(str(td(hours=12, minutes=58, seconds=59)), "12:58:59")
        eq(str(td(hours=2, minutes=3, seconds=4)), "2:03:04")
        eq(str(td(weeks=-30, hours=23, minutes=12, seconds=34)),
           "-210 days, 23:12:34")

        eq(str(td(milliseconds=1)), "0:00:00.001000000")
        eq(str(td(microseconds=3)), "0:00:00.000003000")

        eq(str(td(days=999999999, hours=23, minutes=59, seconds=59,
                   microseconds=999999)),
           "999999999 days, 23:59:59.999999000")


class TestTimeDeltaTwo(unittest.TestCase):

    def test_000_default_constructor(self):
        self.assertEqual(TimeDelta.default, WesternTD)

    def test_010_parameters_passed(self):
        assert TimeDelta.default == WesternTD
        self.assertRaises(TypeError, TimeDelta, 1, 2, 3, 4, 5, 6)
        self.assertRaises(TypeError, TimeDelta, paramaanus = 42)

    def test_020_valid_input_td(self):
        self.assertIsNotNone(TimeDelta(1, input_td = WesternTD))
        self.assertIsNotNone(TimeDelta(1, input_td = BasicTD))

    def test_030_invalid_input_td(self):
        for obj in ('', 0, 1.1, TimeDelta):
            self.assertRaises(TypeError, TimeDelta, input_td = obj)
            
    def test_040_valid_td(self):
        self.assertIsNotNone(TimeDelta(1, td = WesternTD))
        self.assertIsNotNone(TimeDelta(1, td = BasicTD))

    def test_050_invalid_td(self):
        for obj in ('', 0, 1.1, TimeDelta):
            self.assertRaises(TypeError, TimeDelta, td = obj)
            
    def test_100_computations(self):
        assert TimeDelta.default == WesternTD
        eq = self.assertEqual
        td = TimeDelta

        a = td(1) # One day
        b = td(0, 0, 1) # One minute
        c = td(0, 0, 0, 0, 1) # One week
        
        # Addition, subtraction, unary minus
        eq(a + b + c, td(weeks = 1, days = 1, minutes = 1))
        eq(a + b, td(days = 1, minutes = 1))
        eq(a + c, td(weeks = 1, days = 1))
        eq(b + c, td(weeks = 1, minutes = 1))
        eq(a - b, td(hours = 23, minutes = 59))
        eq(b - a, td(hours = -23, minutes = -59))
        eq(a - c, td(days = -6))
        eq(c - a, td(days = 6))
        eq(b - c, td(days = -7, minutes = 1))
        eq(c - b, td(days = 6, hours = 23, minutes = 59))
        eq(-a, td(-1))
        eq(-b, td(-1, 23, 59))
        eq(-c, td(-7))
        
        # absolute value
        eq(abs(a), a)
        eq(abs(-a), a)
        eq(abs(b), b)
        eq(abs(-b), b)
        eq(abs(c), c)
        eq(abs(-c), c)
        
        # Multiplication by integer or float, positive or negative
        eq(a*10, td(10))
        eq(a*10, 10*a)
        eq(a*1.1, td(1, 2, 24))
        eq(a*1.1, 1.1*a)
        eq(a*-10, td(-10))
        eq(a*-10, -a*10)
        eq(a*-1.1, td(-2, 21, 36))
        eq(a*-1.1, -a*1.1)
        eq(b*10, td(0, 0, 10))
        eq(b*10, 10*b)
        eq(b*1.1, td(0, 0, 1, 6))
        eq(b*1.1, 1.1*b)
        eq(b*-10, td(-1, 23, 50))
        eq(b*-10, -b*10)
        eq(b*-1.1, td(-1, 23, 58, 54))
        eq(b*-1.1, -b*1.1)
        eq(c*10, td(70))
        eq(c*10, 10*c)
        eq(c*1.1, td(7, 16, 48))
        eq(c*1.1, 1.1*c)
        eq(c*-10, td(-70))
        eq(c*-10, -c*10)
        eq(c*-1.1, td(-8, 7, 12))
        eq(c*-1.1, -c*1.1)

        # True division by integer or float, positive or negative
        eq(a/10, td(0, 2, 24))
        eq(a/1.2, td(0, 20))
        eq(a/-10, td(-1, 21, 36))
        eq(a/-1.2, td(-1, 4))
        eq(b/10, td(0, 0, 0, 6))
        eq(b/1.2, td(0, 0, 0, 50))
        eq(b/-10, td(-1, 23, 59, 54))
        eq(b/-1.2, td(-1, 23, 59, 10))
        eq(c/10, td(0, 16, 48))
        eq(c/1.2, td(5, 20))
        eq(c/-10, td(-1, 7, 12))
        eq(c/-1.2, td(-6, 4))

        # True division by TimeDelta (inverse of the tests above)
        eq(a/td(0, 2, 24), 10)
        eq(a/td(0, 20), 1.2)
        eq(a/td(-1, 21, 36), -10)
        eq(a/td(-1, 4), -1.2)
        eq(b/td(0, 0, 0, 6), 10)
        eq(b/td(0, 0, 0, 50), 1.2)
        eq(b/td(-1, 23, 59, 54), -10)
        eq(b/td(-1, 23, 59, 10), -1.2)
        eq(c/td(0, 16, 48), 10)
        eq(c/td(5, 20), 1.2)
        eq(c/td(-1, 7, 12), -10)
        eq(c/td(-6, 4), -1.2)

        # True division by integer or float, positive or negative with uglier divisor
        eq(a/11, td(seconds = 7854.5454545454545454545454545455))
        eq(a/1.1, td(seconds = 78545.454545454545454545454545455))
        eq(a/-11, td(seconds = -7854.5454545454545454545454545455))
        eq(a/-1.1, td(seconds = -78545.454545454545454545454545455))
        eq(b/11, td(seconds = 5.45454545454545454545454545455))
        eq(b/1.1, td(seconds = 54.54545454545454545454545455))
        eq(b/-11, td(seconds = -5.45454545454545454545454545455))
        eq(b/-1.1, td(seconds = -54.54545454545454545454545455))
        eq(c/11, td(hours = 15.272727272727272727272727272727))
        eq(c/1.1, td(hours = 152.72727272727272727272727272727))
        eq(c/-11, td(hours = -15.272727272727272727272727272727))
        eq(c/-1.1, td(hours = -152.72727272727272727272727272727))

        # TODO: add tests for floor division, mod and divmod
        
        # TODO: add tests for __ceil__, __floor__ and __trunc__ .

    def test_110_disallowed_computations(self):
        a = TimeDelta(42)
        b = TimeDelta(24)
        z = TimeDelta(0)

        # Add/sub int, float, string, and containers should be illegal
        for obj in (10, 34.5, "abc", {}, [], ()):
            self.assertRaises(TypeError, lambda: a + obj)
            self.assertRaises(TypeError, lambda: a - obj)
            self.assertRaises(TypeError, lambda: obj + a)
            self.assertRaises(TypeError, lambda: obj - a)

        # These opertations are not defined for TimeDelta
        self.assertRaises(TypeError, lambda: pow(a, 1))
        self.assertRaises(TypeError, lambda: pow(1, a))
        self.assertRaises(TypeError, lambda: pow(a, 1.1))
        self.assertRaises(TypeError, lambda: pow(1.1, a))
        self.assertRaises(TypeError, lambda: pow(a, b))
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
        
        # Division of integer or float by TimeDelta doesn't make sense.
        self.assertRaises(TypeError, lambda: 1 // a)
        self.assertRaises(TypeError, lambda: 1.1 // a)
        
        # Multiplication and divion of TimeDelta by string or containers
        # should be illegal
        for obj in ("abc", (), [], {}):
            self.assertRaises(TypeError, lambda: a * obj)
            self.assertRaises(TypeError, lambda: obj * a)
            self.assertRaises(TypeError, lambda: a / obj)
            self.assertRaises(TypeError, lambda: obj / a)
            
        # Division by zero doesn't make sense.
        self.assertRaises(ZeroDivisionError, lambda: a / 0)
        self.assertRaises(ZeroDivisionError, lambda: a / 0.0)
        self.assertRaises(ZeroDivisionError, lambda: a / z)

    @requires_IEEE_754
    def test_120_disallowed_special(self):
        a = TimeDelta(42)
        self.assertRaises(ValueError, a.__mul__, NAN)
        self.assertRaises(ValueError, a.__truediv__, NAN)

    def test_130_compare(self):
        assert TimeDelta.default == WesternTD
        t1 = TimeDelta(2, 3, 4)
        t2 = TimeDelta(2, 3, 4)
        self.assertEqual(t1, t2)
        self.assertTrue(t1 <= t2)
        self.assertTrue(t1 >= t2)
        self.assertTrue(not t1 != t2)
        self.assertTrue(not t1 < t2)
        self.assertTrue(not t1 > t2)

        for args in (3, 3, 3), (2, 4, 4), (2, 3, 5):
            t3 = TimeDelta(*args)   # this is larger than t1
            self.assertTrue(t1 < t3)
            self.assertTrue(t3 > t1)
            self.assertTrue(t1 <= t3)
            self.assertTrue(t3 >= t1)
            self.assertTrue(t1 != t3)
            self.assertTrue(t3 != t1)
            self.assertTrue(not t1 == t3)
            self.assertTrue(not t3 == t1)
            self.assertTrue(not t1 > t3)
            self.assertTrue(not t3 < t1)
            self.assertTrue(not t1 >= t3)
            self.assertTrue(not t3 <= t1)

        t_1 = TimeDelta(-2, -3, -4)
        for args in (-2, -3, -3), (-2, -2, -4), (-1, -3, -4):
            t_3 = TimeDelta(*args)   # this is higher than t1
            self.assertTrue(t_1 < t_3)
            self.assertTrue(t_3 > t_1)
            self.assertTrue(t_1 <= t_3)
            self.assertTrue(t_3 >= t_1)
            self.assertTrue(t_1 != t_3)
            self.assertTrue(t_3 != t_1)
            self.assertTrue(not t_1 == t_3)
            self.assertTrue(not t_3 == t_1)
            self.assertTrue(not t_1 > t_3)
            self.assertTrue(not t_3 < t_1)
            self.assertTrue(not t_1 >= t_3)
            self.assertTrue(not t_3 <= t_1)

        for badarg in (10, 34.5, "abc", {}, [], ()):
            self.assertEqual(t1 == badarg, False)
            self.assertEqual(t1 != badarg, True)
            self.assertEqual(badarg == t1, False)
            self.assertEqual(badarg != t1, True)

            self.assertRaises(TypeError, lambda: t1 <= badarg)
            self.assertRaises(TypeError, lambda: t1 < badarg)
            self.assertRaises(TypeError, lambda: t1 > badarg)
            self.assertRaises(TypeError, lambda: t1 >= badarg)
            self.assertRaises(TypeError, lambda: badarg <= t1)
            self.assertRaises(TypeError, lambda: badarg < t1)
            self.assertRaises(TypeError, lambda: badarg > t1)
            self.assertRaises(TypeError, lambda: badarg >= t1)

    def test_140_bool(self):
        assert TimeDelta.default == WesternTD
        self.assertTrue(TimeDelta(1))
        self.assertTrue(TimeDelta(0, 1))
        self.assertTrue(TimeDelta(0, 0, 1))
        self.assertTrue(TimeDelta(seconds = 0.000001))
        self.assertFalse(TimeDelta())
        self.assertFalse(TimeDelta(0))
        self.assertFalse(TimeDelta(0, 0))
        self.assertFalse(TimeDelta(0, 0, 0))

    def test_200_subclass_TimeDelta(self):
        assert TimeDelta.default == WesternTD

        class T(TimeDelta):
            @staticmethod
            def from_td(td):
                return T(td.days, td.hours, td.minutes, td.seconds)

            def as_hours(self):
                sum = self.days * 24 + self.hours + self.minutes / 60 + self.seconds / 3600
                return float(sum)

        t1 = T(days=1)
        self.assertTrue(isinstance(t1, TimeDelta))
        self.assertFalse(type(t1) is TimeDelta)
        self.assertEqual(t1.as_hours(), 24)

        t2 = T(days=-1, seconds=-3600)
        self.assertEqual(t2.as_hours(), -25)

        t3 = t1 + t2
        self.assertTrue(type(t3) is T)
        self.assertTrue(isinstance(t3, TimeDelta))
        td4 = TimeDelta(hours=-1)
        self.assertEqual(t3, td4)
        t5 = T.from_td(td4)
        self.assertTrue(type(t5) is T)
        self.assertEqual(t3, t5)
        self.assertEqual(t5.as_hours(), -1)

    def test_210_roundtrip(self):
        for td in (TimeDelta(days=9999, hours=23, minutes=59, seconds=59),
                   TimeDelta(days=-9999),
                   TimeDelta(days=9999, seconds=1),
                   TimeDelta(seconds=0.000001),
                   TimeDelta()):

            # Verify td -> string -> td identity.
            s = repr(td)
            td2 = eval(s)
            self.assertEqual(td, td2)

    def test_220_hash_equality(self):
        assert TimeDelta.default == WesternTD
        t1 = TimeDelta(days=100,
                       weeks=-7,
                       hours=-24*(100-49),
                       minutes=-3.5,
                       seconds=210)
        t2 = TimeDelta()
        self.assertEqual(hash(t1), hash(t2))

        t1 += TimeDelta(weeks=7)
        t2 += TimeDelta(days=7*7)
        self.assertEqual(t1, t2)
        self.assertEqual(hash(t1), hash(t2))

        d = {t1: 1}
        d[t2] = 2
        self.assertEqual(len(d), 1)
        self.assertEqual(d[t1], 2)

    def test_230_pickling(self):
        assert TimeDelta.default == WesternTD
        orig = TimeDelta(12, 34, 56)
        for pickler, unpickler, proto in pickle_choices:
            green = pickler.dumps(orig, proto)
            derived = unpickler.loads(green)
            self.assertEqual(orig, derived)



if __name__ == "__main__":
    timedelta_tests = unittest.TestLoader().loadTestsFromTestCase(TestTimeDelta)
    westerntd_tests = unittest.TestLoader().loadTestsFromTestCase(TestWesternTD)
    #all_tests = unittest.TestSuite([timedelta_tests, westerntd_tests])
    all_tests = unittest.TestSuite([timedelta_tests])
    unittest.TextTestRunner().run(all_tests)
