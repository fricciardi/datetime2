# Time class tests

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

from datetime2 import Time, TimeDelta


INF = float("inf")
NAN = float("nan")


time_test_data = [
    [Fraction(0, 1), [0, Fraction(0), Decimal("0"), 0.0, "0", "0/33"]],
    [Fraction(1, 4), [Fraction(1, 4), Decimal("0.25"), 0.25, "0.25", "1/4"]]
]
time_test_data_num_den = [
    [Fraction(2, 3), [(2, 3), (-4, -6)]],
    [Fraction(1, 7), [(1, 7), (-3, -21)]]
]
# we are not going to test more values, because our purpose is not to test the Fraction constructor :-)

utcoffset_test_data = [
    [Fraction(0, 1),  [0, Fraction(0), Decimal("0"), 0.0, "0", "0/33"]],
    [Fraction(1, 4),  [Fraction(1, 4), Decimal("0.25"), 0.25, "0.25", "1/4"]],
    [Fraction(1, -4), [Fraction(-1, 4), Decimal("-0.25"), -0.25, "-0.25", "-1/4"]]
]

# but we want to test with a few strange values
time_strange_test_data = [
    Fraction(123, 4567),
    0.999999,
    "0.999999",
    "0.0000001",
    "5/456789"
]
time_strange_num_den_test_data = [
    (123, 4567),
    (0, 1),
    (9999, 10000)
]
utcoffset_strange_test_data = [
    1,
    Fraction(123, 4567),
    0.999999,
    "0.999999",
    "0.0000001",
    "5/456789",
    -1,
    Fraction(-123, 4567),
    -0.999999,
    "-0.999999",
    "-0.0000001",
    "-5/456789"
]


def test_00_constructor_default():
    # the day_frac argument can be anything that can be passed to the fractions.Fraction constructor
    for day_frac, input_values in time_test_data:
        for input_value in input_values:
            assert Time(input_value).day_frac == day_frac

    # "strange" values
    for input_value in time_strange_test_data:
        Time(input_value)

    # a TypeError exception is raised if the argument type is not one of the accepted types
    # exception with no or three parameters
    with pytest.raises(TypeError):
        Time()
    with pytest.raises(TypeError):
        Time(1, 2, 3)

    # exception with non-numeric types
    for par in (1j, (1,), [1], {1: 1}, [], {}, None, (1, 2), (1, 2, 3)):
        with pytest.raises(TypeError):
            Time(par)

    # the resulting value must be equal or greater than 0 and less than 1
    for par in (-0.00001, 1, 1.00000001, 10000, -10000):
        with pytest.raises(ValueError):
            Time(par)


def test_01_constructor_default_numden():
    # the day_frac argument can be a numerator and denominator
    for day_frac, input_values in time_test_data_num_den:
        for input_value in input_values:
            assert Time(input_value[0], input_value[1]).day_frac == day_frac

    # strange values with num/den
    for input_value in time_strange_num_den_test_data:
        Time(input_value[0], input_value[1])

    # a TypeError exception is raised if the argument type is not one of the accepted types
    # exception with non-numeric types
    for par in (1j, (1,), [1], {1: 1}, [], {}, (1, 2), (1, 2, 3)):
        with pytest.raises(TypeError):
            Time(par, 2)
            Time(1, par)
    # None is invalid as first argument
    with pytest.raises(TypeError):
        Time(None, 2)

    # the resulting value must be equal or greater than 0 and less than 1
    for num, den in (
            (1000, 1),
            (4, 2),
            (Fraction(1.000001), 1),
            (2, 2),
            (-1, -1),
            (Fraction(-0.000001), 1),
            (-1, 1000000),
            (-3, 3),
            (1000000, -2),
    ):
        with pytest.raises(ValueError):
            Time(num, den)

    # denominator should not be 0
    with pytest.raises(ZeroDivisionError):
        Time(2, 0)


