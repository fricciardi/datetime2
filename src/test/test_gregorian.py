# datetime2 package test
# Gregorian calendar

# Copyright (c) 2011 Francesco Ricciardi
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
import unittest

from datetime2 import Date, TimeDelta



gregorian_test_data = [
    # data from Calendrical Calculations: The Millennium Edition, with addition
    #     RD Weekday               Gregorian
    #                  Year  Month  Day   Doy
    [ -214193,      0, (-586,     7,  24), 205],
    [  -61387,      3, (-168,    12,   5), 340],
    [   25469,      3, (  70,     9,  24), 267],
    [   49217,      0, ( 135,    10,   2), 275],
    [  171307,      3, ( 470,     1,   8),   8],
    [  210155,      1, ( 576,     5,  20), 141],
    [  253427,      6, ( 694,    11,  10), 314],
    [  369740,      0, (1013,     4,  25), 115],
    [  400085,      0, (1096,     5,  24), 145],
    [  434355,      5, (1190,     3,  23),  82],
    [  452605,      6, (1240,     3,  10),  70],
    [  470160,      5, (1288,     4,   2),  93],
    [  473837,      0, (1298,     4,  27), 117],
    [  507850,      0, (1391,     6,  12), 163],
    [  524156,      3, (1436,     2,   3),  34],
    [  544676,      6, (1492,     4,   9), 100],
    [  567118,      6, (1553,     9,  19), 262],
    [  569477,      6, (1560,     3,   5),  65],
    [  601716,      3, (1648,     6,  10), 162],
    [  613424,      0, (1680,     6,  30), 182],
    [  626596,      5, (1716,     7,  24), 206],
    [  645554,      0, (1768,     6,  19), 171],
    [  664224,      1, (1819,     8,   2), 214],
    [  671401,      3, (1839,     3,  27),  86],
    [  694799,      0, (1903,     4,  19), 109],
    [  704424,      0, (1929,     8,  25), 237],
    [  708842,      1, (1941,     9,  29), 272],
    [  709409,      1, (1943,     4,  19), 109],
    [  709580,      4, (1943,    10,   7), 280],
    [  727274,      2, (1992,     3,  17),  77],
    [  728714,      0, (1996,     2,  25),  56],
    [  744313,      3, (2038,    11,  10), 314],
    [  764652,      0, (2094,     7,  18), 199],
    # Boundary conditions on RD
    [-1000001,      5, (-2737,    2,   2),  33],
    [-1000000,      6, (-2737,    2,   3),  34],
    [ -999999,      7, (-2737,    2,   4),  35],
    [ -100001,      1, (-273,     3,  17),  76],
    [ -100000,      2, (-273,     3,  18),  77],
    [  -99999,      3, (-273,     3,  19),  78],
    [  -10001,      2, ( -27,     8,  14), 226],
    [  -10000,      3, ( -27,     8,  15), 227],
    [   -9999,      4, ( -27,     8,  16), 228],
    [   -1001,      0, (  -2,     4,   5),  95],
    [   -1000,      1, (  -2,     4,   6),  96],
    [    -999,      2, (  -2,     4,   7),  97],
    [    -101,      4, (   0,     9,  21), 265],
    [    -100,      5, (   0,     9,  22), 266],
    [     -99,      6, (   0,     9,  23), 267],
    [     -11,      3, (   0,    12,  20), 355],
    [     -10,      4, (   0,    12,  21), 356],
    [      -9,      5, (   0,    12,  22), 357],
    [      -1,      6, (   0,    12,  30), 365],
    [       0,      0, (   0,    12,  31), 366],
    [       1,      1, (   1,     1,   1),   1],
    [       9,      2, (   1,     1,   9),   9],
    [      10,      3, (   1,     1,  10),  10],
    [      11,      4, (   1,     1,  11),  11],
    [      99,      1, (   1,     4,   9),  99],
    [     100,      2, (   1,     4,  10), 100],
    [     101,      3, (   1,     4,  11), 101],
    [     999,      5, (   3,     9,  26), 269],
    [    1000,      6, (   3,     9,  27), 270],
    [    1001,      7, (   3,     9,  28), 271],
    [    9999,      3, (  28,     5,  17), 138],
    [   10000,      4, (  28,     5,  18), 139],
    [   10001,      5, (  28,     5,  19), 140],
    [   99999,      4, ( 274,    10,  15), 288],
    [  100000,      5, ( 274,    10,  16), 289],
    [  100001,      6, ( 274,    10,  17), 290],
    [  999999,      0, (2738,    11,  27), 331],
    [ 1000000,      1, (2738,    11,  28), 332],
    [ 1000001,      2, (2738,    11,  29), 333],
    # A few leap days
    [ -146404,      1, (-400,     2,  28),  59],
    [ -146403,      2, (-400,     2,  29),  60],
    [ -146402,      3, (-400,     3,   1),  61],
    [  -73355,      5, (-200,     2,  28),  59],
    [  -73354,      6, (-200,     3,   1),  60],
    [    -307,      1, (   0,     2,  28),  59],
    [    -306,      2, (   0,     2,  29),  60],
    [    -305,      3, (   0,     3,   1),  61],
    [      59,      1, (   1,     2,  28),  59],
    [      60,      2, (   1,     3,   1),  60],
    [   72742,      5, ( 200,     2,  28),  59],
    [   72743,      6, ( 200,     3,   1),  60],
    [  145790,      1, ( 400,     2,  28),  59],
    [  145791,      2, ( 400,     2,  29),  60],
    [  145792,      3, ( 400,     3,   1),  61],
    [  730178,      1, (2000,     2,  28),  59],
    [  730179,      2, (2000,     2,  29),  60],
    [  730180,      3, (2000,     3,   1),  61],
    [  766703,      0, (2100,     2,  28),  59],
    [  766704,      1, (2100,     3,   1),  60],
    # Boundary conditions on years
    [-3652425,      0, (-10000,  12,  31), 366],
    [-3652424,      0, (-9999,    1,   1),   1],
    [ -730485,      0, (-2000,   12,  31), 366],
    [ -730484,      1, (-1999,    1,   1),   1],
    [ -365243,      3, (-1000,   12,  31), 365],
    [ -365242,      4, (-999,     1,   1),   1],
    [  -36525,      3, (-100,    12,  31), 365],
    [  -36524,      4, ( -99,     1,   1),   1],
    [   -3653,      1, ( -10,    12,  31), 365],
    [   -3652,      2, (  -9,     1,   1),   1],
    [    -366,      5, (  -1,    12,  31), 365],
    [    -365,      6, (   0,     1,   1),   1],
    [     365,      0, (   1,    12,  31), 365],
    [     366,      1, (   2,     1,   1),   1],
    [    3287,      4, (   9,    12,  31), 365],
    [    3288,      5, (  10,     1,   1),   1],
    [   36159,      4, (  99,    12,  31), 365],
    [   36160,      5, ( 100,     1,   1),   1],
    [  364877,      4, ( 999,    12,  31), 365],
    [  364878,      5, (1000,     1,   1),   1],
    [  730119,      5, (1999,    12,  31), 365],
    [  730120,      6, (2000,     1,   1),   1],
    [ 3652059,      5, (9999,    12,  31), 365],
    [ 3652060,      5, (10000,    1,   1),   1]
]

