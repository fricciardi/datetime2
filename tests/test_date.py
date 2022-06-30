# datetime2 package test

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

from decimal import Decimal
from fractions import Fraction
import pickle
import pytest

from datetime2 import Date, Time, TimeDelta


INF = float("inf")
NAN = float("nan")

# TODO: use named tuple for test data

#############################################################################
# Date tests
#
date_test_data = (
    -2,
    -1,
    0,
    1,
    2,
    -1000,
    1000,
    -123456789,
    123456789,
    -999999999,
    999999999,
    -1000000000,
    1000000000,
)


def test_00_constructor_default():
    # test for some valid values, only valid type is integer
    for day_count in date_test_data:
        assert Date(day_count).day_count == day_count
    # exception with no or two parameters
    with pytest.raises(TypeError):
        Date()
    with pytest.raises(TypeError):
        Date(1, 2)
    # exception with non-numeric types
    for par in ("1", (1,), [1], {1: 1}, (), [], {}, None):
        with pytest.raises(TypeError):
            Date(par)
    # exception with invalid numeric types
    for par in (1.0, Fraction(1, 1), Decimal(1), 1j):
        with pytest.raises(TypeError):
            Date(par)


def test_02_constructor_today():
    # for the time being, let's use the good old datetime module :-)
    import datetime

    # we need to ensure that we are not testing across date change
    for dummy in range(3):
        today_before = datetime.date.today()
        date_today = Date.today()
        today_after = datetime.date.today()
        if today_before == today_after:
            break
    assert date_today.day_count == today_before.toordinal()


def test_10_hash_equality():
    # Date instances are immutable and can be used as dictionary keys
    d1 = Date(42)
    d2 = Date(42)
    assert hash(d1) == hash(d2)

    dic = {d1: 1}
    dic[d2] = 2
    assert len(dic) == 1
    assert dic[d1] == 2
    assert dic[d2] == 2

    d3 = Date(32) + TimeDelta(10)
    assert hash(d1) == hash(d3)

    dic[d3] = 2
    assert len(dic) == 1
    assert dic[d3] == 2


def test_11_pickling():
    global Derived

    for day_count in date_test_data:
        d = Date(day_count)
        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            pickled = pickle.dumps(d, protocol)
            unpickled = pickle.loads(pickled)
            assert isinstance(unpickled, Date)
            assert d == unpickled

    class Derived(Date):
        def __init__(self, day_count, dummy):
            self.dummy = dummy
            Date.__init__(self, day_count)

        def __eq__(self, other):
            return self.dummy == other.dummy and Date.__eq__(self, other)

    for day_count in date_test_data:
        der = Derived(day_count, 42)
        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            pickled = pickle.dumps(der, protocol)
            unpickled = pickle.loads(pickled)
            assert isinstance(unpickled, Date)
            assert isinstance(unpickled, Derived)
            assert unpickled.dummy == 42
            assert der == unpickled


def test_12_bool():
    # In boolean contexts, all Date instances are considered to be true
    for day_count in date_test_data:
        assert Date(day_count)


def test_20_attribute():
    # the day_count attribute is read-only
    d = Date(1)
    with pytest.raises(AttributeError):
        d.day_count = 3
    # Test reaction with unknown attributes
    # I want to do this, because Date will have attributes added at runtime
    # let's tests this both on class and instance
    with pytest.raises(AttributeError):
        Date.unknown
    d = Date(1)
    with pytest.raises(AttributeError):
        d.unknown
    # attributes added at run time will work (I'll check gregorian: we surely have it :-) )
    d_greg = Date.gregorian(1, 2, 3)
    greg = d.gregorian


def test_30_repr():
    import datetime2

    for day_count in date_test_data:
        d = Date(day_count)
        date_repr = repr(d)
        names, args = date_repr.split("(")
        assert names.split(".") == ["datetime2", "Date"]
        args = args[:-1]  # drop ')'
        assert int(args) == day_count
        assert d == eval(date_repr)


def test_31_str():
    for day_count in date_test_data:
        d = Date(day_count)
        s = str(d)
        assert s[:5] == 'R.D. '
        assert int(s[5:]) == day_count