def test_02_constructor_default_w_utcoffset():
    # the utcoffset argument can be anything that can be passed to the fractions.Fraction constructor
    for utcoffset_frac, input_values in utcoffset_test_data:
        for input_value in input_values:
            assert Time("0.2222", utcoffset=input_value).utcoffset == utcoffset_frac

    # strange values
    for input_value in utcoffset_strange_test_data:
        Time("0.3333", utcoffset=input_value)

    # a TypeError exception is raised if the argument type is not one of the accepted types
    # exception with invalid parameter name
    with pytest.raises(TypeError):
        Time(1, foobar="barfoo")
    with pytest.raises(TypeError):
        Time(1, 2, foobar="barfoo")

    # exception with non-numeric types
    for par in (1j, (1,), [1], {1: 1}, [], {}, (1, 2), (1, 2, 3)):
        with pytest.raises(TypeError):
            Time("0.4444", utcoffset=par)

    # the resulting value must be equal or greater than -1 and less or equal to 1."""
    for par in (-100, -1.00001, 1.00000001, 100):
        with pytest.raises(ValueError):
            Time("0.5555", utcoffset=par)
        with pytest.raises(ValueError):
            Time(2, 3, utcoffset=par)


def test_03_constructor_now():
    # return an object that represents the current moment in the day
    # for the time being, let's use the good old datetime module :-)
    import datetime

    # we must ensure that at least once in three times we get the same values in seconds
    count = 0
    while count < 3:
        datetime_now = datetime.datetime.now()
        time_now = Time.now()
        datetime_frac_seconds = (
                datetime_now.hour * 3600
                + datetime_now.minute * 60
                + datetime_now.second
        )
        if int(time_now.day_frac * 86400) == datetime_frac_seconds:
            break
        count += 1
    assert count < 3, "Unable to get at least one a correct Time.now()"
    # I am commenting the code to test utcoffset, because I have no independent way of testing it
    # assert int(time_now.utcoffset) == Fraction(time.localtime().tm_gmtoff, 86400)


def test_04_constructor_now_w_utcoffset():
    # return an aware object that represents the current moment in the day
    # for the time being, let's use the good old datetime module :-)
    import datetime

    for utcoffset_frac, input_values in utcoffset_test_data:
        utcoffset_seconds = utcoffset_frac * 86400
        for input_value in input_values:
            # we must ensure that at least once in three times we get the same values in seconds
            count = 0
            while count < 3:
                datetime_now = datetime.datetime.utcnow()
                time_now = Time.now(utcoffset=input_value)
                datetime_frac_seconds = (
                        datetime_now.hour * 3600
                        + datetime_now.minute * 60
                        + datetime_now.second
                        + utcoffset_seconds
                )
                if int(time_now.day_frac * 86400) == datetime_frac_seconds:
                    break
                count += 1
            assert count < 3, "Unable to get at least one a correct Time.now(utcoffset=0)"
            assert time_now.utcoffset == utcoffset_frac

    # a TypeError exception is raised if the argument type is not one of the accepted types
    # exception with invalid parameter name
    with pytest.raises(TypeError):
        Time(foobar="barfoo")

    # exception with non-numeric types
    for par in (1j, (1,), [1], {1: 1}, [], {}, (1, 2), (1, 2, 3)):
        with pytest.raises(TypeError):
            Time.now(utcoffset=par)

    # the resulting value must be equal or greater than -1 and less or equal to 1."""
    for par in (-100, -1.00001, 1.00000001, 100):
        with pytest.raises(ValueError):
            Time.now(utcoffset=par)


def test_05_constructor_localnow():
    # return a naive object that represents the current moment in the day with local time
    # for the time being, let's use the good old datetime module :-)
    import datetime

    # we must ensure that at least once in three times we get the same values in seconds
    count = 0
    while count < 3:
        datetime_now = datetime.datetime.now()
        time_now = Time.localnow()
        datetime_frac_seconds = (
                datetime_now.hour * 3600
                + datetime_now.minute * 60
                + datetime_now.second
        )
        if int(time_now.day_frac * 86400) == datetime_frac_seconds:
            break
        count += 1
    assert count < 3, "Unable to get at least one a correct Time.localnow()"
    assert time_now.utcoffset is None


