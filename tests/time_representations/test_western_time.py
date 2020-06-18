# tests for western time representation

# Copyright (c) 2012-2020 Francesco Ricciardi
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

from datetime2.western import WesternTime


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

to_utc_test_data = [
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


class TestWestern:
    def test_000_ok_constructor_types(self):
        # check all types for seconds are accepted
        for integer_second in (3, '3'):
            western = WesternTime(5, 4, integer_second)
            assert isinstance(western.hour, int)
            assert western.hour == 5
            assert isinstance(western.minute, int)
            assert western.minute == 4
            assert isinstance(western.second, Fraction)
            assert western.second == Fraction(3, 1)
            assert western.to_utc is None
        for fractional_second in (1.25, Fraction(5, 4), '1.25', Decimal('1.25'), '5/4'):
            western = WesternTime(5, 4, fractional_second)
            assert isinstance(western.second, Fraction)
            assert western.second == Fraction(5, 4)
            assert western.to_utc is None

    def test_000_ko_constructor_types(self):
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
        # exception with invalid numeric types
        for invalid_par in (1.0, Fraction(1, 1), Decimal(1), 1j, 1 + 1j, INF, NAN):
            with pytest.raises(TypeError):
                WesternTime(invalid_par, 1, 1)
            with pytest.raises(TypeError):
                WesternTime(1, invalid_par, 1)
        for invalid_par in (1j, 1 + 1j, INF, NAN):
            with pytest.raises(TypeError):
                WesternTime(1, 1, invalid_par)

    def test_001_ok_constructor_values(self):
        for test_row in western_time_test_data:
            hour = test_row[1][0]
            minute = test_row[1][1]
            second = Fraction(test_row[1][2])
            western = WesternTime(hour, minute, second)
            assert (western.hour, western.minute, western.second) == (hour, minute, second)
            assert western.to_utc is None

    def test_001_ko_constructor_values(self):
        for test_row in western_time_out_of_range_data:
            hour = test_row[0]
            minute = test_row[1]
            second = test_row[2]
            with pytest.raises(ValueError):
                WesternTime(hour, minute, second)

    def test_010_ok_constr_with_utc_types(self):
        # check all types for to_utc are accepted
        for integer_to_utc in (13, '13'):
            western = WesternTime(5, 4, 3, to_utc=integer_to_utc)
            assert isinstance(western.to_utc, Fraction)
            assert western.to_utc == Fraction(13, 1)
        for fractional_to_utc in (1.25, Fraction(5, 4), '1.25', Decimal('1.25'), '5/4'):
            western = WesternTime(5, 4, 3, to_utc=fractional_to_utc)
            assert isinstance(western.to_utc, Fraction)
            assert western.to_utc == Fraction(5, 4)

    def test_010_ko_constr_with_utc_types(self):
        # exception with unknown named parameter
        with pytest.raises(TypeError):
            WesternTime(1, 2, 3, invalid=0)

        # exception with non-numeric types
        for invalid_to_utc in ((1,), [1], {1: 1}, (), [], {}):
            with pytest.raises(TypeError):
                WesternTime(1, 2, 3, to_utc=invalid_to_utc)

        # exception with invalid numeric types
        for invalid_to_utc in (1j, 1 + 1j, INF, NAN):
            with pytest.raises(TypeError):
                WesternTime(1, 2, 3, to_utc=invalid_to_utc)

    def test_011_ok_constr_with_utc_values(self):
        for test_to_utc in to_utc_test_data:
            western = WesternTime(1, 2, 3, to_utc=test_to_utc[0])
            assert western.to_utc == test_to_utc[1]

    def test_011_ko_constr_with_utc_values(self):
        for invalid_value in (-25, -24.000001, Fraction(24_000_001, -1_000_000), Fraction(24_000_001, 1_000_000), 24.000001, 25):
            with pytest.raises(ValueError):
                WesternTime(1, 2, 3, to_utc=invalid_value)

    def test_020_ok_constr_in_hours_types(self):
        # check all types for seconds are accepted
        for hours in (3, '3'):
            western = WesternTime.in_hours(hours)
            assert isinstance(western.hour, int)
            assert western.hour == 3
            assert isinstance(western.minute, int)
            assert western.minute == 0
            assert isinstance(western.second, Fraction)
            assert western.second == Fraction(0)
            assert western.to_utc is None
        for fractional_hours in (13.125, Fraction(105, 8), '13.125', Decimal('13.125'), '105/8'):
            western = WesternTime.in_hours(fractional_hours)
            assert isinstance(western.hour, int)
            assert western.hour == 13
            assert isinstance(western.minute, int)
            assert western.minute == 7
            assert isinstance(western.second, Fraction)
            assert western.second == Fraction(30)
            assert western.to_utc is None

    def test_020_ko_constr_in_hours_types(self):
        # exception with none, three or four parameters
        with pytest.raises(TypeError):
            WesternTime.in_hours()
        with pytest.raises(TypeError):
            WesternTime.in_hours(1, 2, 3)
        with pytest.raises(TypeError):
            WesternTime.in_hours(1, 2, 3, 4)
        # exception with non-numeric types
        for invalid_hours in ((1,), [1], {1: 1}, (), [], {}, None):
            with pytest.raises(TypeError):
                WesternTime.in_hours(invalid_hours)
        # exception with invalid numeric types
        for invalid_hours in (1j, 1 + 1j, INF, NAN):
            with pytest.raises(TypeError):
                WesternTime.in_hours(invalid_hours)

    def test_021_ok_constr_in_hours_values(self):
        for test_row in western_time_test_data:
            in_hours = Fraction(test_row[2])
            hour = test_row[1][0]
            minute = test_row[1][1]
            second = Fraction(test_row[1][2])
            western = WesternTime.in_hours(in_hours)
            assert (western.hour, western.minute, western.second) == (hour, minute, second)

    def test_021_ko_constr_in_hours_values(self):
        for num, denum in ((24, 1), (1, -1), (24000001, 1000000), (-1, 1000000)):
            with pytest.raises(ValueError):
                WesternTime.in_hours(Fraction(num, denum))

    def test_030_ok_constr_in_hours_with_utc_types(self):
        for integer_to_utc in (13, '13'):
            western = WesternTime.in_hours(5, to_utc=integer_to_utc)
            assert isinstance(western.to_utc, Fraction)
            assert western.to_utc == Fraction(13, 1)
        for fractional_to_utc in (1.25, Fraction(5, 4), '1.25', Decimal('1.25'), '5/4'):
            western = WesternTime.in_hours(3, to_utc=fractional_to_utc)
            assert isinstance(western.to_utc, Fraction)
            assert western.to_utc == Fraction(5, 4)

    def test_030_ko_constr_in_hours_with_utc_types(self):
        # exception with unknown named parameter
        with pytest.raises(TypeError):
            WesternTime.in_hours("789/123", invalid=0)

        # exception with non-numeric types
        for invalid_to_utc in ((1,), [1], {1: 1}, (), [], {}):
            with pytest.raises(TypeError):
                WesternTime.in_hours("789/123", to_utc=invalid_to_utc)

        # exception with invalid numeric types
        for invalid_to_utc in (1j, 1 + 1j, INF, NAN):
            with pytest.raises(TypeError):
                WesternTime.in_hours("789/123", to_utc=invalid_to_utc)

    def test_031_ok_constr_in_hours_with_utc_values(self):
        for test_to_utc in to_utc_test_data:
            western = WesternTime.in_hours(7, to_utc=test_to_utc[0])
            assert western.to_utc == test_to_utc[1]

    def test_031_ko_constr_in_hours_with_utc_values(self):
        for invalid_value in (-25, -24.000001, Fraction(24_000_001, -1_000_000), Fraction(24_000_001, 1_000_000), 24.000001, 25):
            with pytest.raises(ValueError):
                WesternTime.in_hours(7, to_utc=invalid_value)

    def test_040_ok_constr_in_minutes_types(self):
        # check all types for seconds are accepted
        for minutes in (333, '333'):
            western = WesternTime.in_minutes(minutes)
            assert isinstance(western.hour, int)
            assert western.hour == 5
            assert isinstance(western.minute, int)
            assert western.minute == 33
            assert isinstance(western.second, Fraction)
            assert western.second == Fraction(0)
            assert western.to_utc is None
        for fractional_minutes in (333.25, Fraction(1333, 4), '333.25', Decimal('333.25'), '1333/4'):
            western = WesternTime.in_minutes(fractional_minutes)
            assert isinstance(western.hour, int)
            assert western.hour == 5
            assert isinstance(western.minute, int)
            assert western.minute == 33
            assert isinstance(western.second, Fraction)
            assert western.second == Fraction(15)
            assert western.to_utc is None

    def test_040_ko_constr_in_minutes_types(self):
        # exception with none, three or four parameters
        with pytest.raises(TypeError):
            WesternTime.in_minutes()
        with pytest.raises(TypeError):
            WesternTime.in_minutes(1, 2, 3)
        with pytest.raises(TypeError):
            WesternTime.in_minutes(1, 2, 3, 4)
        # exception with non-numeric types
        for invalid_minutes in ((1,), [1], {1: 1}, (), [], {}, None):
            with pytest.raises(TypeError):
                WesternTime.in_minutes(invalid_minutes)
        # exception with invalid numeric types
        for invalid_minutes in (1j, 1 + 1j, INF, NAN):
            with pytest.raises(TypeError):
                WesternTime.in_minutes(invalid_minutes)

    def test_041_ok_constr_in_minutes_values(self):
        for test_row in western_time_test_data:
            in_minutes = Fraction(test_row[3])
            hour = test_row[1][0]
            minute = test_row[1][1]
            second = Fraction(test_row[1][2])
            western = WesternTime.in_minutes(in_minutes)
            assert (western.hour, western.minute, western.second) == (hour, minute, second)

    def test_041_ko_constr_in_minutes_values(self):
        for num, denum in ((60, 1), (1, -1), (60000001, 1000000), (-1, 1000000)):
            with pytest.raises(ValueError):
                WesternTime.in_minutes(Fraction(num, denum))

    def test_050_ok_constr_in_minutes_with_utc_types(self):
        for integer_to_utc in (13, '13'):
            western = WesternTime.in_minutes(333, to_utc=integer_to_utc)
            assert isinstance(western.to_utc, Fraction)
            assert western.to_utc == Fraction(13, 1)
        for fractional_to_utc in (1.25, Fraction(5, 4), '1.25', Decimal('1.25'), '5/4'):
            western = WesternTime.in_minutes(333, to_utc=fractional_to_utc)
            assert isinstance(western.to_utc, Fraction)
            assert western.to_utc == Fraction(5, 4)

    def test_050_ko_constr_in_minutes_with_utc_types(self):
        # exception with unknown named parameter
        with pytest.raises(TypeError):
            WesternTime.in_minutes("78901/123", invalid=0)

        # exception with non-numeric types
        for invalid_to_utc in ((1,), [1], {1: 1}, (), [], {}):
            with pytest.raises(TypeError):
                WesternTime.in_minutes("78901/123", to_utc=invalid_to_utc)

        # exception with invalid numeric types
        for invalid_to_utc in (1j, 1 + 1j, INF, NAN):
            with pytest.raises(TypeError):
                WesternTime.in_minutes("78901/123", to_utc=invalid_to_utc)

    def test_051_ok_constr_in_minutes_with_utc_values(self):
        for test_to_utc in to_utc_test_data:
            western = WesternTime.in_minutes(333, to_utc=test_to_utc[0])
            assert western.to_utc == test_to_utc[1]

    def test_051_ko_constr_in_minutes_with_utc_values(self):
        for invalid_value in (-25, -24.000001, Fraction(24_000_001, -1_000_000), Fraction(24_000_001, 1_000_000), 24.000001, 25):
            with pytest.raises(ValueError):
                WesternTime.in_minutes(333, to_utc=invalid_value)

    def test_060_ok_constr_in_seconds_types(self):
        # check all types for seconds are accepted
        for seconds in (33333, '33333'):
            western = WesternTime.in_minutes(seconds)
            assert isinstance(western.hour, int)
            assert western.hour == 9
            assert isinstance(western.minute, int)
            assert western.minute == 15
            assert isinstance(western.second, Fraction)
            assert western.second == Fraction(33)
            assert western.to_utc is None
        for fractional_minutes in (33333.25, Fraction(133333, 4), '33333.25', Decimal('33333.25'), '133333/4'):
            western = WesternTime.in_minutes(fractional_minutes)
            assert isinstance(western.hour, int)
            assert western.hour == 9
            assert isinstance(western.minute, int)
            assert western.minute == 15
            assert isinstance(western.second, Fraction)
            assert western.second == Fraction(61, 4)
            assert western.to_utc is None

    def test_060_ko_constr_in_seconds_types(self):
        # exception with none, three or four parameters
        with pytest.raises(TypeError):
            WesternTime.in_seconds()
        with pytest.raises(TypeError):
            WesternTime.in_seconds(1, 2, 3)
        with pytest.raises(TypeError):
            WesternTime.in_seconds(1, 2, 3, 4)
        # exception with non-numeric types
        for invalid_minutes in ((1,), [1], {1: 1}, (), [], {}, None):
            with pytest.raises(TypeError):
                WesternTime.in_seconds(invalid_minutes)
        # exception with invalid numeric types
        for invalid_minutes in (1j, 1 + 1j, INF, NAN):
            with pytest.raises(TypeError):
                WesternTime.in_seconds(invalid_minutes)

    def test_061_ok_constr_in_seconds_values(self):
        for test_row in western_time_test_data:
            in_seconds = Fraction(test_row[4])
            hour = test_row[1][0]
            minute = test_row[1][1]
            second = Fraction(test_row[1][2])
            western = WesternTime.in_seconds(in_seconds)
            assert (western.hour, western.minute, western.second) == (hour, minute, second)

    def test_061_ko_constr_in_seconds_values(self):
        for num, denum in ((60, 1), (1, -1), (60000001, 1000000), (-1, 1000000)):
            with pytest.raises(ValueError):
                WesternTime.in_minutes(Fraction(num, denum))

    def test_070_ok_constr_in_seconds_with_utc_types(self):
        for integer_to_utc in (13, '13'):
            western = WesternTime.in_seconds(33333, to_utc=integer_to_utc)
            assert isinstance(western.to_utc, Fraction)
            assert western.to_utc == Fraction(13, 1)
        for fractional_to_utc in (1.25, Fraction(5, 4), '1.25', Decimal('1.25'), '5/4'):
            western = WesternTime.in_seconds(33333, to_utc=fractional_to_utc)
            assert isinstance(western.to_utc, Fraction)
            assert western.to_utc == Fraction(5, 4)

    def test_070_ko_constr_in_seconds_with_utc_types(self):
        # exception with unknown named parameter
        with pytest.raises(TypeError):
            WesternTime.in_seconds("789012/123", invalid=0)

        # exception with non-numeric types
        for invalid_to_utc in ((1,), [1], {1: 1}, (), [], {}):
            with pytest.raises(TypeError):
                WesternTime.in_seconds("789012/123", to_utc=invalid_to_utc)

        # exception with invalid numeric types
        for invalid_to_utc in (1j, 1 + 1j, INF, NAN):
            with pytest.raises(TypeError):
                WesternTime.in_seconds("789012/123", to_utc=invalid_to_utc)

    def test_080_ok_constr_time_pair_types(self):
        for test_row in western_time_test_data:
            day_frac = Fraction(test_row[0])
            western1 = WesternTime.from_time_pair(day_frac, None)
            assert isinstance(western1.hour, int)
            assert isinstance(western1.minute, int)
            assert isinstance(western1.second, Fraction)
            assert western1.to_utc is None
            western2 = WesternTime.from_time_pair(day_frac, Fraction(3, 4))
            assert isinstance(western2.hour, int)
            assert isinstance(western2.minute, int)
            assert isinstance(western2.second, Fraction)
            assert isinstance(western2.to_utc, Fraction)
            western3 = WesternTime.from_time_pair(day_frac, Fraction(-1, 5))
            assert isinstance(western3.hour, int)
            assert isinstance(western3.minute, int)
            assert isinstance(western3.second, Fraction)
            assert isinstance(western3.to_utc, Fraction)

    def test_080_ko_constr_time_pair_types(self):
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

    def test_081_ok_constr_time_pair_values(self):
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

    def test_081_ko_constr_time_pair_values(self):
        for num, denum in ((1, 1), (1, -1), (1000001, 1000000), (-1, 1000000)):
            with pytest.raises(ValueError):
                WesternTime.from_time_pair(Fraction(num, denum), None)
        for num, denum in ((-1000001, 1000000), (1000001, 1000000)):
            with pytest.raises(ValueError):
                WesternTime.from_time_pair(Fraction(3, 5), Fraction(num, denum))

    def test_200_write_attribute(self):
        for western in WesternTime(10, 10, 10), WesternTime(10, 10, 10, to_utc=10):
            with pytest.raises(AttributeError):
                western.hour = 3
            with pytest.raises(AttributeError):
                western.minute = 3
            with pytest.raises(AttributeError):
                western.second = 3
            with pytest.raises(AttributeError):
                western.to_utc = 3

    def test_300_ok_compare(self):
        western1 = WesternTime(2, 3, 4)
        western2 = WesternTime(2, 3, 4)
        assert western1 == western2
        assert western1 <= western2
        assert western1 >= western2
        assert not western1 != western2
        assert not western1 < western2
        assert not western1 > western2

        for hour, minute, second in (3, 3, 3), (2, 4, 4), (2, 3, 5):
            western3 = WesternTime(hour, minute, second)  # this is larger than western1
            assert western1 < western3
            assert western3 > western1
            assert western1 <= western3
            assert western3 >= western1
            assert western1 != western3
            assert western3 != western1
            assert not western1 == western3
            assert not western3 == western1
            assert not western1 > western3
            assert not western3 < western1
            assert not western1 >= western3
            assert not western3 <= western1

    def test_300_ko_compare(self):
        class SomeClass:
            pass

        western = WesternTime(2, 3, 4)

        # exception with non-numeric types
        for par in ("1", (1,), [1], {1: 1}, (), [], {}, None):
            assert not western == par
            assert western != par
            with pytest.raises(TypeError):
                western < par
            with pytest.raises(TypeError):
                western > par
            with pytest.raises(TypeError):
                western <= par
            with pytest.raises(TypeError):
                western >= par
        # exception with numeric types (all invalid) and other objects
        for par in (1, 1.0, Fraction(1, 1), Decimal(1), 1j, 1 + 1j, INF, NAN, SomeClass()):
            assert not western == par
            assert western != par
            with pytest.raises(TypeError):
                western < par
            with pytest.raises(TypeError):
                western > par
            with pytest.raises(TypeError):
                western <= par
            with pytest.raises(TypeError):
                western >= par

    def test_310_ok_compare_with_utc(self):
        western1 = WesternTime(2, 3, 4, to_utc=5)
        western2 = WesternTime(2, 3, 4, to_utc=-19)
        assert western1 == western2
        assert western1 <= western2
        assert western1 >= western2
        assert not western1 != western2
        assert not western1 < western2
        assert not western1 > western2

        for hour, minute, second, to_utc in (3, 3, 3, 5), (2, 4, 4, 5), (2, 3, 5, 5), (2, 3, 4, 6), (2, 3, 4, -18):
            western3 = WesternTime(hour, minute, second, to_utc=to_utc)  # this is larger than western1
            assert western1 < western3
            assert western3 > western1
            assert western1 <= western3
            assert western3 >= western1
            assert western1 != western3
            assert western3 != western1
            assert not western1 == western3
            assert not western3 == western1
            assert not western1 > western3
            assert not western3 < western1
            assert not western1 >= western3
            assert not western3 <= western1

    def test_320_hash_equality(self):
        western1 = WesternTime(11, 12, 13)
        # same thing
        western2 = WesternTime(11, 12, 13)
        assert hash(western1) == hash(western2)

        dic = {western1: 1}
        dic[western2] = 2
        assert len(dic) == 1
        assert dic[western1] == 2
        assert dic[western2] == 2

        western3 = WesternTime(1, 12, 13).replace(hour = 11)
        assert hash(western1) == hash(western3)

        dic[western3] = 2
        assert len(dic) == 1
        assert dic[western3] == 2

    def test_330_hash_equality_with_utc(self):
        western1 = WesternTime(10, 12, 13, to_utc=1)
        # same thing
        western2 = WesternTime(12, 12, 13, to_utc=-1)
        assert hash(western1) == hash(western2)

        dic = {western1: 1}
        dic[western2] = 2
        assert len(dic) == 1
        assert dic[western1] == 2
        assert dic[western2] == 2

        western3 = WesternTime(11, 12, 13, to_utc=3).replace(to_utc=0)
        assert hash(western1) == hash(western3)

        dic[western3] = 3
        assert len(dic) == 1
        assert dic[western1] == 3
        assert dic[western3] == 3

    def test_340_hash_equality_mix(self):
        western1 = WesternTime(11, 12, 13)
        # different thing
        western2 = WesternTime(9, 12, 13, to_utc=2)
        assert hash(western1) != hash(western2)

        western3 = western1.localize(0)
        assert hash(western2) == hash(western3)

        western4 = western2.delocalize(0)
        assert hash(western1) == hash(western4)

    def test_400_bool(self):
        for test_row in western_time_test_data:
            hour = test_row[1][0]
            minute = test_row[1][1]
            second = Fraction(test_row[1][2])
            assert WesternTime(hour, minute, second)

    def test_420_to_hours(self):
        for test_row in western_time_test_data:
            hour = test_row[1][0]
            minute = test_row[1][1]
            second = Fraction(test_row[1][2])
            to_hours = Fraction(test_row[2])
            assert WesternTime(hour, minute, second).to_hours() == to_hours

    def test_440_to_minutes(self):
        for test_row in western_time_test_data:
            hour = test_row[1][0]
            minute = test_row[1][1]
            second = Fraction(test_row[1][2])
            to_minutes = Fraction(test_row[3])
            assert WesternTime(hour, minute, second).to_minutes() == to_minutes

    def test_480_to_seconds(self):
        for test_row in western_time_test_data:
            hour = test_row[1][0]
            minute = test_row[1][1]
            second = Fraction(test_row[1][2])
            to_seconds = Fraction(test_row[4])
            assert WesternTime(hour, minute, second).to_seconds() == to_seconds

    def test_630_to_day_frac(self):
        for test_row in western_time_test_data:
            day_frac = Fraction(test_row[0])
            hour = test_row[1][0]
            minute = test_row[1][1]
            second = Fraction(test_row[1][2])
            assert WesternTime(hour, minute, second).to_day_frac() == day_frac

    def test_650_replace(self):
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

    def test_653_replace_invalid_types(self):
        western = WesternTime(11, 10, 9)
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
        # exception with invalid numeric types
        for par in (1.0, Fraction(1, 1), Decimal(1), 1j, 1 + 1j, INF, NAN):
            with pytest.raises(TypeError):
                western.replace(hour=par)
            with pytest.raises(TypeError):
                western.replace(minute=par)
        for par in (1j, 1 + 1j, INF):
            with pytest.raises(TypeError):
                western.replace(second=par)

    def test_656_replace_invalid_values(self):
        western1 = WesternTime(11, 10, 9)
        with pytest.raises(ValueError):
            western1.replace(hour=-1)
        with pytest.raises(ValueError):
            western1.replace(minute=-1)
        with pytest.raises(ValueError):
            western1.replace(second=-1)
        with pytest.raises(ValueError):
            western1.replace(hour=24)
        with pytest.raises(ValueError):
            western1.replace(minute=60)
        with pytest.raises(ValueError):
            western1.replace(second=60)
        with pytest.raises(TypeError):
            western1.replace(second=NAN)

    def test_700_repr(self):
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
            assert Fraction(eval(found_second)) == second

    def test_720_str(self):
        for test_row in western_time_test_data:
            hour = test_row[1][0]
            minute = test_row[1][1]
            second = Fraction(test_row[1][2])
            western = WesternTime(hour, minute, second)
            expected = '{:02d}:{:02d}:{:02d}'.format(hour, minute, floor(second))
            assert str(western) == expected

    def test_730_cformat_numbers(self):
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
            assert western.cformat('%S') == '{:02d}'.format(floor(second))

    def test_740_cformat_microseconds(self):
        for fraction, microseconds in western_time_microseconds:
            western = WesternTime.in_seconds(Fraction(fraction))
            assert western.cformat('%f') == microseconds

    def test_750_cformat_percent(self):
        western = WesternTime(1, 2, 3)
        assert western.cformat('%') == '%'
        assert western.cformat('%%') == '%'
        assert western.cformat('%%%') == '%%'
        assert western.cformat('abcd%') == 'abcd%'
        assert western.cformat('%k') == '%k'
        assert western.cformat('a%k') == 'a%k'
        assert western.cformat('%k%') == '%k%'

    def test_760_cformat_invalid_type(self):
        western = WesternTime(1, 2, 3)
        for par in (1, (1,), [1], {1: 1}, None):
            with pytest.raises(TypeError):
                western.cformat(par)

    def test_900_pickling(self):
        for test_row in western_time_test_data:
            hour = test_row[1][0]
            minute = test_row[1][1]
            second = Fraction(test_row[1][2])
            western = WesternTime(hour, minute, second)
            for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
                pickled = pickle.dumps(western, protocol)
                derived = pickle.loads(pickled)
                assert western == derived

    def test_920_subclass(self):

        class W(WesternTime):
            theAnswer = 42

            def __init__(self, *args, **kws):
                temp = kws.copy()
                self.extra = temp.pop('extra')
                WesternTime.__init__(self, *args, **temp)

            def newmeth(self, start):
                return start + self.hour + self.second

        western1 = WesternTime(11, 12, 13)
        western2 = W(11, 12, 13, extra=7)

        assert western2.theAnswer == 42
        assert western2.extra == 7
        assert western1.to_day_frac() == western2.to_day_frac()
        assert western2.newmeth(-7) == western1.hour + western1.second - 7

