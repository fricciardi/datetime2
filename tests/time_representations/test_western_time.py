# tests for western time representation

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

__author__ = 'Francesco Ricciardi <francescor2010 at yahoo.it>'

from decimal import Decimal
from fractions import Fraction
import pickle
import pytest

from datetime2.western import WesternTime

# TODO: Also implement to_time_pair tests

INF = float('inf')
NAN = float('nan')

western_time_test_data = [
    # day_frac           western                    as hours         as minutes         as seconds
    #   numer denom       h   m   s                 num denum         num denum         num denum

    # Boundary conditions around midnight
    # hour, minute, second and their halves second
    [      "0/1",       ( 0,  0,  0),                "0/1",            "0/1",            "0/1"],
    [      "1/24",      ( 1,  0,  0),                "1/1",           "60/1",         "3600/1"],
    [     "23/24",      (23,  0,  0),               "23/1",         "1380/1",        "82800/1"],
    [      "1/48",      ( 0, 30,  0),                "1/2",           "30/1",         "1800/1"],
    [     "47/48",      (23, 30,  0),               "47/2",         "1410/1",        "84600/1"],
    [      "1/1440",    ( 0,  1,  0),                "1/60",           "1/1",           "60/1"],
    [   "1439/1440",    (23, 59,  0),             "1439/60",        "1439/1",        "86340/1"],
    [      "1/2880",    ( 0,  0, 30),                "1/120",          "1/2",           "30/1"],
    [   "2879/2880",    (23, 59, 30),             "2879/120",       "2879/2",        "86370/1"],
    [      "1/86400",   ( 0,  0,  1),                "1/3600",         "1/60",           "1/1"],
    [  "86399/86400",   (23, 59, 59),            "86399/3600",     "86399/60",       "86399/1"],
    [      "1/172800",  ( 0,  0,  0.5),              "1/7200",         "1/120",          "1/2"],
    [ "172799/172800",  (23, 59, 59.5),         "172799/7200",    "172799/120",     "172799/2"],

    # Boundary conditions around noon (e.g. for AM/PM switch)
    # hour, minute, second and their halves second
    [      "1/2",       (12,  0,  0),               "12/1",          "720/1",        "43200/1"],
    [     "11/24",      (11,  0,  0),               "11/1",          "660/1",        "39600/1"],
    [     "13/24",      (13,  0,  0),               "13/1",          "780/1",        "46800/1"],
    [     "23/48",      (11, 30,  0),               "23/2",          "690/1",        "41400/1"],
    [     "25/48",      (12, 30,  0),               "25/2",          "750/1",        "45000/1"],
    [    "719/1440",    (11, 59,  0),              "719/60",         "719/1",        "43140/1"],
    [    "721/1440",    (12,  1,  0),              "721/60",         "721/1",        "43260/1"],
    [   "1439/2880",    (11, 59, 30),             "1439/120",       "1439/2",        "43170/1"],
    [   "1441/2880",    (12,  0, 30),             "1441/120",       "1441/2",        "43230/1"],
    [  "43199/86400",   (11, 59, 59),            "43199/3600",     "43199/60",       "43199/1"],
    [  "43201/86400",   (12,  0,  1),            "43201/3600",     "43201/60",       "43201/1"],
    [  "86399/172800",  (11, 59, 59.5),          "86399/7200",     "86399/120",      "86399/2"],
    [  "86401/172800",  (12,  0,  0.5),          "86401/7200",     "86401/120",      "86401/2"],

    # fractional part of day
    [ "     1/10",      ( 2, 24, 0),                "12/5",          "144/1",         "8640/1"],
    [      "1/100",     ( 0, 14, 24),                "6/25",          "72/5",          "864/1"],
    [      "1/1000",    ( 0,  1, "132/5"),           "3/125",         "36/25",         "432/5"],
    [      "1/10000",   ( 0,  0, "216/25"),          "3/1250",        "18/125",        "216/25"],
    [      "1/100000",  ( 0,  0, "108/125"),         "3/12500",        "9/625",        "108/125"],
    [      "1/1000000", ( 0,  0, "54/625"),          "3/125000",       "9/6250",        "54/625"],
    [ "999999/1000000", (23, 59, "37446/625"), "2999997/125000", "8999991/6250",  "53999946/625"],
    [  "99999/100000",  (23, 59, "7392/125"),   "299997/12500",   "899991/625",   "10799892/125"],
    [   "9999/10000",   (23, 59, "1284/25"),     "29997/1250",    "179982/125",    "2159784/25"],
    [    "999/1000",    (23, 58, "168/5"),        "2997/125",      "35964/25",      "431568/5"],
    [     "99/100",     (23, 45, 36),              "594/25",        "7128/5",        "85536/1"],
    [      "9/10",      (21, 36,  0),              "108/5",         "1296/1",        "77760/1"]
]

