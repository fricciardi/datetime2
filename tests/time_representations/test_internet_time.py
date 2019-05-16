# tests for western time representation

# Copyright (c) 2012-2019 Francesco Ricciardi
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
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
from math import floor
import pickle
import pytest

from datetime2.modern import InternetTime



INF = float('inf')
NAN = float('nan')

internet_time_test_data = [
    # day_frac           internet as fraction
    # numer  denom       beat

    # Boundary conditions around midnight
    # beat and half beat
    [    "0/1",         0],
    [    "1/1000",      1],
    [  "999/1000",    999],
    [    "1/2000",      0.5],
    [ "1999/2000",    999.5],

    # fractional part of day
    [    "1/10",      100],
    [    "1/100",      10],
    [    "1/1000",      1],
    [    "1/10000",   "1/10"],
    [    "1/100000",  "1/100"],
    [    "1/1000000", "1/1000"]
]

internet_time_invalid_data = [
    -1,
    1000,
    "10001/10",
    1001,
    NAN
]

internet_time_millibeat = [
    # boundary conditions
    [   "0/1",       "000"],
    [   "1/1000",    "001"],
    [   "1/2000",    "000"],
    [ "999/1000",    "999"],
    ["1999/2000",    "999"],
    # a few not so random numbers
    [     "5/7",     "714"],
    [ "12345/56789", "217"]
]

