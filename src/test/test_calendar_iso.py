# tests for ISO calendar

# Copyright (c) 2013 Francesco Ricciardi
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
import unittest

from datetime2.calendars.iso import IsoCalendar


INF = float('inf')
NAN = float('nan')

iso_test_data = [
    # data from Calendrical Calculations: The Millennium Edition, with addition
    #      RD         ISO
    #           Year Week Day
    [ -214193,  -586,  29,  7, 203],
    [  -61387,  -168,  49,  3, 339],
    [   25469,    70,  39,  3, 269],
    [   49217,   135,  39,  7, 273],
    [  171307,    47,   2,  3,  10],
    [  210155,   576,  21,  1, 141],
    [  253427,   694,  45,  6, 314],
    [  369740,  1013,  16,  7, 112],
    [  400085,  1096,  21,  7, 147],
    [  434355,  1190,  12,  5,  82],
    [  452605,  1240,  10,  6,  69],
    [  470160,  1288,  14,  5,  96],
    [  473837,  1298,  17,  7, 119],
    [  507850,  1391,  23,  7, 161],
    [  524156,  1436,   5,  3,  31],
    [  544676,  1492,  14,  6,  97],
    [  567118,  1553,  38,  6, 265],
    [  569477,  1560,   9,  6,  62],
    [  601716,  1648,  24,  3, 164],
    [  613424,  1680,  26,  7, 182],
    [  626596,  1716,  30,  5, 208],
    [  645554,  1768,  24,  7, 168],
    [  664224,  1819,  31,  1, 211],
    [  671401,  1839,  13,  3,  87],
    [  694799,  1903,  16,  7, 112],
    [  704424,  1929,  34,  7, 238],
    [  708842,  1941,  40,  1, 274],
    [  709409,  1943,  16,  1, 106],
    [  709580,  1943,  40,  4, 277],
    [  727274,  1992,  12,  2,  79],
    [  728714,  1996,   8,  7,  56],
    [  744313,  2038,  45,  3, 311],
    [  764652,  2094,  28,  7, 196],    # Boundary conditions on RD
    [-1000001,  -2737,  5,  5,  33],
    [-1000000,  -2737,  5,  6,  34],
    [ -999999,  -2737,  5,  7,  35],
    [ -100001,   -273, 12,  1,  78],
    [ -100000,   -273, 12,  2,  79],
    [  -99999,   -273, 12,  3,  80],
    [  -10001,    -27, 33,  2, 226],
    [  -10000,    -27, 33,  3, 227],
    [   -9999,    -27, 33,  4, 228],
    [   -1001,     -2, 14,  7,  98],
    [   -1000,     -2, 15,  1,  99],
    [    -999,     -2, 15,  2, 100],
    [    -101,      0, 38,  4, 263],
    [    -100,      0, 38,  5, 264],
    [     -99,      0, 38,  6, 265],
    [     -11,      0, 51,  3, 353],
    [     -10,      0, 51,  4, 354],
    [      -9,      0, 51,  5, 355],
    [      -1,      0, 52,  6, 363],
    [       0,      0, 52,  7, 364],
    [       1,      1,  1,  1,   1],
    [       9,      1,  2,  2,   9],
    [      10,      1,  2,  3,  10],
    [      11,      1,  2,  4,  11],
    [      99,      1, 15,  1,  99],
    [     100,      1, 15,  2, 100],
    [     101,      1, 15,  3, 101],
    [     999,      3, 39,  5, 271],
    [    1000,      3, 39,  6, 272],
    [    1001,      3, 39,  7, 273],
    [    9999,     28, 20,  3, 136],
    [   10000,     28, 20,  4, 137],
    [   10001,     28, 20,  5, 138],
    [   99999,    274, 42,  4, 291],
    [  100000,    274, 42,  5, 292],
    [  100001,    274, 42,  6, 293],
    [  999999,   2738, 47,  7, 329],
    [ 1000000,   2738, 48,  1, 330],
    [ 1000001,   2738, 48,  2, 331],    # A few long years
    [ -589181,  -1613, 52,  7, 364],
    [ -589180,  -1613, 53,  1, 365],
    [ -589174,  -1613, 53,  7, 371],
    [ -589173,  -1612,  1,  1,   1],
    [ -578914,  -1585, 52,  7, 364],
    [ -578913,  -1585, 53,  1, 365],
    [ -578907,  -1585, 53,  7, 371],
    [ -578906,  -1584,  1,  1,   1],
    [ -422590,  -1157, 52,  7, 364],
    [ -422589,  -1157, 53,  1, 365],
    [ -422583,  -1157, 53,  7, 371],
    [ -422582,  -1156,  1,  1,   1],
    [ -266266,   -719, 52,  7, 364],
    [ -266265,   -719, 53,  1, 365],
    [ -266259,   -719, 53,  7, 371],
    [ -266259,   -718,  1,  1,   1],
    [ -109942,   -301, 52,  7, 364],
    [ -109941,   -301, 53,  1, 365],
    [ -109935,   -301, 53,  7, 371],
    [ -109934,   -300,  1,  1,   1],
    [  -99351,   -272, 52,  7, 364],
    [  -99350,   -272, 53,  1, 365],
    [  -99344,   -272, 53,  7, 371],
    [  -99343,   -271,  1,  1,   1],
    [   56973,    156, 52,  7, 364],
    [   56974,    156, 53,  1, 365],
    [   56980,    156, 53,  7, 371],
    [   56981,    157,  1,  1,   1],
    [  211106,    578, 52,  7, 364],
    [  211107,    578, 53,  1, 365],
    [  211113,    578, 53,  7, 371],
    [  211114,    579,  1,  1,   1],
    [  367794,   1007, 52,  7, 364],
    [  367795,   1007, 53,  1, 365],
    [  367801,   1007, 53,  7, 371],
    [  367802,   1008,  1,  1,   1],
    [  524118,   1435, 52,  7, 364],
    [  524119,   1435, 53,  1, 365],
    [  524125,   1435, 53,  7, 371],
    [  524126,   1436,  1,  1,   1],
    [  680442,   1863, 52,  7, 364],
    [  680443,   1863, 53,  1, 365],
    [  680449,   1863, 53,  7, 371],
    [  680450,   1864,  1,  1,   1],
    [  836766,   2291, 52,  7, 364],
    [  836767,   2291, 53,  1, 365],
    [  836773,   2291, 53,  7, 371],
    [  836774,   2292,  1,  1,   1],
    [  993454,   2720, 52,  7, 364],
    [  993455,   2720, 53,  1, 365],
    [  993461,   2720, 53,  7, 371],
    [  993462,   2721,  1,  1,   1],
    [ 1149778,   3148, 52,  7, 364],
    [ 1149779,   3148, 53,  1, 365],
    [ 1149785,   3148, 53,  7, 371],
    [ 1149786,   3149,  1,  1,   1],                         # Boundary conditions on ISO years
    [-3652425, -10000, 52,  7, 364],
    [-3652424,  -9999,  1,  1,   1],
    [-1826216,  -5000, 52,  7, 364],
    [-1826215,  -4999,  1,  1,   1],
    [ -365246,  -1000, 52,  7, 364],
    [ -365245,   -999,  1,  1,   1],
    [  -36526,   -100, 52,  7, 364],
    [  -36525,    -99,  1,  1,   1],
    [   -3654,    -10, 52,  7, 364],
    [   -3653,     -9,  1,  1,   1],
    [    -364,     -1, 52,  7, 364],
    [    -363,      0,  1,  1,   1],
    [     364,      1, 52,  7, 364],
    [     365,      2,  1,  1,   1],
    [    3283,      9, 52,  7, 364],
    [    3284,     10,  1,  1,   1],
    [   36155,     99, 52,  7, 364],
    [   36156,    100,  1,  1,   1],
    [  364875,    999, 52,  7, 364],
    [  364876,   1000,  1,  1,   1],
    [ 1825845,   4999, 52,  7, 364],
    [ 1825846,   5000,  1,  1,   1],
    [ 3652061,   9999, 52,  7, 364],
    [ 3652062,  10000,  1,  1,   1]
]