western_time_out_of_range_data = [
    # negative hour, minute or second
    [-1, 20,  30],
    [10, -1,  30],
    [10, 20,  -1],
    # values above limits
    [24, 20,  30],
    [25, 20,  30],
    [10, 60,  30],
    [10, 61,  30],
    [10, 20,  60],
    [10, 20,  61]
]

western_time_microseconds = [
    # boundary conditions
    [      "0/1",       "000000"],
    [      "1/1000000", "000001"],
    [      "1/2000000", "000000"],
    [ "999999/1000000", "999999"],
    ["1999999/2000000", "999999"],
    # a few not so random numbers
    [     "3/7",        "428571"],
    [ "12345/23456",    "526304"]
]

timezone_test_data = [
    ["-24",             Fraction(-24, 1)],
    [Decimal("-23.5"),  Fraction(-47, 2)],
    [-2,                Fraction(-2, 1)],
    [-0.5,              Fraction(-1, 2)],
    [Fraction(0, 1),    Fraction(0, 1)],
    [Decimal(0.25),     Fraction(1, 4)],
    [2,                 Fraction(2, 1)],
    [23.5,              Fraction(47, 2)],
    ["24",              Fraction(24, 1)]
]

timezone_cformat_test_data = [
    ["-24",             "-24:00"],
    [Decimal("-23.5"),  "-23:30"],
    [-2,                "-02:00"],
    [-0.5,              "-00:30"],
    [Fraction(0, 1),    "+00:00"],
    [Decimal(0.25),     "+00:15"],
    [2,                 "+02:00"],
    [23.5,              "+23:30"],
    ["24",              "+24:00"],
    [Fraction(2831, 225), "+12:34:56"],
    [Fraction(-23, 7),    "-03:17:08.571428"]
]


def test_00_constructor():
    # check all types for seconds are accepted
    for integer_second in (3, '3'):
        for timezone in (None, 1):
            western = WesternTime(5, 4, integer_second, timezone=timezone)
            assert isinstance(western.hour, int)
            assert western.hour == 5
            assert isinstance(western.minute, int)
            assert western.minute == 4
            assert isinstance(western.second, Fraction)
            assert western.second == Fraction(3, 1)
            if timezone is None:
                assert western.timezone is None
            else:
                assert isinstance(western.timezone, Fraction)
                assert western.timezone == Fraction(1, 1)
    for fractional_second in (1.25, Fraction(5, 4), '1.25', Decimal('1.25'), '5/4'):
        for timezone in (None, 1):
            western = WesternTime(5, 4, fractional_second, timezone=timezone)
            assert isinstance(western.second, Fraction)
            assert western.second == Fraction(5, 4)
            if timezone is None:
                assert western.timezone is None
            else:
                assert isinstance(western.timezone, Fraction)
                assert western.timezone == Fraction(1, 1)

    # check all types for timezone are accepted
    for integer_timezone in (13, '13'):
        western = WesternTime(5, 4, 3, timezone=integer_timezone)
        assert isinstance(western.timezone, Fraction)
        assert western.timezone == Fraction(13, 1)
    for fractional_timezone in (1.25, Fraction(5, 4), '1.25', Decimal('1.25'), '5/4'):
        western = WesternTime(5, 4, 3, timezone=fractional_timezone)
        assert isinstance(western.timezone, Fraction)
        assert western.timezone == Fraction(5, 4)

    # exception with none, two or four parameters
    with pytest.raises(TypeError):
        WesternTime()
    with pytest.raises(TypeError):
        WesternTime(1, 2)
    with pytest.raises(TypeError):
        WesternTime(1, 2, 3, 4)

    # exception with non-numeric types
    for invalid_par in ("1", (1,), [1], {1: 1}, (), [], {}, None):
        with pytest.raises(TypeError):
            WesternTime(invalid_par, 1, 1)
        with pytest.raises(TypeError):
            WesternTime(1, invalid_par, 1)
    for invalid_par in ((1,), [1], {1: 1}, (), [], {}, None): # "1" is acceptable for seconds, since it is a valid Fraction argument
        with pytest.raises(TypeError):
            WesternTime(1, 1, invalid_par)
    for invalid_par in ((1,), [1], {1: 1}, (), [], {}):  # and also None is acceptable for timezone
        with pytest.raises(TypeError):
            WesternTime(1, 1, 1, timezone=invalid_par)

    # exception with unknown named parameter
    with pytest.raises(TypeError):
        WesternTime(1, 2, 3, invalid=0)

    # exception with invalid numeric types
    for invalid_par in (1.0, Fraction(1, 1), Decimal(1), 1j, 1 + 1j, INF, NAN):
        with pytest.raises(TypeError):
            WesternTime(invalid_par, 1, 1)
        with pytest.raises(TypeError):
            WesternTime(1, invalid_par, 1)
    for invalid_par in (1j, 1 + 1j, INF, NAN):
        with pytest.raises(TypeError):
            WesternTime(1, 1, invalid_par)
        with pytest.raises(TypeError):
            WesternTime(1, 2, 3, timezone=invalid_par)

    # valid constructor values
    for test_row in western_time_test_data:
        hour = test_row[1][0]
        minute = test_row[1][1]
        second = Fraction(test_row[1][2])
        western = WesternTime(hour, minute, second)
        assert (western.hour, western.minute, western.second) == (hour, minute, second)
        assert western.timezone is None
    for test_timezone in timezone_test_data:
        western = WesternTime(1, 2, 3, timezone=test_timezone[0])
        assert western.timezone == test_timezone[1]

    # invalid constructor values
    for test_row in western_time_out_of_range_data:
        hour = test_row[0]
        minute = test_row[1]
        second = test_row[2]
        with pytest.raises(ValueError):
            WesternTime(hour, minute, second)
    for invalid_value in (-25, -24.000001, Fraction(24_000_001, -1_000_000), Fraction(24_000_001, 1_000_000), 24.000001, 25):
        with pytest.raises(ValueError):
            WesternTime(1, 2, 3, timezone=invalid_value)


