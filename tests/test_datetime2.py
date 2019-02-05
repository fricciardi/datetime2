# datetime2 package test

# Copyright (c) 2011-2019 Francesco Ricciardi
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

from decimal import Decimal
from fractions import Fraction
import pickle
import pytest

from datetime2 import Date, Time, TimeDelta


INF = float("inf")
NAN = float("nan")


#############################################################################
# Date tests
#
date_test_data = (-2, -1, 0, 1, 2, -1000, 1000, -123456789, 123456789, -999999999, 999999999, -1000000000, 1000000000)

class TestDate:
    def test_000_valid_parameter_types(self):
        "The argument is required and must be an integer."
        for day_count in date_test_data:
            assert Date(day_count).day_count == day_count

    def test_010_invalid_parameter_types(self):
        "The argument is required and must be an integer."
        # exception with no or two parameters
        with pytest.raises(TypeError):
            Date()
        with pytest.raises(TypeError):
            Date(1, 2)
        # exception with non-numeric types
        for par in ('1', (1,), [1], {1:1}, (), [], {}, None):
            with pytest.raises(TypeError):
                Date(par)
        # exception with invalid numeric types
        for par in (1.0, Fraction(1, 1), Decimal(1), 1j):
            with pytest.raises(TypeError):
                Date(par)

    def test_020_today(self):
        "Return a Date object that represents the current local date."
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

    def test_100_write_attribute(self):
        "This attribute is read-only."
        d = Date(1)
        with pytest.raises(AttributeError):
            d.day_count = 3

    def test_110_get_unknown_attribute(self):
        "Date instances have one attribute."
        # I want to do this, because Date will have attributes added at runtime
        # let's tests this both on class and instance
        with pytest.raises(AttributeError):
            Date.unknown
        d = Date(1)
        with pytest.raises(AttributeError):
            d.unknown

    def test_300_valid_operations(self):
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

    def test_310_disallowed_operations(self):
        a = Date(42)
        b = Date(24)

        # These operations are invalid because TimeDelta is not integer.
        for value in (42.25, 41.75, -42.25, -41.75):
            with pytest.raises(ValueError):
                a + TimeDelta(value)
            with pytest.raises(ValueError):
                a - TimeDelta(value)

        # Add/sub int, float, string, complex, specials and containers should be illegal
        for obj in (10, 34.5, "abc", 1 + 2j, INF, NAN, {}, [], ()):
            with pytest.raises(TypeError):
                a + obj
            with pytest.raises(TypeError):
                a - obj
            with pytest.raises(TypeError):
                obj + a
            with pytest.raises(TypeError):
                obj - a

        # Reverse operations
        with pytest.raises(TypeError):
            TimeDelta(2) - a

        for obj in (1, 1.1, b):
            with pytest.raises(TypeError):
                a * obj
            with pytest.raises(TypeError):
                obj * a
            with pytest.raises(TypeError):
                a / obj
            with pytest.raises(TypeError):
                obj / a
            with pytest.raises(TypeError):
                a // obj
            with pytest.raises(TypeError):
                obj // a
            with pytest.raises(TypeError):
                pow(a, obj)
            with pytest.raises(TypeError):
                pow(obj, a)
            with pytest.raises(TypeError):
                a ^ obj
            with pytest.raises(TypeError):
                obj ^ a
            with pytest.raises(TypeError):
                a >> obj
            with pytest.raises(TypeError):
                obj >> a
            with pytest.raises(TypeError):
                a << obj
            with pytest.raises(TypeError):
                obj << a

    def test_320_comparisons(self):
        d1 = Date(42)
        d2 = Date(42)
        assert d1 == d2
        assert d1 <= d2
        assert d1 >= d2
        assert not (d1 != d2)
        assert not (d1 < d2)
        assert not(d1 > d2)

        d3 = Date(4242)   # this is larger than d1
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

    def test_330_comparison_with_invalid_types(self):
        class SomeClass:
            pass

        d = Date(1)

        # exception with non-numeric types
        for par in ("1", (1,), [1], {1: 1}, (), [], {}, None, SomeClass()):
            assert not (d == par)
            assert d != par
            with pytest.raises(TypeError):
                d < par
            with pytest.raises(TypeError):
                d > par
            with pytest.raises(TypeError):
                d <= par
            with pytest.raises(TypeError):
                d >= par

        # exception with numeric types (all invalid)
        for par in (1, 1.0, Fraction(1, 1), Decimal(1), 1j, 1 + 1j, INF, NAN):
            assert not (d == par)
            assert d != par
            with pytest.raises(TypeError):
                d < par
            with pytest.raises(TypeError):
                d > par
            with pytest.raises(TypeError):
                d <= par
            with pytest.raises(TypeError):
                d >= par

    def test_340_hash_equality(self):
        "Date instances are immutable."
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

    def test_350_bool(self):
        "In boolean contexts, all Date instances are considered to be true."
        for day_count in date_test_data:
            assert Date(day_count)

    def test_500_repr(self):
        import datetime2
        for day_count in date_test_data:
            d = Date(day_count)
            date_repr = repr(d)
            names, args = date_repr.split('(')
            assert names.split('.') == ['datetime2', 'Date']
            args = args[:-1]  # drop ')'
            assert int(args) == day_count
            assert d == eval(repr(d))

    def test_520_str(self):
        for day_count in date_test_data:
            d = Date(day_count)
            assert int(str(d)[5:]) == day_count

    def test_900_pickling(self):
        for day_count in date_test_data:
            d = Date(day_count)
            for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
                pickled = pickle.dumps(d, protocol)
                derived = pickle.loads(pickled)
                assert d == derived

    def test_920_subclass1(self):
        # check that there is no interference from the interface mechanism and from possible additional arguments
        class D(Date):
            theAnswer = 42

            def __init__(self, *args, **kws):
                temp = kws.copy()
                self.extra = temp.pop('extra')
                Date.__init__(self, *args, **temp)

            def newmeth(self, start):
                return start + (self.day_count * 3) // 2

        d1 = Date(102013)
        d2 = D(102013, extra=7)

        assert d2.theAnswer == 42
        assert d2.extra == 7
        assert d1.day_count == d2.day_count
        assert d2.newmeth(-7) == (d1.day_count * 3) // 2 - 7

    def test_930_subclass2(self):
        # check that all possible methods return subclass
        class D(Date):
            pass

        d_sub = D(102030)
        assert type(D.today()) is D
        assert type(d_sub + TimeDelta(1)) is D
        assert type(d_sub - TimeDelta(1)) is D