class TestInternet():
    def test_000_constructor(self):
        for test_row in internet_time_test_data:
            beat = test_row[1]
            internet = InternetTime(beat)
            assert internet.beat == Fraction(beat)

    def test_003_constructor_types_for_beats(self):
        for integer_beat in (3, '3'):
            internet = InternetTime(integer_beat)
            assert internet.beat == 3
        for integer_beat in (1.25, Fraction(5, 4), '1.25', Decimal('1.25'), '5/4'):
            internet = InternetTime(integer_beat)
            assert internet.beat == Fraction(5, 4)

    def test_006_constructor_day_frac(self):
        for test_row in internet_time_test_data:
            day_frac = Fraction(test_row[0])
            beat = test_row[1]
            internet = InternetTime.from_day_frac(day_frac)
            assert internet.beat == Fraction(beat)

    def test_010_invalid_parameter_types(self):
        # exception with none or two
        with pytest.raises(TypeError):
            InternetTime()
        with pytest.raises(TypeError):
            InternetTime(1, 2)

        # exception with non-numeric types
        for par in ((1,), [1], {1: 1}, (), [], {}, None):
            with pytest.raises(TypeError):
                InternetTime(par)

        # exception with invalid numeric types
        for par in (1j, 1 + 1j, INF):
            with pytest.raises(TypeError):
                InternetTime(par)

    def test_015_invalid_parameter_types_day_frac(self):
        # exception with none, two or four parameters
        with pytest.raises(TypeError):
            InternetTime.from_day_frac()
        with pytest.raises(TypeError):
            InternetTime.from_day_frac(1, 2)

        # exception with non-numeric types
        for par in ("1", (1,), [1], {1: 1}, (), [], {}, None):
            with pytest.raises(TypeError):
                InternetTime.from_day_frac(par)

        # exception with invalid numeric types
        for par in (1.0, Decimal(1), 1j, 1 + 1j, INF, NAN):
            with pytest.raises(TypeError):
                InternetTime.from_day_frac(par)

    def test_020_invalid_values(self):
        for test_beat in internet_time_invalid_data:
            with pytest.raises(ValueError):
                InternetTime(test_beat)

    def test_025_invalid_values_day_frac(self):
        for num, denum in ((1, 1), (1, -1), (1000001, 1000000), (-1, 1000000)):
            with pytest.raises(ValueError):
                InternetTime.from_day_frac(Fraction(num, denum))

    def test_100_write_attribute(self):
        internet = InternetTime(10)
        with pytest.raises(AttributeError):
            internet.beat = 3

    def test_300_compare(self):
        internet1 = InternetTime(3)
        internet2 = InternetTime(3)
        assert internet1 == internet2
        assert internet1 <= internet2
        assert internet1 >= internet2
        assert not internet1 != internet2
        assert not internet1 < internet2
        assert not internet1 > internet2

        internet3 = InternetTime(4)
        assert internet1 < internet3
        assert internet3 > internet1
        assert internet1 <= internet3
        assert internet3 >= internet1
        assert internet1 != internet3
        assert internet3 != internet1
        assert not internet1 == internet3
        assert not internet3 == internet1
        assert not internet1 > internet3
        assert not internet3 < internet1
        assert not internet1 >= internet3
        assert not internet3 <= internet1

    def test_310_compare_invalid_types(self):
        class SomeClass:
            pass

        internet = InternetTime(3)

        # exception with non-numeric types
        for par in ("1", (1,), [1], {1: 1}, (), [], {}, None):
            assert not internet == par
            assert internet != par
            with pytest.raises(TypeError):
                internet < par
            with pytest.raises(TypeError):
                internet > par
            with pytest.raises(TypeError):
                internet <= par
            with pytest.raises(TypeError):
                internet >= par
        # exception with numeric types (all invalid) and other objects
        for par in (1, 1.0, Fraction(1, 1), Decimal(1), 1j, 1 + 1j, INF, NAN, SomeClass()):
            assert not internet == par
            assert internet != par
            with pytest.raises(TypeError):
                internet < par
            with pytest.raises(TypeError):
                internet > par
            with pytest.raises(TypeError):
                internet <= par
            with pytest.raises(TypeError):
                internet >= par

    def test_320_hash_equality(self):
        internet1 = InternetTime(12)
        # same thing
        internet2 = InternetTime(12)
        assert hash(internet1) == hash(internet2)

        dic = {internet1: 1}
        dic[internet2] = 2
        assert len(dic) == 1
        assert dic[internet1] == 2
        assert dic[internet2] == 2

    def test_330_bool(self):
        for test_row in internet_time_test_data:
            beat = test_row[1]
            assert InternetTime(beat)

    def test_400_to_day_frac(self):
        for test_row in internet_time_test_data:
            day_frac = Fraction(test_row[0])
            beat = test_row[1]
            assert InternetTime(beat).to_day_frac() == day_frac

    def test_500_repr(self):
        import datetime2
        for test_row in internet_time_test_data:
            beat = Fraction(test_row[1])
            internet = InternetTime(beat)
            internet_repr = repr(internet)
            assert internet_repr.startswith('datetime2.modern.InternetTime(') and internet_repr.endswith(')')
            args = internet_repr[30:-1]
            assert internet == eval(internet_repr)
            assert Fraction(eval(args)) == beat

    def test_520_str(self):
        for test_row in internet_time_test_data:
            beat = Fraction(test_row[1])
            internet = InternetTime(beat)
            expected = '@{:03d}'.format(floor(beat))
            assert str(internet) == expected

    def test_530_cformat_numbers(self):
        for test_row in internet_time_test_data:
            beat = Fraction(test_row[1])
            internet = InternetTime(beat)
            assert internet.cformat('%b') == '{:03d}'.format(floor(beat))

    def test_540_cformat_millibeat(self):
        for fraction, millibeat in internet_time_millibeat:
            internet = InternetTime(Fraction(fraction))
            assert internet.cformat('%f') == millibeat

    def test_550_cformat_percent(self):
        internet = InternetTime(2)
        assert internet.cformat('%') == '%'
        assert internet.cformat('%%') == '%'
        assert internet.cformat('%%%') == '%%'
        assert internet.cformat('abcd%') == 'abcd%'
        assert internet.cformat('%k') == '%k'
        assert internet.cformat('a%k') == 'a%k'
        assert internet.cformat('%k%') == '%k%'

    def test_560_cformat_invalid_type(self):
        western = InternetTime(3)
        for par in (1, (1,), [1], {1: 1}, None):
            with pytest.raises(TypeError):
                western.cformat(par)

    def test_900_pickling(self):
        for test_row in internet_time_test_data:
            beat = Fraction(test_row[1])
            internet = InternetTime(beat)
            for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
                pickled = pickle.dumps(internet, protocol)
                derived = pickle.loads(pickled)
                assert internet == derived

    def test_920_subclass(self):

        class W(InternetTime):
            theAnswer = 42

            def __init__(self, *args, **kws):
                temp = kws.copy()
                self.extra = temp.pop('extra')
                InternetTime.__init__(self, *args, **temp)

            def newmeth(self, start):
                return start + self.beat * 2

        internet1 = InternetTime(12)
        internet2 = W(12, extra=7)

        assert internet2.theAnswer == 42
        assert internet2.extra == 7
        assert internet1.to_day_frac() == internet2.to_day_frac()
        assert internet2.newmeth(-7) == internet1.beat * 2 - 7