def test_02_constructor_from_time_pair():
    # valid types
    for test_row in western_time_test_data:
        day_frac = Fraction(test_row[0])
        western1 = WesternTime.from_time_pair(day_frac, None)
        assert isinstance(western1.hour, int)
        assert isinstance(western1.minute, int)
        assert isinstance(western1.second, Fraction)
        assert western1.timezone is None
        western2 = WesternTime.from_time_pair(day_frac, Fraction(3, 4))
        assert isinstance(western2.hour, int)
        assert isinstance(western2.minute, int)
        assert isinstance(western2.second, Fraction)
        assert isinstance(western2.timezone, Fraction)
        western3 = WesternTime.from_time_pair(day_frac, Fraction(-1, 5))
        assert isinstance(western3.hour, int)
        assert isinstance(western3.minute, int)
        assert isinstance(western3.second, Fraction)
        assert isinstance(western3.timezone, Fraction)

    # exception with none, one or three parameters
    with pytest.raises(TypeError):
        WesternTime.from_time_pair()
    with pytest.raises(TypeError):
        WesternTime.from_time_pair(1)
    with pytest.raises(TypeError):
        WesternTime.from_time_pair(1, 2, 3)

    # exception with non-numeric types
    for invalid_time_pair in ("1", (1,), [1], {1: 1}, (), [], {}, None):
        with pytest.raises(TypeError):
            WesternTime.from_time_pair(invalid_time_pair, None)
            WesternTime.from_time_pair(invalid_time_pair, Fraction(3, 4))
            WesternTime.from_time_pair(Fraction(3, 4), invalid_time_pair)

    # exception with invalid numeric types
    for invalid_time_pair in (1.0, Decimal(1), 1j, 1 + 1j, INF, NAN):
        with pytest.raises(TypeError):
            WesternTime.from_time_pair(invalid_time_pair, None)
            WesternTime.from_time_pair(invalid_time_pair, Fraction(3, 4))
            WesternTime.from_time_pair(Fraction(3, 4), invalid_time_pair)

    # valid values
    for test_row in western_time_test_data:
        day_frac = Fraction(test_row[0])
        hour = test_row[1][0]
        minute = test_row[1][1]
        second = Fraction(test_row[1][2])
        western1 = WesternTime.from_time_pair(day_frac, None)
        assert (western1.hour, western1.minute, western1.second) == (hour, minute, second)
        western2 = WesternTime.from_time_pair(day_frac, Fraction(3, 4))
        assert (western2.hour, western2.minute, western2.second) == (hour, minute, second)
        western3 = WesternTime.from_time_pair(day_frac, Fraction(-1, 5))
        assert (western3.hour, western3.minute, western3.second) == (hour, minute, second)

    # invalid values
    for num, denum in ((1, 1), (1, -1), (1000001, 1000000), (-1, 1000000)):
        with pytest.raises(ValueError):
            WesternTime.from_time_pair(Fraction(num, denum), None)
    for num, denum in ((-1000001, 1000000), (1000001, 1000000)):
        with pytest.raises(ValueError):
            WesternTime.from_time_pair(Fraction(3, 5), Fraction(num, denum))


