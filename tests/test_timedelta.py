# TimeDelta class tests

# Copyright (c) 2011-2022 Francesco Ricciardi
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

__author__ = "Francesco Ricciardi <francescor2010 at yahoo.it>"

from collections import namedtuple
from decimal import Decimal
from fractions import Fraction
import pickle
import pytest

from datetime2 import TimeDelta


INF = float("inf")
NAN = float("nan")


TimeDeltaTestData = namedtuple('TimeDeltaTestData', ['frac_days', 'int_part', 'frac_part', 'string', 'input_values'])


timedelta_test_data = [
    TimeDeltaTestData(Fraction(-6, 1),  -6, Fraction(0, 1), "-6 days", [-6, Fraction(-12, 2), Decimal("-6"), -6.0, "-6", "-18/3"]),
    TimeDeltaTestData(Fraction(-13, 4), -3, Fraction(-1, 4), "-3 days and -1/4 of a day", [Fraction(-39, 12), Decimal("-3.25"), -3.25, "-3.25", "-26/8"]),
    TimeDeltaTestData(Fraction(-1, 1),  -1, Fraction(0, 1), "-1 day", ["-1"]),  # for the singular day
    TimeDeltaTestData(Fraction(-3, 8),   0, Fraction(-3, 8), "-3/8 of a day", [Fraction(-3, 8), Decimal("-0.375"), -0.375, "-0.375", "-3/8"]),
    TimeDeltaTestData(Fraction(0, 1),    0, Fraction(0, 1), "0 days", [0, Fraction(0), Decimal("0"), 0.0, "0", "0/33"]),
    TimeDeltaTestData(Fraction(1, 4),    0, Fraction(1, 4), "1/4 of a day", [Fraction(1, 4), Decimal("0.25"), 0.25, "0.25", "1/4"]),
    TimeDeltaTestData(Fraction(1, 1),    1, Fraction(0, 1), "1 day", ["1"]),  # for the singular day
    TimeDeltaTestData(Fraction(29, 8),   3, Fraction(5, 8), "3 days and 5/8 of a day", [Fraction(58, 16), Decimal("3.625"), 3.625, "3.625", "87/24"]),
    TimeDeltaTestData(Fraction(5, 1),    5, Fraction(0, 1), "5 days", [5, Fraction(15, 3), Decimal("5"), 5.0, "5", "10/2"])
]

timedelta_test_data_num_den = [
    [Fraction(-15, 4), [(15, -4), (-30, 8)]],
    [Fraction(-1, 7), [(1, -7), (-3, 21)]],
    [Fraction(2, 3), [(2, 3), (-4, -6)]],
    [Fraction(14, 3), [(14, 3), (-28, -6)]]
]
# we are not going to test more values, because our purpose is not to test the Fraction constructor :-)

# but we want to test with a few strange values
timedelta_strange_test_data = [
    Fraction(90123, 4567),
    9.999999,
    "99.999999",
    "100.0000001",
    "5/456789"
]
time_strange_num_den_test_data = [
    (1234, 567),
    (99999, 9999)
]


def test_00_constructor_default():
    # the fractional_days argument can be anything that can be passed to the fractions.Fraction constructor
    for test_datum in timedelta_test_data:
        for input_value in test_datum.input_values:
            td = TimeDelta(input_value)
            assert td.fractional_days == test_datum.frac_days

    # "strange" values
    for input_value in timedelta_strange_test_data:
        TimeDelta(input_value)

    # a TypeError exception is raised if the argument type is not one of the accepted types
    # exception with no or three parameters
    with pytest.raises(TypeError):
        TimeDelta()
    with pytest.raises(TypeError):
        TimeDelta(1, 2, 3)

    # exception with non-numeric types
    for par in (1j, (1,), [1], {1: 1}, [], {}, None, (1, 2), (1, 2, 3)):
        with pytest.raises(TypeError):
            TimeDelta(par)


def test_01_constructor_default_numden():
    # the day_frac argument can be a numerator and denominator
    for fractional_days, input_values in timedelta_test_data_num_den:
        for input_value in input_values:
            assert TimeDelta(input_value[0], input_value[1]).fractional_days == fractional_days

    # strange values with num/den
    for input_value in time_strange_num_den_test_data:
        TimeDelta(input_value[0], input_value[1])

    # a TypeError exception is raised if the argument type is not one of the accepted types
    # exception with non-numeric types
    for par in (1j, (1,), [1], {1: 1}, [], {}, (1, 2), (1, 2, 3)):
        with pytest.raises(TypeError):
            TimeDelta(par, 2)
            TimeDelta(1, par)
    # None is invalid as first argument
    with pytest.raises(TypeError):
        TimeDelta(None, 2)

    # denominator should not be 0
    with pytest.raises(ZeroDivisionError):
        TimeDelta(2, 0)