#############################################################################
# Time tests
#
class DummyTZ:
    def __init__(self, num, den):
        self.num = num
        self.den = den

    def time_to_utc(self):
        return Fraction(self.num, self.den)

time_test_data = [
    [Fraction(0, 1), [0, Fraction(0), Decimal('0'), 0.0, '0', '0/33', (0, 5)]],
    [Fraction(1, 4), [Fraction(1, 4), Decimal('0.25'), 0.25, '0.25', '1/4', (2, 8)]]]
# we are not going to test more values, because we don't want to test the Fraction constructor :-)

to_utc_test_data = [
    [Fraction(0, 1), [0, Fraction(0), Decimal('0'), 0.0, '0', '0/33', (0, 5), DummyTZ(0, -3)]],
    [Fraction(1, 4), [Fraction(1, 4), Decimal('0.25'), 0.25, '0.25', '1/4', (2, 8), DummyTZ(3, 12)]],
    [Fraction(1, -4), [Fraction(-1, 4), Decimal('-0.25'), -0.25, '-0.25', '-1/4', (2, -8), DummyTZ(-3, 12)]]]

# but we want to test with a few strange values
time_strange_test_data = (Fraction(123, 4567), 0.999999, '0.999999', '0.0000001', '5/456789', (123, 4567))
to_utc_strange_test_data = [Fraction(123, 4567), 0.999999, '0.999999', '0.0000001', '5/456789', (123, 4567),
                            Fraction(-123, 4567), -0.999999, '-0.999999', '-0.0000001', '-5/456789', (123, -4567)]

