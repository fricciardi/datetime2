# datetime2 package main file

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


from math import floor
from functools import total_ordering

import datetime2.osinterface


__all__ = ['Date']


class TimeDelta:
    # This is a stub in version 0.1a1
    def __init__(self, days):
        self._days = days
        
    def __repr__(self):
        return "TimeDelta({})".format(self.days)
    
    @property
    def days(self):
        return self._days
    
    def __add__(self, other):
        raise TypeError   # required to let Date tests pass

@total_ordering    
class Date:
    def __init__(self, day_count):
        if isinstance(day_count, int):
            self._day_count = day_count
        else:
            raise TypeError("an integer is required")

    @classmethod
    def today(cls):
        return cls(floor(datetime2.osinterface.get_moment()))

    @property
    def day_count(self):
        return self._day_count
    
    def __repr__(self):
        return "Date({})".format(self.day_count)
    
    def __str__(self):
        return "R.D. {}".format(self.day_count)
    
    def __add__(self, other):
        if isinstance(other, TimeDelta):
            return Date(self.day_count + other.days)
        else:
            raise NotImplemented
        
    def __radd__(self, other):
        return self + other
    
    def __sub__(self, other):
        if isinstance(other, Date):
            return TimeDelta(self.day_count - other.day_count)
        elif isinstance(other, TimeDelta):
            return Date(self.day_count - other.days)
        else:
            raise NotImplemented
        
    def __eq__(self, other):
        return isinstance(other, Date) and self.day_count == other.day_count

    def __lt__(self, other):
        if isinstance(other, Date):
            return self.day_count < other.day_count
        else:
            raise NotImplemented
        
    def __hash__(self):
        return hash(self._day_count)
    