def test_10_hash_equality():
    # TimeDelta instances are immutable
    td1 = TimeDelta("13/5")
    td2 = TimeDelta(13, 5)
    assert hash(td1) == hash(td2)
    dic = {td1: 1}
    assert dic[td2] == 1
    dic[td2] = 2
    assert len(dic) == 1
    assert dic[td1] == 2

    td3 = TimeDelta(13000001, 5000000)
    assert hash(td1) != hash(td3)
    dic[td3] = 3
    assert len(dic) == 2
    assert dic[td3] == 3


def test_11_pickling():
    global Derived

    # without utcoffset
    for test_datum in timedelta_test_data:
        for input_value in test_datum.input_values:
            td = TimeDelta(input_value)
            for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
                pickled = pickle.dumps(td, protocol)
                unpickled = pickle.loads(pickled)
                assert td == unpickled

    class Derived(TimeDelta):
        def __init__(self, fractional_days, dummy):
            self.dummy = dummy
            TimeDelta.__init__(self, fractional_days)

        def __eq__(self, other):
            return self.dummy == other.dummy and TimeDelta.__eq__(self, other)

    for test_datum in timedelta_test_data:
        der = Derived(test_datum.frac_days, 42)
        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            pickled = pickle.dumps(der, protocol)
            unpickled = pickle.loads(pickled)
            assert isinstance(unpickled, TimeDelta)
            assert isinstance(unpickled, Derived)
            assert unpickled.dummy == 42
            assert der == unpickled


def test_12_bool():
    # A TimeDelta instance is true unless it is equal to TimeDelta(0)
    for test_datum in timedelta_test_data:
        for input_value in test_datum.input_values:
            if test_datum.frac_days == 0:
                assert not TimeDelta(input_value)
            else:
                assert TimeDelta(input_value)
    for fractional_days, input_values in timedelta_test_data_num_den:
        for input_value in input_values:
            if fractional_days.numerator == 0:
                assert not TimeDelta(input_value[0], input_value[1])
            else:
                assert TimeDelta(input_value[0], input_value[1])


def test_20_attributes():
    # the attribute of a TimeDelta instance is read-only
    td1 = TimeDelta("0.12345")
    with pytest.raises(AttributeError):
        td1.fractional_days = Fraction(3, 7)
    # Test reaction with unknown attributes
    # I want to do this, because TimeDelta will have attributes added at runtime
    # let's tests this both on class and instance
    with pytest.raises(AttributeError):
        TimeDelta.unknown
    td2 = TimeDelta("0.12345")
    with pytest.raises(AttributeError):
        td2.unknown


def test_30_repr():
    import datetime2

    for test_datum in timedelta_test_data:
        for input_value in test_datum.input_values:
            td = TimeDelta(input_value)
            time_repr = repr(td)
            names, args = time_repr.split("(")
            assert names.split(".") == ["datetime2", "TimeDelta"]
            args = args[:-1]  # drop ')'
            assert eval(args) == str(test_datum.frac_days)
            assert td == eval(time_repr)


def test_31_str():
    for test_datum in timedelta_test_data:
        for input_value in test_datum.input_values:
            td = TimeDelta(input_value)
            assert str(td) == test_datum.string