def test_20_attributes():
    for western in WesternTime(10, 10, 10), WesternTime(10, 10, 10, timezone=10):
        with pytest.raises(AttributeError):
            western.hour = 3
        with pytest.raises(AttributeError):
            western.minute = 3
        with pytest.raises(AttributeError):
            western.second = 3
        with pytest.raises(AttributeError):
            western.timezone = 3


def test_30_repr():
    import datetime2
    for test_row in western_time_test_data:
        hour = test_row[1][0]
        minute = test_row[1][1]
        second = Fraction(test_row[1][2])
        western = WesternTime(hour, minute, second)
        western_repr = repr(western)
        assert western_repr.startswith('datetime2.western.WesternTime(') and western_repr.endswith(')')
        args = western_repr[30:-1]
        found_hour, found_minute, found_second = args.split(',', 2)
        assert western == eval(western_repr)
        assert int(found_hour.strip()) == hour
        assert int(found_minute.strip()) == minute
        assert eval(found_second) == second
    for test_timezone in timezone_test_data:
        western = WesternTime(1, 2, 3, timezone=test_timezone[0])
        western_repr = repr(western)
        assert western_repr.startswith('datetime2.western.WesternTime(') and western_repr.endswith(')')
        args = western_repr[30:-1]
        found_hour, found_minute, second_and_timezone = args.split(',', 2)
        found_second, found_timezone = second_and_timezone.split(', timezone=')
        assert western == eval(western_repr)
        assert int(found_hour.strip()) == 1
        assert int(found_minute.strip()) == 2
        assert eval(found_second) == Fraction(3, 1)
        assert eval(found_timezone) == test_timezone[1]


def test_31_str():
    for test_row in western_time_test_data:
        hour = test_row[1][0]
        minute = test_row[1][1]
        second = Fraction(test_row[1][2])
        western = WesternTime(hour, minute, second)
        expected = '{:02d}:{:02d}:{:02d}'.format(hour, minute, int(second))
        assert str(western) == expected
    for test_timezone in timezone_test_data:
        western = WesternTime(1, 2, 3, timezone=test_timezone[0])
        tz_hour = int(test_timezone[1])
        expected_timezone = f"{tz_hour:+02d}:{int((test_timezone[1] - tz_hour) * 60):02d}"
        assert str(western) == f"01:02:03{expected_timezone}"


def test_32_cformat():
    for test_row in western_time_test_data:
        hour = test_row[1][0]
        minute = test_row[1][1]
        second = Fraction(test_row[1][2])
        western = WesternTime(hour, minute, second)
        # hours
        assert western.cformat('%H') == '{:02d}'.format(hour)
        if hour == 0:
            assert western.cformat('%I') == '12'
            assert western.cformat('%p') == 'AM'
        elif hour <= 11:
            assert western.cformat('%I') == '{:02d}'.format(hour)
            assert western.cformat('%p') == 'AM'
        elif hour == 12:
            assert western.cformat('%I') == '{:02d}'.format(hour)
            assert western.cformat('%p') == 'PM'
        else:
            assert western.cformat('%I') == '{:02d}'.format(hour - 12)
            assert western.cformat('%p') == 'PM'
        # minutes and seconds
        assert western.cformat('%M') == '{:02d}'.format(minute)
        assert western.cformat('%S') == '{:02d}'.format(int(second))
        #empty timezone
        assert western.cformat('%z') == ''

    # microseconds
    for fraction, microseconds in western_time_microseconds:
        western = WesternTime(12, 34, Fraction(fraction) + 56)
        assert western.cformat('%f') == microseconds

    # timezone
    for test_cformat_timezone in timezone_cformat_test_data:
        western = WesternTime(1, 2, 3, timezone=test_cformat_timezone[0])
        assert western.cformat('%z') == test_cformat_timezone[1]

    # percent
    western = WesternTime(1, 2, 3)
    assert western.cformat('%') == '%'
    assert western.cformat('%%') == '%'
    assert western.cformat('%%%') == '%%'
    assert western.cformat('abcd%') == 'abcd%'
    assert western.cformat('%k') == '%k'
    assert western.cformat('a%k') == 'a%k'
    assert western.cformat('%k%') == '%k%'

    # invalid types
    for par in (1, (1,), [1], {1: 1}, None):
        with pytest.raises(TypeError):
            western.cformat(par)


