# tests for Gregorian calendar

# Copyright (c) 2012 Francesco Ricciardi
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

from datetime2.western import GregorianCalendar


INF = float('inf')
NAN = float('nan')

gregorian_test_data = [
    # data from Calendrical Calculations: The Millennium Edition, with addition
    # RD      Weekday    Gregorian
    #                    Year Month  Day   Doy  WNS   WNM     WNS = Week Number starting on Sunday, WNM = Week Number starting on Munday
    [ -214193,      7, ( -586,    7,  24), 205, '30', '29'],
    [  -61387,      3, ( -168,   12,   5), 340, '49', '49'],
    [   25469,      3, (   70,    9,  24), 267, '38', '38'],
    [   49217,      7, (  135,   10,   2), 275, '40', '39'],
    [  171307,      3, (  470,    1,   8),   8, '01', '01'],
    [  210155,      1, (  576,    5,  20), 141, '20', '21'],
    [  253427,      6, (  694,   11,  10), 314, '44', '45'],
    [  369740,      7, ( 1013,    4,  25), 115, '17', '16'],
    [  400085,      7, ( 1096,    5,  24), 145, '21', '20'],
    [  434355,      5, ( 1190,    3,  23),  82, '11', '12'],
    [  452605,      6, ( 1240,    3,  10),  70, '10', '10'],
    [  470160,      5, ( 1288,    4,   2),  93, '13', '13'],
    [  473837,      7, ( 1298,    4,  27), 117, '17', '16'],
    [  507850,      7, ( 1391,    6,  12), 163, '24', '23'],
    [  524156,      3, ( 1436,    2,   3),  34, '05', '05'],
    [  544676,      6, ( 1492,    4,   9), 100, '14', '14'],
    [  567118,      6, ( 1553,    9,  19), 262, '37', '37'],
    [  569477,      6, ( 1560,    3,   5),  65, '09', '09'],
    [  601716,      3, ( 1648,    6,  10), 162, '23', '23'],
    [  613424,      7, ( 1680,    6,  30), 182, '26', '26'],
    [  626596,      5, ( 1716,    7,  24), 206, '29', '29'],
    [  645554,      7, ( 1768,    6,  19), 171, '25', '24'],
    [  664224,      1, ( 1819,    8,   2), 214, '31', '31'],
    [  671401,      3, ( 1839,    3,  27),  86, '12', '12'],
    [  694799,      7, ( 1903,    4,  19), 109, '16', '15'],
    [  704424,      7, ( 1929,    8,  25), 237, '34', '33'],
    [  708842,      1, ( 1941,    9,  29), 272, '39', '39'],
    [  709409,      1, ( 1943,    4,  19), 109, '16', '16'],
    [  709580,      4, ( 1943,   10,   7), 280, '40', '40'],
    [  727274,      2, ( 1992,    3,  17),  77, '11', '11'],
    [  728714,      7, ( 1996,    2,  25),  56, '08', '08'],
    [  744313,      3, ( 2038,   11,  10), 314, '45', '45'],
    [  764652,      7, ( 2094,    7,  18), 199, '29', '28'],
    # Boundary conditions on RD
    [-1000001,      5, (-2737,    2,   2),  33, '04', '05'],
    [-1000000,      6, (-2737,    2,   3),  34, '04', '05'],
    [ -999999,      7, (-2737,    2,   4),  35, '05', '05'],
    [ -100001,      1, ( -273,    3,  17),  76, '11', '11'],
    [ -100000,      2, ( -273,    3,  18),  77, '11', '11'],
    [  -99999,      3, ( -273,    3,  19),  78, '11', '11'],
    [  -10001,      2, (  -27,    8,  14), 226, '32', '33'],
    [  -10000,      3, (  -27,    8,  15), 227, '32', '33'],
    [   -9999,      4, (  -27,    8,  16), 228, '32', '33'],
    [   -1001,      7, (   -2,    4,   5),  95, '14', '13'],
    [   -1000,      1, (   -2,    4,   6),  96, '14', '14'],
    [    -999,      2, (   -2,    4,   7),  97, '14', '14'],
    [    -101,      4, (    0,    9,  21), 265, '38', '38'],
    [    -100,      5, (    0,    9,  22), 266, '38', '38'],
    [     -99,      6, (    0,    9,  23), 267, '38', '38'],
    [     -11,      3, (    0,   12,  20), 355, '51', '51'],
    [     -10,      4, (    0,   12,  21), 356, '51', '51'],
    [      -9,      5, (    0,   12,  22), 357, '51', '51'],
    [      -1,      6, (    0,   12,  30), 365, '52', '52'],
    [       0,      7, (    0,   12,  31), 366, '53', '52'],
    [       1,      1, (    1,    1,   1),   1, '00', '01'],
    [       9,      2, (    1,    1,   9),   9, '01', '02'],
    [      10,      3, (    1,    1,  10),  10, '01', '02'],
    [      11,      4, (    1,    1,  11),  11, '01', '02'],
    [      99,      1, (    1,    4,   9),  99, '14', '15'],
    [     100,      2, (    1,    4,  10), 100, '14', '15'],
    [     101,      3, (    1,    4,  11), 101, '14', '15'],
    [     999,      5, (    3,    9,  26), 269, '38', '38'],
    [    1000,      6, (    3,    9,  27), 270, '38', '38'],
    [    1001,      7, (    3,    9,  28), 271, '39', '38'],
    [    9999,      3, (   28,    5,  17), 138, '20', '20'],
    [   10000,      4, (   28,    5,  18), 139, '20', '20'],
    [   10001,      5, (   28,    5,  19), 140, '20', '20'],
    [   99999,      4, (  274,   10,  15), 288, '41', '41'],
    [  100000,      5, (  274,   10,  16), 289, '41', '41'],
    [  100001,      6, (  274,   10,  17), 290, '41', '41'],
    [  999999,      7, ( 2738,   11,  27), 331, '48', '47'],
    [ 1000000,      1, ( 2738,   11,  28), 332, '48', '48'],
    [ 1000001,      2, ( 2738,   11,  29), 333, '48', '48'],
    # A few leap days
    [ -146404,      1, ( -400,    2,  28),  59, '09', '09'],
    [ -146403,      2, ( -400,    2,  29),  60, '09', '09'],
    [ -146402,      3, ( -400,    3,   1),  61, '09', '09'],
    [  -73355,      5, ( -200,    2,  28),  59, '08', '08'],
    [  -73354,      6, ( -200,    3,   1),  60, '08', '08'],
    [    -307,      1, (    0,    2,  28),  59, '09', '09'],
    [    -306,      2, (    0,    2,  29),  60, '09', '09'],
    [    -305,      3, (    0,    3,   1),  61, '09', '09'],
    [      59,      3, (    1,    2,  28),  59, '08', '09'],
    [      60,      4, (    1,    3,   1),  60, '08', '09'],
    [   72742,      5, (  200,    2,  28),  59, '08', '08'],
    [   72743,      6, (  200,    3,   1),  60, '08', '08'],
    [  145790,      1, (  400,    2,  28),  59, '09', '09'],
    [  145791,      2, (  400,    2,  29),  60, '09', '09'],
    [  145792,      3, (  400,    3,   1),  61, '09', '09'],
    [  730178,      1, ( 2000,    2,  28),  59, '09', '09'],
    [  730179,      2, ( 2000,    2,  29),  60, '09', '09'],
    [  730180,      3, ( 2000,    3,   1),  61, '09', '09'],
    [  766703,      7, ( 2100,    2,  28),  59, '09', '08'],
    [  766704,      1, ( 2100,    3,   1),  60, '09', '09'],
    # Boundary conditions on years
    [-3652425,      7, (-10000,  12,  31), 366, '53', '52'],
    [-3652424,      1, (-9999,    1,   1),   1, '00', '01'],
    [ -730485,      7, (-2000,   12,  31), 366, '53', '52'],
    [ -730484,      1, (-1999,    1,   1),   1, '00', '01'],
    [ -365243,      3, (-1000,   12,  31), 365, '52', '52'],
    [ -365242,      4, ( -999,    1,   1),   1, '00', '00'],
    [  -36525,      1, ( -100,   12,  31), 365, '52', '53'],
    [  -36524,      2, (  -99,    1,   1),   1, '00', '00'],
    [   -3653,      1, (  -10,   12,  31), 365, '52', '53'],
    [   -3652,      2, (   -9,    1,   1),   1, '00', '00'],
    [    -366,      5, (   -1,   12,  31), 365, '52', '52'],
    [    -365,      6, (    0,    1,   1),   1, '00', '00'],
    [     365,      1, (    1,   12,  31), 365, '52', '53'],
    [     366,      2, (    2,    1,   1),   1, '00', '00'],
    [    3287,      4, (    9,   12,  31), 365, '52', '52'],
    [    3288,      5, (   10,    1,   1),   1, '00', '00'],
    [   36159,      4, (   99,   12,  31), 365, '52', '52'],
    [   36160,      5, (  100,    1,   1),   1, '00', '00'],
    [  364877,      2, (  999,   12,  31), 365, '52', '52'],
    [  364878,      3, ( 1000,    1,   1),   1, '00', '00'],
    [  730119,      5, ( 1999,   12,  31), 365, '52', '52'],
    [  730120,      6, ( 2000,    1,   1),   1, '00', '00'],
    [ 3652059,      5, ( 9999,   12,  31), 365, '52', '52'],
    [ 3652060,      6, (10000,    1,   1),   1, '00', '00'],
    # Boundary conditions on cformat's %U and %W
    # year starts and ends on Sunday
    [  732312,      7, ( 2006,    1,   1),   1, '01', '00'],
    [  732313,      1, ( 2006,    1,   2),   2, '01', '01'],
    [  732318,      6, ( 2006,    1,   7),   7, '01', '01'],
    [  732319,      7, ( 2006,    1,   8),   8, '02', '01'],
    [  732669,      7, ( 2006,   12,  24), 358, '52', '51'],
    [  732670,      1, ( 2006,   12,  25), 359, '52', '52'],
    [  732675,      6, ( 2006,   12,  30), 364, '52', '52'],
    [  732676,      7, ( 2006,   12,  31), 365, '53', '52'],
    # year starts and ends on Monday
    [  730486,      1, ( 2001,    1,   1),   1, '00', '01'],
    [  730492,      7, ( 2001,    1,   7),   7, '01', '01'],
    [  730493,      1, ( 2001,    1,   8),   8, '01', '02'],
    [  730499,      7, ( 2001,    1,  14),  14, '02', '02'],
    [  730842,      7, ( 2001,   12,  23), 357, '51', '51'],
    [  730843,      1, ( 2001,   12,  24), 358, '51', '52'],
    [  730849,      7, ( 2001,   12,  30), 364, '52', '52'],
    [  730850,      1, ( 2001,   12,  31), 365, '52', '53'],
    # leap year starts on Sunday and ends on Monday
    [  724276,      7, ( 1984,    1,   1),   1, '01', '00'],
    [  724277,      1, ( 1984,    1,   2),   2, '01', '01'],
    [  724283,      7, ( 1984,    1,   8),   8, '02', '01'],
    [  724284,      1, ( 1984,    1,   9),   9, '02', '02'],
    [  724639,      6, ( 1984,   12,  29), 364, '52', '52'],
    [  724640,      7, ( 1984,   12,  30), 365, '53', '52'],
    [  724641,      1, ( 1984,   12,  31), 366, '53', '53']
]