def test_06_constructor_utcnow():
    # return a naive object that represents the current moment in the day with UTC time
    # for the time being, let's use the good old datetime module :-)
    import datetime

    # we must ensure that at least once in three times we get the same values in seconds
    count = 0
    while count < 3:
        datetime_now = datetime.datetime.utcnow()
        time_now = Time.utcnow()
        datetime_frac_seconds = (
                datetime_now.hour * 3600
                + datetime_now.minute * 60
                + datetime_now.second
        )
        if int(time_now.day_frac * 86400) == datetime_frac_seconds:
            break
        count += 1
    assert count < 3, "Unable to get at least one a correct Time.utcnow()"
    assert time_now.utcoffset is None


def test_10_hash_equality():
    # Time instances are immutable
    t1 = Time("3/5")
    t2 = Time(3, 5)
    assert hash(t1) == hash(t2)
    dic = {t1: 1}
    assert dic[t2] == 1
    dic[t2] = 2
    assert len(dic) == 1
    assert dic[t1] == 2

    t3 = Time(3000001, 5000000)
    assert hash(t1) != hash(t3)
    dic[t3] = 3
    assert len(dic) == 2
    assert dic[t3] == 3

    # now with utcoffset
    # Time instances are immutable
    t4 = Time("3/5", utcoffset=-0.25)
    t5 = Time(4, 5, utcoffset="-1/20")
    assert hash(t4) == hash(t5)    # t4 and t5 indicate the same time
    assert hash(t4) != hash(t1)
    assert hash(t4) != hash(t2)
    dic[t4] = 4
    assert len(dic) == 3
    assert dic[t5] == 4
    dic[t5] = 5
    assert dic[t4] == 5

    t6 = Time(Decimal("0.2"), utcoffset="-13/20")  # as t4, one day earlier
    assert hash(t6) == hash(t4)
    assert dic[t6] == 5
    dic[t6] = 6
    assert len(dic) == 3
    assert dic[t4] == 6


def test_11_pickling():
    global Derived

    # without utcoffset
    for day_frac, input_values in time_test_data:
        for input_value in input_values:
            t = Time(input_value)
            for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
                pickled = pickle.dumps(t, protocol)
                unpickled = pickle.loads(pickled)
                assert t == unpickled
    # with utcoffset
    for day_frac, input_values in time_test_data:
        for input_value in input_values:
            t = Time(0.25, utcoffset=input_value)
            for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
                pickled = pickle.dumps(t, protocol)
                unpickled = pickle.loads(pickled)
                assert t == unpickled

    class Derived(Time):
        def __init__(self, day_frac, dummy):
            self.dummy = dummy
            Time.__init__(self, day_frac)

        def __eq__(self, other):
            return self.dummy == other.dummy and Time.__eq__(self, other)

    for day_frac, input_values in time_test_data:
        der = Derived(day_frac, 42)
        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            pickled = pickle.dumps(der, protocol)
            unpickled = pickle.loads(pickled)
            assert isinstance(unpickled, Time)
            assert isinstance(unpickled, Derived)
            assert unpickled.dummy == 42
            assert der == unpickled


def test_12_bool():
    # In boolean contexts, all Time instances are considered to be true
    # without utcoffset
    for day_frac, input_values in time_test_data:
        for input_value in input_values:
            assert Time(input_value)
    for day_frac, input_values in time_test_data_num_den:
        for input_value in input_values:
            assert Time(input_value[0], input_value[1])
    # with utcoffset
    for utcoffset_frac, input_values in utcoffset_test_data:
        for input_value in input_values:
            assert Time("0.2222", utcoffset=input_value)


def test_20_attributes():
    # the attributes of a Time instance are read-only
    t1 = Time("0.12345")
    with pytest.raises(AttributeError):
        t1.day_frac = Fraction(3, 7)
        t1.utcoffset = Fraction(1, 11)
    t2 = Time("0.6789", utcoffset="-1/2")
    with pytest.raises(AttributeError):
        t2.day_frac = Fraction(3, 7)
        t2.utcoffset = Fraction(1, 11)
    # Test reaction with unknown attributes
    # I want to do this, because Time will have attributes added at runtime
    # let's tests this both on class and instance
    with pytest.raises(AttributeError):
        Time.unknown
    t = Time("0.12345")
    with pytest.raises(AttributeError):
        t.unknown
    t = Time("0.12345", utcoffset=0)
    with pytest.raises(AttributeError):
        t.unknown


