# tests for western time intervals

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

from collections import namedtuple
from decimal import Decimal
from fractions import Fraction
import pytest

from datetime2.western import WesternTimeDelta

INF = float('inf')
NAN = float('nan')

WesternTimeDeltaTestData = namedtuple('WesternTimeDeltaTestData', ['fractional_days', 'days', 'hours', 'minutes', 'seconds', 'expected'])

western_timedelta_test_data = [
    # fracional_days      d   h   m   s

    # Boundary conditions around zero and unity
    # hour, minute, second and their halves second
    WesternTimeDeltaTestData("0/1",        0, 0, 0, Fraction(0, 1), "0 days"),
    WesternTimeDeltaTestData("1/86400",    0, 0, 0, Fraction(1, 1), "1 second"),
    WesternTimeDeltaTestData("-1/86400",   0, 0, 0, Fraction(-1, 1), "-1 second"),
    WesternTimeDeltaTestData("1/192800",   0, 0, 0, Fraction(1, 2), "0 days"),
    WesternTimeDeltaTestData("-1/192800",  0, 0, 0, Fraction(-1, 2), "0 days"),
    WesternTimeDeltaTestData("1/1440",     0, 0, 1, Fraction(0, 1), "1 minute"),
    WesternTimeDeltaTestData("-1/1440",    0, 0, -1, Fraction(0, 1), "-1 minute"),
    WesternTimeDeltaTestData("1/2880",     0, 0, 0, Fraction(30, 1), "30 seconds"),
    WesternTimeDeltaTestData("-1/2880",    0, 0, 0, Fraction(-30, 1), "-30 seconds"),
    WesternTimeDeltaTestData("1/24",       0, 1, 0, Fraction(0, 1), "1 hour"),
    WesternTimeDeltaTestData("-1/24",      0, -1, 0, Fraction(0, 1), "-1 hour"),
    WesternTimeDeltaTestData("1/48",       0, 0, 30, Fraction(0, 1), "30 minutes"),
    WesternTimeDeltaTestData("-1/48",      0, 0, -30, Fraction(0, 1), "-30 minutes"),
    WesternTimeDeltaTestData("1/2",        0, 12, 0, Fraction(0, 1), "12 hours"),
    WesternTimeDeltaTestData("-1/2",       0, -12, 0, Fraction(0, 1), "-12 hours"),

    # Days
    WesternTimeDeltaTestData("1/1",        1, 0, 0, Fraction(0, 1), "1 day"),
    WesternTimeDeltaTestData("-1/1",       -1, 0, 0, Fraction(0, 1), "-1 day"),
    WesternTimeDeltaTestData("100/1",      100, 0, 0, Fraction(0, 1), "100 days"),
    WesternTimeDeltaTestData("-100/1",     -100, 0, 0, Fraction(0, 1), "-100 days"),
    WesternTimeDeltaTestData("10000/1",    10000, 0, 0, Fraction(0, 1), "10000 days"),
    WesternTimeDeltaTestData("-10000/1",   -10000, 0, 0, Fraction(0, 1), "-10000 days"),

    # mixing days, hours, minutes and seconds
    WesternTimeDeltaTestData("1791334471/1814400", 987, 6, 54, Fraction(31, 21), "987 days, 6 hours, 54 minutes and 1 second"),
    WesternTimeDeltaTestData("-546173/273600",   -1, -23, -45, Fraction(-678, 19), "-1 day, -23 hours, -45 minutes and 35 seconds"),

    # testing str
    # days and hours
    WesternTimeDeltaTestData("25/24", 1, 1, 0, Fraction(0, 1), "1 day and 1 hour"),
    WesternTimeDeltaTestData("-25/24", -1, -1, 0, Fraction(0, 1), "-1 day and -1 hour"),
    WesternTimeDeltaTestData("49/24", 2, 1, 0, Fraction(0, 1), "2 days and 1 hour"),
    WesternTimeDeltaTestData("-49/24", -2, -1, 0, Fraction(0, 1), "-2 days and -1 hour"),
    WesternTimeDeltaTestData("13/12", 1, 2, 0, Fraction(0, 1), "1 day and 2 hours"),
    WesternTimeDeltaTestData("-13/12", -1, -2, 0, Fraction(0, 1), "-1 day and -2 hours"),
    WesternTimeDeltaTestData("25/12", 2, 2, 0, Fraction(0, 1), "2 days and 2 hours"),
    WesternTimeDeltaTestData("-25/12", -2, -2, 0, Fraction(0, 1), "-2 days and -2 hours"),
    # days and minutes
    WesternTimeDeltaTestData("1441/1440", 1, 0, 1, Fraction(0, 1), "1 day and 1 minute"),
    WesternTimeDeltaTestData("-1441/1440", -1, 0, -1, Fraction(0, 1), "-1 day and -1 minute"),
    WesternTimeDeltaTestData("2881/1440", 2, 0, 1, Fraction(0, 1), "2 days and 1 minute"),
    WesternTimeDeltaTestData("-2881/1440", -2, 0, -1, Fraction(0, 1), "-2 days and -1 minute"),
    WesternTimeDeltaTestData("721/720", 1, 0, 2, Fraction(0, 1), "1 day and 2 minutes"),
    WesternTimeDeltaTestData("-721/720", -1, 0, -2, Fraction(0, 1), "-1 day and -2 minutes"),
    WesternTimeDeltaTestData("1441/720", 2, 0, 2, Fraction(0, 1), "2 days and 2 minutes"),
    WesternTimeDeltaTestData("-1441/720", -2, 0, -2, Fraction(0, 1), "-2 days and -2 minutes"),
    # days and seconds
    WesternTimeDeltaTestData("86401/86400", 1, 0, 0, Fraction(1, 1), "1 day and 1 second"),
    WesternTimeDeltaTestData("-86401/86400", -1, 0, 0, Fraction(-1, 1), "-1 day and -1 second"),
    WesternTimeDeltaTestData("172801/172800", 2, 0, 0, Fraction(1, 1), "2 days and 1 second"),
    WesternTimeDeltaTestData("-172801/172800", -2, 0, 0, Fraction(-1, 1), "-2 days and -1 second"),
    WesternTimeDeltaTestData("43201/43200", 1, 0, 0, Fraction(2, 1), "1 day and 2 seconds"),
    WesternTimeDeltaTestData("-43201/43200", -1, 0, 0, Fraction(-2, 1), "-1 day and -2 seconds"),
    WesternTimeDeltaTestData("86401/43200", 2, 0, 0, Fraction(2, 1), "2 days and 2 seconds"),
    WesternTimeDeltaTestData("-86401/43200", -2, 0, 0, Fraction(-2, 1), "-1 days and -2 seconds"),
    # hours and minutes
    WesternTimeDeltaTestData("61/1440", 0, 1, 1, Fraction(0, 1), "1 hour and 1 minute"),
    WesternTimeDeltaTestData("-61/1440", 0, -1, -1, Fraction(0, 1), "-1 hour and -1 minute"),
    WesternTimeDeltaTestData("121/1440", 0, 2, 1, Fraction(0, 1), "2 hours and 1 minute"),
    WesternTimeDeltaTestData("-121/1440", 0, -2, -1, Fraction(0, 1), "-2 hours and -1 minute"),
    WesternTimeDeltaTestData("31/7200", 0, 1, 2, Fraction(0, 1), "1 hour and 2 minutes"),
    WesternTimeDeltaTestData("-31/7200", 0, -1, -2, Fraction(0, 1), "-1 hour and -2 minutes"),
    WesternTimeDeltaTestData("61/7200", 0, 2, 2, Fraction(0, 1), "2 hours and 2 minutes"),
    WesternTimeDeltaTestData("-61/7200", 0, -2, -2, Fraction(0, 1), "-2 hours and -2 minutes"),
    # hours and seconds
    WesternTimeDeltaTestData("3601/86400", 0, 1, 0, Fraction(1, 1), "1 hour and 1 second"),
    WesternTimeDeltaTestData("-3601/86400", 0, -1, 0, Fraction(-1, 1), "-1 hour and -1 second"),
    WesternTimeDeltaTestData("7201/86400", 0, 2, 0, Fraction(1, 1), "2 hours and 1 second"),
    WesternTimeDeltaTestData("-7201/86400", 0, -2, 0, Fraction(-1, 1), "-2 hours and -1 second"),
    WesternTimeDeltaTestData("1801/43200", 0, 1, 0, Fraction(2, 1), "1 hour and 2 seconds"),
    WesternTimeDeltaTestData("-1801/43200", 0, -1, 0, Fraction(-2, 1), "-1 hour and -2 seconds"),
    WesternTimeDeltaTestData("3601/43200", 0, 2, 0, Fraction(2, 1), "2 hours and 2 seconds"),
    WesternTimeDeltaTestData("-3601/43200", 0, -2, 0, Fraction(-2, 1), "-2 hours and -2 seconds"),
    # minutes and seconds
    WesternTimeDeltaTestData("61/86400", 0, 0, 1, Fraction(1, 1), "1 minute and 1 second"),
    WesternTimeDeltaTestData("-61/86400", 0, -0, -1, Fraction(-1, 1), "-1 minute and -1 second"),
    WesternTimeDeltaTestData("121/86400", 0, 0, 2, Fraction(1, 1), "2 minutes and 1 second"),
    WesternTimeDeltaTestData("-121/86400", 0, -0, -2, Fraction(-1, 1), "-2 minutes and -1 second"),
    WesternTimeDeltaTestData("31/43200", 0, 0, 1, Fraction(2, 1), "1 minute and 2 seconds"),
    WesternTimeDeltaTestData("-31/43200", 0, -0, -1, Fraction(-2, 1), "-1 minute and -2 seconds"),
    WesternTimeDeltaTestData("61/43200", 0, 0, 2, Fraction(2, 1), "2 minutes and 2 seconds"),
    WesternTimeDeltaTestData("-61/43200", 0, -0, -2, Fraction(-2, 1), "-2 minutes and -2 seconds"),
    # days, hours and minutes
    WesternTimeDeltaTestData("1501/1440", 1, 1, 1, Fraction(0, 1), "1 day, 1 hour and 1 minute"),
    WesternTimeDeltaTestData("-1501/1440", -1, -1, 1, Fraction(0, 1), "-1 day, -1 hour and -1 minute"),
    WesternTimeDeltaTestData("2941/1440", 2, 1, 1, Fraction(0, 1), "2 days, 1 hour and 1 minute"),
    WesternTimeDeltaTestData("-2941/1440", -2, -1, 1, Fraction(0, 1), "-2 days, -1 hour and -1 minute"),
    WesternTimeDeltaTestData("1561/1440", 1, 2, 1, Fraction(0, 1), "1 day, 2 hours and 1 minute"),
    WesternTimeDeltaTestData("-1561/1440", -1, -2, 1, Fraction(0, 1), "-1 day, -2 hours and -1 minute"),
    WesternTimeDeltaTestData("3001/1440", 2, 2, 1, Fraction(0, 1), "2 days, 2 hours and 1 minute"),
    WesternTimeDeltaTestData("-3001/1440", -2, -2, 1, Fraction(0, 1), "-2 days, -2 hours and -1 minute"),
    WesternTimeDeltaTestData("3001/1440", 2, 2, 1, Fraction(0, 1), "2 days, 2 hours and 1 minute"),
    WesternTimeDeltaTestData("-3001/1440", -2, -2, 1, Fraction(0, 1), "-2 days, -2 hours and -1 minute"),
    WesternTimeDeltaTestData("751/720", 1, 1, 2, Fraction(0, 1), "1 day, 1 hour and 2 minutes"),
    WesternTimeDeltaTestData("-751/720", -1, -1, 2, Fraction(0, 1), "-1 day, -1 hour and -2 minutes"),
    WesternTimeDeltaTestData("1471/720", 2, 1, 2, Fraction(0, 1), "2 days, 1 hour and 2 minutes"),
    WesternTimeDeltaTestData("-1471/720", -2, -1, 2, Fraction(0, 1), "-2 days, -1 hour and -2 minutes"),
    WesternTimeDeltaTestData("781/720", 1, 2, 2, Fraction(0, 1), "1 day, 2 hours and 2 minutes"),
    WesternTimeDeltaTestData("-781/720", -1, -2, 2, Fraction(0, 1), "-1 day, -2 hours and -2 minutes"),
    WesternTimeDeltaTestData("1501/720", 2, 2, 2, Fraction(0, 1), "2 days, 2 hours and 2 minutes"),
    WesternTimeDeltaTestData("-1501/720", -2, -2, 2, Fraction(0, 1), "-2 days, -2 hours and -2 minutes"),
    # days, hours and seconds
    WesternTimeDeltaTestData("90001/86400", 1, 1, 0, Fraction(1, 1), "1 day, 1 hour and 1 second"),
    WesternTimeDeltaTestData("-90001/86400", -1, -1, 0, Fraction(-1, 1), "-1 day, -1 hour and -1 second"),
    WesternTimeDeltaTestData("176401/86400", 2, 1, 0, Fraction(1, 1), "2 days, 1 hour and 1 second"),
    WesternTimeDeltaTestData("-176401/86400", -2, -1, 0, Fraction(-1, 1), "-2 days, -1 hour and -1 second"),
    WesternTimeDeltaTestData("93601/86400", 1, 2, 0, Fraction(1, 1), "1 day, 2 hours and 1 second"),
    WesternTimeDeltaTestData("-93601/86400", -1, -2, 0, Fraction(-1, 1), "-1 day, -2 hours and -1 second"),
    WesternTimeDeltaTestData("180001/86400", 2, 2, 0, Fraction(1, 1), "2 days, 2 hours and 1 second"),
    WesternTimeDeltaTestData("-180001/86400", -2, -2, 0, Fraction(-1, 1), "-2 days, -2 hours and -1 second"),
    WesternTimeDeltaTestData("45001/43200", 1, 1, 0, Fraction(2, 1), "1 day, 1 hour and 2 seconds"),
    WesternTimeDeltaTestData("-45001/43200", -1, -1, 0, Fraction(-2, 1), "-1 day, -1 hour and -2 seconds"),
    WesternTimeDeltaTestData("88201/43200", 2, 1, 0, Fraction(2, 1), "2 days, 1 hour and 2 seconds"),
    WesternTimeDeltaTestData("-88201/43200", -2, -1, 0, Fraction(-2, 1), "-2 days, -1 hour and -2 seconds"),
    WesternTimeDeltaTestData("46801/43200", 1, 2, 0, Fraction(2, 1), "1 day, 2 hours and 2 seconds"),
    WesternTimeDeltaTestData("-46801/43200", -1, -2, 0, Fraction(-2, 1), "-1 day, -2 hours and -2 seconds"),
    WesternTimeDeltaTestData("90001/43200", 2, 2, 0, Fraction(2, 1), "2 days, 2 hours and 2 seconds"),
    WesternTimeDeltaTestData("-90001/43200", -2, -2, 0, Fraction(-2, 1), "-2 days, -2 hours and -2 seconds"),
    # days, minutes and seconds
    WesternTimeDeltaTestData("86461/86400", 1, 0, 1, Fraction(1, 1), "1 day, 1 minute and 1 second"),
    WesternTimeDeltaTestData("-86461/86400", -1, 0, -1, Fraction(-1, 1), "-1 day, -1 minute and -1 second"),
    WesternTimeDeltaTestData("172861/86400", 2, 0, 1, Fraction(1, 1), "2 days, 1 minute and 1 second"),
    WesternTimeDeltaTestData("-172861/86400", -2, 0, -1, Fraction(-1, 1), "-2 days, -1 minute and -1 second"),
    WesternTimeDeltaTestData("86521/86400", 1, 0, 2, Fraction(1, 1), "1 day, 2 minutes and 1 second"),
    WesternTimeDeltaTestData("-86521/86400", -1, 0, -2, Fraction(-1, 1), "-1 day, -2 minutes and -1 second"),
    WesternTimeDeltaTestData("172921/86400", 2, 0, 2, Fraction(1, 1), "1 day, 2 minutes and 1 second"),
    WesternTimeDeltaTestData("-172921/86400", -2, 0, -2, Fraction(-1, 1), "-1 day, -2 minutes and -1 second"),
    WesternTimeDeltaTestData("43231/43200", 1, 0, 1, Fraction(2, 1), "1 day, 1 minute and 2 seconds"),
    WesternTimeDeltaTestData("-43231/43200", -1, 0, -1, Fraction(-2, 1), "-1 day, -1 minute and -2 seconds"),
    WesternTimeDeltaTestData("86431/43200", 2, 0, 1, Fraction(2, 1), "2 days, 1 minute and 2 seconds"),
    WesternTimeDeltaTestData("-86431/43200", -2, 0, -1, Fraction(-2, 1), "-2 days, -1 minute and -2 seconds"),
    WesternTimeDeltaTestData("43261/43200", 1, 0, 2, Fraction(2, 1), "1 day, 2 minutes and 2 seconds"),
    WesternTimeDeltaTestData("-43261/43200", -1, 0, -2, Fraction(-2, 1), "-1 day, -2 minutes and -2 seconds"),
    WesternTimeDeltaTestData("86461/43200", 2, 0, 2, Fraction(2, 1), "2 days, 2 minutes and 2 seconds"),
    WesternTimeDeltaTestData("-86461/43200", -2, 0, -2, Fraction(-2, 1), "-2 days, -2 minutes and -2 seconds"),
    # hours, minutes and seconds
    WesternTimeDeltaTestData("3661/86400", 0, 1, 1, Fraction(1, 1), "1 hour, 1 minute and 1 second"),
    WesternTimeDeltaTestData("-3661/86400", 0, -1, -1, Fraction(-1, 1), "-1 hour, -1 minute and -1 second"),
    WesternTimeDeltaTestData("3661/86400", 0, 2, 1, Fraction(1, 1), "2 hours, 1 minute and 1 second"),
    WesternTimeDeltaTestData("-3661/86400", 0, -2, -1, Fraction(-1, 1), "-2 hours, -1 minute and -1 second"),
    WesternTimeDeltaTestData("3721/86400", 0, 1, 2, Fraction(1, 1), "1 hour, 2 minutes and 1 second"),
    WesternTimeDeltaTestData("-3721/86400", 0, -1, -2, Fraction(-1, 1), "-1 hour, -2 minutes and -1 second"),
    WesternTimeDeltaTestData("7321/86400", 0, 2, 2, Fraction(1, 1), "2 hours, 2 minutes and 1 second"),
    WesternTimeDeltaTestData("-7321/86400", 0, -2, -2, Fraction(-1, 1), "-2 hours, -2 minutes and -1 second"),
    WesternTimeDeltaTestData("1831/43200", 0, 1, 1, Fraction(2, 1), "1 hour, 1 minute and 2 seconds"),
    WesternTimeDeltaTestData("-1831/43200", 0, -1, -1, Fraction(-2, 1), "-1 hour, -1 minute and -2 seconds"),
    WesternTimeDeltaTestData("3631/43200", 0, 2, 1, Fraction(2, 1), "2 hours, 1 minute and 2 seconds"),
    WesternTimeDeltaTestData("-3631/43200", 0, -2, -1, Fraction(-2, 1), "-2 hours, -1 minute and -2 seconds"),
    WesternTimeDeltaTestData("1861/43200", 0, 1, 2, Fraction(2, 1), "1 hour, 2 minutes and 2 seconds"),
    WesternTimeDeltaTestData("-1861/43200", 0, -1, -2, Fraction(-2, 1), "-1 hour, -2 minutes and -2 seconds"),
    WesternTimeDeltaTestData("3661/43200", 0, 2, 2, Fraction(2, 1), "2 hours, 2 minutes and 2 seconds"),
    WesternTimeDeltaTestData("-3661/43200", 0, -2, -2, Fraction(-2, 1), "-2 hours, -2 minutes and -2 seconds"),
    # days, hours, minutes and seconds
    WesternTimeDeltaTestData("90061/86400", 1, 1, 1, Fraction(1, 1), "1 day, 1 hour, 1 minute and 1 second"),
    WesternTimeDeltaTestData("-90061/86400", -1, -1, -1, Fraction(-1, 1), "-1 day, -1 hour, -1 minute and -1 second"),
    WesternTimeDeltaTestData("176461/86400", 2, 1, 1, Fraction(1, 1), "2 days, 1 hour, 1 minute and 1 second"),
    WesternTimeDeltaTestData("-176461/86400", -2, -1, -1, Fraction(-1, 1), "-2 days, -1 hour, -1 minute and -1 second"),
    WesternTimeDeltaTestData("90061/86400", 1, 2, 1, Fraction(1, 1), "1 day, 2 hours, 1 minute and 1 second"),
    WesternTimeDeltaTestData("-90061/86400", -1, -2, -1, Fraction(-1, 1), "-1 day, -2 hours, -1 minute and -1 second"),
    WesternTimeDeltaTestData("180061/86400", 2, 2, 1, Fraction(1, 1), "2 day, 2 hours, 1 minute and 1 second"),
    WesternTimeDeltaTestData("-180061/86400", -2, -2, -1, Fraction(-1, 1), "-2 day, -2 hours, -1 minute and -1 second"),
    WesternTimeDeltaTestData("90121/86400", 1, 1, 2, Fraction(1, 1), "1 day, 1 hour, 2 minutes and 1 second"),
    WesternTimeDeltaTestData("-90121/86400", -1, -1, -2, Fraction(-1, 1), "-1 day, -1 hour, -2 minutes and -1 second"),
    WesternTimeDeltaTestData("176521/86400", 2, 1, 2, Fraction(1, 1), "2 days, 1 hour, 2 minutes and 1 second"),
    WesternTimeDeltaTestData("-176521/86400", -2, -1, -2, Fraction(-1, 1), "-2 days, -1 hour, -2 minutes and -1 second"),
    WesternTimeDeltaTestData("93721/86400", 1, 2, 2, Fraction(1, 1), "1 day, 2 hours, 2 minutes and 1 second"),
    WesternTimeDeltaTestData("-93721/86400", -1, -2, -2, Fraction(-1, 1), "-1 day, -2 hours, -2 minutes and -1 second"),
    WesternTimeDeltaTestData("180121/86400", 2, 2, 2, Fraction(1, 1), "2 days, 2 hours, 2 minutes and 1 second"),
    WesternTimeDeltaTestData("-180121/86400", -2, -2, -2, Fraction(-1, 1), "-2 days, -2 hours, -2 minutes and -1 second"),
    WesternTimeDeltaTestData("45031/43200", 1, 1, 1, Fraction(2, 1), "1 day, 1 hour, 1 minute and 2 seconds"),
    WesternTimeDeltaTestData("-45031/43200", -1, -1, -1, Fraction(-2, 1), "-1 day, -1 hour, -1 minute and -2 seconds"),
    WesternTimeDeltaTestData("88231/43200", 2, 1, 1, Fraction(2, 1), "2 days, 1 hour, 1 minute and 2 seconds"),
    WesternTimeDeltaTestData("-88231/43200", -2, -1, -1, Fraction(-2, 1), "-2 days, -1 hour, -1 minute and -2 seconds"),
    WesternTimeDeltaTestData("46831/43200", 1, 2, 1, Fraction(2, 1), "1 day, 2 hours, 1 minute and 2 seconds"),
    WesternTimeDeltaTestData("-46831/43200", -1, -2, -1, Fraction(-2, 1), "-1 day, -2 hours, -1 minute and -2 seconds"),
    WesternTimeDeltaTestData("90031/43200", 2, 2, 1, Fraction(2, 1), "1 day, 2 hours, 1 minute and 2 seconds"),
    WesternTimeDeltaTestData("-90031/43200", -2, -2, -1, Fraction(-2, 1), "-1 day, -2 hours, -1 minute and -2 seconds"),
    WesternTimeDeltaTestData("45061/43200", 1, 1, 2, Fraction(2, 1), "1 day, 1 hour, 2 minutes and 2 seconds"),
    WesternTimeDeltaTestData("-45061/43200", -1, -1, -2, Fraction(-2, 1), "-1 day, -1 hour, -2 minutes and -2 seconds"),
    WesternTimeDeltaTestData("88261/43200", 2, 1, 2, Fraction(2, 1), "2 days, 1 hour, 2 minutes and 2 seconds"),
    WesternTimeDeltaTestData("-88261/43200", -2, -1, -2, Fraction(-2, 1), "-2 days, -1 hour, -2 minutes and -2 seconds"),
    WesternTimeDeltaTestData("46861/43200", 1, 2, 2, Fraction(2, 1), "1 day, 2 hours, 2 minutes and 2 seconds"),
    WesternTimeDeltaTestData("-46861/43200", -1, -2, -2, Fraction(-2, 1), "-1 day, -2 hours, -2 minutes and -2 seconds"),
    WesternTimeDeltaTestData("90061/43200", 2, 2, 2, Fraction(2, 1), "2 days, 2 hours, 2 minutes and 2 seconds"),
    WesternTimeDeltaTestData("-90061/43200", -2, -2, -2, Fraction(-2, 1), "-2 days, -2 hours, -2 minutes and -2 seconds"),
    # truncation of seconds
    WesternTimeDeltaTestData("1/172800", 0, 0, 0, Fraction(1, 2), "0 days"),
    WesternTimeDeltaTestData("-1/172800", 0, 0, 0, Fraction(-1, 2), "0 days"),
    WesternTimeDeltaTestData("1/57600", 0, 0, 0, Fraction(3, 2), "1 second"),
    WesternTimeDeltaTestData("-1/57600", 0, 0, 0, Fraction(-3, 2), "-1 second")
]