iso_invalid_data = [
    # zero or negative week or day
    (   1,  0,  1),
    (   1,  1,  0),
    (   1, -1,  1),
    (   1,  1, -1),
    # day greater than days in week
    (   1,  1,  8),
    # number of weeks
    ( 101,  55, 1),
    (   1,  53, 1),  # short year
    (   4,  54, 1)   # long year
]

class TestISO(unittest.TestCase):
    def test_000_constructor(self):
        for test_row in iso_test_data:
            year = test_row[1]
            week = test_row[2]
            day = test_row[3]
            iso = IsoCalendar(year, week, day)
            self.assertEqual(iso.year, year, msg = 'year attribute, date = {}-W{}-{}'.format(year, week, day))
            self.assertEqual(iso.week, week, msg = 'week attribute, date = {}-W{}-{}'.format(year, week, day))
            self.assertEqual(iso.day, day, msg = 'day attribute, date = {}-W{}-{}'.format(year, week, day))

    def test_005_constructor_rata_die(self):
        for test_row in iso_test_data:
            rd = test_row[0]
            year = test_row[1]
            week = test_row[2]
            day = test_row[3]
            iso_rd = IsoCalendar.from_rata_die(rd)
            self.assertEqual(iso_rd.year, year, msg = 'year attribute, date = {}-W{}-{}'.format(year, week, day))
            self.assertEqual(iso_rd.week, week, msg = 'week attribute, date = {}-W{}-{}'.format(year, week, day))
            self.assertEqual(iso_rd.day, day, msg = 'day attribute, date = {}-W{}-{}'.format(year, week, day))

    def test_010_invalid_parameter_types(self):
        # exception with none, two or four parameters
        self.assertRaises(TypeError, IsoCalendar)
        self.assertRaises(TypeError, IsoCalendar, 1, 2)
        self.assertRaises(TypeError, IsoCalendar, 1, 2, 3, 4)
        # exception with non-numeric types
        for par in ("1", (1,), [1], {1:1}, (), [], {}, None):
            self.assertRaises(TypeError, IsoCalendar, par, 1, 1)
            self.assertRaises(TypeError, IsoCalendar, 1, par, 1)
            self.assertRaises(TypeError, IsoCalendar, 1, 1, par)
        # exception with invalid numeric types
        for par in (1.0, fractions.Fraction(1, 1), decimal.Decimal(1), 1j, 1 + 1j, INF, NAN):
            self.assertRaises(TypeError, IsoCalendar, par, 1, 1)
            self.assertRaises(TypeError, IsoCalendar, 1, par, 1)
            self.assertRaises(TypeError, IsoCalendar, 1, 1, par)

    def test_015_invalid_parameter_types_rata_die(self):
        # exception with none, two or four parameters
        self.assertRaises(TypeError, IsoCalendar.from_rata_die)
        self.assertRaises(TypeError, IsoCalendar.from_rata_die, 1, 2)
        # exception with non-numeric types
        for par in ("1", (1,), [1], {1:1}, (), [], {}, None):
            self.assertRaises(TypeError, IsoCalendar.from_rata_die, par)
        # exception with invalid numeric types
        for par in (1.0, fractions.Fraction(1, 1), decimal.Decimal(1), 1j, 1 + 1j, INF, NAN):
            self.assertRaises(TypeError, IsoCalendar.from_rata_die, par)

    def test_020_invalid_values(self):
        for test_row in iso_invalid_data:
            year = test_row[0]
            week = test_row[1]
            day = test_row[2]
            self.assertRaises(ValueError, IsoCalendar, year, week, day)

    def test_040_write_attribute(self):
        iso = IsoCalendar(1, 1, 1)
        self.assertRaises(AttributeError, setattr, iso, 'year', 3)
        self.assertRaises(AttributeError, setattr, iso, 'week', 3)
        self.assertRaises(AttributeError, setattr, iso, 'day', 3)

    def test_120_create_from_attr(self):
        for test_row in iso_test_data:
            year = test_row[1]
            week = test_row[2]
            day = test_row[3]
            iso = IsoCalendar(year, week, day)
            self.assertEqual(iso, IsoCalendar(iso.year, iso.month, iso.day),
                             msg = 'create from attributes, date = {}-{}-{}'.format(year, week, day))

    def test_200_long_years(self):
        # long years
        for year in (-2847, -2424, -2002, -1974, -1546, -1118, -689, -261,
                     167, 595, 1024, 1452, 1880, 2308, 2731):
            self.assertTrue(IsoCalendar.is_long_year(year), msg = 'is_long_year, year = {}'.format(year))
            self.assertEqual(IsoCalendar.days_in_year(year), 366, msg = 'days_in_year, year = {}'.format(year))
        # non-leap years
        for year in (-2845, -2422, -2000, -1972, -1544, -1116, -687, -259,
                     169, 597, 1026, 1454, 1882, 2310, 2733):
            self.assertFalse(IsoCalendar.is_long_year(year), msg = 'is_long_year, year = {}'.format(year))
            self.assertEqual(IsoCalendar.days_in_year(year), 365, msg = 'days_in_year, year = {}'.format(year))

    def test_300_compare(self):
        iso1 = IsoCalendar(2, 3, 4)
        iso2 = IsoCalendar(2, 3, 4)
        self.assertEqual(iso1, iso2)
        self.assertTrue(iso1 <= iso2)
        self.assertTrue(iso1 >= iso2)
        self.assertFalse(iso1 != iso2)
        self.assertFalse(iso1 < iso2)
        self.assertFalse(iso1 > iso2)

        for year, week, day in (3, 3, 3), (2, 4, 4), (2, 3, 5):
            iso2 = IsoCalendar(year, week, day)   # this is larger than iso1
            self.assertTrue(iso1 < iso2)
            self.assertTrue(iso2 > iso1)
            self.assertTrue(iso1 <= iso2)
            self.assertTrue(iso2 >= iso1)
            self.assertTrue(iso1 != iso2)
            self.assertTrue(iso2 != iso1)
            self.assertFalse(iso1 == iso2)
            self.assertFalse(iso2 == iso1)
            self.assertFalse(iso1 > iso2)
            self.assertFalse(iso2 < iso1)
            self.assertFalse(iso1 >= iso2)
            self.assertFalse(iso2 <= iso1)

    def test_310_compare_invalid_types(self):
        import operator

        class SomeClass:
            pass

        iso = IsoCalendar(2, 3, 4)

        # exception with non-numeric types
        for par in ("1", (1,), [1], {1:1}, (), [], {}, None):
            self.assertFalse(iso == par)
            self.assertTrue(iso != par)
            self.assertRaises(TypeError, operator.lt, iso, par)
            self.assertRaises(TypeError, operator.gt, iso, par)
            self.assertRaises(TypeError, operator.le, iso, par)
            self.assertRaises(TypeError, operator.ge, iso, par)
        # exception with numeric types (all invalid) and other objects
        for par in (1, 1.0, fractions.Fraction(1, 1), decimal.Decimal(1), 1j, 1 + 1j, INF, NAN, SomeClass()):
            self.assertFalse(iso == par)
            self.assertTrue(iso != par)
            self.assertRaises(TypeError, operator.lt, iso, par)
            self.assertRaises(TypeError, operator.gt, iso, par)
            self.assertRaises(TypeError, operator.le, iso, par)
            self.assertRaises(TypeError, operator.ge, iso, par)

    def test_320_hash_equality(self):
        iso1 = IsoCalendar(2000, 12, 3)
        # same thing
        iso2 = IsoCalendar(2000, 12, 3)
        self.assertEqual(hash(iso1), hash(iso2))

        dic = {iso1: 1}
        dic[iso2] = 2
        self.assertEqual(len(dic), 1)
        self.assertEqual(dic[iso1], 2)
        self.assertEqual(dic[iso2], 2)

        iso1 = IsoCalendar(2001, 1, 1)
        # same thing
        iso2 = IsoCalendar(2001, 1, 1)
        self.assertEqual(hash(iso1), hash(iso2))

        dic = {iso1: 1}
        dic[iso2] = 2
        self.assertEqual(len(dic), 1)
        self.assertEqual(dic[iso1], 2)
        self.assertEqual(dic[iso2], 2)

    def test_400_to_rata_die(self):
        for test_row in iso_test_data:
            year = test_row[1]
            week = test_row[2]
            day = test_row[3]
            rd = test_row[0]
            self.assertEqual(IsoCalendar(year, week, day).to_rata_die(), rd,
                msg = 'to_rata_die, date = {}-{}-{}'.format(year, week, day))

    def test_410_day_of_year(self):
        for test_row in iso_test_data:
            year = test_row[1]
            week = test_row[2]
            day = test_row[3]
            doy = test_row[4]
            self.assertEqual(IsoCalendar(year, week, day).day_of_year(), doy,
                msg = 'day_of_year, date = {}-{}-{}'.format(year, week, day))

    def test_420_replace(self):
        for test_row in iso_test_data[:33]:   # take Calendrical Calculations test data only (other may make replace fail, as in the next test method)
            year = test_row[1]
            week = test_row[2]
            day = test_row[3]
            iso = IsoCalendar(year, week, day)
            self.assertEqual(iso.replace(), IsoCalendar(year, week, day),
                msg = 'replace, no change, date = {}-{}-{}'.format(year, week, day))
            self.assertEqual(iso.replace(year = 11), IsoCalendar(11, week, day),
                msg = 'replace, year changed, date = {}-{}-{}'.format(year, week, day))
            self.assertEqual(iso.replace(week = 10), IsoCalendar(year, 10, day),
                msg = 'replace, week changed, date = {}-{}-{}'.format(year, week, day))
            self.assertEqual(iso.replace(day = 2), IsoCalendar(year, week, 2),
                msg = 'replace, day changed, date = {}-{}-{}'.format(year, week, day))
            self.assertEqual(iso.replace(week = 10, year = 11), IsoCalendar(11, 10, day),
                msg = 'replace, year & week changed, date = {}-{}-{}'.format(year, week, day))
            self.assertEqual(iso.replace(day = 3, year = 11), IsoCalendar(11, week, 3),
                msg = 'replace, year & day changed, date = {}-{}-{}'.format(year, week, day))
            self.assertEqual(iso.replace(day = 4, week = 10), IsoCalendar(year, 10, 4),
                msg = 'replace, week & day changed, date = {}-{}-{}'.format(year, week, day))
            self.assertEqual(iso.replace(day = 1, week = 10, year = 11), IsoCalendar(11, 10, 1),
                msg = 'replace, all changed, date = {}-{}-{}'.format(year, week, day))

    def test_423_replace_invalid_types(self):
        iso = IsoCalendar(11, 10, 9)
        # exception for positional parameters
        self.assertRaises(TypeError, iso.replace, 1)
        # exception with non-numeric types
        for par in ("1", (1,), [1], {1:1}, (), [], {}):
            self.assertRaises(TypeError, iso.replace, year = par)
            self.assertRaises(TypeError, iso.replace, week = par)
            self.assertRaises(TypeError, iso.replace, day = par)
        # exception with invalid numeric types
        for par in (1.0, fractions.Fraction(1, 1), decimal.Decimal(1), 1j):
            self.assertRaises(TypeError, iso.replace, year = par)
            self.assertRaises(TypeError, iso.replace, week = par)
            self.assertRaises(TypeError, iso.replace, day = par)

    def test_426_replace_invalid_values(self):
        iso = IsoCalendar(11, 10, 9)
        self.assertRaises(ValueError, iso.replace, week = 0)
        self.assertRaises(ValueError, iso.replace, day = 0)
        self.assertRaises(ValueError, iso.replace, week = -1)
        self.assertRaises(ValueError, iso.replace, day = -1)
        self.assertRaises(ValueError, iso.replace, week = 54)
        self.assertRaises(ValueError, iso.replace, day = 8)
        iso = IsoCalendar(1, 9, 2)   # short year
        self.assertRaises(ValueError, iso.replace, week = 53)
        iso = IsoCalendar(4, 9, 2)   # long year
        self.assertRaises(ValueError, iso.replace, week = 54)

    def test_500_repr(self):
        import datetime2

        for test_row in iso_test_data:
            year = test_row[1]
            week = test_row[2]
            day = test_row[3]
            iso = IsoCalendar(year, week, day)
            iso_repr = repr(IsoCalendar(year, week, day))
            names, args = iso_repr.split('(')
            self.assertEqual(names.split('.'), ['datetime2', 'calendars', 'iso', 'IsoCalendar'], msg='Repr test 1 for {}-W{}-{}'.format(year, week, day))
            args = args[:-1] # drop ')'
            for found, expected in zip(args.split(','), (year, week, day)):
                self.assertEqual(int(found), expected, msg='Repr test 2 for {}-W{}-{}'.format(year, week, day))
            self.assertEqual(iso, eval(repr(iso)), msg='Repr test 3 for {}-W{}-{}'.format(year, week, day))

    def test_520_str(self):
        for test_row in iso_test_data:
            year = test_row[1]
            week = test_row[2]
            day = test_row[3]
            iso = IsoCalendar(year, week, day)
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
            expected += '-W' + ('0' + str(week))[-2:]
            expected += '-' + ('0' + str(day))[-2:]
            self.assertEqual(str(iso), expected, msg='Str test for {}-W{}-{}'.format(iso.year, week, day))

    def test_900_pickling(self):
        for test_row in iso_test_data:
            year = test_row[1]
            week = test_row[2]
            day = test_row[3]
            iso = IsoCalendar(year, week, day)
            for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
                pickled = pickle.dumps(iso, protocol)
                derived = pickle.loads(pickled)
                self.assertEqual(iso, derived)

    def test_920_subclass(self):

        class I(IsoCalendar):
            theAnswer = 42

            def __init__(self, *args, **kws):
                temp = kws.copy()
                self.extra = temp.pop('extra')
                IsoCalendar.__init__(self, *args, **temp)

            def newmeth(self, start):
                return start + self.year + self.week

        iso1 = IsoCalendar(2003, 14, 4)
        iso2 = I(2003, 14, 4, extra = 7)

        self.assertEqual(iso2.theAnswer, 42)
        self.assertEqual(iso2.extra, 7)
        self.assertEqual(iso1.to_rata_die(), iso2.to_rata_die())
        self.assertEqual(iso2.newmeth(-7), iso1.year + iso1.week - 7)