def test_30_repr():
    import datetime2

    for day_frac, input_values in time_test_data:
        for input_value in input_values:
            t = Time(input_value)
            time_repr = repr(t)
            names, args = time_repr.split("(")
            assert names.split(".") == ["datetime2", "Time"]
            args = args[:-1]  # drop ')'
            assert eval(args) == str(day_frac)
            assert t == eval(time_repr)

    for day_frac, input_values in time_test_data:
        for input_value in input_values:
            t = Time("0.25", utcoffset=input_value)
            time_repr = repr(t)
            names, args = time_repr.split("(")
            assert names.split(".") == ["datetime2", "Time"]
            args = '(' + args  # there is already a ')'
            args = args.replace("utcoffset=", '')
            assert eval(args) == (str(Fraction(1, 4)), str(day_frac))
            assert t == eval(time_repr)


def test_31_str():
    for day_frac, input_values in time_test_data:
        for input_value in input_values:
            t = Time(input_value)
            string = str(t)
            assert string.endswith(" of a day")
            assert string[:-9] == str(day_frac)

    for day_frac, input_values in time_test_data:
        for input_value in input_values:
            t = Time(0.25, utcoffset=input_value)
            string = str(t)
            assert string.startswith("1/4 of a day, ")
            assert string.endswith(" of a day from UTC")
            assert string[14:-18] == str(day_frac)