def test_40_operations():
    a = Date(0)
    b = Date(-3)
    c = Date(5)
    zero = TimeDelta(0)
    one = TimeDelta(1)
    minusone = TimeDelta(-1)

    # Addition between Date and TimeDelta
    # test with zero, negative and positive dates
    assert a + zero == Date(0)
    assert a + one == Date(1)
    assert a + minusone == Date(-1)
    assert b + zero == Date(-3)
    assert b + one == Date(-2)
    assert b + minusone == Date(-4)
    assert c + zero == Date(5)
    assert c + one == Date(6)
    assert c + minusone == Date(4)

    # Reverse addition between TimeDelta and Date
    # test with zero, negative and positive dates
    assert zero + a == Date(0)
    assert one + a == Date(1)
    assert minusone + a == Date(-1)
    assert zero + b == Date(-3)
    assert one + b == Date(-2)
    assert minusone + b == Date(-4)
    assert zero + c == Date(5)
    assert one + c == Date(6)
    assert minusone + c == Date(4)

    # subtraction between Date and TimeDelta, reverse is not defined
    # test with zero, negative and positive dates
    assert a - zero == Date(0)
    assert a - one == Date(-1)
    assert a - minusone == Date(1)
    assert b - zero == Date(-3)
    assert b - one == Date(-4)
    assert b - minusone == Date(-2)
    assert c - zero == Date(5)
    assert c - one == Date(4)
    assert c - minusone == Date(6)

    # subtraction between two Date's, reverse is not defined
    # test with zero, negative and positive dates
    assert a - a == TimeDelta(0)
    assert a - b == TimeDelta(3)
    assert a - c == TimeDelta(-5)
    assert b - a == TimeDelta(-3)
    assert b - b == TimeDelta(0)
    assert b - c == TimeDelta(-8)
    assert c - a == TimeDelta(5)
    assert c - b == TimeDelta(8)
    assert c - c == TimeDelta(0)

    # forbidden operations
    # These operations are invalid because TimeDelta is not integer.
    for value in (42.25, 41.75, -42.25, -41.75):
        with pytest.raises(ValueError):
            c + TimeDelta(value)
        with pytest.raises(ValueError):
            c - TimeDelta(value)

    # Add/sub int, float, string, complex, specials and containers should be illegal
    for obj in (10, 34.5, "abc", 1 + 2j, INF, NAN, {}, [], ()):
        with pytest.raises(TypeError):
            c + obj
        with pytest.raises(TypeError):
            c - obj
        with pytest.raises(TypeError):
            obj + c
        with pytest.raises(TypeError):
            obj - c

    # Reverse operations
    with pytest.raises(TypeError):
        TimeDelta(2) - c

    for obj in (1, 1.1, a):
        with pytest.raises(TypeError):
            c * obj
        with pytest.raises(TypeError):
            obj * c
        with pytest.raises(TypeError):
            c / obj
        with pytest.raises(TypeError):
            obj / c
        with pytest.raises(TypeError):
            c // obj
        with pytest.raises(TypeError):
            obj // c
        with pytest.raises(TypeError):
            pow(c, obj)
        with pytest.raises(TypeError):
            pow(obj, c)
        with pytest.raises(TypeError):
            c ^ obj
        with pytest.raises(TypeError):
            obj ^ c
        with pytest.raises(TypeError):
            c >> obj
        with pytest.raises(TypeError):
            obj >> c
        with pytest.raises(TypeError):
            c << obj
        with pytest.raises(TypeError):
            obj << c


def test_41_comparisons():
    d1 = Date(42)
    d2 = Date(42)
    assert d1 == d2
    assert d1 <= d2
    assert d1 >= d2
    assert not (d1 != d2)
    assert not (d1 < d2)
    assert not (d1 > d2)

    d3 = Date(4242)  # this is larger than d1
    assert d1 < d3
    assert d3 > d1
    assert d1 <= d3
    assert d3 >= d1
    assert d1 != d3
    assert d3 != d1
    assert not (d1 == d3)
    assert not (d3 == d1)
    assert not (d1 > d3)
    assert not (d3 < d1)
    assert not (d1 >= d3)
    assert not (d3 <= d1)

    # Reverse comparison mechanism
    class DateLike:
        def __init__(self):
            self.day_count = 42

        def __eq__(self, other):
            return self.day_count == other.day_count

        def __ne__(self, other):
            return self.day_count != other.day_count

        def __lt__(self, other):
            return self.day_count < other.day_count

        def __le__(self, other):
            return self.day_count <= other.day_count

        def __gt__(self, other):
            return self.day_count > other.day_count

        def __ge__(self, other):
            return self.day_count >= other.day_count

    dl = DateLike()
    d4 = Date(4)
    d42 = Date(42)
    d55 = Date(55)
    assert not (d4 == dl)
    assert d42 == dl
    assert not (d55 == dl)
    assert d4 != dl
    assert not (d42 != dl)
    assert d55 != dl
    assert d4 < dl
    assert not (d42 < dl)
    assert not (d55 < dl)
    assert d4 <= dl
    assert d42 <= dl
    assert not (d55 <= dl)
    assert not (d4 > dl)
    assert not (d42 > dl)
    assert d55 > dl
    assert not (d4 >= dl)
    assert d42 >= dl
    assert d55 >= dl

    # comparisons with invalid types
    class SomeClass:
        pass

    # exception with non-numeric types
    for par in ("1", (1,), [1], {1: 1}, (), [], {}, None, SomeClass()):
        assert not (d4 == par)
        assert d4 != par
        with pytest.raises(TypeError):
            d4 < par
        with pytest.raises(TypeError):
            d4 > par
        with pytest.raises(TypeError):
            d4 <= par
        with pytest.raises(TypeError):
            d4 >= par

    # exception with numeric types (all invalid)
    for par in (1, 1.0, Fraction(1, 1), Decimal(1), 1j, 1 + 1j, INF, NAN):
        assert not (d4 == par)
        assert d4 != par
        with pytest.raises(TypeError):
            d4 < par
        with pytest.raises(TypeError):
            d4 > par
        with pytest.raises(TypeError):
            d4 <= par
        with pytest.raises(TypeError):
            d4 >= par


def test_90_subclass1():
    # check that there is no interference from the interface mechanism and from possible additional arguments
    class D(Date):
        theAnswer = 42

        def __init__(self, *args, **kws):
            temp = kws.copy()
            self.extra = temp.pop("extra")
            Date.__init__(self, *args, **temp)

        def newmeth(self, start):
            return start + (self.day_count * 3) // 2

    d1 = Date(102013)
    d2 = D(102013, extra=7)

    assert d2.theAnswer == 42
    assert d2.extra == 7
    assert d1.day_count == d2.day_count
    assert d2.newmeth(-7) == (d1.day_count * 3) // 2 - 7


def test_91_subclass2():
    # check that all possible methods return subclass
    class D(Date):
        pass

    assert type(D.today()) is D

    d_sub = D(102030)
    assert type(d_sub + TimeDelta(1)) is D
    assert type(d_sub - TimeDelta(1)) is D
