# tests for ISO calendar

# Copyright (c) 2013-2023 Francesco Ricciardi
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
import pytest

from datetime2.modern import IsoCalendar


INF = float('inf')
NAN = float('nan')

# TODO: use named tuple for test data

iso_test_data = [
    # data from Calendrical Calculations: The Millennium Edition, with addition
    #      RD         ISO      doy
    #           Year Week Day
    [ -214193,  -586,  29,  7, 203],
    [  -61387,  -168,  49,  3, 339],
    [   25469,    70,  39,  3, 269],
    [   49217,   135,  39,  7, 273],
    [  171307,   470,   2,  3,  10],
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
    [  764652,  2094,  28,  7, 196],
    # Boundary conditions on RD
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
    [ 1000001,   2738, 48,  2, 331],
    # A few long years
    [ -589141,  -1613, 52,  7, 364],
    [ -589140,  -1613, 53,  1, 365],
    [ -589134,  -1613, 53,  7, 371],
    [ -589133,  -1612,  1,  1,   1],
    [ -578914,  -1585, 52,  7, 364],
    [ -578913,  -1585, 53,  1, 365],
    [ -578907,  -1585, 53,  7, 371],
    [ -578906,  -1584,  1,  1,   1],
    [ -422590,  -1157, 52,  7, 364],
    [ -422589,  -1157, 53,  1, 365],
    [ -422583,  -1157, 53,  7, 371],
    [ -422582,  -1156,  1,  1,   1],
    [ -266266,   -729, 52,  7, 364],
    [ -266265,   -729, 53,  1, 365],
    [ -266259,   -729, 53,  7, 371],
    [ -266258,   -728,  1,  1,   1],
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
    [ 1149786,   3149,  1,  1,   1],
    # Boundary conditions on ISO years
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
    [    3290,      9, 53,  7, 371],
    [    3291,     10,  1,  1,   1],
    [   36162,     99, 53,  7, 371],
    [   36163,    100,  1,  1,   1],
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


def iso_equal(first, second):
    return first.year == second.year and first.week == second.week and first.day == second.day


def test_00_constructor():
    for test_row in iso_test_data:
        year = test_row[1]
        week = test_row[2]
        day = test_row[3]
        iso = IsoCalendar(year, week, day)
        assert iso.year == year
        assert iso.week == week
        assert iso.day == day

    # exception with none, two or four parameters
    with pytest.raises(TypeError):
        IsoCalendar()
    with pytest.raises(TypeError):
        IsoCalendar(1, 2)
    with pytest.raises(TypeError):
        IsoCalendar(1, 2, 3, 4)

    # exception with non-numeric types
    for par in ("1", (1,), [1], {1:1}, (), [], {}, None):
        with pytest.raises(TypeError):
            IsoCalendar(par, 1, 1)
        with pytest.raises(TypeError):
            IsoCalendar(1, par, 1)
        with pytest.raises(TypeError):
            IsoCalendar(1, par, 1)

    # exception with invalid numeric types
    for par in (1.0, Fraction(1, 1), Decimal(1), 1j, 1 + 1j, INF, NAN):
        with pytest.raises(TypeError):
            IsoCalendar(par, 1, 1)
        with pytest.raises(TypeError):
            IsoCalendar(1, par, 1)
        with pytest.raises(TypeError):
            IsoCalendar(1, par, 1)

    # invalid values
    for test_row in iso_invalid_data:
        year = test_row[0]
        week = test_row[1]
        day = test_row[2]
        with pytest.raises(TypeError):
            IsoCalendar.from_rata_die(year, week, day)


def test_09_constructor_rata_die():
    # valid dates
    for test_row in iso_test_data:
        rd = test_row[0]
        year = test_row[1]
        week = test_row[2]
        day = test_row[3]
        iso_rd = IsoCalendar.from_rata_die(rd)
        assert iso_rd.year == year
        assert iso_rd.week == week
        assert iso_rd.day == day

    # exception with none, two or four parameters
    with pytest.raises(TypeError):
        IsoCalendar.from_rata_die()
    with pytest.raises(TypeError):
        IsoCalendar.from_rata_die(1, 2)

    # exception with non-numeric types
    for par in ("1", (1,), [1], {1:1}, (), [], {}, None):
        with pytest.raises(TypeError):
            IsoCalendar.from_rata_die(par)

    # exception with invalid numeric types
    for par in (1.0, Fraction(1, 1), Decimal(1), 1j, 1 + 1j, INF, NAN):
        with pytest.raises(TypeError):
            IsoCalendar.from_rata_die(par)


def test_20_attribute():
    iso = IsoCalendar(1, 1, 1)
    with pytest.raises(AttributeError):
        iso.year = 3
    with pytest.raises(AttributeError):
        iso.week = 3
    with pytest.raises(AttributeError):
        iso.day = 3


def test_21_long_years():
    # long years
    for year in (-2847, -2424, -2002, -1974, -1546, -1118, -689, -261,
                 167, 595, 1024, 1452, 1880, 2308, 2731):
        assert IsoCalendar.is_long_year(year)
        assert IsoCalendar.weeks_in_year(year) == 53
    # short years
    for year in (-2845, -2422, -2000, -1972, -1544, -1116, -687, -259,
                 169, 597, 1026, 1454, 1882, 2310, 2733):
        assert not IsoCalendar.is_long_year(year)
        assert IsoCalendar.weeks_in_year(year) == 52


def test_30_repr():
    import datetime2
    for test_row in iso_test_data:
        year = test_row[1]
        week = test_row[2]
        day = test_row[3]
        iso = IsoCalendar(year, week, day)
        iso_repr = repr(iso)
        names, args = iso_repr.split('(')
        assert names.split('.') == ['datetime2', 'modern', 'IsoCalendar']
        args = args[:-1] # drop ')'
        for found, expected in zip(args.split(','), (year, week, day)):
            assert int(found) == expected
        assert iso_equal(iso, eval(iso_repr))


def test_31_str():
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
        expected += '-' + str(day)
        assert str(iso) == expected


def test_32_cformat():
    # valid numbers
    for test_row in iso_test_data:
        year = test_row[1]
        week = test_row[2]
        day = test_row[3]
        doy = test_row[4]
        iso = IsoCalendar(year, week, day)
        assert iso.cformat('%j') == '{:03d}'.format(doy)
        assert iso.cformat('%w') == '{:1d}'.format(day)
        assert iso.cformat('%W') == '{:02d}'.format(week)
        assert iso.cformat('%y') == ('{:04d}'.format(year))[-2:]
        if year >= 0:
            assert iso.cformat('%Y') == '{:04d}'.format(year)
        else:
            assert iso.cformat('%Y') == '-{:04d}'.format(-year)

    # valid names
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    abbr_weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    for test_row in iso_test_data:
        year = test_row[1]
        week = test_row[2]
        day = test_row[3]
        iso = IsoCalendar(year, week, day)
        assert iso.cformat('%a') == abbr_weekdays[day - 1]
        assert iso.cformat('%A') == weekdays[day - 1]

    # percent
    iso = IsoCalendar(1, 2, 3)
    assert iso.cformat('%') == '%'
    assert iso.cformat('%%') == '%'
    assert iso.cformat('%%%') == '%%'
    assert iso.cformat('%%%%') == '%%'
    assert iso.cformat('abcd%') == 'abcd%'
    assert iso.cformat('abcd%%') == 'abcd%'
    assert iso.cformat('%k') == '%k'
    assert iso.cformat('a%k') == 'a%k'
    assert iso.cformat('%k%') == '%k%'
    assert iso.cformat('%k%%') == '%k%'
    assert iso.cformat('%kw') == '%kw'
    assert iso.cformat('%k%w') == '%k3'
    assert iso.cformat('%w%k') == '3%k'

    # invalid types
    for par in (1, (1,), [1], {1:1}, None):
        with pytest.raises(TypeError):
            iso.cformat(par)


def test_50_to_rata_die():
    for test_row in iso_test_data:
        year = test_row[1]
        week = test_row[2]
        day = test_row[3]
        rd = test_row[0]
        assert IsoCalendar(year, week, day).to_rata_die() == rd


def test_51_replace():
    for test_row in iso_test_data[:33]:   # take Calendrical Calculations tests data only (other may make replace fail, as in the next tests method)
        year = test_row[1]
        week = test_row[2]
        day = test_row[3]
        iso = IsoCalendar(year, week, day)
        assert iso_equal(iso.replace(),  IsoCalendar(year, week, day))
        assert iso_equal(iso.replace(year=11),  IsoCalendar(11, week, day))
        assert iso_equal(iso.replace(week=10),  IsoCalendar(year, 10, day))
        assert iso_equal(iso.replace(day=2),  IsoCalendar(year, week, 2))
        assert iso_equal(iso.replace(week=10, year=11),  IsoCalendar(11, 10, day))
        assert iso_equal(iso.replace(day=3, year=11),  IsoCalendar(11, week, 3))
        assert iso_equal(iso.replace(day=4, week=10),  IsoCalendar(year, 10, 4))
        assert iso_equal(iso.replace(day=1, week=10, year=11),  IsoCalendar(11, 10, 1))

    # test invalid types
    iso = IsoCalendar(11, 10, 4)
    # exception for positional parameters
    with pytest.raises(TypeError):
        iso.replace(1)

    # exception with non-numeric types
    for par in ("1", (1,), [1], {1:1}, (), [], {}):
        with pytest.raises(TypeError):
            iso.replace(year=par)
        with pytest.raises(TypeError):
            iso.replace(week=par)
        with pytest.raises(TypeError):
            iso.replace(day=par)

    # exception with invalid numeric types
    for par in (1.0, Fraction(1, 1), Decimal(1), 1j):
        with pytest.raises(TypeError):
            iso.replace(year=par)
        with pytest.raises(TypeError):
            iso.replace(week=par)
        with pytest.raises(TypeError):
            iso.replace(day=par)

    # test invalid values
    iso1 = IsoCalendar(11, 10, 4)
    with pytest.raises(ValueError):
        iso1.replace(week=0)
    with pytest.raises(ValueError):
        iso1.replace(day=0)
    with pytest.raises(ValueError):
        iso1.replace(week=-1)
    with pytest.raises(ValueError):
        iso1.replace(day=-1)
    with pytest.raises(ValueError):
        iso1.replace(week=54)
    with pytest.raises(ValueError):
        iso1.replace(day=8)
    iso2 = IsoCalendar(1, 9, 2)   # short year
    with pytest.raises(ValueError):
        iso2.replace(week=53)
    iso3 = IsoCalendar(4, 9, 2)   # long year
    with pytest.raises(ValueError):
        iso3.replace(week=54)


def test_52_day_of_year():
    for test_row in iso_test_data:
        year = test_row[1]
        week = test_row[2]
        day = test_row[3]
        doy = test_row[4]
        assert IsoCalendar(year, week, day).day_of_year() == doy

