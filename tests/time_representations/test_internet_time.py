# tests for internet time representation

# Copyright (c) 2012-2022 Francesco Ricciardi
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

__author__ = "Francesco Ricciardi <francescor2010 at yahoo.it>"

from decimal import Decimal
from fractions import Fraction
from math import floor
import pickle
import pytest

from datetime2.modern import InternetTime


INF = float("inf")
NAN = float("nan")

    # day_frac    internet  with to_utc=1/3       with to_utc=-1/5
internet_time_test_data = [
    # beat and half beat
    ["0/1",       0,        Fraction(1, 3),       Fraction(4, 5)],
    ["1/1000",    1,        Fraction(1003, 3000), Fraction(801, 1000)],
    ["999/1000",  999,      Fraction(997, 3000),  Fraction(799, 1000)],
    ["1/2000",    0.5,      Fraction(2003, 6000), Fraction(1601, 2000)],
    ["1999/2000", 999.5,    Fraction(1997, 6000), Fraction(1599, 2000)],
    # fractional part of day
    ["1/10",      100,      Fraction(13, 30),     Fraction(9, 10)],
    ["1/100",     10,       Fraction(103, 300),   Fraction(81, 100)],
    ["1/1000",    1,        Fraction(1003, 3000), Fraction(801, 1000)],
    ["1/10000",   "1/10",   Fraction(10003, 30000), Fraction(8001, 10000)],
    ["1/100000",  "1/100",  Fraction(100003, 300000), Fraction(80001, 100000)],
    ["1/1000000", "1/1000", Fraction(1000003, 3000000), Fraction(800001, 1000000)]
]

internet_time_out_of_range = [-1, 1000, "10001/10", 1001]

internet_time_millibeat = [
    # boundary conditions
    ["0/1", "000"],
    ["1/1000", "001"],
    ["1/2000", "000"],
    ["999/1000", "999"],
    ["1999/2000", "999"],
    # a few not so random numbers
    ["5/7", "714"],
    ["12345/56789", "217"],
]