def test_40_operations():
    a = Time(0)
    b = Time(0.25)
    c = Time(0.75)
    zero = TimeDelta(0)
    # please remember that TimeDelta is in days
    plus_half = TimeDelta(0.5)
    minus_half = TimeDelta(-1.5)
    integer = TimeDelta(3)

    # Addition between Time and TimeDelta
    # test with zero, negative and positive dates
    assert a + zero == Time(0)
    assert a + plus_half == Time(0.5)
    assert a + minus_half == Time(0.5)
    assert a + integer == Time(0)
    assert b + zero == Time(0.25)
    assert b + plus_half == Time(0.75)
    assert b + minus_half == Time(0.75)
    assert b + integer == Time(0.25)
    assert c + zero == Time(0.75)
    assert c + plus_half == Time(0.25)
    assert c + minus_half == Time(0.25)
    assert c + integer == Time(0.75)

    # Reversed addition between Time and TimeDelta
    # test with zero, negative and positive dates
    assert zero + a == Time(0)
    assert plus_half + a == Time(0.5)
    assert minus_half + a == Time(0.5)
    assert integer + a == Time(0)
    assert zero + b == Time(0.25)
    assert plus_half + b == Time(0.75)
    assert minus_half + b == Time(0.75)
    assert integer + b == Time(0.25)
    assert zero + c == Time(0.75)
    assert plus_half + c == Time(0.25)
    assert minus_half + c == Time(0.25)
    assert integer + c == Time(0.75)

    # subtraction between Time and TimeDelta, reverse is not defined
    # test with zero, negative and positive Times
    assert a - zero == Time(0)
    assert a - plus_half == Time(0.5)
    assert a - minus_half == Time(0.5)
    assert a - integer == Time(0)
    assert b - zero == Time(0.25)
    assert b - plus_half == Time(0.75)
    assert b - minus_half == Time(0.75)
    assert b - integer == Time(0.25)
    assert c - zero == Time(0.75)
    assert c - plus_half == Time(0.25)
    assert c - minus_half == Time(0.25)
    assert c - integer == Time(0.75)

    # Same with utcoffset
    d = Time(0, utcoffset="1/3")
    e = Time(0.25, utcoffset="-1/4")
    f = Time(0.75, utcoffset="1/6")
    # test with zero, negative and positive dates
    assert d + zero == Time(0, utcoffset="1/3")
    assert d + plus_half == Time(0.5, utcoffset="1/3")
    assert d + minus_half == Time(0.5, utcoffset="1/3")
    assert d + integer == Time(0, utcoffset="1/3")
    assert e + zero == Time(0.25, utcoffset="-1/4")
    assert e + plus_half == Time(0.75, utcoffset="-1/4")
    assert e + minus_half == Time(0.75, utcoffset="-1/4")
    assert e + integer == Time(0.25, utcoffset="-1/4")
    assert f + zero == Time(0.75, utcoffset="1/6")
    assert f + plus_half == Time(0.25, utcoffset="1/6")
    assert f + minus_half == Time(0.25, utcoffset="1/6")
    assert f + integer == Time(0.75, utcoffset="1/6")

    # Reversed addition between Time and TimeDelta
    # test with zero, negative and positive dates
    assert zero + d == Time(0, utcoffset="1/3")
    assert plus_half + d == Time(0.5, utcoffset="1/3")
    assert minus_half + d == Time(0.5, utcoffset="1/3")
    assert integer + d == Time(0, utcoffset="1/3")
    assert zero + e == Time(0.25, utcoffset="-1/4")
    assert plus_half + e == Time(0.75, utcoffset="-1/4")
    assert minus_half + e == Time(0.75, utcoffset="-1/4")
    assert integer + e == Time(0.25, utcoffset="-1/4")
    assert zero + f == Time(0.75, utcoffset="1/6")
    assert plus_half + f == Time(0.25, utcoffset="1/6")
    assert minus_half + f == Time(0.25, utcoffset="1/6")
    assert integer + f == Time(0.75, utcoffset="1/6")

    # subtraction between Time and TimeDelta, reverse is not defined
    # test with zero, negative and positive Times
    assert d - zero == Time(0, utcoffset="1/3")
    assert d - plus_half == Time(0.5, utcoffset="1/3")
    assert d - minus_half == Time(0.5, utcoffset="1/3")
    assert d - integer == Time(0, utcoffset="1/3")
    assert e - zero == Time(0.25, utcoffset="-1/4")
    assert e - plus_half == Time(0.75, utcoffset="-1/4")
    assert e - minus_half == Time(0.75, utcoffset="-1/4")
    assert e - integer == Time(0.25, utcoffset="-1/4")
    assert c - zero == Time(0.75, utcoffset="1/6")
    assert c - plus_half == Time(0.25, utcoffset="1/6")
    assert c - minus_half == Time(0.25, utcoffset="1/6")
    assert c - integer == Time(0.75, utcoffset="1/6")

    # corner cases with overflows and underflows
    g = Time("1/2")
    assert g + plus_half == Time(0)
    assert g - plus_half == Time(0)
    assert g + minus_half == Time(0)
    assert g - minus_half == Time(0)
    assert plus_half + g == Time(0)
    assert plus_half - g == Time(0)
    assert minus_half + g == Time(0)
    assert minus_half - g == Time(0)
    h = Time(0.25)
    td_fr14 = TimeDelta("1/4")
    td_fr34 = TimeDelta("3/4")
    td_fr54 = TimeDelta("5/4")
    td_fr74 = TimeDelta("7/4")
    assert h - td_fr14 == Time(0)
    assert h + td_fr34 == Time(0)
    assert h - td_fr54 == Time(0)
    assert h + td_fr74 == Time(0)
    i = Time("1/2", utcoffset='1/5')
    assert i + plus_half == Time(0, utcoffset='1/5')
    assert i - plus_half == Time(0, utcoffset='1/5')
    assert i + minus_half == Time(0, utcoffset='1/5')
    assert i - minus_half == Time(0, utcoffset='1/5')
    assert plus_half + i == Time(0, utcoffset='1/5')
    assert plus_half - i == Time(0, utcoffset='1/5')
    assert minus_half + i == Time(0, utcoffset='1/5')
    assert minus_half - i == Time(0, utcoffset='1/5')
    j = Time(0.25, utcoffset='-2/5')
    td_fr14 = TimeDelta("1/4")
    td_fr34 = TimeDelta("3/4")
    td_fr54 = TimeDelta("5/4")
    td_fr74 = TimeDelta("7/4")
    assert j - td_fr14 == Time(0, utcoffset='-2/5')
    assert j + td_fr34 == Time(0, utcoffset='-2/5')
    assert j - td_fr54 == Time(0, utcoffset='-2/5')
    assert j + td_fr74 == Time(0, utcoffset='-2/5')

    # disallowed operations
    k = Time("3/4")
    l = Time("2/5", utcoffset="1/8")

    # Add/sub int, float, string, complex, specials and containers should be illegal
    for obj in (10, 34.5, "abc", 1 + 2j, INF, NAN, {}, [], ()):
        with pytest.raises(TypeError):
            k + obj
        with pytest.raises(TypeError):
            k - obj
        with pytest.raises(TypeError):
            obj + k
        with pytest.raises(TypeError):
            obj - k
        with pytest.raises(TypeError):
            l + obj
        with pytest.raises(TypeError):
            l - obj
        with pytest.raises(TypeError):
            obj + l
        with pytest.raises(TypeError):
            obj - l

    # Reverse operations
    with pytest.raises(TypeError):
        TimeDelta(-0.25) - k
    with pytest.raises(TypeError):
        TimeDelta(-0.25) - l

    for obj in (1, 1.1, Time("2/5")):
        with pytest.raises(TypeError):
            k * obj
        with pytest.raises(TypeError):
            obj * k
        with pytest.raises(TypeError):
            k / obj
        with pytest.raises(TypeError):
            obj / k
        with pytest.raises(TypeError):
            k // obj
        with pytest.raises(TypeError):
            obj // k
        with pytest.raises(TypeError):
            pow(k, obj)
        with pytest.raises(TypeError):
            pow(obj, k)
        with pytest.raises(TypeError):
            k ^ obj
        with pytest.raises(TypeError):
            obj ^ k
        with pytest.raises(TypeError):
            k >> obj
        with pytest.raises(TypeError):
            obj >> k
        with pytest.raises(TypeError):
            k << obj
        with pytest.raises(TypeError):
            obj << k
        with pytest.raises(TypeError):
            l * obj
        with pytest.raises(TypeError):
            obj * l
        with pytest.raises(TypeError):
            l / obj
        with pytest.raises(TypeError):
            obj / l
        with pytest.raises(TypeError):
            l // obj
        with pytest.raises(TypeError):
            obj // l
        with pytest.raises(TypeError):
            pow(l, obj)
        with pytest.raises(TypeError):
            pow(obj, l)
        with pytest.raises(TypeError):
            l ^ obj
        with pytest.raises(TypeError):
            obj ^ l
        with pytest.raises(TypeError):
            l >> obj
        with pytest.raises(TypeError):
            obj >> l
        with pytest.raises(TypeError):
            l << obj
        with pytest.raises(TypeError):
            obj << l