class TestTime:
    def test_000_valid_argument_types(self):
        "The day_frac argument can be anything that can be passed to the fractions.Fraction constructor."
        for day_frac, input_values in time_test_data:
            for input_value in input_values:
                assert Time(input_value).day_frac == day_frac

    def test_002_valid_argument_types_to_utc(self):
        "The to_utc argument can be anything that can be passed to the fractions.Fraction constructor."
        for to_utc_frac, input_values in to_utc_test_data:
            for input_value in input_values:
                assert Time("0.2222", to_utc=input_value).to_utc == to_utc_frac

    def test_005_valid_argument_types_strange(self):
        "The day_frac argument can be anything that can be passed to the fractions.Fraction constructor."
        for input_value in time_strange_test_data:
            Time(input_value)

    def test_007_valid_argument_types_strange_to_utc(self):
        "The to_utc argument can be anything that can be passed to the fractions.Fraction constructor."
        for input_value in to_utc_strange_test_data:
            Time("0.3333", to_utc=input_value)

    def test_010_invalid_argument_types(self):
        "A TypeError exception is raised if the argument type is not one of the accepted types."
        # exception with no or two parameters
        with pytest.raises(TypeError):
            Time()
        with pytest.raises(TypeError):
            Time(1, 2)
        # exception with non-numeric types
        for par in (1j, (1,), [1], {1:1}, [], {}, None, (1,2,3)):
            with pytest.raises(TypeError):
                Time(par)

    def test_012_invalid_argument_types_to_utc(self):
        "A TypeError exception is raised if the argument type is not one of the accepted types."
        # this object has a time_to_utc attribute, but is isn't callable
        class WrongObj:
            def __init__(self):
                self.time_to_utc = 'foo'

        # exception with invalid parameter name
        with pytest.raises(TypeError):
            Time(1, foobar='barfoo')
        # exception with non-numeric types
        for par in (1j, (1,), [1], {1:1}, [], {}, (1,2,3), WrongObj()):
            with pytest.raises(TypeError):
                Time("0.4444", to_utc=par)

    def test_015_invalid_argument_values(self):
        "The resulting value must be equal or greater than 0 and less than 1."
        for par in (-0.00001, 1, 1.00000001, 10000, -10000):
            with pytest.raises(ValueError):
                Time(par)
        # same for tuple argument
        for par in ( (1000, 1), (4, 2), (2, 2), (-1, -1), (-1, 1000000), (-3, 3), (1000000, -2)):
            with pytest.raises(ValueError):
                Time(par)
        # tuple argument should not have 0 as denominator
        with pytest.raises(ZeroDivisionError):
            Time((2, 0))

    def test_017_invalid_argument_values_to_utc(self):
        "The resulting value must be greater than -1 and less than 1."
        for par in (-100, -1.00001, -1, 1, 1.00000001, 100):
            with pytest.raises(ValueError):
                Time("0.5555", to_utc=par)
        # same for tuple argument
        for par in ( (-100, 1), (-4, 3), (-2, 2), (2, 2), (4, 3), (100, 1) ):
            with pytest.raises(ValueError):
                Time("0.6666", to_utc=par)
        # tuple argument should not have 0 as denominator
        with pytest.raises(ZeroDivisionError):
            Time("0.7777", to_utc=(3, 0))

    def test_020_now(self):
        "Return an object that represents the current moment in the day."
        # for the time being, let's use the good old datetime module :-)
        import datetime, time

        # we must ensure that at least once in three times we get the same values in seconds
        count = 0
        while count < 3:
            datetime_now = datetime.datetime.now()
            datetime_frac_seconds = datetime_now.hour * 3600 + datetime_now.minute * 60 + datetime_now.second
            time_now = Time.now()
            if int(time_now.day_frac * 86400) == datetime_frac_seconds:
                break
            count += 1
        assert count < 3, "Unable to get at least one a correct Time.now()"
        assert int(time_now.to_utc) == time.timezone

    def test_030_now_with_argument(self):
        "Return an object that represents the current moment in the day."
        # for the time being, let's use the good old datetime module :-)
        import datetime

        # we must ensure that at least once in three times we get the same values in seconds
        count = 0
        while count < 3:
            datetime_now = datetime.datetime.utcnow()
            datetime_frac_seconds = datetime_now.hour * 3600 + datetime_now.minute * 60 + datetime_now.second
            time_now = Time.now(to_utc=0)
            if int(time_now.day_frac * 86400) == datetime_frac_seconds:
                break
            count += 1
        assert count < 3, "Unable to get at least one a correct Time.now(to_utc=0)"
        assert time_now.to_utc == 0
        assert time_now.to_utc_obj is None

        # again but with class
        count = 0
        while count < 3:
            datetime_now = datetime.datetime.utcnow()
            datetime_frac_seconds = datetime_now.hour * 3600 + datetime_now.minute * 60 + datetime_now.second
            time_now = Time.now(to_utc=DummyTZ(0, 1))
            if int(time_now.day_frac * 86400) == datetime_frac_seconds:
                break
            count += 1
        assert count < 3, "Unable to get at least one a correct Time.now(to_utc=DummyTZ(0, 1))"
        assert time_now.to_utc == 0
        assert time_now.to_utc_obj is not None

    def test_040_localnow(self):
        "Return an object that represents the current moment in the day."
        # for the time being, let's use the good old datetime module :-)
        import datetime

        # we must ensure that at least once in three times we get the same values in seconds
        count = 0
        while count < 3:
            datetime_now = datetime.datetime.now()
            datetime_frac_seconds = datetime_now.hour * 3600 + datetime_now.minute * 60 + datetime_now.second
            time_now = Time.localnow()
            if int(time_now.day_frac * 86400) == datetime_frac_seconds:
                break
            count += 1
        assert count < 3, "Unable to get at least one a correct Time.localnow()"
        assert time_now.to_utc is None
        assert time_now.to_utc_obj is None

    def test_050_utcnow(self):
        "Return an object that represents the current moment in the day."
        # for the time being, let's use the good old datetime module :-)
        import datetime

        # we must ensure that at least once in three times we get the same values in seconds
        count = 0
        while count < 3:
            datetime_now = datetime.datetime.utcnow()
            datetime_frac_seconds = datetime_now.hour * 3600 + datetime_now.minute * 60 + datetime_now.second
            time_now = Time.utcnow()
            if int(time_now.day_frac * 86400) == datetime_frac_seconds:
                break
            count += 1
        assert count < 3, "Unable to get at least one a correct Time.localnow()"
        assert time_now.to_utc is None
        assert time_now.to_utc_obj is None

    def test_100_write_attributes(self):
        "This attribute is read-only."
        t1 = Time('0.12345')
        with pytest.raises(AttributeError):
            t1.day_frac = Fraction(3, 7)
            t1.to_utc = Fraction(1, 11)
            t1.to_utc_obj = object()
        t2 = Time('0.6789', to_utc='-1/2')
        with pytest.raises(AttributeError):
            t2.day_frac = Fraction(3, 7)
            t2.to_utc = Fraction(1, 11)
            t2.to_utc_obj = object()
        t3 = Time('0.0123', to_utc=DummyTZ(-2, 3))
        with pytest.raises(AttributeError):
            t3.day_frac = Fraction(3, 7)
            t3.to_utc = Fraction(1, 11)
            t3.to_utc_obj = object()

    def test_110_get_unknown_attribute(self):
        "Time instances have one attribute."
        # I want to do this, because Time will have attributes added at runtime
        # let's tests this both on class and instance
        with pytest.raises(AttributeError):
            Time.unknown
        t = Time('0.12345')
        with pytest.raises(AttributeError):
            t.unknown

    def test_300_valid_operations(self):
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
        assert integer + b  == Time(0.25)
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

    def test_302_valid_operations_to_utc(self):
        a = Time(0, to_utc='1/3')
        b = Time(0.25, to_utc='-1/4')
        c = Time(0.75, to_utc='1/6')
        zero = TimeDelta(0)
        # note that TimeDelta is in days
        plus_half = TimeDelta(0.5)
        minus_half = TimeDelta(-1.5)
        integer = TimeDelta(3)

        # Addition between Time and TimeDelta
        # test with zero, negative and positive dates
        assert a + zero == Time(0, to_utc='1/3')
        assert a + plus_half == Time(0.5, to_utc='1/3')
        assert a + minus_half == Time(0.5, to_utc='1/3')
        assert a + integer == Time(0, to_utc='1/3')
        assert b + zero == Time(0.25, to_utc='-1/4')
        assert b + plus_half == Time(0.75, to_utc='-1/4')
        assert b + minus_half == Time(0.75, to_utc='-1/4')
        assert b + integer == Time(0.25, to_utc='-1/4')
        assert c + zero == Time(0.75, to_utc='1/6')
        assert c + plus_half == Time(0.25, to_utc='1/6')
        assert c + minus_half == Time(0.25, to_utc='1/6')
        assert c + integer == Time(0.75, to_utc='1/6')

        # Reversed addition between Time and TimeDelta
        # test with zero, negative and positive dates
        assert zero + a == Time(0, to_utc='1/3')
        assert plus_half + a == Time(0.5, to_utc='1/3')
        assert minus_half + a == Time(0.5, to_utc='1/3')
        assert integer + a == Time(0, to_utc='1/3')
        assert zero + b == Time(0.25, to_utc='-1/4')
        assert plus_half + b == Time(0.75, to_utc='-1/4')
        assert minus_half + b == Time(0.75, to_utc='-1/4')
        assert integer + b  == Time(0.25, to_utc='-1/4')
        assert zero + c == Time(0.75, to_utc='1/6')
        assert plus_half + c == Time(0.25, to_utc='1/6')
        assert minus_half + c == Time(0.25, to_utc='1/6')
        assert integer + c == Time(0.75, to_utc='1/6')

        # subtraction between Time and TimeDelta, reverse is not defined
        # test with zero, negative and positive Times
        assert a - zero == Time(0, to_utc='1/3')
        assert a - plus_half == Time(0.5, to_utc='1/3')
        assert a - minus_half == Time(0.5, to_utc='1/3')
        assert a - integer == Time(0, to_utc='1/3')
        assert b - zero == Time(0.25, to_utc='-1/4')
        assert b - plus_half == Time(0.75, to_utc='-1/4')
        assert b - minus_half == Time(0.75, to_utc='-1/4')
        assert b - integer == Time(0.25, to_utc='-1/4')
        assert c - zero == Time(0.75, to_utc='1/6')
        assert c - plus_half == Time(0.25, to_utc='1/6')
        assert c - minus_half == Time(0.25, to_utc='1/6')
        assert c - integer == Time(0.75, to_utc='1/6')

    def test_308_operations_preserve_naivety(self):
        a = Time('3/8')
        b = Time((3,4), to_utc='1/6')
        test_obj = DummyTZ(-1, 8)
        c = Time(0.25, to_utc=test_obj)

        for td in (TimeDelta(0.5), TimeDelta(-0.25), TimeDelta(3), TimeDelta(-2.75)):
            res_a_plus = a + td
            assert res_a_plus.to_utc is None
            assert res_a_plus.to_utc_obj is None
            res_a_minus = a - td
            assert res_a_minus.to_utc is None
            assert res_a_minus.to_utc_obj is None
            res_b_plus = b + td
            assert res_b_plus.to_utc == Fraction(1, 6)
            assert res_b_plus.to_utc_obj is None
            res_b_minus = b - td
            assert res_b_minus.to_utc == Fraction(1, 6)
            assert res_b_minus.to_utc_obj is None
            res_c_plus = c + td
            assert res_c_plus.to_utc == Fraction(-1, 8)
            assert res_c_plus.to_utc_obj is test_obj
            res_c_plus = c - td
            assert res_c_plus.to_utc == Fraction(-1, 8)
            assert res_c_plus.to_utc_obj is test_obj

    def test_310_disallowed_operations(self):
        a = Time('3/4')
        b = Time('2/5', to_utc='1/8')

        # Add/sub int, float, string, complex, specials and containers should be illegal
        for obj in (10, 34.5, "abc", 1 + 2j, INF, NAN, {}, [], ()):
            with pytest.raises(TypeError):
                a + obj
            with pytest.raises(TypeError):
                a - obj
            with pytest.raises(TypeError):
                obj + a
            with pytest.raises(TypeError):
                obj - a
            with pytest.raises(TypeError):
                b + obj
            with pytest.raises(TypeError):
                b - obj
            with pytest.raises(TypeError):
                obj + b
            with pytest.raises(TypeError):
                obj - b

        # Reverse operations
        with pytest.raises(TypeError):
            TimeDelta(-0.25) - a
        with pytest.raises(TypeError):
            TimeDelta(-0.25) - b

        for obj in (1, 1.1, Time('2/5')):
            with pytest.raises(TypeError):
                a * obj
            with pytest.raises(TypeError):
                obj * a
            with pytest.raises(TypeError):
                a / obj
            with pytest.raises(TypeError):
                obj / a
            with pytest.raises(TypeError):
                a // obj
            with pytest.raises(TypeError):
                obj // a
            with pytest.raises(TypeError):
                pow(a, obj)
            with pytest.raises(TypeError):
                pow(obj, a)
            with pytest.raises(TypeError):
                a ^ obj
            with pytest.raises(TypeError):
                obj ^ a
            with pytest.raises(TypeError):
                a >> obj
            with pytest.raises(TypeError):
                obj >> a
            with pytest.raises(TypeError):
                a << obj
            with pytest.raises(TypeError):
                obj << a
            with pytest.raises(TypeError):
                b * obj
            with pytest.raises(TypeError):
                obj * b
            with pytest.raises(TypeError):
                b / obj
            with pytest.raises(TypeError):
                obj / b
            with pytest.raises(TypeError):
                b // obj
            with pytest.raises(TypeError):
                obj // b
            with pytest.raises(TypeError):
                pow(b, obj)
            with pytest.raises(TypeError):
                pow(obj, b)
            with pytest.raises(TypeError):
                b ^ obj
            with pytest.raises(TypeError):
                obj ^ b
            with pytest.raises(TypeError):
                b >> obj
            with pytest.raises(TypeError):
                obj >> b
            with pytest.raises(TypeError):
                b << obj
            with pytest.raises(TypeError):
                obj << b

        # operations mixing naive and aware instances
        with pytest.raises(ValueError):
            a - b
        with pytest.raises(ValueError):
            b - a

    def test_320_comparisons(self):
        t1 = Time("3/8")
        t2 = Time(0.375)
        assert t1 == t2
        assert t1 <= t2
        assert t1 >= t2
        assert not (t1 != t2)
        assert not (t1 < t2)
        assert not(t1 > t2)

        t3 = Time("5/7")   # this is larger than t1
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
        t12 = Time((1, 2))
        t34 = Time("3/4")
        t45 = Time((4, 5))
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

    def test_322_comparisons_to_utc(self):
        t1 = Time("7/8", to_utc='5/6')  # These value have a lot of overflows and underflows
        t2 = Time(0.375, to_utc=(-2,3))
        assert t1 == t2
        assert t1 <= t2
        assert t1 >= t2
        assert not (t1 != t2)
        assert not (t1 < t2)
        assert not(t1 > t2)

        t3 = Time("1/2", to_utc=0.25)   # this is larger than t1
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
        assert t2 < t3                # repeating the tests with an instance with negative to_utc
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

        # Reverse comparison mechanism
        class TimeLike:
            def __init__(self):
                self.day_frac = Fraction(3, 4)

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
        # We need not implement naivety checks, which are delegated to the Time-like class, not under test
        t12 = Time((1, 2), to_utc='-1/3')
        t34 = Time("3/4", to_utc=0.25)
        t45 = Time((4, 5), to_utc=(-1, 8))
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

    def test_330_comparison_with_invalid_types(self):
        class SomeClass:
            pass

        t = Time(0)

        # exception with non-numeric types
        for par in ("1", (1,), [1], {1: 1}, (), [], {}, None, SomeClass()):
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

    def test_340_hash_equality(self):
        "Time instances are immutable."
        t1 = Time("3/5")
        t2 = Time("3/5")
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

    def test_350_bool(self):
        "In boolean contexts, all Time instances are considered to be true."
        for day_frac, input_values in time_test_data:
            for input_value in input_values:
                assert Time(input_value)

    def test_400_relocate(self):
        "Return another Time instance that identifies the same time"
        # Im using a mix of values, then check that relocated instance is equal
        for day_frac, time_input_values in time_test_data:
            for to_utc_frac, utc_input_values in to_utc_test_data:
                first = Time(time_input_values[0], to_utc=utc_input_values[0])
                for new_utc_value in to_utc_strange_test_data:
                    second = first.relocate(new_utc_value)
                    diff = (first.day_frac + first.to_utc) - (second.day_frac + second.to_utc)
                    # Note that for some of the test value we have an overflow/underflow,
                    # so we must impement a precise test
                    assert diff == int(diff)

    def test_410_relocate_invalid_type(self):
        "Return another Time instance that identifies the same time"
        class WrongObj:
            def __init__(self):
                self.time_to_utc = 'foo'

        t = Time('123/456', to_utc='-78/90')

        # exception with invalid parameter name
        with pytest.raises(TypeError):
            t.relocate()
        with pytest.raises(TypeError):
            t.relocate(1, 2)
        with pytest.raises(TypeError):
            t.relocate(foobar='barfoo')

        # exception with non-numeric types
        for par in (1j, (1,), [1], {1:1}, [], {}, None, (1,2,3), WrongObj()):
            with pytest.raises(TypeError):
                t.relocate(par)

    def test_420_relocate_invalid_values(self):
        "Return another Time instance that identifies the same time"
        for par in (-100, -1.00001, -1, 1, 1.00000001, 100):
            with pytest.raises(ValueError):
                Time("0.5555", to_utc=par)
        # same for tuple argument
        for par in ( (-100, 1), (-4, 3), (-2, 2), (2, 2), (4, 3), (100, 1) ):
            with pytest.raises(ValueError):
                Time("0.6666", to_utc=par)
        # tuple argument should not have 0 as denominator
        with pytest.raises(ZeroDivisionError):
            Time("0.7777", to_utc=(3, 0))

    def test_500_repr(self):
        import datetime2
        for day_frac, input_values in time_test_data:
            for input_value in input_values:
                t = Time(input_value)
                time_repr = repr(t)
                names, args = time_repr.split('(')
                assert names.split('.') == ['datetime2', 'Time']
                args = args[:-1]  # drop ')'
                assert t == eval(time_repr)

    def test_520_str(self):
        for day_frac, input_values in time_test_data:
            for input_value in input_values:
                t = Time(input_value)
                assert str(t).split(' of ')[0] == str(day_frac)

    def test_900_pickling(self):
        for day_frac, input_values in time_test_data:
            for input_value in input_values:
                t = Time(input_value)
                for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
                    pickled = pickle.dumps(t, protocol)
                    derived = pickle.loads(pickled)
                    assert t == derived

    def test_920_subclass1(self):
        # check that there is no interference from the interface mechanism and from possible additional arguments
        class T(Time):
            theAnswer = 42

            def __init__(self, *args, **kws):
                temp = kws.copy()
                self.extra = temp.pop('extra')
                Time.__init__(self, *args, **temp)

            def newmeth(self, start):
                return start + (self.day_frac * 3) // 2

        t1 = Time("3/8")
        t2 = T(0.375, extra=7)

        assert t2.theAnswer == 42
        assert t2.extra == 7
        assert t1.day_frac == t2.day_frac
        assert t2.newmeth(-7) == (t1.day_frac * 3) // 2 - 7

    def test_920_subclass2(self):
        class T(Time):
            pass

        t_sub = T('3/4')
        assert type(T.now()) is T
        assert type(T.localnow()) is T
        assert type(T.utcnow()) is T
        assert type(t_sub.relocate('1/3')) is T
        assert type(t_sub + TimeDelta(0.25)) is T
        assert type(t_sub - TimeDelta(0.25)) is T