class TestInternet:
    def test_000_ok_constructor_types(self):
        for beat in (11, "11", Decimal("11"), Fraction(11, 1)):
            internet = InternetTime(beat)
            assert isinstance(internet.beat, Fraction)
            assert internet.beat == Fraction(11)
        for beat in (111.25, "111.25", Decimal("111.25"), "445/4"):
            internet = InternetTime(beat)
            assert isinstance(internet.beat, Fraction)
            assert internet.beat == Fraction(445, 4)

    def test_000_ko_constructor_types(self):
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
        for par in (1j, 1 + 1j, INF, NAN):
            with pytest.raises(TypeError):
                InternetTime(par)

    def test_001_ok_constructor_values_(self):
        for test_row in internet_time_test_data:
            internet = InternetTime(test_row[1])
            assert internet.beat == Fraction(test_row[0]) * 1000

    def test_001_ko_constructor_values(self):
        for test_beat in internet_time_out_of_range:
            with pytest.raises(ValueError):
                InternetTime(test_beat)

    def test_010_ok_constructor_time_pair_types(self):
        internet1 = InternetTime.from_time_pair(Fraction("3/4"), Fraction(-0.5))
        assert isinstance(internet1.beat, Fraction)
        # with overflow
        internet2 = InternetTime.from_time_pair(Fraction("3/4"), Fraction(0.5))
        assert isinstance(internet2.beat, Fraction)
        # with underflow
        internet3 = InternetTime.from_time_pair(Fraction("1/4"), Fraction(-0.5))
        assert isinstance(internet3.beat, Fraction)

    def test_010_ko_constructor_time_pair_types(self):
        # exception with none, one or three parameters
        with pytest.raises(TypeError):
            InternetTime.from_time_pair()
        with pytest.raises(TypeError):
            InternetTime.from_time_pair(Fraction(1))
        with pytest.raises(TypeError):
            InternetTime.from_time_pair(Fraction(1), Fraction(0.5), Fraction(0.5))

        # exception with non-numeric types
        for par in ("1", (1,), [1], {1: 1}, (), [], {}, None):
            with pytest.raises(TypeError):
                InternetTime.from_time_pair(par, Fraction(0.5))
            with pytest.raises(TypeError):
                InternetTime.from_time_pair(Fraction(0.5), par)

        # exception with invalid numeric types
        for par in (1, 1.0, Decimal(1), 1j, 1 + 1j, INF, NAN):
            with pytest.raises(TypeError):
                InternetTime.from_time_pair(par, Fraction(0.5))
            with pytest.raises(TypeError):
                InternetTime.from_time_pair(Fraction(0.5), par)

    def test_011_ok_constructor_time_pair_values(self):
        for test_row in internet_time_test_data:
            internet1 = InternetTime.from_time_pair(Fraction(test_row[0]), Fraction(0))
            assert internet1.beat == Fraction(test_row[1])
            internet2 = InternetTime.from_time_pair(Fraction(test_row[2]), Fraction('1/3'))
            assert internet2.beat == Fraction(test_row[1])
            internet3 = InternetTime.from_time_pair(Fraction(test_row[3]), Fraction('-1/5'))
            assert internet3.beat == Fraction(test_row[1])
            internet4 = InternetTime.from_time_pair(Fraction(test_row[0]), Fraction(1))
            assert internet4.beat == Fraction(test_row[1])
            internet5 = InternetTime.from_time_pair(Fraction(test_row[0]), Fraction(-1))
            assert internet5.beat == Fraction(test_row[1])

    def test_011_ko_constructor_time_pair_values(self):
        for par in (Fraction(1000001, 1000000), Fraction(-1, 1000000)):
            with pytest.raises(ValueError):
                InternetTime.from_time_pair(par, Fraction(1, 2))
        for par in (Fraction(1000001, 1000000), Fraction(-1000001, 1000000)):
            with pytest.raises(ValueError):
                InternetTime.from_time_pair(Fraction(1, 2), par)

    def test_020_to_and_from_time_pair(self):
        for test_row in internet_time_test_data:
            internet1 = InternetTime(test_row[1])
            assert internet1.to_time_pair() == (Fraction(test_row[0]), Fraction(-1, 24))
            internet2 = InternetTime.from_time_pair(test_row[2], Fraction("1/3"))
            assert internet2.to_time_pair() == (Fraction(test_row[0]), Fraction(-1, 24))
            internet3 = InternetTime.from_time_pair(test_row[3], Fraction("-1/5"))
            assert internet3.to_time_pair() == (Fraction(test_row[0]), Fraction(-1, 24))

    def test_200_write_attribute(self):
        internet1 = InternetTime(10)
        with pytest.raises(AttributeError):
            internet1.beat = 3
        internet2 = InternetTime.from_time_pair(Fraction(2, 7), Fraction(0.5))
        with pytest.raises(AttributeError):
            internet1.beat = 3

    def test_300_ok_compare(self):
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

    def test_300_ko_compare(self):
        # we can have errors only with wrong types
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
        internet1 = InternetTime(100)
        # same thing
        internet2 = InternetTime(100)
        assert hash(internet1) == hash(internet2)
        internet3 = InternetTime.from_time_pair(Fraction(1, 5), Fraction(1, 10))
        assert hash(internet1) == hash(internet3)
        internet4 = InternetTime.from_time_pair(Fraction(9, 10), Fraction(-1, 5))
        assert hash(internet1) == hash(internet4)
        internet5 = InternetTime.from_time_pair(Fraction(1, 20), Fraction(19, 20))
        assert hash(internet1) == hash(internet5)

        dic = {internet1: 1}
        dic[internet2] = 2
        assert len(dic) == 1
        assert dic[internet1] == 2
        assert dic[internet2] == 2
        dic[internet3] = 2
        assert len(dic) == 1
        assert dic[internet3] == 2
        dic[internet4] = 2
        assert len(dic) == 1
        assert dic[internet4] == 2
        dic[internet5] = 2
        assert len(dic) == 1
        assert dic[internet5] == 2

    def test_330_bool(self):
        for test_row in internet_time_test_data:
            beat = test_row[1]
            assert InternetTime(beat)

    def test_500_repr(self):
        import datetime2

        for test_row in internet_time_test_data:
            beat = Fraction(test_row[1])
            internet = InternetTime(beat)
            internet_repr = repr(internet)
            assert internet_repr.startswith("datetime2.modern.InternetTime(") and internet_repr.endswith(")")
            args = internet_repr[30:-1]
            assert internet == eval(internet_repr)
            assert Fraction(eval(args)) == beat

    def test_520_str(self):
        for test_row in internet_time_test_data:
            beat = Fraction(test_row[1])
            internet = InternetTime(beat)
            expected = "@{:03d}".format(floor(beat))
            assert str(internet) == expected

    def test_530_cformat_numbers(self):
        for test_row in internet_time_test_data:
            beat = Fraction(test_row[1])
            internet = InternetTime(beat)
            assert internet.cformat("%b") == "{:03d}".format(floor(beat))

    def test_540_cformat_millibeat(self):
        for fraction, millibeat in internet_time_millibeat:
            internet = InternetTime(Fraction(fraction))
            assert internet.cformat("%f") == millibeat

    def test_550_cformat_percent(self):
        internet = InternetTime(2)
        assert internet.cformat("%") == "%"
        assert internet.cformat("%%") == "%"
        assert internet.cformat("%%%") == "%%"
        assert internet.cformat("abcd%") == "abcd%"
        assert internet.cformat("%k") == "%k"
        assert internet.cformat("a%k") == "a%k"
        assert internet.cformat("%k%") == "%k%"

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
                self.extra = temp.pop("extra")
                InternetTime.__init__(self, *args, **temp)

            def newmeth(self, start):
                return start + self.beat * 2

        internet1 = InternetTime(12)
        internet2 = W(12, extra=7)

        assert internet2.theAnswer == 42
        assert internet2.extra == 7
        assert internet1.to_time_pair() == internet2.to_time_pair()
        assert internet2.newmeth(-7) == internet1.beat * 2 - 7