def test_41_comparisons():
    t1 = Time("3/8")
    t2 = Time(0.375)
    assert t1 == t2
    assert t1 <= t2
    assert t1 >= t2
    assert not (t1 != t2)
    assert not (t1 < t2)
    assert not (t1 > t2)

    t3 = Time("5/7")  # this is larger than t1
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

    # Reverse comparison mechanism
    class TimeLike:
        def __init__(self):
            self.day_frac = Fraction(3, 4)
            self.utcoffset = 'unchecked'

        def __eq__(self, other):
            return self.day_frac == other.day_frac

        def __ne__(self, other):
            return self.day_frac != other.day_frac

        def __lt__(self, other):
            return self.day_frac < other.day_frac

        def __le__(self, other):
            return self.day_frac <= other.day_frac

        def __gt__(self, other):
            return self.day_frac > other.day_frac

        def __ge__(self, other):
            return self.day_frac >= other.day_frac

    tl = TimeLike()
    t5 = Time(1, 2)
    t6 = Time("3/4")
    t7 = Time(4, 5)
    assert not (t5 == tl)
    assert t6 == tl
    assert not (t7 == tl)
    assert t5 != tl
    assert not (t6 != tl)
    assert t7 != tl
    assert t5 < tl
    assert not (t6 < tl)
    assert not (t7 < tl)
    assert t5 <= tl
    assert t6 <= tl
    assert not (t7 <= tl)
    assert not (t5 > tl)
    assert not (t6 > tl)
    assert t7 > tl
    assert not (t5 >= tl)
    assert t6 >= tl
    assert t7 >= tl

    class SomeClass1:
        def __init__(self):
            self.day_frac = 'unchecked'

    class SomeClass2:
        def __init__(self):
            self.utcoffset = 'unchecked'

    t0 = Time(0)

    # exception with non-numeric types
    for par in ("1", (1,), [1], {1: 1}, (), [], {}, None, SomeClass1(), SomeClass2()):
        assert not (t0 == par)
        assert t0 != par
        with pytest.raises(TypeError):
            t0 < par
        with pytest.raises(TypeError):
            t0 > par
        with pytest.raises(TypeError):
            t0 <= par
        with pytest.raises(TypeError):
            t0 >= par

    # exception with numeric types (all invalid) and other objects
    for par in (1, 1.0, Fraction(1, 1), Decimal(1), 1j, 1 + 1j, INF, NAN):
        assert not (t0 == par)
        assert t0 != par
        with pytest.raises(TypeError):
            t0 < par
        with pytest.raises(TypeError):
            t0 > par
        with pytest.raises(TypeError):
            t0 <= par
        with pytest.raises(TypeError):
            t0 >= par

    # mixing aware and naive instances
    t8 = Time(11, 24, utcoffset="1/6")
    assert t1 != t8
    assert t8 != t1
    assert not (t1 == t8)
    assert not (t8 == t1)
    with pytest.raises(TypeError):
        t1 < t8
    with pytest.raises(TypeError):
        t1 <= t8
    with pytest.raises(TypeError):
        t1 > t8
    with pytest.raises(TypeError):
        t1 >= t8
    with pytest.raises(TypeError):
        t8 < t1
    with pytest.raises(TypeError):
        t8 <= t1
    with pytest.raises(TypeError):
        t8 > t1
    with pytest.raises(TypeError):
        t8 >= t1