def test_40_operations_add_sub():
    a = TimeDelta(0)
    b = TimeDelta("-17/6")
    c = TimeDelta(4.125)

    assert a + a == TimeDelta(0)
    assert a + b == TimeDelta(-17, 6)
    assert a + c == TimeDelta(33, 8)
    assert b + a == TimeDelta(-17, 6)
    assert b + b == TimeDelta(-34, 6)
    assert b + c == TimeDelta(31, 24)
    assert c + a == TimeDelta(4.125)
    assert c + b == TimeDelta(31, 24)
    assert c + c == TimeDelta(33, 4)

    assert a - a == TimeDelta(0)
    assert a - b == TimeDelta(17, 6)
    assert a - c == TimeDelta(-33, 8)
    assert b - a == TimeDelta(-17, 6)
    assert b - b == TimeDelta(0)
    assert b - c == TimeDelta(-167, 24)
    assert c - a == TimeDelta(33, 8)
    assert c - b == TimeDelta(167, 24)
    assert c - c == TimeDelta(0)

    assert +a == TimeDelta(0)
    assert +b == TimeDelta(-17, 6)
    assert +c == TimeDelta(33, 8)

    assert -a == TimeDelta(0)
    assert -b == TimeDelta(17, 6)
    assert -c == TimeDelta(-33, 8)

    assert abs(a) == TimeDelta(0)
    assert abs(b) == TimeDelta(17, 6)
    assert abs(c) == TimeDelta(33, 8)

    # disallowed operations
    d = TimeDelta("3/4")

    # Add/sub int, float, string, complex, specials and containers should be illegal
    for obj in (10, 34.5, "abc", 1 + 2j, INF, NAN, {}, [], ()):
        with pytest.raises(TypeError):
            d + obj
        with pytest.raises(TypeError):
            d - obj
        with pytest.raises(TypeError):
            obj + d
        with pytest.raises(TypeError):
            obj - d