gregorian_invalid_data = [
    # zero ore negative day or month
    (   1,  0,  1),
    (   1,  1,  0),
    (   1, -1,  1),
    (   1,  1, -1),
    # day greater than days in month
    (   1,  1,  32),
    (   1,  2,  29),  # non-leap year
    ( 100,  2,  29),  # non-leap year
    (   4,  2,  30),  # leap year
    (   1,  3,  32),
    (   1,  4,  31),
    (   1,  5,  32),
    (   1,  6,  31),
    (   1,  7,  32),
    (   1,  8,  32),
    (   1,  9,  31),
    (   1, 10,  32),
    (   1, 11,  31),
    (   1, 12,  32)
]

class TestDateGregorian(unittest.TestCase):

    def test_000_constructors(self):
        for test_row in gregorian_test_data:
            rd = test_row[0]
            year = test_row[2][0]
            month = test_row[2][1]
            day = test_row[2][2]
            doy = test_row[3]
            self.assertEqual(Date.gregorian(year, month, day), Date(rd), msg = 'gregorian with rd = {}'.format(rd))
            self.assertEqual(Date.gregorian.year_day(year, doy), Date(rd), msg = 'gregorian.year_day with rd = {}'.format(rd))

    def test_010_invalid_parameter_types(self):
        # exception with none, two or four parameters
        self.assertRaises(TypeError, Date.gregorian)
        self.assertRaises(TypeError, Date.gregorian, 1, 2)
        self.assertRaises(TypeError, Date.gregorian, 1, 2, 1, 2)
        # exception with non-numeric types
        for par in ("1", (1,), [1], {1:1}, (), [], {}, None):
            self.assertRaises(TypeError, Date.gregorian, par, 1, 1)
            self.assertRaises(TypeError, Date.gregorian, 1, par, 1)
            self.assertRaises(TypeError, Date.gregorian, 1, 1, par)
            # exception with invalid numeric types
        for par in (1.0, fractions.Fraction(1, 1), decimal.Decimal(1), 1j):
            self.assertRaises(TypeError, Date.gregorian, par, 1, 1)
            self.assertRaises(TypeError, Date.gregorian, 1, par, 1)
            self.assertRaises(TypeError, Date.gregorian, 1, 1, par)

    def test_015_invalid_parameter_types_year_day(self):
        # exception with none, one or three parameters
        self.assertRaises(TypeError, Date.gregorian.year_day)
        self.assertRaises(TypeError, Date.gregorian.year_day, 1)
        self.assertRaises(TypeError, Date.gregorian.year_day, 1, 2, 3)
        # exception with non-numeric types
        for par in ("1", (1,), [1], {1:1}, (), [], {}, None):
            self.assertRaises(TypeError, Date.gregorian.year_day, par)
            # exception with invalid numeric types
        for par in (1.0, fractions.Fraction(1, 1), decimal.Decimal(1), 1j):
            self.assertRaises(TypeError, Date.gregorian.year_day, par)

    def test_020_invalid_values(self):
        for test_row in gregorian_invalid_data:
            year = test_row[0]
            month = test_row[1]
            day = test_row[2]
            print(year,month,day)
            self.assertRaises(ValueError, Date.gregorian, year, month, day)

    def test_025_invalid_values_year_day(self):
        for year, day_count in ((1, 0), (1, -1), (1, 366), (4, 367)):
            self.assertRaises(ValueError, Date.gregorian.year_day, year, day_count)

    def test_030_attributes(self):
        for test_row in gregorian_test_data:
            rd = test_row[0]
            year = test_row[2][0]
            month = test_row[2][1]
            day = test_row[2][2]
            d = Date(rd)
            self.assertEqual(d.gregorian.year, year, msg = 'gregorian year, rd = {}'.format(rd))
            self.assertEqual(d.gregorian.month, month, msg = 'gregorian month, rd = {}'.format(rd))
            self.assertEqual(d.gregorian.day, day, msg = 'gregorian day, rd = {}'.format(rd))

    @unittest.skip("not supported")
    def test_040_write_attribute(self):
        d = Date(1)
        self.assertRaises(AttributeError, setattr, d.gregorian, 'year', 3)
        self.assertRaises(AttributeError, setattr, d.gregorian, 'month', 3)
        self.assertRaises(AttributeError, setattr, d.gregorian, 'day', 3)

    @unittest.skip("not supported")
    def test_050_get_unknown_attribute(self):
        self.assertRaises(AttributeError, getattr, Date.gregorian, 'unknown')
        d = Date(1)
        self.assertRaises(AttributeError, getattr, d.gregorian, 'unknown')

    @unittest.skip("not supported")
    def test_100_leap_years(self):
        # leap years
        for year in (-10000, -2000, -1996, -804, -800, -104, -4, 0,
                     10000,  2000,  1996,  804,  800,  100,  4):
            self.assertTrue(Date.gregorian.is_leap_year(year), msg = 'is_leap_year, year = {}'.format(year))
            self.assertEqual(Date.gregorian.days_in_year(year), 366, msg = 'days_in_year, year = {}'.format(year))
            # non-leap years
        for year in (-2001, -1900, -1000, -999, -100, -99, -10, -1, 0,
                     2001,  1900,  1000,  999,  100,  99,  10,  1):
            self.assertFalse(Date.gregorian.is_leap_year(year), msg = 'is_leap_year, year = {}'.format(year))
            self.assertEqual(Date.gregorian.days_in_year(year), 365, msg = 'days_in_year, year = {}'.format(year))

    @unittest.skip("not supported")
    def test_110_weekday(self):
        for test_row in gregorian_test_data:
            rd = test_row[0]
            weekday = test_row[1]
            self.assertEqual(Date(rd).gregorian.weekday(), weekday, msg = 'weekday, RD = {}'.format(rd))

    @unittest.skip("not supported")
    def test_120_day_of_year(self):
        for test_row in gregorian_test_data:
            rd = test_row[0]
            doy = test_row[3]
            self.assertEqual(Date(rd).gregorian.day_of_year(), doy, msg = 'day_of_year, RD = {}'.format(rd))

    @unittest.skip("not supported")
    def test_120_replace(self):
        # we use the test data from Calendrical Calculations
        for test_row in gregorian_test_data[:33]:
            rd = test_row[0]
            year = test_row[2][0]
            month = test_row[2][1]
            day = test_row[2][2]
            d = Date.gregorian(year, month, day)
            self.assertEqual(d.replace(), Date(rd), msg = 'replace, no change')
            self.assertEqual(d.replace(year = 10), Date.gregorian(10, month, day), msg = 'replaced year = 10')
            self.assertEqual(d.replace(month = 10), Date.gregorian(year, 10, day), msg = 'replaced month = 10')
            self.assertEqual(d.replace(day = 10), Date.gregorian(year, month, 10), msg = 'replaced day = 10')

    @unittest.skip("not supported")
    def test_125_replace_invalid_parameter_types(self):
        d = Date(12345678)
        # exception with positional parameters
        self.assertRaises(TypeError, d.replace, 1)
        self.assertRaises(TypeError, d.replace, 1, 2)
        self.assertRaises(TypeError, d.replace, 1, 2, 3)
        self.assertRaises(TypeError, d.replace, 1, 2, 3, 4)
        # exception with positional and key parameters
        self.assertRaises(TypeError, d.replace, 1, day = 14)
        self.assertRaises(TypeError, d.replace, 1, month = 7)
        self.assertRaises(TypeError, d.replace, 1, year = 1234)
        # exception with non-numeric types
        for par in ("1", (1,), [1], {1:1}, (), [], {}, None):
            self.assertRaises(TypeError, d.replace, day = par)
            self.assertRaises(TypeError, d.replace, month = par)
            self.assertRaises(TypeError, d.replace, year = par)
            # exception with invalid numeric types
        for par in (1.0, Fraction(1, 1), decimal.Decimal(1), 1j):
            self.assertRaises(TypeError, d.replace, day = par)
            self.assertRaises(TypeError, d.replace, month = par)
            self.assertRaises(TypeError, d.replace, year = par)

    @unittest.skip("not supported")
    def test_127_replace_invalid_values(self):
        d = Date(12345678)
        # generic invalid values
        self.assertRaises(ValueError, d.replace, day = -1)
        self.assertRaises(ValueError, d.replace, day = 0)
        self.assertRaises(ValueError, d.replace, day = 32)
        self.assertRaises(ValueError, d.replace, month = -1)
        self.assertRaises(ValueError, d.replace, month = 0)
        self.assertRaises(ValueError, d.replace, month = 13)
        # leap day invalid values
        d = Date.gregorian(2011, 3, 1)
        self.assertRaises(ValueError, d.replace, month = 2, day = 30)
        self.assertRaises(ValueError, d.replace, month = 2, day = 29)
        self.assertRaises(ValueError, d.replace, year = 2012, month = 2, day = 30)
        d.replace(year = 2012, month = 2, day = 29)  # this is valid

    @unittest.skip("not supported")
    def test_130_week_and_day(self):
        # I am using all dates (even if computation is longer, because many boundary conditions are interesting here
        for test_row in gregorian_test_data:
            rd = test_row[0]
            year = test_row[2][0]
            d = Date(rd)
            jan1st = Date.gregorian(year, 1, 1).weekday()
            for week_start in range(7):
                week, day = d.gregorian.week_and_day(week_start)
                tentative_day_of_year = (week - 1) * 7 + day + ((week_start - jan1st + 7) % 7)
                self.assertEqual(d.gregorian.day_of_year(), tentative_day_of_year, msg = 'week_and_day, RD = {}, week_start = {}'.format(rd, week_start))

    @unittest.skip("not supported")
    def test_135_invalid_week_and_day(self):
        d = Date(12345678)
        # exception with none or two parameters
        self.assertRaises(TypeError, d.gregorian.week_and_day)
        self.assertRaises(TypeError, d.gregorian.week_and_day, 1, 2)
        # exception with non-numeric types
        for par in ("1", (1,), [1], {1:1}, (), [], {}, None):
            self.assertRaises(TypeError, d.gregorian.week_and_day, par)
            # exception with invalid numeric types
        for par in (1.0, fractions.Fraction(1, 1), decimal.Decimal(1), 1j):
            self.assertRaises(TypeError, d.gregorian.week_and_day, par)

    @unittest.skip("not supported")
    def test_200_str(self):
        for test_row in gregorian_test_data:
            rd = test_row[0]
            year = test_row[2][0]
            month = test_row[2][1]
            day = test_row[2][2]
            d = Date.gregorian(year, month, day)
            expected_format = "[04]-{02}-{02}" if year >= 0 and year <= 9999 else "{+05}-{02}-{02}"
            self.assertEqual(str(d.gregorian), expected_format.format(year, month, day), msg = 'str, RD = {}'.format(rd))

    @unittest.skip("not supported")
    def test_210_cformat(self):
        wd = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        abbr_wd = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        mo = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        abbr_mo = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        for test_row in gregorian_test_data:
            rd = test_row[0]
            weekday = test_row[1]
            year = test_row[2][0]
            month = test_row[2][1]
            day = test_row[2][2]
            doy = test_row[3]
            d = Date(rd)
            self.assertEqual(d.cformat('%a'), abbr_wd[weekday], msg = "cformat('%a')")
            self.assertEqual(d.cformat('%A'), wd[weekday], msg = "cformat('%A')")
            self.assertEqual(d.cformat('%b'), abbr_mo[month], msg = "cformat('%b')")
            self.assertEqual(d.cformat('%B'), mo[month], msg = "cformat('%B')")
            self.assertEqual(d.cformat('%d'), day.format('{02d}'), msg = "cformat('%d')")
            self.assertEqual(d.cformat('%j'), doy.format('{03d}'), msg = "cformat('%j')")
            self.assertEqual(d.cformat('%m'), month.format('{02d}'), msg = "cformat('%m')")
            self.assertEqual(d.cformat('%U'), format((doy - weekday) // 7, '{d}'), msg = "cformat('%U')")
            self.assertEqual(d.cformat('%w'), weekday.format('{d}'), msg = "cformat('%w')")
            self.assertEqual(d.cformat('%W'), format((doy - (weekday + 1) % 7) // 7, '{d}'), msg = "cformat('%W')")
            self.assertEqual(d.cformat('%y'), year.format('{02d}')[-2:], msg = "cformat('%y')")
            self.assertEqual(d.cformat('%Y'), year.format('{d}'), msg = "cformat('%Y')")
            self.assertEqual(d.cformat('%%'), '%', msg = "cformat('%%')")
            for c in "DEJefgu":    # a collection of random characters in the unsupported set
                # TODO: add more characters outside standard ASCII range
                format_string = '%' + c
                self.assertEqual(d.cformat(format_string), format_string, msg = "cformat('{}')".format(format_string))
