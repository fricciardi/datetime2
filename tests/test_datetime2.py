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
import pytest
from fractions import Fraction

from datetime2 import Date, TimeDelta


INF = float("inf")
NAN = float("nan")

date_test_data = (-2, -1, 0, 1, 2, -1000, 1000, -123456789, 123456789, -999999999, 999999999, -1000000000, 1000000000)


#############################################################################
# Date tests
#
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
        for par in (1.0, Fraction(1, 1), decimal.Decimal(1), 1j):
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

        # Addition between Date and TimeDelta, reverse is not defined
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

    def test_310_disallowed_operations(self):
        a = Date(42)
        b = Date(24)

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

        # These operations make no sense for Date objects
        with pytest.raises(TypeError):
            TimeDelta(2) + a
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

    def test_330_comparison_with_invalid_types(self):
        class SomeClass:
            pass

        d = Date(1)

        # exception with non-numeric types
        for par in ("1", (1,), [1], {1: 1}, (), [], {}, None):
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

        # exception with numeric types (all invalid) and other objects
        for par in (1, 1.0, fractions.Fraction(1, 1), decimal.Decimal(1), 1j, 1 + 1j, INF, NAN, SomeClass()):
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
            assert bool(Date(day_count))

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
        d2 = D(2013, extra=7)

        assert d2.theAnswer == 42
        assert d2.extra == 7
        assert d1.day_count == d2.day_count
        assert d2.newmeth(-7) == (d1.day_count * 3) // 2 - 7