def test_42_comparisons_with_utcoffset():
    t1 = Time("1/8", utcoffset="-1/3")
    t2 = Time(0.875, utcoffset=Fraction(5, 12))  # this is equal to t1
    t3 = Time("2/3", utcoffset=0.125)  # this is larger than t1
    t4 = Time("1/6", utcoffset="17/24")  # this is equal to t1, one day earlier, should compare equal
    assert t1 == t2
    assert t1 <= t2
    assert t1 >= t2
    assert not (t1 != t2)
    assert not (t1 < t2)
    assert not (t1 > t2)

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
    assert t2 < t3  # repeating the tests with an instance with negative utcoffset
    assert t3 > t2
    assert t2 <= t3
    assert t3 >= t2
    assert t2 != t3
    assert t3 != t2
    assert not (t2 == t3)
    assert not (t3 == t2)
    assert not (t2 > t3)
    assert not (t3 < t2)
    assert not (t2 >= t3)
    assert not (t3 <= t2)

    assert t1 != t4
    assert not (t1 == t4)
    assert t4 < t1
    assert t4 <= t1
    assert t1 > t4
    assert t1 >= t4

    # Reverse comparison mechanism
    class TimeLike:
        def __init__(self):
            self.day_frac = Fraction(0.75)
            self.utcoffset = Fraction("1/4")

        # what follows is not a proper implementation, but it is enough for our tests
        def __eq__(self, other):
            return self.day_frac + self.utcoffset == other.day_frac + other.utcoffset

        def __ne__(self, other):
            return self.day_frac + self.utcoffset != other.day_frac + other.utcoffset

        def __lt__(self, other):
            return self.day_frac + self.utcoffset < other.day_frac + other.utcoffset

        def __le__(self, other):
            return self.day_frac + self.utcoffset <= other.day_frac + other.utcoffset

        def __gt__(self, other):
            return self.day_frac + self.utcoffset > other.day_frac + other.utcoffset

        def __ge__(self, other):
            return self.day_frac + self.utcoffset >= other.day_frac + other.utcoffset

    tl = TimeLike()
    # We need not implement naivety checks, which are delegated to the Time-like class, not under test
    t5 = Time(1, 2, utcoffset="-1/3")
    t6 = Time("3/4", utcoffset=0.25)
    t7 = Time(4, 5, utcoffset=Fraction(3, 8))
    assert not (t5 == tl)
    assert t6 == tl
    assert not (t7 == tl)
    assert t5 != tl
    assert not (t6 != tl)
    assert t7 != tl
    assert t5 < tl
    assert not (t6 < tl)
    assert not (t7 < tl)
    assert t5 <= tl
    assert t6 <= tl
    assert not (t7 <= tl)
    assert not (t5 > tl)
    assert not (t6 > tl)
    assert t7 > tl
    assert not (t5 >= tl)
    assert t6 >= tl
    assert t7 >= tl

    t8 = Time(11, 24)  # this is naive
    assert t8 != t1
    assert not (t8 == t1)
    with pytest.raises(TypeError):
        t8 < t1
    with pytest.raises(TypeError):
        t8 <= t1
    with pytest.raises(TypeError):
        t8 > t1
    with pytest.raises(TypeError):
        t8 >= t1