def test_50_to_time_pair():
    for test_row in western_time_test_data:
        day_frac = Fraction(test_row[0])
        hour = test_row[1][0]
        minute = test_row[1][1]
        second = Fraction(test_row[1][2])
        assert WesternTime(hour, minute, second).to_time_pair() == (day_frac, None)
        assert WesternTime(hour, minute, second, timezone="7.5").to_time_pair() == (day_frac, Fraction(5, 16))
        assert WesternTime(hour, minute, second, timezone=-4).to_time_pair() == (day_frac, Fraction(-1, 6))
    for test_timezone in timezone_test_data:
        western = WesternTime(1, 2, 3, timezone=test_timezone[0])
        assert western.to_time_pair()[1] == test_timezone[1] / 24


def test_51_replace():
    for test_row in western_time_test_data:
        hour = test_row[1][0]
        minute = test_row[1][1]
        second = Fraction(test_row[1][2])
        western = WesternTime(hour, minute, second)
        assert western.replace() == WesternTime(hour, minute, second)
        assert western.replace(hour=11) == WesternTime(11, minute, second)
        assert western.replace(minute=10) == WesternTime(hour, 10, second)
        assert western.replace(second=9) == WesternTime(hour, minute, 9)
        assert western.replace(minute=10, hour=11) == WesternTime(11, 10, second)
        assert western.replace(second=9, hour=11) == WesternTime(11, minute, 9)
        assert western.replace(second=9, minute=10) == WesternTime(hour, 10, 9)
        assert western.replace(second=9, minute=10, hour=11) == WesternTime(11, 10, 9)
    for test_timezone in timezone_test_data:
        western = WesternTime(1, 2, 3, timezone=test_timezone[0])
        assert western.replace(hour=11, timezone=-1) == WesternTime(11, 2, 3, timezone=-1)
        assert western.replace(minute=22, timezone=2) == WesternTime(1, 22, 3, timezone=2)
        assert western.replace(second=33, timezone=-3) == WesternTime(1, 2, 33, timezone=-3)

    ### invalid types
    western = WesternTime(11, 10, 9)
    western_t = WesternTime(11, 10, 9, timezone=4)
    # exception for positional parameters
    with pytest.raises(TypeError):
        western.replace(1)
    # exception with non-numeric types
    for par in ("1", (1,), [1], {1: 1}, (), [], {}):
        with pytest.raises(TypeError):
            western.replace(hour=par)
        with pytest.raises(TypeError):
            western.replace(minute=par)
    for par in ((1,), [1], {1: 1}, (), [], {}):
        with pytest.raises(TypeError):
            western.replace(second=par)
        with pytest.raises(TypeError):
            western_t.replace(timezone=par)
    # exception with invalid numeric types
    for par in (1.0, Fraction(1, 1), Decimal(1), 1j, 1 + 1j, INF, NAN):
        with pytest.raises(TypeError):
            western.replace(hour=par)
        with pytest.raises(TypeError):
            western.replace(minute=par)
    for par in (1j, 1 + 1j, INF):
        with pytest.raises(TypeError):
            western.replace(second=par)
        with pytest.raises(TypeError):
            western_t.replace(timezone=par)

    # invalid values
    with pytest.raises(ValueError):
        western.replace(hour=-1)
    with pytest.raises(ValueError):
        western.replace(hour=24)
    with pytest.raises(ValueError):
        western.replace(minute=-1)
    with pytest.raises(ValueError):
        western.replace(minute=60)
    with pytest.raises(ValueError):
        western.replace(second='-1/1000000')
    with pytest.raises(ValueError):
        western.replace(second=60)
    with pytest.raises(TypeError):
        western.replace(second=NAN)
    with pytest.raises(ValueError):
        western_t.replace(timezone='-24000001/1000000')
    with pytest.raises(ValueError):
        western_t.replace(timezone='24000001/1000000')
    with pytest.raises(TypeError):
        western_t.replace(timezone=NAN)

    # replacing timezone in a naive instance
    with pytest.raises(TypeError):
        western.replace(timezone=3)