gregorian_invalid_data = [
    # zero or negative day or month
    ( 111,  0,  1),
    ( 111,  1,  0),
    ( 111, -1,  1),
    ( 111,  1, -1),
    # day greater than days in month
    ( 111,  1, 32),
    ( 111,  2, 29),  # non-leap year
    ( 100,  2, 29),  # non-leap year
    ( 104,  2, 30),  # leap year
    ( 111,  3, 32),
    ( 111,  4, 31),
    ( 111,  5, 32),
    ( 111,  6, 31),
    ( 111,  7, 32),
    ( 111,  8, 32),
    ( 111,  9, 31),
    ( 111, 10, 32),
    ( 111, 11, 31),
    ( 111, 12, 32),
    # invalid month
    ( 111, 13,  1)
]


class TestGregorian():
    def test_000_constructor(self):
        for test_row in gregorian_test_data:
            year = test_row[2][0]
            month = test_row[2][1]
            day = test_row[2][2]
            greg = GregorianCalendar(year, month, day)
            assert (greg.year, greg.month, greg.day) == (year, month, day)

    def test_003_constructor_year_day(self):
        for test_row in gregorian_test_data:
            year = test_row[2][0]
            month = test_row[2][1]
            day = test_row[2][2]
            doy = test_row[3]
            greg_yd = GregorianCalendar.year_day(year, doy)
            assert (greg_yd.year, greg_yd.month, greg_yd.day) == (year, month, day)

    def test_006_constructor_rata_die(self):
        for test_row in gregorian_test_data:
            rd = test_row[0]
            year = test_row[2][0]
            month = test_row[2][1]
            day = test_row[2][2]
            greg_rd = GregorianCalendar.from_rata_die(rd)
            assert (greg_rd.year, greg_rd.month, greg_rd.day) == (year, month, day)

    def test_010_invalid_parameter_types(self):
        # exception with none, two or four parameters
        with pytest.raises(TypeError):
            GregorianCalendar()
        with pytest.raises(TypeError):
            GregorianCalendar(1, 2)
        with pytest.raises(TypeError):
            GregorianCalendar(1, 2, 3, 4)
        # exception with non-numeric types
        for par in ("1", (1,), [1], {1: 1}, (), [], {}, None):
            with pytest.raises(TypeError):
                GregorianCalendar(par, 1, 1)
            with pytest.raises(TypeError):
                GregorianCalendar(1, par, 1)
            with pytest.raises(TypeError):
                GregorianCalendar(1, 1, par)
        # exception with invalid numeric types
        for par in (1.0, Fraction(1, 1), Decimal(1), 1j, 1 + 1j, INF, NAN):
            with pytest.raises(TypeError):
                GregorianCalendar(par, 1, 1)
            with pytest.raises(TypeError):
                GregorianCalendar(1, par, 1)
            with pytest.raises(TypeError):
                GregorianCalendar(1, 1, par)

    def test_013_invalid_parameter_types_year_day(self):
        # exception with none, two or four parameters
        with pytest.raises(TypeError):
            GregorianCalendar.year_day()
        with pytest.raises(TypeError):
            GregorianCalendar.year_day(1)
        with pytest.raises(TypeError):
            GregorianCalendar.year_day(1, 2, 3)
        for par in ("1", (1,), [1], {1: 1}, (), [], {}, None):
            with pytest.raises(TypeError):
                GregorianCalendar.year_day(par, 1)
            with pytest.raises(TypeError):
                GregorianCalendar.year_day(1, par)
        # exception with invalid numeric types
        for par in (1.0, Fraction(1, 1), Decimal(1), 1j, 1 + 1j, INF, NAN):
            with pytest.raises(TypeError):
                GregorianCalendar.year_day(par, 1)
            with pytest.raises(TypeError):
                GregorianCalendar.year_day(1, par)

    def test_016_invalid_parameter_types_rata_die(self):
        # exception with none, two or four parameters
        with pytest.raises(TypeError):
            GregorianCalendar.from_rata_die()
        with pytest.raises(TypeError):
            GregorianCalendar.from_rata_die(1, 2)
        # exception with non-numeric types
        for par in ("1", (1,), [1], {1: 1}, (), [], {}, None):
            with pytest.raises(TypeError):
                GregorianCalendar.from_rata_die(par)
        # exception with invalid numeric types
        for par in (1.0, Fraction(1, 1), Decimal(1), 1j, 1 + 1j, INF, NAN):
            with pytest.raises(TypeError):
                GregorianCalendar.from_rata_die(par)

    def test_020_invalid_values(self):
        for test_row in gregorian_invalid_data:
            year = test_row[0]
            month = test_row[1]
            day = test_row[2]
            with pytest.raises(ValueError):
                GregorianCalendar(year, month, day)

    def test_023_invalid_values_year_day(self):
        for year, day_count in ((1, 0), (1, -1), (1, 366), (4, 367)):
            with pytest.raises(ValueError):
                GregorianCalendar.year_day(year, day_count)

    def test_100_write_attribute(self):
        greg = GregorianCalendar(1, 1, 1)
        with pytest.raises(AttributeError):
            greg.year = 3
        with pytest.raises(AttributeError):
            greg.month = 3
        with pytest.raises(AttributeError):
            greg.day = 3

    def test_200_leap_years(self):
        # leap years
        for year in (-10000, -2000, -1996, -804, -800, -104, -4, 0,
                     10000, 2000, 1996, 804, 800, 104, 4):
            assert GregorianCalendar.is_leap_year(year)
            assert GregorianCalendar.days_in_year(year) == 366
        # non-leap years
        for year in (-2001, -1900, -1000, -999, -100, -99, -10, -1,
                     2001, 1900, 1000, 999, 100, 99, 10, 1):
            assert not GregorianCalendar.is_leap_year(year)
            assert GregorianCalendar.days_in_year(year) == 365

    def test_300_compare(self):
        greg1 = GregorianCalendar(2, 3, 4)
        greg2 = GregorianCalendar(2, 3, 4)
        assert greg1 == greg2
        assert greg1 <= greg2
        assert greg1 >= greg2
        assert not greg1 != greg2
        assert not greg1 < greg2
        assert not greg1 > greg2

        for year, month, day in (3, 3, 3), (2, 4, 4), (2, 3, 5):
            greg3 = GregorianCalendar(year, month, day)  # this is larger than greg1
            assert greg1 < greg3
            assert greg3 > greg1
            assert greg1 <= greg3
            assert greg3 >= greg1
            assert greg1 != greg3
            assert greg3 != greg1
            assert not greg1 == greg3
            assert not greg3 == greg1
            assert not greg1 > greg3
            assert not greg3 < greg1
            assert not greg1 >= greg3
            assert not greg3 <= greg1

    def test_310_compare_invalid_types(self):
        class SomeClass:
            pass

        greg = GregorianCalendar(2, 3, 4)

        # exception with non-numeric types
        for par in ("1", (1,), [1], {1: 1}, (), [], {}, None):
            assert not greg == par
            assert greg != par
            with pytest.raises(TypeError):
                greg < par
            with pytest.raises(TypeError):
                greg > par
            with pytest.raises(TypeError):
                greg <= par
            with pytest.raises(TypeError):
                greg >= par
        # exception with numeric types (all invalid) and other objects
        for par in (1, 1.0, Fraction(1, 1), Decimal(1), 1j, 1 + 1j, INF, NAN, SomeClass()):
            assert not greg == par
            assert greg != par
            with pytest.raises(TypeError):
                greg < par
            with pytest.raises(TypeError):
                greg > par
            with pytest.raises(TypeError):
                greg <= par
            with pytest.raises(TypeError):
                greg >= par

    def test_320_hash_equality(self):
        greg1 = GregorianCalendar(2000, 12, 31)
        # same thing
        greg2 = GregorianCalendar(2000, 12, 31)
        assert hash(greg1) == hash(greg2)

        dic = {greg1: 1}
        dic[greg2] = 2
        assert len(dic) == 1
        assert dic[greg1] == 2
        assert dic[greg2] == 2

    def test_330_bool(self):
        for test_row in gregorian_test_data:
            year = test_row[2][0]
            month = test_row[2][1]
            day = test_row[2][2]
            assert GregorianCalendar(year, month, day)

    def test_400_to_rata_die(self):
        for test_row in gregorian_test_data:
            year = test_row[2][0]
            month = test_row[2][1]
            day = test_row[2][2]
            rd = test_row[0]
            assert GregorianCalendar(year, month, day).to_rata_die() == rd

    def test_410_weekday(self):
        for test_row in gregorian_test_data:
            year = test_row[2][0]
            month = test_row[2][1]
            day = test_row[2][2]
            weekday = test_row[1]
            assert GregorianCalendar(year, month, day).weekday() == weekday

    def test_420_day_of_year(self):
        for test_row in gregorian_test_data:
            year = test_row[2][0]
            month = test_row[2][1]
            day = test_row[2][2]
            doy = test_row[3]
            assert GregorianCalendar(year, month, day).day_of_year() == doy

    def test_430_replace(self):
        for test_row in gregorian_test_data[:33]:   # take Calendrical Calculations tests data only (other may make replace fail, as in the next tests method)
            year = test_row[2][0]
            month = test_row[2][1]
            day = test_row[2][2]
            greg = GregorianCalendar(year, month, day)
            assert greg.replace() == GregorianCalendar(year, month, day)
            assert greg.replace(year=11) == GregorianCalendar(11, month, day)
            assert greg.replace(month=10) == GregorianCalendar(year, 10, day)
            assert greg.replace(day=9) == GregorianCalendar(year, month, 9)
            assert greg.replace(month=10, year=11) == GregorianCalendar(11, 10, day)
            assert greg.replace(day=9, year=11) == GregorianCalendar(11, month, 9)
            assert greg.replace(day=9, month=10) == GregorianCalendar(year, 10, 9)
            assert greg.replace(day=9, month=10, year=11) == GregorianCalendar(11, 10, 9)

    def test_433_replace_invalid_types(self):
        greg = GregorianCalendar(11, 10, 9)
        # exception for positional parameters
        with pytest.raises(TypeError):
            greg.replace(1)
        # exception with non-numeric types
        for par in ("1", (1,), [1], {1: 1}, (), [], {}):
            with pytest.raises(TypeError):
                greg.replace(year=par)
            with pytest.raises(TypeError):
                greg.replace(month=par)
            with pytest.raises(TypeError):
                greg.replace(day=par)
        # exception with invalid numeric types
        for par in (1.0, Fraction(1, 1), Decimal(1), 1j, 1 + 1j, INF, NAN):
            with pytest.raises(TypeError):
                greg.replace(year=par)
            with pytest.raises(TypeError):
                greg.replace(month=par)
            with pytest.raises(TypeError):
                greg.replace(day=par)

    def test_436_replace_invalid_values(self):
        greg1 = GregorianCalendar(11, 10, 9)
        with pytest.raises(ValueError):
            greg1.replace(month=0)
        with pytest.raises(ValueError):
            greg1.replace(day=0)
        with pytest.raises(ValueError):
            greg1.replace(month=-1)
        with pytest.raises(ValueError):
            greg1.replace(day=-1)
        with pytest.raises(ValueError):
            greg1.replace(month=13)
        with pytest.raises(ValueError):
            greg1.replace(day=32)
        for month in (4, 6, 9, 11):
            greg2 = GregorianCalendar(11, month, 9)
            with pytest.raises(ValueError):
                greg2.replace(day=31)
            greg3 = GregorianCalendar(11, 10, 31)
            with pytest.raises(ValueError):
                greg3.replace(month=month)
        for day in (29, 30, 31):
            greg4 = GregorianCalendar(11, 3, day)
            with pytest.raises(ValueError):
                greg4.replace(month=2)
            greg5 = GregorianCalendar(11, 2, 4)
            with pytest.raises(ValueError):
                greg5.replace(day=day)
        for day in (30, 31):
            greg6 = GregorianCalendar(4, 3, day)  # leap year
            with pytest.raises(ValueError):
                greg6.replace(month=2)
            greg7 = GregorianCalendar(4, 2, 4)
            with pytest.raises(ValueError):
                greg7.replace(day=day)

    def test_500_repr(self):
        import datetime2
        for test_row in gregorian_test_data:
            year = test_row[2][0]
            month = test_row[2][1]
            day = test_row[2][2]
            greg = GregorianCalendar(year, month, day)
            greg_repr = repr(greg)
            names, args = greg_repr.split('(')
            assert names.split('.') == ['datetime2', 'western', 'GregorianCalendar']
            args = args[:-1]  # drop ')'
            for found, expected in zip(args.split(','), (year, month, day)):
                assert int(found) == expected
            assert greg == eval(greg_repr)

    def test_520_str(self):
        for test_row in gregorian_test_data:
            year = test_row[2][0]
            month = test_row[2][1]
            day = test_row[2][2]
            greg = GregorianCalendar(year, month, day)
            if year < 0:
                expected = '-'
                year = -year
            else:
                expected = ''
            ys = str(year)
            if len(ys) < 4:
                expected += ('000' + ys)[-4:]
            else:
                expected += ys
            expected += '-' + ('0' + str(month))[-2:]
            expected += '-' + ('0' + str(day))[-2:]
            assert str(greg) == expected

    def test_530_cformat_numbers(self):
        for test_row in gregorian_test_data:
            wday = test_row[1]
            year = test_row[2][0]
            month = test_row[2][1]
            day = test_row[2][2]
            doy = test_row[3]
            greg = GregorianCalendar(year, month, day)
            assert greg.cformat('%d') == '{:02d}'.format(day)
            assert greg.cformat('%j') == '{:03d}'.format(doy)
            assert greg.cformat('%m') == '{:02d}'.format(month)
            assert greg.cformat('%w') == '{:d}'.format(wday)
            if year >= 0:
                assert greg.cformat('%y') == ('0' + str(year))[-2:]
                assert greg.cformat('%Y') == '{:04d}'.format(year)
            else:
                assert greg.cformat('%y') == ('0' + str(-year))[-2:]
                assert greg.cformat('%Y') == '-{:04d}'.format(-year)

    def test_540_cformat_names(self):
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        abbr_weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
        abbr_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        for test_row in gregorian_test_data:
            wday = test_row[1]
            year = test_row[2][0]
            month = test_row[2][1]
            day = test_row[2][2]
            greg = GregorianCalendar(year, month, day)
            assert greg.cformat('%a') == abbr_weekdays[wday - 1]
            assert greg.cformat('%A') == weekdays[wday - 1]
            assert greg.cformat('%b') == abbr_months[month - 1]
            assert greg.cformat('%B') == months[month - 1]

    def test_550_cformat_week_number(self):
        for test_row in gregorian_test_data:
            year = test_row[2][0]
            month = test_row[2][1]
            day = test_row[2][2]
            WNS = test_row[4]
            WNM = test_row[5]
            greg = GregorianCalendar(year, month, day)
            assert greg.cformat('%U')== WNS
            assert greg.cformat('%W') == WNM

    def test_560_cformat_percent(self):
        greg = GregorianCalendar(1, 2, 3)
        assert greg.cformat('%') == '%'
        assert greg.cformat('%%') == '%'
        assert greg.cformat('%%%') == '%%'
        assert greg.cformat('abcd%') == 'abcd%'
        assert greg.cformat('%k') == '%k'
        assert greg.cformat('a%k') == 'a%k'
        assert greg.cformat('%k%') == '%k%'

    def test_570_cformat_invalid_type(self):
        greg = GregorianCalendar(1, 2, 3)
        for par in (1, (1,), [1], {1: 1}, None):
            with pytest.raises(TypeError):
                greg.cformat(par)

    def test_900_pickling(self):
        for test_row in gregorian_test_data:
            year = test_row[2][0]
            month = test_row[2][1]
            day = test_row[2][2]
            greg = GregorianCalendar(year, month, day)
            for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
                pickled = pickle.dumps(greg, protocol)
                derived = pickle.loads(pickled)
                assert greg == derived

    def test_920_subclass(self):

        class G(GregorianCalendar):
            theAnswer = 42

            def __init__(self, *args, **kws):
                temp = kws.copy()
                self.extra = temp.pop('extra')
                GregorianCalendar.__init__(self, *args, **temp)

            def newmeth(self, start):
                return start + self.year + self.month

        greg1 = GregorianCalendar(2003, 4, 14)
        greg2 = G(2003, 4, 14, extra=7)

        assert greg2.theAnswer == 42
        assert greg2.extra == 7
        assert greg1.to_rata_die() == greg2.to_rata_die()
        assert greg2.newmeth(-7) == greg1.year + greg1.month - 7