western_timedelta_out_of_range_data = [
    WesternTimeDeltaTestData(None, 0, 0, 0, 60, ""),
    WesternTimeDeltaTestData(None, 0, 0, 0, -60, ""),
    WesternTimeDeltaTestData(None, 0, 0, 60, 0, ""),
    WesternTimeDeltaTestData(None, 0, 0, -60, 0, ""),
    WesternTimeDeltaTestData(None, 0, 24, 0, 0, ""),
    WesternTimeDeltaTestData(None, 0, -24, 0, 0, "")
]

western_timedelta_wrong_sign_data = [
    WesternTimeDeltaTestData(None, 1, 1, 1, -1),
    WesternTimeDeltaTestData(None, 1, 1, -1, 1),
    WesternTimeDeltaTestData(None, 1, -1, 1, 1),
    WesternTimeDeltaTestData(None, -1, -1, -1, 1),
    WesternTimeDeltaTestData(None, -1, -1, 1, -1),
    WesternTimeDeltaTestData(None, -1, 1, -1, -1)
]

western_timedelta_microseconds = [
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


def western_timedelta_exactly_equal(first, second):
    return first.days == second.days and first.hours == second.hours and first.minutes == second.minutse and first.seconds == second.seconds


def test_00_constructor():
    # check all types for seconds are accepted
    for integer_second in (4, '4'):
        wtd = WesternTimeDelta(1, 2, 3, integer_second)
        assert isinstance(wtd.days, int)
        assert wtd.days == 1
        assert isinstance(wtd.hours, int)
        assert wtd.hours == 2
        assert isinstance(wtd.minutes, int)
        assert wtd.minute == 3
        assert isinstance(wtd.seconds, Fraction)
        assert wtd.second == Fraction(4, 1)
    for integer_second in (-4, '-4'):
        wtd = WesternTimeDelta(-1, -2, -3, integer_second)
        assert isinstance(wtd.days, int)
        assert wtd.days == -1
        assert isinstance(wtd.hours, int)
        assert wtd.hours == -2
        assert isinstance(wtd.minutes, int)
        assert wtd.minute == -3
        assert isinstance(wtd.seconds, Fraction)
        assert wtd.second == Fraction(-4, 1)
    for fractional_seconds in (11.25, Fraction(45, 4), '11.25', Decimal('11.25'), '45/4'):
        wtd = WesternTimeDelta(2, 3, 4, fractional_seconds)
        assert isinstance(wtd.seconds, Fraction)
        assert wtd.second == Fraction(45, 4)
    for fractional_seconds in (-11.25, Fraction(-45, 4), '-11.25', Decimal('-11.25'), '-45/4'):
        wtd = WesternTimeDelta(-2, -3, -4, fractional_seconds)
        assert isinstance(wtd.seconds, Fraction)
        assert wtd.second == Fraction(-45, 4)

    # exception with none, two or five parameters
    with pytest.raises(TypeError):
        WesternTimeDelta()
    with pytest.raises(TypeError):
        WesternTimeDelta(1, 2)
    with pytest.raises(TypeError):
        WesternTimeDelta(1, 2, 3, 4, 5)

    # exception with non-numeric types
    for invalid_par in ("1", (1,), [1], {1: 1}, (), [], {}, None):
        with pytest.raises(TypeError):
            WesternTimeDelta(invalid_par, 1, 1, 1)
        with pytest.raises(TypeError):
            WesternTimeDelta(invalid_par, -1, -1, -1)
        with pytest.raises(TypeError):
            WesternTimeDelta(1, invalid_par, 1, 1)
        with pytest.raises(TypeError):
            WesternTimeDelta(-1, invalid_par, -1, -1)
        with pytest.raises(TypeError):
            WesternTimeDelta(1, 1, invalid_par, 1)
        with pytest.raises(TypeError):
            WesternTimeDelta(-1, -1, invalid_par, -1)
    for invalid_par in ((1,), [1], {1: 1}, (), [], {}, None): # "1" is acceptable for seconds, since it is a valid Fraction argument
        with pytest.raises(TypeError):
            WesternTimeDelta(1, 1, 1, invalid_par)
        with pytest.raises(TypeError):
            WesternTimeDelta(-1, -1, -1, invalid_par)

    # exception with invalid numeric types
    for invalid_par in (1.0, Fraction(1, 1), Decimal(1), 1j, 1 + 1j, INF, NAN):
        with pytest.raises(TypeError):
            WesternTimeDelta(invalid_par, 1, 1, 1)
        with pytest.raises(TypeError):
            WesternTimeDelta(invalid_par, -1, -1, -1)
        with pytest.raises(TypeError):
            WesternTimeDelta(1, invalid_par, 1, 1)
        with pytest.raises(TypeError):
            WesternTimeDelta(-1, invalid_par, -1, -1)
        with pytest.raises(TypeError):
            WesternTimeDelta(1, 1, invalid_par, 1)
        with pytest.raises(TypeError):
            WesternTimeDelta(-1, -1, invalid_par, -1)
    for invalid_par in (1j, 1 + 1j, INF, NAN):
        with pytest.raises(TypeError):
            WesternTimeDelta(1, 1, 1, invalid_par)
        with pytest.raises(TypeError):
            WesternTimeDelta(-1, -1, -1, invalid_par)

    # valid constructor values
    for test_datum in western_timedelta_test_data:
        days = test_datum.days
        hours = test_datum.hours
        minutes = test_datum.minutes
        seconds = test_datum.seconds
        wtd = WesternTimeDelta(days, hours, minutes, seconds)
        assert (wtd.days, wtd.hours, wtd.minutes, wtd.seconds) == (days, hours, minutes, seconds)

    # invalid constructor values
    for test_datum in western_timedelta_out_of_range_data:
        days = test_datum.days
        hours = test_datum.hours
        minutes = test_datum.minutes
        seconds = test_datum.seconds
        with pytest.raises(ValueError):
            WesternTimeDelta(days, hours, minutes, seconds)
    for test_datum in western_timedelta_wrong_sign_data:
        days = test_datum.days
        hours = test_datum.hours
        minutes = test_datum.minutes
        seconds = test_datum.seconds
        with pytest.raises(ValueError):
            WesternTimeDelta(days, hours, minutes, seconds)


def test_02_constructor_from_fractional_days():
    # valid types
    for test_datum in western_timedelta_test_data:
        wtd1 = WesternTimeDelta.from_fractional_days(test_datum.fractional_days)
        assert isinstance(wtd1.days, int)
        assert isinstance(wtd1.hours, int)
        assert isinstance(wtd1.minutes, int)
        assert isinstance(wtd1.seconds, Fraction)

    # exception with none, one or three parameters
    with pytest.raises(TypeError):
        WesternTimeDelta.from_fractional_days()
    with pytest.raises(TypeError):
        WesternTimeDelta.from_fractional_days(1, 2)

    # exception with non-numeric types
    for invalid_time_interval in ("1", (1,), [1], {1: 1}, (), [], {}, None):
        with pytest.raises(TypeError):
            WesternTimeDelta.from_fractional_days(invalid_time_interval)

    # exception with invalid numeric types
    for invalid_time_interval in (1.0, Decimal(1), 1j, 1 + 1j, INF, NAN):
        with pytest.raises(TypeError):
            WesternTimeDelta.from_fractional_days(invalid_time_interval)

    # valid values
    for test_datum in western_timedelta_test_data:
        fractional_days = Fraction(test_datum.fractional_days)
        days = test_datum.days
        hours = test_datum.hours
        minutes = test_datum.minutes
        seconds = test_datum.seconds
        wtd1 = WesternTimeDelta.from_fractional_days(fractional_days)
        assert (wtd1.days, wtd1.hours, wtd1.minutes, wtd1.seconds) == (days, hours, minutes, seconds)


def test_20_attributes():
    wtd = WesternTimeDelta(11, 12, 13, 14)
    with pytest.raises(AttributeError):
        wtd.days = 3
    with pytest.raises(AttributeError):
        wtd.hours = 3
    with pytest.raises(AttributeError):
        wtd.minutes = 3
    with pytest.raises(AttributeError):
        wtd.seconds = 3


def test_30_repr():
    import datetime2
    for test_datum in western_timedelta_test_data:
        days = test_datum.days
        hours = test_datum.hours
        minutes = test_datum.minutes
        seconds = test_datum.seconds
        wtd = WesternTimeDelta(days, hours, minutes, seconds)
        wtd_repr = repr(wtd)
        assert wtd_repr.startswith('datetime2.western.WesternTimeDelta(') and wtd_repr.endswith(')')
        args = wtd_repr[35:-1]
        found_days, found_hours, found_minutes, found_seconds = args.split(',', 3)
        assert western_timedelta_exactly_equal(wtd, eval(wtd_repr))
        assert int(found_days.strip()) == days
        assert int(found_hours.strip()) == hours
        assert int(found_minutes.strip()) == minutes
        assert eval(found_seconds) == seconds


def test_31_str():
    for test_datum in western_timedelta_test_data:
        days = test_datum.days
        hours = test_datum.hours
        minutes = test_datum.minutes
        seconds = test_datum.seconds
        wtd = WesternTimeDelta(days, hours, minutes, seconds)
        assert str(wtd) == test_datum.expected


def test_32_cformat():
    for test_datum in western_timedelta_test_data:
        days = test_datum.days
        hours = test_datum.hours
        minutes = test_datum.minutes
        seconds = test_datum.seconds
        wtd = WesternTimeDelta(days, hours, minutes, seconds)
        assert wtd.cformat('%d') == f'{days}'
        assert wtd.cformat('%H') == f'{hours:02d}'
        assert wtd.cformat('%M') == f'{minutes:02d}'
        assert wtd.cformat('%S') == f'{int(seconds):02d}'

    # microseconds
    for fraction, microseconds in western_timedelta_microseconds:
        wtd = WesternTimeDelta(12, 34, Fraction(fraction) + 56)
        assert wtd.cformat('%f') == microseconds

    # percent
    wtd = WesternTimeDelta(1, 2, 3, 4)
    assert wtd.cformat('%') == '%'
    assert wtd.cformat('%%') == '%'
    assert wtd.cformat('%%%') == '%%'
    assert wtd.cformat('abcd%') == 'abcd%'
    assert wtd.cformat('%k') == '%k'
    assert wtd.cformat('a%k') == 'a%k'
    assert wtd.cformat('%k%') == '%k%'

    # invalid types
    for par in (1, (1,), [1], {1: 1}, None):
        with pytest.raises(TypeError):
            wtd.cformat(par)


def test_50_to_fractional_days():
    for test_datum in western_timedelta_test_data:
        fractional_days = Fraction(test_datum.fractional_days)
        days = test_datum.days
        hours = test_datum.hours
        minutes = test_datum.minutes
        seconds = test_datum.seconds
        assert WesternTimeDelta(days, hours, minutes, seconds).to_fractional_days() == fractional_days


def test_51_replace():
    for test_datum in western_timedelta_test_data:
        days = test_datum.days
        hours = test_datum.hours
        minutes = test_datum.minutes
        seconds = test_datum.seconds
        wtd = WesternTimeDelta(days, hours, minutes, seconds)
        assert western_timedelta_exactly_equal(wtd.replace(),  WesternTimeDelta(days, hours, minutes, seconds))
        assert western_timedelta_exactly_equal(wtd.replace(days=12),  WesternTimeDelta(12, hours, minutes, seconds))
        assert western_timedelta_exactly_equal(wtd.replace(hours=11),  WesternTimeDelta(days, 11, minutes, seconds))
        assert western_timedelta_exactly_equal(wtd.replace(minutes=10),  WesternTimeDelta(days, hours, 10, seconds))
        assert western_timedelta_exactly_equal(wtd.replace(seconds=9),  WesternTimeDelta(days, hours, minutes, 9))
        assert western_timedelta_exactly_equal(wtd.replace(hours=11, days=12),  WesternTimeDelta(12, 11, minutes, seconds))
        assert western_timedelta_exactly_equal(wtd.replace(minutes=10, days=12),  WesternTimeDelta(12, hours, 10, seconds))
        assert western_timedelta_exactly_equal(wtd.replace(seconds=9, days=12),  WesternTimeDelta(12, hours, minutes, 9))
        assert western_timedelta_exactly_equal(wtd.replace(minutes=10, hours=11),  WesternTimeDelta(days, 11, 10, seconds))
        assert western_timedelta_exactly_equal(wtd.replace(seconds=9, hours=11),  WesternTimeDelta(days, 11, minutes, 9))
        assert western_timedelta_exactly_equal(wtd.replace(seconds=9, minutes=10),  WesternTimeDelta(days, hours, 10, 9))
        assert western_timedelta_exactly_equal(wtd.replace(minutes=10, hours=11, days=12),  WesternTimeDelta(12, 11, 10, seconds))
        assert western_timedelta_exactly_equal(wtd.replace(seconds=9, hours=11, days=12),  WesternTimeDelta(12, 11, 9, seconds))
        assert western_timedelta_exactly_equal(wtd.replace(seconds=9, minutes=10, days=12),  WesternTimeDelta(12, hours, 10, 9))
        assert western_timedelta_exactly_equal(wtd.replace(seconds=9, minutes=10, hours=11),  WesternTimeDelta(days, 11, 10, 9))
        assert western_timedelta_exactly_equal(wtd.replace(second=9, minute=10, hour=11, days=12),  WesternTimeDelta(12, 11, 10, 9))

    # invalid types
    wtd = WesternTimeDelta(12, 11, 10, 9)
    # exception for positional parameters
    with pytest.raises(TypeError):
        wtd.replace(1)
    # exception with non-numeric types
    for par in ("1", (1,), [1], {1: 1}, (), [], {}):
        with pytest.raises(TypeError):
            wtd.replace(hour=par)
        with pytest.raises(TypeError):
            wtd.replace(minute=par)
    for par in ((1,), [1], {1: 1}, (), [], {}):
        with pytest.raises(TypeError):
            wtd.replace(second=par)
    # exception with invalid numeric types
    for par in (1.0, Fraction(1, 1), Decimal(1), 1j, 1 + 1j, INF, NAN):
        with pytest.raises(TypeError):
            wtd.replace(hour=par)
        with pytest.raises(TypeError):
            wtd.replace(minute=par)
    for par in (1j, 1 + 1j, INF):
        with pytest.raises(TypeError):
            wtd.replace(second=par)

    # invalid values
    with pytest.raises(ValueError):
        wtd.replace(hour=-1)
    with pytest.raises(ValueError):
        wtd.replace(hour=24)
    with pytest.raises(ValueError):
        wtd.replace(minute=-1)
    with pytest.raises(ValueError):
        wtd.replace(minute=60)
    with pytest.raises(ValueError):
        wtd.replace(second='-1/1000000')
    with pytest.raises(ValueError):
        wtd.replace(second=60)
    with pytest.raises(TypeError):
        wtd.replace(second=NAN)
