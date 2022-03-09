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


class DummyToUtc:
    def __init__(self, num, den):
        self.num = num
        self.den = den

    def time_to_utc(self):
        return Fraction(self.num, self.den)


time_test_data = [
    [Fraction(0, 1), [0, Fraction(0), Decimal("0"), 0.0, "0", "0/33"]],
    [Fraction(1, 4), [Fraction(1, 4), Decimal("0.25"), 0.25, "0.25", "1/4"]]
]
time_test_data_num_den = [
    [Fraction(2, 3), [(2, 3), (-4, -6)]],
    [Fraction(1, 7), [(1, 7), (-3, -21)]]
]
# we are not going to test more values, because our purpose is not to test the Fraction constructor :-)

to_utc_test_data = [
    [Fraction(0, 1),  [0, Fraction(0), Decimal("0"), 0.0, "0", "0/33", DummyToUtc(0, -3)]],
    [Fraction(1, 4),  [Fraction(1, 4), Decimal("0.25"), 0.25, "0.25", "1/4", DummyToUtc(3, 12)]],
    [Fraction(1, -4), [Fraction(-1, 4), Decimal("-0.25"), -0.25, "-0.25", "-1/4", DummyToUtc(-3, 12), ]]
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
to_utc_strange_test_data = [
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


def test_000_constructor_default():
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


def test_001_constructor_default_numden():
    # the day_frac argument can be a numerator and denominator
    for day_frac, input_values in time_test_data_num_den:
        for input_value in input_values:
            assert Time(input_value[0], input_value[1]).day_frac == day_frac

    # strange values with num/den
    for input_value in time_strange_num_den_test_data:
        Time(input_value[0], input_value[1])

    # a TypeError exception is raised if the argument type is not one of the accepted types
    # exception with non-numeric types
    for par in (1j, (1,), [1], {1: 1}, [], {}, None, (1, 2), (1, 2, 3)):
        with pytest.raises(TypeError):
            Time(par, 2)

    # None is valid as second argument, so we are not testing it
    for par in (1j, (1,), [1], {1: 1}, [], {},       (1, 2), (1, 2, 3)):
        with pytest.raises(TypeError):
            Time(1, par)

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


def test_002_constructor_default_w_to_utc():
    # the to_utc argument can be anything that can be passed to the fractions.Fraction constructor
    for to_utc_frac, input_values in to_utc_test_data:
        for input_value in input_values:
            assert Time("0.2222", to_utc=input_value).to_utc == to_utc_frac

    # strange values
    for input_value in to_utc_strange_test_data:
        Time("0.3333", to_utc=input_value)

    # a TypeError exception is raised if the argument type is not one of the accepted types
    # exception with invalid parameter name
    with pytest.raises(TypeError):
        Time(1, foobar="barfoo")
    with pytest.raises(TypeError):
        Time(1, 2, foobar="barfoo")

    # this object has a time_to_utc attribute, but it isn't callable
    class WrongObj:
        def __init__(self):
            self.time_to_utc = "foo"

    # exception with non-numeric types
    for par in (1j, (1,), [1], {1: 1}, [], {}, (1, 2), (1, 2, 3), WrongObj()):
        with pytest.raises(TypeError):
            Time("0.4444", to_utc=par)

    # the resulting value must be equal or greater than -1 and less or equal to 1."""
    for par in (-100, -1.00001, 1.00000001, 100):
        with pytest.raises(ValueError):
            Time("0.5555", to_utc=par)
        with pytest.raises(ValueError):
            Time(2, 3, to_utc=par)


def test_003_constructor_now():
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
    # I am commenting the code to test to_utc, because I have no independent way of testing it
    # assert int(time_now.to_utc) == Fraction(time.localtime().tm_gmtoff, 86400)


def test_004_constructor_now_w_to_utc():
    # return an aware object that represents the current moment in the day
    # for the time being, let's use the good old datetime module :-)
    import datetime

    for to_utc_frac, input_values in to_utc_test_data:
        to_uct_seconds = to_utc_frac * 86400
        for input_value in input_values:
            # we must ensure that at least once in three times we get the same values in seconds
            count = 0
            while count < 3:
                datetime_now = datetime.datetime.utcnow()
                time_now = Time.now(to_utc=input_value)
                datetime_frac_seconds = (
                        datetime_now.hour * 3600
                        + datetime_now.minute * 60
                        + datetime_now.second
                        - to_uct_seconds
                )
                if int(time_now.day_frac * 86400) == datetime_frac_seconds:
                    break
                count += 1
            assert count < 3, "Unable to get at least one a correct Time.now(to_utc=0)"
            assert time_now.to_utc == to_utc_frac

    # a TypeError exception is raised if the argument type is not one of the accepted types
    # exception with invalid parameter name
    with pytest.raises(TypeError):
        Time(foobar="barfoo")

    # this object has a time_to_utc attribute, but it isn't callable
    class WrongObj:
        def __init__(self):
            self.time_to_utc = "foo"

    # exception with non-numeric types
    for par in (1j, (1,), [1], {1: 1}, [], {}, (1, 2), (1, 2, 3), WrongObj()):
        with pytest.raises(TypeError):
            Time.now(to_utc=par)

    # the resulting value must be equal or greater than -1 and less or equal to 1."""
    for par in (-100, -1.00001, 1.00000001, 100):
        with pytest.raises(ValueError):
            Time.now(to_utc=par)


def test_005_constructor_localnow():
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
    assert time_now.to_utc is None


def test_006_constructor_utcnow():
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
    assert count < 3, "Unable to get at least one a correct Time.localnow()"
    assert time_now.to_utc is None


def test_050_write_attributes():
    # the attributes of a Tie instance are read-only
    t1 = Time("0.12345")
    with pytest.raises(AttributeError):
        t1.day_frac = Fraction(3, 7)
        t1.to_utc = Fraction(1, 11)
    t2 = Time("0.6789", to_utc="-1/2")
    with pytest.raises(AttributeError):
        t2.day_frac = Fraction(3, 7)
        t2.to_utc = Fraction(1, 11)
    t3 = Time("0.0123", to_utc=DummyToUtc(-2, 3))
    with pytest.raises(AttributeError):
        t3.day_frac = Fraction(3, 7)
        t3.to_utc = Fraction(1, 11)


def test_051_get_unknown_attribute():
    # I want to do this, because Time will have attributes added at runtime
    # let's tests this both on class and instance
    with pytest.raises(AttributeError):
        Time.unknown
    t = Time("0.12345")
    with pytest.raises(AttributeError):
        t.unknown


def test_150_comparisons():
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
            self.to_utc = 'unchecked'

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
    t12 = Time(1, 2)
    t34 = Time("3/4")
    t45 = Time(4, 5)
    assert not (t12 == tl)
    assert t34 == tl
    assert not (t45 == tl)
    assert t12 != tl
    assert not (t34 != tl)
    assert t45 != tl
    assert t12 < tl
    assert not (t34 < tl)
    assert not (t45 < tl)
    assert t12 <= tl
    assert t34 <= tl
    assert not (t45 <= tl)
    assert not (t12 > tl)
    assert not (t34 > tl)
    assert t45 > tl
    assert not (t12 >= tl)
    assert t34 >= tl
    assert t45 >= tl

    class SomeClass1:
        def __init__(self):
            self.day_frac = 'unchecked'

    class SomeClass2:
        def __init__(self):
            self.to_utc = 'unchecked'

    t = Time(0)

    # exception with non-numeric types
    for par in ("1", (1,), [1], {1: 1}, (), [], {}, None, SomeClass1(), SomeClass2()):
        assert not (t == par)
        assert t != par
        with pytest.raises(TypeError):
            t < par
        with pytest.raises(TypeError):
            t > par
        with pytest.raises(TypeError):
            t <= par
        with pytest.raises(TypeError):
            t >= par

    # exception with numeric types (all invalid) and other objects
    for par in (1, 1.0, Fraction(1, 1), Decimal(1), 1j, 1 + 1j, INF, NAN):
        assert not (t == par)
        assert t != par
        with pytest.raises(TypeError):
            t < par
        with pytest.raises(TypeError):
            t > par
        with pytest.raises(TypeError):
            t <= par
        with pytest.raises(TypeError):
            t >= par

    t5 = Time(11, 24)  # this is naive
    assert t1 != t5
    assert not (t1 == t5)
    with pytest.raises(TypeError):
        t1 < t5
        t1 <= t5
        t1 > t5
        t1 >= t5


def test_151_comparisons_w_to_utc():
    t1 = Time("1/8", to_utc="1/3")
    t2 = Time(0.875, to_utc=Fraction(-5, 12))  # this is equal to t1
    t3 = Time("2/3", to_utc=0.125)             # this is larger than t1
    t4 = Time(0.375, to_utc="-1/6")            # this is equal to t1, one day earlier, should NOT compare equal
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
    assert t2 < t3  # repeating the tests with an instance with negative to_utc
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
            self.to_utc = Fraction("1/4")

        # what follows is not a proper implementation, but it is enough for our tests
        def __eq__(self, other):
            return self.day_frac + self.to_utc == other.day_frac + other.to_utc

        def __ne__(self, other):
            return self.day_frac + self.to_utc != other.day_frac + other.to_utc

        def __lt__(self, other):
            return self.day_frac + self.to_utc < other.day_frac + other.to_utc

        def __le__(self, other):
            return self.day_frac + self.to_utc <= other.day_frac + other.to_utc

        def __gt__(self, other):
            return self.day_frac + self.to_utc > other.day_frac + other.to_utc

        def __ge__(self, other):
            return self.day_frac + self.to_utc >= other.day_frac + other.to_utc

    tl = TimeLike()
    # We need not implement naivety checks, which are delegated to the Time-like class, not under test
    t12 = Time(1, 2, to_utc="-1/3")
    t34 = Time("3/4", to_utc=0.25)
    t45 = Time(4, 5, to_utc=Fraction(-1, 8))
    assert not (t12 == tl)
    assert t34 == tl
    assert not (t45 == tl)
    assert t12 != tl
    assert not (t34 != tl)
    assert t45 != tl
    assert t12 < tl
    assert not (t34 < tl)
    assert not (t45 < tl)
    assert t12 <= tl
    assert t34 <= tl
    assert not (t45 <= tl)
    assert not (t12 > tl)
    assert not (t34 > tl)
    assert t45 > tl
    assert not (t12 >= tl)
    assert t34 >= tl
    assert t45 >= tl
    
    t5 = Time(11, 24)  # this is naive
    assert t5 != t1
    assert not (t5 == t1)
    with pytest.raises(TypeError):
        t5 < t1
        t5 <= t1
        t5 > t1
        t5 >= t1


def test_160_hash_equality(self):
    """Time instances are immutable."""
    t1 = Time("3/5")
    t2 = Time(3, 5)
    assert hash(t1) == hash(t2)

    dic = {t1: 1}
    dic[t2] = 2
    assert len(dic) == 1
    assert dic[t1] == 2
    assert dic[t2] == 2

    t3 = Time("7/20") + TimeDelta(0.25)
    assert hash(t1) == hash(t3)

    dic[t3] = 2
    assert len(dic) == 1
    assert dic[t3] == 2


def test_161_hash_equality_w_to_utc():
    # Time instances are immutable
    t1 = Time("3/5", to_utc=0.25)
    t2 = Time(4, 5, to_utc="1/20")
    assert hash(t1) == hash(t2)

    dic = {t1: 1}
    dic[t2] = 2
    assert len(dic) == 1
    assert dic[t1] == 2
    assert dic[t2] == 2

    t3 = Time(Decimal("0.2"), to_utc="-7/20")  # as t1, one day earlier
    assert hash(t1) != hash(t3)

    dic[t3] = 2
    assert len(dic) == 1
    assert dic[t3] == 2

    # naive and aware instances have different hashes
    t4 = Time(4, 5)                 # as t1, without to_uts
    t5 = Time(1, 2, to_utc="1/20")  # same to_utc as t1
    t6 = Time(17, 20)               # "equivalent" to t1

    assert hash(t1) != hash(t4)
    assert hash(t1) != hash(t5)
    assert hash(t1) != hash(t6)


def test_170_bool():
    # In boolean contexts, all Time instances are considered to be true
    for day_frac, input_values in time_test_data:
        for input_value in input_values:
            assert Time(input_value)
    for day_frac, input_values in time_test_data_num_den:
        for input_value in input_values:
            assert Time(input_value[0], input_value[1])


def test_171_bool_w_to_utc():
    # In boolean contexts, all Time instances are considered to be true
    for to_utc_frac, input_values in to_utc_test_data:
        for input_value in input_values:
            assert Time("0.2222", to_utc=input_value)


def test_500_repr():
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


def test_501_repr_w_to_utc():
    import datetime2

    for day_frac, input_values in time_test_data:
        for input_value in input_values:
            t = Time("0.25", to_utc=input_value)
            time_repr = repr(t)
            names, args = time_repr.split("(")
            assert names.split(".") == ["datetime2", "Time"]
            args = args[:-1]  # drop ')'
            assert eval(args) == f"Fraction( 1, 4), to_utc={day_frac!s}"
            assert t == eval(time_repr)


def test_510_str():
    for day_frac, input_values in time_test_data:
        for input_value in input_values:
            t = Time(input_value)
            string = str(t)
            assert string.endswith(" of a day")
            assert string[:-9] == str(day_frac)


def test_511_str_w_to_utc():
    for day_frac, input_values in time_test_data:
        for input_value in input_values:
            t = Time(0.25, to_utc=input_value)
            string = str(t)
            assert string.startswith("1/4 of a day, ")
            assert string.endswith(" of a day to UTC")
            assert string[14:-16] == str(day_frac)


def test_900_pickling():
    for day_frac, input_values in time_test_data:
        for input_value in input_values:
            t = Time(input_value)
            for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
                pickled = pickle.dumps(t, protocol)
                derived = pickle.loads(pickled)
                assert t == derived


def test_901_pickling_w_to_utc():
    for day_frac, input_values in time_test_data:
        for input_value in input_values:
            t = Time(0,25, input_value)
            for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
                pickled = pickle.dumps(t, protocol)
                derived = pickle.loads(pickled)
                assert t == derived


def test_920_subclass():
    # check that there is no interference from the interface mechanism
    # and from possible additional arguments
    class T1(Time):
        the_answer = 42

        def __init__(self, *args, **kws):
            temp = kws.copy()
            self.extra = temp.pop("extra")
            Time.__init__(self, *args, **temp)

        def newmeth(self, start):
            return (start + self.day_frac * 3) // 2

    t1 = Time("3/8")
    t2 = T1(0.375, extra=7)

    assert t2.the_answer == 42
    assert t2.extra == 7
    assert t1 == t2
    assert t2.newmeth(1) == 1
    assert t2.newmeth(-5) == -2

    t3 = Time("3/8", to_utc=0.5)
    t4 = T1(0.375, extra=7, to_utc=0.5)

    assert t4.the_answer == 42
    assert t4.extra == 7
    assert t3 == t4
    assert t4.newmeth(1) == 1
    assert t4.newmeth(-5) == -2

    class T3(Time):
        pass

    assert type(T3.now()) is T3
    assert type(T3.localnow()) is T3
    assert type(T3.utcnow()) is T3
