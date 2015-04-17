# datetime2 base class interface test

# Copyright (c) 2011-2012 Francesco Ricciardi
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

import pytest

from datetime2 import Date, TimeDelta


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
    def clead_Date_class():
        for name in [name for name in Date.__dict__.keys() if name.startswith('test_')]:
            delattr(Date, name)

    request.addfinalizer(clead_Date_class)

class TestCalendarInterface():
    def test_000_register_new_calendar(self, clean_Date):
        assert not hasattr(Date, 'test_1')
        with pytest.raises(AttributeError):
            Date.test_1
        Date.register_new_calendar('test_1', ExampleTestCalendar)
        assert hasattr(Date, 'test_1')
        assert Date.test_1

    def test_010_register_new_calendar_existing_calendar_or_attribute(self):
        with pytest.raises(AttributeError):
            Date.register_new_calendar('gregorian', ExampleTestCalendar)
        with pytest.raises(AttributeError):
            Date.register_new_calendar('day_count', ExampleTestCalendar)

    def test_020_register_new_calendar_invalid_attribute_name(self):
        with pytest.raises(ValueError):
            Date.register_new_calendar('', ExampleTestCalendar)
        with pytest.raises(ValueError):
            Date.register_new_calendar('123new', ExampleTestCalendar)
        with pytest.raises(ValueError):
            Date.register_new_calendar(123, ExampleTestCalendar)

    def test_030_register_new_calendar_invalid_calendar_class(self):
        class NoFromCalendar:  # without from_rata_die
            def __init__(self, week, day):
                self.week = week
                self.day = day

            def to_rata_die(self):
                return 7 * (self.week - 1) + self.day

        with pytest.raises(TypeError):
            Date.register_new_calendar('test_1', NoFromCalendar)

        class NoToCalendar:  # without to_rata_die
            def __init__(self, week, day):
                self.week = week
                self.day = day

            @classmethod
            def from_rata_die(cls, rata_die):
                return cls((rata_die - 1) // 7 + 1, (rata_die - 1) % 7 + 1)

        with pytest.raises(TypeError):
            Date.register_new_calendar('test_1', NoToCalendar)

    def test_040_registered_attribute_simple_class(self):
        Date.register_new_calendar('test_1', ExampleTestCalendar)

        # Date attribute type and metaclass are correct
        assert Date.test_1.__name__ == 'ExampleTestCalendarInDate'
        assert type(Date.test_1).__name__ == 'ModifiedClass'
        assert issubclass(Date.test_1, ExampleTestCalendar)

        # constructed date type and value are is correct
        d1a = Date.test_1(100, 4)
        assert type(d1a) == Date
        assert d1a.day_count == 697

        # new attribute on date instance, type and value are correct
        d1b = Date(1000)
        assert isinstance(d1b.test_1, ExampleTestCalendar)
        assert type(d1b.test_1).__name__ == 'ExampleTestCalendarInDate'
        assert type(d1b.test_1.__class__).__name__ == 'ModifiedClass'
        assert d1b.test_1.week == 143
        assert d1b.test_1.day == 6

        # new attribute on date instance build by another calendar, type and value are correct
        d1c = Date.gregorian(100, 2, 3)
        assert isinstance(d1c.test_1, ExampleTestCalendar)
        assert type(d1c.test_1).__name__ == 'ExampleTestCalendarInDate'
        assert type(d1c.test_1.__class__).__name__ == 'ModifiedClass'
        assert d1c.test_1.week == 5171
        assert d1c.test_1.day == 3

    def test_043_registered_attribute_class_with_other_constructors(self):
        class ExampleTestCalendar2(ExampleTestCalendar):
            @classmethod
            def with_thousands(cls, thousands, week, day):
                return cls(1000 * thousands + week, day)

        Date.register_new_calendar('test_2', ExampleTestCalendar2)

        # Date attribute type and metaclass are correct
        assert Date.test_2.__name__ == 'ExampleTestCalendar2InDate'
        assert type(Date.test_2).__name__ == 'ModifiedClass'
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
        assert type(d2b.test_2).__name__ == 'ExampleTestCalendar2InDate'
        assert type(d2b.test_2.__class__).__name__ == 'ModifiedClass'
        assert d2b.test_2.week == 143
        assert d2b.test_2.day == 6

        # new attribute on date instance build by another calendar, type and value are correct
        d2c = Date.gregorian(100, 2, 3)
        assert isinstance(d2c.test_2, ExampleTestCalendar2)
        assert type(d2c.test_2).__name__ == 'ExampleTestCalendar2InDate'
        assert type(d2c.test_2.__class__).__name__ == 'ModifiedClass'
        assert d2c.test_2.week == 5171
        assert d2c.test_2.day == 3

    def test_046_registered_attribute_class_with_static_methods(self):
        class ExampleTestCalendar3(ExampleTestCalendar):
            @staticmethod
            def is_odd(number):
                return (number % 2) == 1

        Date.register_new_calendar('test_3', ExampleTestCalendar3)

        # Date attribute type and metaclass are correct
        assert Date.test_3.__name__ == 'ExampleTestCalendar3InDate'
        assert type(Date.test_3).__name__ == 'ModifiedClass'
        assert issubclass(Date.test_3, ExampleTestCalendar)

        # constructed date type and value are is correct
        d3a = Date.test_3(100, 4)
        assert type(d3a) == Date
        assert d3a.day_count == 697

        # new attribute on date instance, type and value are correct
        d3b = Date(1000)
        assert isinstance(d3b.test_3, ExampleTestCalendar3)
        assert type(d3b.test_3).__name__ == 'ExampleTestCalendar3InDate'
        assert type(d3b.test_3.__class__).__name__ == 'ModifiedClass'
        assert d3b.test_3.week == 143
        assert d3b.test_3.day == 6

        # new attribute on date instance build by another calendar, type and value are correct
        d3c = Date.gregorian(100, 2, 3)
        assert isinstance(d3c.test_3, ExampleTestCalendar3)
        assert type(d3c.test_3).__name__ == 'ExampleTestCalendar3InDate'
        assert type(d3c.test_3.__class__).__name__ == 'ModifiedClass'
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

    def test_100_date_has_attributes_but_instance_not(self):
        # the date class aways has a registered attribute
        assert hasattr(Date, 'gregorian')
        assert Date.gregorian
        # an instance created with another calendar or by Date does not have
        #   the attribute; it is instead is reachable via the Date class
        d1 = Date(4)
        with pytest.raises(KeyError):
            d1.__dict__['gregorian']
        assert hasattr(d1, 'gregorian')
        assert d1.gregorian
        d2 = Date.iso(3, 4, 5)
        with pytest.raises(KeyError):
            d2.__dict__['gregorian']
        assert hasattr(d2, 'gregorian')
        assert d2.gregorian
        # a Date instance created via the calendar does have the same attribute
        d3 = Date.gregorian(3, 4, 5)
        assert hasattr(d3, 'gregorian')
        assert d3.gregorian

    def test_900_avoid_date_override(self):
        d = Date.gregorian(1, 1, 1)
        # I do not want an instance of Date created through a Gregorian to have its static methods
        # One of the implementation I used had this error and I want to avoid it
        with pytest.raises(AttributeError):
            getattr(d, 'is_leap_year')
        with pytest.raises(AttributeError):
            d.is_leap_year
