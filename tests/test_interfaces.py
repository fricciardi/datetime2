# datetime2 base class interface test

# Copyright (c) 2011-2022 Francesco Ricciardi
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

__author__ = "Francesco Ricciardi <francescor2010 at yahoo.it>"


from fractions import Fraction
import pytest

from datetime2 import Date, Time, TimeDelta


#############################################################################
# Date interface
#
class ExampleTestCalendar:  # probably one of the simplest form, it is also used in documentation as example
    def __init__(self, week, day):
        self.week = week
        self.day = day

    @classmethod
    def from_rata_die(cls, rata_die):
        return cls((rata_die - 1) // 7 + 1, (rata_die - 1) % 7 + 1)

    def to_rata_die(self):
        return 7 * (self.week - 1) + self.day


@pytest.fixture
def clean_Date(request):
    def clear_Date_class():
        for name in [name for name in Date.__dict__.keys() if name.startswith("test_")]:
            delattr(Date, name)

    request.addfinalizer(clear_Date_class)


def test_000_register_new_calendar(clean_Date):
    # valid call
    assert not hasattr(Date, "test_1")
    with pytest.raises(AttributeError):
        Date.test_1
    Date.register_new_calendar("test_1", ExampleTestCalendar)
    assert hasattr(Date, "test_1")
    Date.test_1

    with pytest.raises(AttributeError):
        Date.register_new_calendar("gregorian", ExampleTestCalendar)
    with pytest.raises(AttributeError):
        Date.register_new_calendar("day_count", ExampleTestCalendar)

    with pytest.raises(ValueError):
        Date.register_new_calendar("", ExampleTestCalendar)
    with pytest.raises(ValueError):
        Date.register_new_calendar("123new", ExampleTestCalendar)
    with pytest.raises(ValueError):
        Date.register_new_calendar(123, ExampleTestCalendar)

    class NoFromCalendar:  # without from_rata_die
        def __init__(self, week, day):
            self.week = week
            self.day = day

        def to_rata_die(self):
            return 7 * (self.week - 1) + self.day

    with pytest.raises(TypeError):
        Date.register_new_calendar("test_2", NoFromCalendar)

    class NoToCalendar:  # without to_rata_die
        def __init__(self, week, day):
            self.week = week
            self.day = day

        @classmethod
        def from_rata_die(cls, rata_die):
            return cls((rata_die - 1) // 7 + 1, (rata_die - 1) % 7 + 1)

    with pytest.raises(TypeError):
        Date.register_new_calendar("test_2", NoToCalendar)


def test_010_registered_cal_attribute_simple_class(clean_Date):
    Date.register_new_calendar("test_1", ExampleTestCalendar)

    # Date attribute type and metaclass are correct
    assert Date.test_1.__name__ == "ExampleTestCalendarInDate"
    assert type(Date.test_1).__name__ == "ModifiedClass"
    assert issubclass(Date.test_1, ExampleTestCalendar)

    # constructed date type and value are is correct
    d1a = Date.test_1(100, 4)
    assert type(d1a) == Date
    assert d1a.day_count == 697

    # new attribute on date instance, type and value are correct
    d1b = Date(1000)
    assert isinstance(d1b.test_1, ExampleTestCalendar)
    assert type(d1b.test_1).__name__ == "ExampleTestCalendarInDate"
    assert type(type(d1b.test_1)).__name__ == "ModifiedClass"
    assert d1b.test_1.week == 143
    assert d1b.test_1.day == 6

    # new attribute on date instance build by another calendar, type and value are correct
    d1c = Date.gregorian(100, 2, 3)
    assert isinstance(d1c.test_1, ExampleTestCalendar)
    assert type(d1c.test_1).__name__ == "ExampleTestCalendarInDate"
    assert type(type(d1c.test_1)).__name__ == "ModifiedClass"
    assert d1c.test_1.week == 5171
    assert d1c.test_1.day == 3


def test_012_registered_cal_attribute_class_with_other_constructors(clean_Date):
    class ExampleTestCalendar2(ExampleTestCalendar):
        @classmethod
        def with_thousands(cls, thousands, week, day):
            return cls(1000 * thousands + week, day)

    Date.register_new_calendar("test_2", ExampleTestCalendar2)

    # Date attribute type and metaclass are correct
    assert Date.test_2.__name__ == "ExampleTestCalendar2InDate"
    assert type(Date.test_2).__name__ == "ModifiedClass"
    assert issubclass(Date.test_2, ExampleTestCalendar)

    # constructed date type and value are is correct
    d2a = Date.test_2(100, 4)
    assert type(d2a) == Date
    assert d2a.day_count == 697
    d2d = Date.test_2.with_thousands(2, 3, 4)
    assert type(d2d) == Date
    assert d2d.day_count == 14018

    # new attribute on date instance, type and value are correct
    d2b = Date(1000)
    assert isinstance(d2b.test_2, ExampleTestCalendar2)
    assert type(d2b.test_2).__name__ == "ExampleTestCalendar2InDate"
    assert type(type(d2b.test_2)).__name__ == "ModifiedClass"
    assert d2b.test_2.week == 143
    assert d2b.test_2.day == 6

    # new attribute on date instance build by another calendar, type and value are correct
    d2c = Date.gregorian(100, 2, 3)
    assert isinstance(d2c.test_2, ExampleTestCalendar2)
    assert type(d2c.test_2).__name__ == "ExampleTestCalendar2InDate"
    assert type(type(d2c.test_2)).__name__ == "ModifiedClass"
    assert d2c.test_2.week == 5171
    assert d2c.test_2.day == 3


def test_014_registered_cal_attribute_class_with_static_methods(clean_Date):
    class ExampleTestCalendar3(ExampleTestCalendar):
        @staticmethod
        def is_odd(number):
            return (number % 2) == 1

    Date.register_new_calendar("test_3", ExampleTestCalendar3)

    # Date attribute type and metaclass are correct
    assert Date.test_3.__name__ == "ExampleTestCalendar3InDate"
    assert type(Date.test_3).__name__ == "ModifiedClass"
    assert issubclass(Date.test_3, ExampleTestCalendar)

    # constructed date type and value are is correct
    d3a = Date.test_3(100, 4)
    assert type(d3a) == Date
    assert d3a.day_count == 697

    # new attribute on date instance, type and value are correct
    d3b = Date(1000)
    assert isinstance(d3b.test_3, ExampleTestCalendar3)
    assert type(d3b.test_3).__name__ == "ExampleTestCalendar3InDate"
    assert type(type(d3b.test_3)).__name__ == "ModifiedClass"
    assert d3b.test_3.week == 143
    assert d3b.test_3.day == 6

    # new attribute on date instance build by another calendar, type and value are correct
    d3c = Date.gregorian(100, 2, 3)
    assert isinstance(d3c.test_3, ExampleTestCalendar3)
    assert type(d3c.test_3).__name__ == "ExampleTestCalendar3InDate"
    assert type(type(d3c.test_3)).__name__ == "ModifiedClass"
    assert d3c.test_3.week == 5171
    assert d3c.test_3.day == 3

    # static method can be reached on the class and on all types of instance
    assert Date.test_3.is_odd(3)
    assert not Date.test_3.is_odd(4)
    assert d3a.test_3.is_odd(3)
    assert not d3a.test_3.is_odd(4)
    assert d3b.test_3.is_odd(3)
    assert not d3b.test_3.is_odd(4)
    assert d3c.test_3.is_odd(3)
    assert not d3c.test_3.is_odd(4)


def test_016_Date_has_attributes_but_instance_not():
    # the date class aways has a registered attribute
    assert hasattr(Date, "gregorian")
    assert Date.gregorian
    # an instance created with another calendar or by Date does not have
    #   the attribute; it is instead is reachable via the Date class
    d1 = Date(4)
    with pytest.raises(KeyError):
        d1.__dict__["gregorian"]
    assert hasattr(d1, "gregorian")
    d1.gregorian
    d2 = Date.iso(3, 4, 5)
    with pytest.raises(KeyError):
        d2.__dict__["gregorian"]
    assert hasattr(d2, "gregorian")
    d2.gregorian
    # a Date instance created via the calendar does have the same attribute
    d3 = Date.gregorian(3, 4, 5)
    assert hasattr(d3, "gregorian")
    d3.gregorian


def test_090_avoid_date_override():
    # In the past it happened that a date instance, created via a Gregorian calendar,
    # was able to directly get an attribute which instead belonged to the calendar class.
    # This is not desirable, better must be thought as an error.
    d = Date.gregorian(1, 1, 1)
    with pytest.raises(AttributeError):
        getattr(d, "is_leap_year")
    with pytest.raises(AttributeError):
        d.is_leap_year


#############################################################################
# Time interface
#
class ExampleTestTimeRepresentation:
    # a fictional representation where there are 100 hours in a day and 100 minutes in an hour
    # (e.g. a minute in this representation is less than a second in the western time representation)
    def __init__(self, hour100, minute100):
        self.hour100 = hour100
        self.minute100 = minute100

    @classmethod
    def from_time_pair(cls, day_frac, utcoffset=None):
        minutes_tot = day_frac * 10000
        hour100 = int(minutes_tot / 100)
        return cls(hour100, minutes_tot - hour100 * 100)

    def to_time_pair(self):
        return Fraction(self.hour100 * 100 + self.minute100, 10000), None


@pytest.fixture
def clean_Time(request):
    def clear_Time_class():
        for name in [name for name in Time.__dict__.keys() if name.startswith("test_")]:
            delattr(Time, name)

    request.addfinalizer(clear_Time_class)


def test_200_register_new_time_repr(clean_Time):
    # valid call
    assert not hasattr(Time, "test_1")
    with pytest.raises(AttributeError):
        Time.test_1
    Time.register_new_time("test_1", ExampleTestTimeRepresentation)
    assert hasattr(Time, "test_1")
    Time.test_1

    # existing time repr or attribute
    with pytest.raises(AttributeError):
        Time.register_new_time("western", ExampleTestTimeRepresentation)
    with pytest.raises(AttributeError):
        Time.register_new_time("day_frac", ExampleTestTimeRepresentation)

    # invalid attribute name
    with pytest.raises(ValueError):
        Time.register_new_time("", ExampleTestTimeRepresentation)
    with pytest.raises(ValueError):
        Time.register_new_time("123new", ExampleTestTimeRepresentation)
    with pytest.raises(ValueError):
        Time.register_new_time(123, ExampleTestTimeRepresentation)

    # invalid time repr class
    class NoFromTimeRepr:  # without from_time_pair
        def __init__(self, hour100, minute100):
            self.hour100 = hour100
            self.minute100 = minute100

        def to_time_pair(self):
            return Fraction(self.hour100 * 100 + self.minute100, 10000), None

    with pytest.raises(TypeError):
        Time.register_new_time("test_2", NoFromTimeRepr)

    class NoToTimeRepr:  # without to_time_pair
        def __init__(self, hour100, minute100):
            self.hour100 = hour100
            self.minute100 = minute100

        @classmethod
        def from_time_pair(cls, day_frac):
            minutes_tot = day_frac * 10000
            hour100 = int(minutes_tot / 100)
            return cls(hour100, minutes_tot - hour100 * 100)

    with pytest.raises(TypeError):
        Time.register_new_time("test_2", NoToTimeRepr)


def test_210_registered_time_attribute_simple_class(clean_Time):
    Time.register_new_time("test_1", ExampleTestTimeRepresentation)

    # Time attribute type and metaclass are correct
    assert Time.test_1.__name__ == "ExampleTestTimeRepresentationInTime"
    assert type(Time.test_1).__name__ == "ModifiedClass"
    assert issubclass(Time.test_1, ExampleTestTimeRepresentation)

    # constructed Time type and value are is correct
    t1a = Time.test_1(10, 8)
    assert type(t1a) == Time
    assert t1a.day_frac == Fraction(63, 625)

    # new attribute on Time instance, type and value are correct
    t1b = Time("963/1250")
    assert isinstance(t1b.test_1, ExampleTestTimeRepresentation)
    assert type(t1b.test_1).__name__ == "ExampleTestTimeRepresentationInTime"
    assert type(type(t1b.test_1)).__name__ == "ModifiedClass"
    assert t1b.test_1.hour100 == 77
    assert t1b.test_1.minute100 == 4

    # new attribute on Time instance build by another calendar, type and value are correct
    t1c = Time.western(10, 35, 15)
    assert isinstance(t1c.test_1, ExampleTestTimeRepresentation)
    assert type(t1c.test_1).__name__ == "ExampleTestTimeRepresentationInTime"
    assert type(type(t1c.test_1)).__name__ == "ModifiedClass"
    assert t1c.test_1.hour100 == 44
    assert t1c.test_1.minute100 == Fraction("275/24")


def test_212_registered_time_attribute_class_with_other_constructors(clean_Time):
    class ExampleTestTimeRepresentation2(ExampleTestTimeRepresentation):
        @classmethod
        def with_seconds(cls, hour100, minute100, second100):
            return cls(hour100, minute100 + Fraction(second100, 100))

    Time.register_new_time("test_2", ExampleTestTimeRepresentation2)

    # Time attribute type and metaclass are correct
    assert Time.test_2.__name__ == "ExampleTestTimeRepresentation2InTime"
    assert type(Time.test_2).__name__ == "ModifiedClass"
    assert issubclass(Time.test_2, ExampleTestTimeRepresentation)

    # constructed Time type and value are is correct
    t2a = Time.test_2(10, 8)
    assert type(t2a) == Time
    assert t2a.day_frac == Fraction(63, 625)
    d2d = Time.test_2.with_seconds(40, 40, 40)
    assert type(d2d) == Time
    assert d2d.day_frac == Fraction("10101/25000")

    # new attribute on Time instance, type and value are correct
    t2b = Time("963/1250")
    assert isinstance(t2b.test_2, ExampleTestTimeRepresentation2)
    assert type(t2b.test_2).__name__ == "ExampleTestTimeRepresentation2InTime"
    assert type(type(t2b.test_2)).__name__ == "ModifiedClass"
    assert t2b.test_2.hour100 == 77
    assert t2b.test_2.minute100 == 4

    # new attribute on Time instance build by another calendar, type and value are correct
    t2c = Time.western(10, 35, 15)
    assert isinstance(t2c.test_2, ExampleTestTimeRepresentation2)
    assert type(t2c.test_2).__name__ == "ExampleTestTimeRepresentation2InTime"
    assert type(type(t2c.test_2)).__name__ == "ModifiedClass"
    assert t2c.test_2.hour100 == 44
    assert t2c.test_2.minute100 == Fraction("275/24")


def test_214_registered_time_attribute_class_with_static_methods(clean_Time):
    class ExampleTestTimeRepresentation3(ExampleTestTimeRepresentation):
        @staticmethod
        def is_odd(number):
            return (number % 2) == 1

    Time.register_new_time("test_3", ExampleTestTimeRepresentation3)

    # Time attribute type and metaclass are correct
    assert Time.test_3.__name__ == "ExampleTestTimeRepresentation3InTime"
    assert type(Time.test_3).__name__ == "ModifiedClass"
    assert issubclass(Time.test_3, ExampleTestTimeRepresentation)

    # constructed Time type and value are is correct
    t3a = Time.test_3(10, 8)
    assert type(t3a) == Time
    assert t3a.day_frac == Fraction(63, 625)

    # new attribute on Time instance, type and value are correct
    t3b = Time("963/1250")
    assert isinstance(t3b.test_3, ExampleTestTimeRepresentation3)
    assert type(t3b.test_3).__name__ == "ExampleTestTimeRepresentation3InTime"
    assert type(type(t3b.test_3)).__name__ == "ModifiedClass"
    assert t3b.test_3.hour100 == 77
    assert t3b.test_3.minute100 == 4

    # new attribute on Time instance build by another calendar, type and value are correct
    t3c = Time.western(10, 35, 15)
    assert isinstance(t3c.test_3, ExampleTestTimeRepresentation3)
    assert type(t3c.test_3).__name__ == "ExampleTestTimeRepresentation3InTime"
    assert type(type(t3c.test_3)).__name__ == "ModifiedClass"
    assert t3c.test_3.hour100 == 44
    assert t3c.test_3.minute100 == Fraction("275/24")

    # static method can be reached on the class and on all types of instance
    assert Time.test_3.is_odd(3)
    assert not Time.test_3.is_odd(4)
    assert t3a.test_3.is_odd(3)
    assert not t3a.test_3.is_odd(4)
    assert t3b.test_3.is_odd(3)
    assert not t3b.test_3.is_odd(4)
    assert t3c.test_3.is_odd(3)
    assert not t3c.test_3.is_odd(4)


def test_216_Time_has_attributes_but_instance_not():
    # the Time class always has a registered attribute
    assert hasattr(Time, "western")
    assert Time.western
    # an instance created with another calendar or by Time does not have
    #   the attribute; it is instead is reachable via the Time class
    t1 = Time("4/10")
    with pytest.raises(KeyError):
        t1.__dict__["western"]
    assert hasattr(t1, "western")
    t1.western
    t2 = Time.internet(345)
    with pytest.raises(KeyError):
        t2.__dict__["western"]
    assert hasattr(t2, "western")
    t2.western
    # a Time instance created via the time class does have the same attribute
    t3 = Time.western(3, 4, 5)
    assert hasattr(t3, "western")
    t3.western


def test_230_naivety_is_preserved():
    class NaivetyCheck:
        def __init__(self, hour100, minute100, utcoffset=None):
            self.hour100 = hour100
            self.minute100 = minute100
            self.utcoffset = utcoffset

        def to_time_pair(self):
            return Fraction(self.hour100 * 100 + self.minute100, 10000), self.utcoffset

        @classmethod
        def from_time_pair(cls, day_frac, utcoffset=None):
            minutes_tot = day_frac * 10000
            hour100 = int(minutes_tot / 100)
            return cls(hour100, minutes_tot - hour100 * 100, utcoffset=utcoffset)

    Time.register_new_time("test_1", NaivetyCheck)

    t1 = Time("17/24")
    assert t1.test_1.utcoffset is None

    t2 = Time("17/24", utcoffset=0)
    assert t2.test_1.utcoffset is not None

    t3 = Time.test_1(11, 12)
    assert t3.utcoffset is None

    t4 = Time.test_1(11, 12, utcoffset=0)
    assert t4.utcoffset is not None


#############################################################################
# TimeDelta interface
#
class ExampleTestTimeInterval:
    # a fictional time interval given in days and thousandths of a day
    def __init__(self, days, thousandths):
        self.days = days
        self.thousandths = thousandths

    @classmethod
    def from_fractional_days(cls, fractional_days):
        days = int(fractional_days)
        return cls(days, (fractional_days - days) * 1000)

    def to_fractional_days(self):
        return Fraction(self.thousandths, 1000) + self.days


@pytest.fixture
def clean_TimeDelta(request):
    def clear_TimeDelta_class():
        for name in [name for name in TimeDelta.__dict__.keys() if name.startswith("test_")]:
            delattr(TimeDelta, name)

    request.addfinalizer(clear_TimeDelta_class)


def test_400_register_new_time_interval(clean_TimeDelta):
    # valid call
    assert not hasattr(TimeDelta, "test_1")
    with pytest.raises(AttributeError):
        TimeDelta.test_1
    TimeDelta.register_new_time_interval("test_1", ExampleTestTimeInterval)
    assert hasattr(TimeDelta, "test_1")
    TimeDelta.test_1

    # existing time interval or attribute
    with pytest.raises(AttributeError):
        TimeDelta.register_new_time_interval("western", ExampleTestTimeInterval)
    with pytest.raises(AttributeError):
        TimeDelta.register_new_time_interval("frac", ExampleTestTimeInterval)

    # invalid attribute name
    with pytest.raises(ValueError):
        TimeDelta.register_new_time_interval("", ExampleTestTimeInterval)
    with pytest.raises(ValueError):
        TimeDelta.register_new_time_interval("123new", ExampleTestTimeInterval)
    with pytest.raises(ValueError):
        TimeDelta.register_new_time_interval(123, ExampleTestTimeInterval)

    # invalid time repr class
    class WithoutFromFractional:  # without from_fractional_days
        def __init__(self, days, thousandths):
            self.days = days
            self.thousandths = thousandths

        def to_fractional_days(self):
            return self.thousandths / 1000 + self.days

    with pytest.raises(TypeError):
        TimeDelta.register_new_time_interval("test_2", WithoutFromFractional)

    class WithoutToFractional:  # without to_time_pair
        def __init__(self, days, thousandths):
            self.days = days
            self.thousandths = thousandths

        @classmethod
        def from_fractional_days(cls, fractional_days):
            days = int(fractional_days)
            return cls(days, (fractional_days - days) * 1000)

    with pytest.raises(TypeError):
        TimeDelta.register_new_time_interval("test_2", WithoutToFractional)


def test_410_registered_time_attribute_simple_class(clean_TimeDelta):
    TimeDelta.register_new_time_interval("test_1", ExampleTestTimeInterval)

    # Time attribute type and metaclass are correct
    assert TimeDelta.test_1.__name__ == "ExampleTestTimeIntervalInTimeDelta"
    assert type(TimeDelta.test_1).__name__ == "ModifiedClass"
    assert issubclass(TimeDelta.test_1, ExampleTestTimeInterval)

    # constructed TimeDelta type and value are is correct
    td1 = TimeDelta.test_1(2, 222)
    assert type(td1) == TimeDelta
    assert td1.fractional_days == Fraction(1111, 500)

    # new attribute on TimeDelta instance, type and value are correct
    td2 = TimeDelta("12511/653")
    assert isinstance(td2.test_1, ExampleTestTimeInterval)
    assert type(td2.test_1).__name__ == "ExampleTestTimeIntervalInTimeDelta"
    assert type(type(td2.test_1)).__name__ == "ModifiedClass"
    assert td2.test_1.days == 19
    assert td2.test_1.thousandths == Fraction(104000, 653)

    # new attribute on TimeDelta instance build by another calendar, type and value are correct
    td3 = TimeDelta.western(12, 23, 34, 45)
    assert isinstance(td3.test_1, ExampleTestTimeInterval)
    assert type(td3.test_1).__name__ == "ExampleTestTimeIntervalInTimeDelta"
    assert type(type(td3.test_1)).__name__ == "ModifiedClass"
    assert td3.test_1.days == 12
    assert td3.test_1.thousandths == Fraction("141475/144")


def test_412_registered_timedelta_attribute_class_with_other_constructors(clean_TimeDelta):
    class ExampleTestTimeInterval2(ExampleTestTimeInterval):
        @classmethod
        def with_microdays(cls, days, thousandths, udays):
            return cls(days, thousandths + Fraction(udays, 1000))

    TimeDelta.register_new_time_interval("test_2", ExampleTestTimeInterval2)

    # TimeDelta attribute type and metaclass are correct
    assert TimeDelta.test_2.__name__ == "ExampleTestTimeInterval2InTimeDelta"
    assert type(TimeDelta.test_2).__name__ == "ModifiedClass"
    assert issubclass(TimeDelta.test_2, ExampleTestTimeInterval)

    # constructed TimeDelta type and value are is correct
    td1 = TimeDelta.test_2(1, 234)
    assert type(td1) == TimeDelta
    assert td1.fractional_days == Fraction(617, 500)
    td2 = TimeDelta.test_2.with_microdays(40, 123, 456)
    assert type(td2) == TimeDelta
    assert td2.fractional_days == Fraction(626929, 15625)

    # new attribute on TimeDelta instance, type and value are correct
    td3 = TimeDelta("1963/1250")
    assert isinstance(td3.test_2, ExampleTestTimeInterval2)
    assert type(td3.test_2).__name__ == "ExampleTestTimeInterval2InTimeDelta"
    assert type(type(td3.test_2)).__name__ == "ModifiedClass"
    assert td3.test_2.days == 1
    assert td3.test_2.thousandths == Fraction(2852, 5)

    # new attribute on TimeDelta instance build by another calendar, type and value are correct
    td4 = TimeDelta.western(9, 10, 11, 12)
    assert isinstance(td4.test_2, ExampleTestTimeInterval2)
    assert type(td4.test_2).__name__ == "ExampleTestTimeInterval2InTimeDelta"
    assert type(type(td4.test_2)).__name__ == "ModifiedClass"
    assert td4.test_2.days == 9
    assert td4.test_2.thousandths == Fraction(3820, 9)


def test_414_registered_timedelta_attribute_class_with_static_methods(clean_TimeDelta):
    class ExampleTestTimeInterval3(ExampleTestTimeInterval):
        @staticmethod
        def is_odd(number):
            return (number % 2) == 1

    TimeDelta.register_new_time_interval("test_3", ExampleTestTimeInterval3)

    # Time attribute type and metaclass are correct
    assert TimeDelta.test_3.__name__ == "ExampleTestTimeInterval3InTimeDelta"
    assert type(TimeDelta.test_3).__name__ == "ModifiedClass"
    assert issubclass(TimeDelta.test_3, ExampleTestTimeInterval)

    # constructed Time type and value are is correct
    td1 = TimeDelta.test_3(3, 789)
    assert type(td1) == TimeDelta
    assert td1.fractional_days == Fraction(3789, 1000)

    # new attribute on Time instance, type and value are correct
    td2 = TimeDelta("11250/963")
    assert isinstance(td2.test_3, ExampleTestTimeInterval3)
    assert type(td2.test_3).__name__ == "ExampleTestTimeInterval3InTimeDelta"
    assert type(type(td2.test_3)).__name__ == "ModifiedClass"
    assert td2.test_3.days == 11
    assert td2.test_3.thousandths == Fraction(73000, 107)

    # new attribute on Time instance build by another calendar, type and value are correct
    td3 = TimeDelta.western(12, 11, 10, 9)
    assert isinstance(td3.test_3, ExampleTestTimeInterval3)
    assert type(td3.test_3).__name__ == "ExampleTestTimeInterval3InTimeDelta"
    assert type(type(td3.test_3)).__name__ == "ModifiedClass"
    assert td3.test_3.days == 12
    assert td3.test_3.thousandths == Fraction(67015, 144)

    # static method can be reached on the class and on all types of instance
    assert TimeDelta.test_3.is_odd(3)
    assert not TimeDelta.test_3.is_odd(4)
    assert td1.test_3.is_odd(3)
    assert not td1.test_3.is_odd(4)
    assert td2.test_3.is_odd(3)
    assert not td2.test_3.is_odd(4)
    assert td3.test_3.is_odd(3)
    assert not td3.test_3.is_odd(4)


def test_416_TimeDelta_has_attributes_but_instance_not():
    # the TimeDelta class always has a registered attribute
    assert hasattr(TimeDelta, "western")
    assert TimeDelta.western
    # an instance created with another time interval or directly by TimeDelta
    # does not have the attribute; it is instead is reachable via the Time
    # class
    td1 = TimeDelta(1234, 567)
    with pytest.raises(KeyError):
        td1.__dict__["western"]
    assert hasattr(td1, "western")
    td1.western
    # TODO: if and when we'll have another time interval class we'll add it here
    # td2 = TimeDelta.internet(345)
    # with pytest.raises(KeyError):
    #     td2.__dict__["western"]
    # assert hasattr(td2, "western")
    # td2.western
    # a TimeDelta instance created via the time interval class does have the
    # same attribute
    td3 = TimeDelta.western(3, 4, 5, 6)
    assert hasattr(td3, "western")
    td3.western

