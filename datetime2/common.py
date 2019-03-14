# Gregorian calendar in calendars package

# Copyright (c) 2019 Francesco Ricciardi
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


from fractions import Fraction


__author__ = 'Francesco Ricciardi <francescor2010 at yahoo.it>'


def verify_fractional_value(fractional, min=None, max=None, min_excl=None, max_excl=None):
    if min is not None and min_excl is not None:
        raise ValueError("Only one minimum value can be given.")
    if max is not None and max_excl is not None:
        raise ValueError("Only one maximum value can be given.")
    try:
        if type(fractional) == tuple:
            if len(fractional) == 2:
                value = Fraction(*fractional)
            else:
                raise TypeError('Tuple argument must have two elements.')
        else:
            value = Fraction(fractional)
    except ZeroDivisionError:
        raise ValueError("Denomnator cannot be 0.")
    except (TypeError, OverflowError):
        raise TypeError("Invalid fractional value.")
    if min is not None and value < min:
        raise ValueError("Value must be more than or equal to {}".format(min))
    if min_excl is not None and value <= min_excl:
        raise ValueError("Value must be more than {}".format(min_excl))
    if max is not None and value > max:
        raise ValueError("Value must be less than or equal to {}".format(max))
    if max_excl is not None and value >= max_excl:
        raise ValueError("Value must be less than {}".format(max))
    return value