def test_41_operations_mul_div():
    a = TimeDelta(0)
    b = TimeDelta("-17/6")
    c = TimeDelta(4.125)

    assert a * 3 == TimeDelta(0)
    assert a * Fraction(1, 3) == TimeDelta(0)
    assert a * Decimal("-2.5") == TimeDelta(0)
    assert b * 3 == TimeDelta(-17, 2)
    assert b * Fraction(1, 3) == TimeDelta(-17, 18)
    assert b * Decimal("-2.5") == TimeDelta(85, 12)
    assert c * 3 == TimeDelta(99, 8)
    assert c * Fraction(1, 3) == TimeDelta(11, 8)
    assert c * Decimal("-2.5") == TimeDelta(-165, 16)

    assert 3 * a == TimeDelta(0)
    assert Fraction(1, 3) * a == TimeDelta(0)
    assert Decimal("-2.5") * a == TimeDelta(0)
    assert 3 * b == TimeDelta(-17, 2)
    assert Fraction(1, 3) * b == TimeDelta(-17, 18)
    assert Decimal("-2.5") * b == TimeDelta(85, 12)
    assert 3 * c == TimeDelta(99, 8)
    assert Fraction(1, 3) * c == TimeDelta(11, 8)
    assert Decimal("-2.5") * c == TimeDelta(-165, 16)

    assert a / 3 == TimeDelta(0)
    assert a / Fraction(1, 3) == TimeDelta(0)
    assert a / Decimal("-2.5") == TimeDelta(0)
    assert b / 3 == TimeDelta(-17, 18)
    assert b / Fraction(1, 3) == TimeDelta(-17, 2)
    assert b / Decimal("-2.5") == TimeDelta(17, 15)
    assert c / 3 == TimeDelta(11, 8)
    assert c / Fraction(1, 3) == TimeDelta(99, 8)
    assert c / Decimal("-2.5") == TimeDelta(-33, 20)

    assert a // 3 == TimeDelta(0)
    assert a // Fraction(1, 3) == TimeDelta(0)
    assert a // Decimal("-2.5") == TimeDelta(0)
    assert b // 3 == TimeDelta(-1)
    assert b // Fraction(1, 3) == TimeDelta(-9)
    assert b // Decimal("-2.5") == TimeDelta(1)
    assert c // 3 == TimeDelta(1)
    assert c // Fraction(1, 3) == TimeDelta(12)
    assert c // Decimal("-2.5") == TimeDelta(-2)

    assert a % 3 == TimeDelta(0)
    assert a % Fraction(1, 3) == TimeDelta(0)
    assert a % Decimal("-2.5") == TimeDelta(0)
    assert b % 3 == TimeDelta(1, 6)
    assert b % Fraction(1, 3) == TimeDelta(1, 6)
    assert b % Decimal("-2.5") == TimeDelta(-1, 3)
    assert c % 3 == TimeDelta(9, 8)
    assert c % Fraction(1, 3) == TimeDelta(1, 8)
    assert c % Decimal("-2.5") == TimeDelta(-7, 8)

    d = TimeDelta(-3, 4)
    e = TimeDelta(2, 3)
    
    assert a / b == Fraction(0)
    assert a / c == Fraction(0)
    assert a / d == Fraction(0)
    assert a / e == Fraction(0)
    assert b / b == Fraction(1)
    assert b / c == Fraction(-68, 99)
    assert b / d == Fraction(34, 9)
    assert b / e == Fraction(-17, 4)
    assert c / b == Fraction(-99, 68)
    assert c / c == Fraction(1)
    assert c / d == Fraction(-11, 2)
    assert c / e == Fraction(99, 16)
    assert d / b == Fraction(9, 34)
    assert d / c == Fraction(-2, 11)
    assert d / d == Fraction(1)
    assert d / e == Fraction(-9, 8)
    assert e / b == Fraction(-4, 17)
    assert e / c == Fraction(16, 99)
    assert e / d == Fraction(-8, 9)
    assert e / e == Fraction(1)

    assert a // b == 0
    assert a // c == 0
    assert a // d == 0
    assert a // e == 0
    assert b // b == 1
    assert b // c == -1
    assert b // d == 3
    assert b // e == -5
    assert c // b == -2
    assert c // c == 1
    assert c // d == -6
    assert c // e == 6
    assert d // b == 0
    assert d // c == -1
    assert d // d == 1
    assert d // e == -2
    assert e // b == -1
    assert e // c == 0
    assert e // d == -1
    assert e // e == 1

    assert a % b == Fraction(0)
    assert a % c == Fraction(0)
    assert a % d == Fraction(0)
    assert a % e == Fraction(0)
    assert b % b == Fraction(0)
    assert b % c == Fraction(31, 24)
    assert b % d == Fraction(-7, 12)
    assert b % e == Fraction(1, 2)
    assert c % b == Fraction(-37, 24)
    assert c % c == Fraction(0)
    assert c % d == Fraction(-3, 8)
    assert c % e == Fraction(1, 8)
    assert d % b == Fraction(-3, 4)
    assert d % c == Fraction(27, 8)
    assert d % d == Fraction(0)
    assert d % e == Fraction(7, 12)
    assert e % b == Fraction(-13, 6)
    assert e % c == Fraction(2, 3)
    assert e % d == Fraction(-1, 12)
    assert e % e == Fraction(0)

    # We'll not test divmod(), which is the simple concatenation of // and %
    
    # disallowed operations
    f = TimeDelta("3/4")

    # Muliplication by string, complex, specials and containers should be illegal
    for obj in ("abc", 1 + 2j, INF, NAN, {}, [], (), TimeDelta(1)):
        with pytest.raises(TypeError):
            f * obj
        with pytest.raises(TypeError):
            obj * f
        with pytest.raises(TypeError):
            pow(f, obj)
        with pytest.raises(TypeError):
            pow(obj, f)
        with pytest.raises(TypeError):
            f ^ obj
        with pytest.raises(TypeError):
            obj ^ f
        with pytest.raises(TypeError):
            f >> obj
        with pytest.raises(TypeError):
            obj >> f
        with pytest.raises(TypeError):
            f << obj
        with pytest.raises(TypeError):
            obj << f
    # Division by string, complex, specials and containers should be illegal
    for obj in ("abc", 1 + 2j, INF, NAN, {}, [], ()):
        with pytest.raises(TypeError):
            f / obj
        with pytest.raises(TypeError):
            obj / f
        with pytest.raises(TypeError):
            f // obj
        with pytest.raises(TypeError):
            obj // f