def test_42_operations_and_naivety():
    # addition or subtraction with timedelta preserves naivety
    a = Time("3/8")
    b = Time(3, 4, utcoffset="1/6")

    for td in (TimeDelta(0.5), TimeDelta(-0.25), TimeDelta(3), TimeDelta(-2.75)):
        res_a_plus = a + td
        assert res_a_plus.utcoffset is None
        res_a_minus = a - td
        assert res_a_minus.utcoffset is None
        res_b_plus = b + td
        assert res_b_plus.utcoffset == Fraction(1, 6)
        res_b_minus = b - td
        assert res_b_minus.utcoffset == Fraction(1, 6)

    # time objects in a subtraction must have the same naivety
    c = Time(5, 6, utcoffset="-2/3")
    d = Time(1, 3)
    dummy = a - d
    dummy = b - c
    with pytest.raises(ValueError):
        dummy = a - b
    with pytest.raises(ValueError):
        dummy = c - d


def test_43_time_subtraction():
    a = Time("1/2")
    b = Time(0.5)
    assert a - b == TimeDelta(0)

    c = Time(0)
    assert a - c == TimeDelta(Fraction(1, 2))
    assert c - a == TimeDelta(Fraction(1, 2))  # -0.5 under flows to 0.5

    d = Time(0.25)
    e = Time("3/4")
    assert d - e == TimeDelta(Fraction(1, 2))  # -0.5 under flows to 0.5


def test_90_subclass():
    # check that there is no interference from the interface mechanism and from possible additional arguments
    class T(Time):
        the_answer = 42

        def __init__(self, *args, **kws):
            temp = kws.copy()
            self.extra = temp.pop("extra")
            Time.__init__(self, *args, **temp)

        def newmeth(self, start):
            return (start + self.day_frac * 3) // 2

    t1 = Time("3/8")
    t2 = T(0.375, extra=7)

    assert t2.the_answer == 42
    assert t2.extra == 7
    assert t1 == t2
    assert t2.newmeth(1) == 1
    assert t2.newmeth(-5) == -2

    t3 = Time("3/8", utcoffset=0.5)
    t4 = T(0.375, extra=7, utcoffset=0.5)

    assert t4.the_answer == 42
    assert t4.extra == 7
    assert t3 == t4
    assert t4.newmeth(1) == 1
    assert t4.newmeth(-5) == -2


def test_91_subclass2():
    # check that all possible methods return subclass
    class T(Time):
        pass

    assert type(T.now()) is T
    assert type(T.localnow()) is T
    assert type(T.utcnow()) is T

    t_sub = T("5/7")
    assert type(t_sub + TimeDelta(0.5)) is T
    assert type(t_sub - TimeDelta(0.5)) is T
