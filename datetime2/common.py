# Gregorian calendar in calendars package

# Copyright (c) 2022 Francesco Ricciardi
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


__author__ = "Francesco Ricciardi <francescor2010 at yahoo.it>"


def verify_value(num, den, min, max, min_excl, max_excl, strict):
    """Raised exceptions:
    - RuntimeError: if both min and min_excl, or max and max_excl are provided.
    - TypeError: if tuple argument for fraction is invalid or has wrong values
                 (0 denominator, NaN or similar)
    - ValueError: if fractional value does not observe condition(s)."""
    if min is not None and min_excl is not None:
        raise RuntimeError("Only one minimum value can be given.")
    if max is not None and max_excl is not None:
        raise RuntimeError("Only one maximum value can be given.")
    if strict:
        if den is None:
            if not isinstance(num, Fraction):
                raise TypeError("Value must be a Python Fraction.")
            den = 1
        else:
            if not isinstance(num, Fraction):
                raise TypeError("Numerator must be a Python Fraction.")
            if not isinstance(den, Fraction):
                raise TypeError("Denominator must be a Python Fraction.")
    try:
        value = Fraction(num, den)
    except TypeError as exc:
        raise TypeError("Invalid type in a fractional value.") from exc
    except (OverflowError, ValueError) as exc:
        raise TypeError("Invalid fractional value.") from exc
    if min is not None and value < min:
        raise ValueError(f"Value must be more than or equal to {min}")
    if min_excl is not None and value <= min_excl:
        raise ValueError(f"Value must be more than {min_excl}")
    if max is not None and value > max:
        raise ValueError(f"Value must be less than or equal to {max}")
    if max_excl is not None and value >= max_excl:
        raise ValueError(f"Value must be less than {max}")
    return value


def verify_fractional_value(fractional, min=None, max=None, min_excl=None, max_excl=None, strict=False):
    return verify_value(fractional, None, min, max, min_excl, max_excl, strict)


def verify_fractional_value_num_den(numerator, denominator, min=None, max=None, min_excl=None, max_excl=None, strict=False):
    return verify_value(numerator, denominator, min, max, min_excl, max_excl, strict)