def test_42_comparisons():
    t1 = TimeDelta("11/8")
    t2 = TimeDelta(1.375)
    assert t1 == t2
    assert t1 <= t2
    assert t1 >= t2
    assert not (t1 != t2)
    assert not (t1 < t2)
    assert not (t1 > t2)

    t3 = TimeDelta("12/7")  # this is larger than t1
    assert t1 < t3
    assert t3 > t1
    assert t1 <= t3
    assert t3 >= t1
    assert t1 != t3
    assert t3 != t1
    assert not (t1 == t3)
    assert not (t3 == t1)
    assert not (t1 > t3)
    assert not (t3 < t1)
    assert not (t1 >= t3)
    assert not (t3 <= t1)

    t4 = TimeDelta("-3/5")  # this is less than t1
    assert t4 < t1
    assert t1 > t4
    assert t4 <= t1
    assert t1 >= t4
    assert t4 != t1
    assert t1 != t4
    assert not (t4 == t1)
    assert not (t1 == t4)
    assert not (t4 > t1)
    assert not (t1 < t4)
    assert not (t4 >= t1)
    assert not (t1 <= t4)

    # Reverse comparison mechanism
    class TimeDeltaLike:
        def __init__(self):
            self.fractional_days = Fraction(-7, 4)

        def __eq__(self, other):
            return self.fractional_days == other.fractional_days

        def __ne__(self, other):
            return self.fractional_days != other.fractional_days

        def __lt__(self, other):
            return self.fractional_days < other.fractional_days

        def __le__(self, other):
            return self.fractional_days <= other.fractional_days

        def __gt__(self, other):
            return self.fractional_days > other.fractional_days

        def __ge__(self, other):
            return self.fractional_days >= other.fractional_days

    tdl = TimeDeltaLike()
    td5 = TimeDelta(-3)
    td6 = TimeDelta(-1.75)
    td7 = TimeDelta(4, 5)
    assert not (td5 == tdl)
    assert td6 == tdl
    assert not (td7 == tdl)
    assert td5 != tdl
    assert not (td6 != tdl)
    assert td7 != tdl
    assert td5 < tdl
    assert not (td6 < tdl)
    assert not (td7 < tdl)
    assert td5 <= tdl
    assert td6 <= tdl
    assert not (td7 <= tdl)
    assert not (td5 > tdl)
    assert not (td6 > tdl)
    assert td7 > tdl
    assert not (td5 >= tdl)
    assert td6 >= tdl
    assert td7 >= tdl

    class SomeClass:
        def __init__(self):
            self.fractional_days = 'unchecked'

    td0 = TimeDelta(0)

    # exception with non-numeric types
    for par in ("1", (1,), [1], {1: 1}, (), [], {}, None, SomeClass()):
        assert not (td0 == par)
        assert td0 != par
        with pytest.raises(TypeError):
            td0 < par
        with pytest.raises(TypeError):
            td0 > par
        with pytest.raises(TypeError):
            td0 <= par
        with pytest.raises(TypeError):
            td0 >= par

    # exception with numeric types (all invalid) and other objects
    for par in (1, 1.0, Fraction(1, 1), Decimal(1), 1j, 1 + 1j, INF, NAN):
        assert not (td0 == par)
        assert td0 != par
        with pytest.raises(TypeError):
            td0 < par
        with pytest.raises(TypeError):
            td0 > par
        with pytest.raises(TypeError):
            td0 <= par
        with pytest.raises(TypeError):
            td0 >= par


def test_50_int_part_frac_part():
    for test_datum in timedelta_test_data:
        for input_value in test_datum.input_values:
            td = TimeDelta(input_value)
            assert td.int_part == test_datum.int_part
            assert td.frac_part == test_datum.frac_part


def test_51_int_frac():
    for test_datum in timedelta_test_data:
        for input_value in test_datum.input_values:
            td = TimeDelta(input_value)
            assert td.int() == TimeDelta(test_datum.int_part)
            assert td.frac() == TimeDelta(test_datum.frac_part)


def test_51_is_integer():
    for test_datum in timedelta_test_data:
        for input_value in test_datum.input_values:
            td = TimeDelta(input_value)
            assert td.is_integer() == (test_datum.frac_part == 0)


def test_90_subclass():
    # check that there is no interference from the interface mechanism and from possible additional arguments
    class TD(TimeDelta):
        the_answer = 42

        def __init__(self, *args, **kws):
            temp = kws.copy()
            self.extra = temp.pop("extra")
            TimeDelta.__init__(self, *args, **temp)

        def newmeth(self, start):
            return (start + self.fractional_days * 3) // 2

    td1 = TimeDelta("3/8")
    td2 = TD(0.375, extra=7)

    assert td2.the_answer == 42
    assert td2.extra == 7
    assert td1 == td2
    assert td2.newmeth(1) == 1
    assert td2.newmeth(-5) == -2


def test_91_subclass2():
    # check that all possible methods return subclass
    class TD(TimeDelta):
        pass

    td_sub = TD("5/7")
    assert type(td_sub + TimeDelta(0.5)) is TD
    assert type(td_sub - TimeDelta(0.5)) is TD
    assert type(td_sub * 3.5) is TD
    assert type(-1.5 * td_sub) is TD
    assert type(td_sub / 3.5) is TD
    assert type(td_sub // 3.5) is TD
    assert type(td_sub % 3.5) is TD
    # again, no need to test divmod
