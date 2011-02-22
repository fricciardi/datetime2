"""datetime2

Date and time types with broader calendar coverage"""


__all__ = ('TimeDelta', 'WesternTD')


import collections
import decimal
import fractions
import functools
import keyword
import numbers


#==============================================================================
#====== TimeDelta
#==============================================================================

#def td_factory(td_class_name, main_units, secondary_units = '', str_function = None, verbose=False):
#    """Returns a class the represents a specific TimeDelta system.
#
#    Parameter:
#      td_class_name :    name of the class that will be generated
#      main_units :       list of units that will be stored in the class; this is list a string with the
#                         following pattern:
#                         
#                         (unit_name':'multiplier';')*'days'(';'divider':'unit_name)*
#                         
#                         notes: 1) units are listed from larger to smaller and must include 'days'
#                                2) unit names are made of alphanumeric characters and underscores,
#                                   not beginning with underscore or digit
#                                3) multipliers are integers and relative to following unit
#                                4) dividers are integers and relative to previous unit
#                                5) unit names must not be duplicates nor Python keywords
#                                
#                         e.g.   "weeks:7;days;24:hours;60:minutes" means:
#                                - a week is made of 7 days
#                                - a day is made of 24 hours
#                                - an hour is made of 60 minutes 
#      secondary_units :  list of units that will be used for input and conversion, but will not be stored
#                         in this class; this list is a string with the following pattern:
#                         
#                         unit_name':'ratio_to_day(';'unit_name':'ratio_to_day)*
#                         
#                         notes: 1) units are unordered
#                                2) unit names are made of alphanumeric characters and underscores,
#                                   not beginning with underscore or digit
#                                3) ratio to day can be either an integer or a fraction of integers
#                                4) unit names must not be duplicates (of main or secondary units) nor
#                                   Python keywords 
#                                
#                         e.g.   "fortnights:14;beats:1/1000" means:
#                                - a fortnight is made of 14 days
#                                - a day is made of 1000 beats
#    str_function :       function used to print the instance in a user friendly manner
#    verbose :            if True prints out the class definitions as created by the function
#    
#    Note: code for this function has been greatly copied from collections.namedtuple .
#    """
#
#    # Parse and validate the field names.  Validation serves two purposes,
#    # generating informative error messages and preventing template injection attacks.
#    main_units = main_units.split(';')
#    try:
#        days_index = main_units.index('days')
#    except ValueError:
#        raise ValueError("Main unit string does not contain 'days'.")
#    main_units_parsed = {}
#    for unit in main_units[:days_index]:
#        try:
#            unit_name, multiplier = unit.split(':')
#        except ValueError:
#            raise ValueError("Unit definition '{}' is not in the 'unit_name:multiplier' format.".format(unit))
#        if (not all(c.isalnum() or c=='_' for c in unit_name) or keyword.iskeyword(unit_name)
#            or not unit_name or unit_name[0].isdigit() or unit_name.startswith('_') or unit_name
#              in seen):
#            
#            
#            
#    if isinstance(field_names, str):
#        field_names = field_names.replace(',', ' ').split() # names separated by whitespace and/or commas
#    field_names = tuple(map(str, field_names))
#    if rename:
#        names = list(field_names)
#        seen = set()
#        for i, name in enumerate(names):
#            if (not all(c.isalnum() or c=='_' for c in name) or _iskeyword(name)
#                or not name or name[0].isdigit() or name.startswith('_')
#                or name in seen):
#                names[i] = '_%d' % i
#            seen.add(name)
#        field_names = tuple(names)
#    for name in (typename,) + field_names:
#        if not all(c.isalnum() or c=='_' for c in name):
#            raise ValueError('Type names and field names can only contain alphanumeric characters and underscores: %r' % name)
#        if _iskeyword(name):
#            raise ValueError('Type names and field names cannot be a keyword: %r' % name)
#        if name[0].isdigit():
#            raise ValueError('Type names and field names cannot start with a number: %r' % name)
#    seen_names = set()
#    for name in field_names:
#        if name.startswith('_') and not rename:
#            raise ValueError('Field names cannot start with an underscore: %r' % name)
#        if name in seen_names:
#            raise ValueError('Encountered duplicate field name: %r' % name)
#        seen_names.add(name)
#
#    # Create and fill-in the class template
#    numfields = len(field_names)
#    argtxt = repr(field_names).replace("'", "")[1:-1]   # tuple repr without parens or quotes
#    reprtxt = ', '.join('%s=%%r' % name for name in field_names)
#    template = '''class %(typename)s(tuple):
#        '%(typename)s(%(argtxt)s)' \n
#        __slots__ = () \n
#        _fields = %(field_names)r \n
#        def __new__(_cls, %(argtxt)s):
#            'Create new instance of %(typename)s(%(argtxt)s)'
#            return _tuple.__new__(_cls, (%(argtxt)s)) \n
#        @classmethod
#        def _make(cls, iterable, new=tuple.__new__, len=len):
#            'Make a new %(typename)s object from a sequence or iterable'
#            result = new(cls, iterable)
#            if len(result) != %(numfields)d:
#                raise TypeError('Expected %(numfields)d arguments, got %%d' %% len(result))
#            return result \n
#        def __repr__(self):
#            'Return a nicely formatted representation string'
#            return self.__class__.__name__ + '(%(reprtxt)s)' %% self \n
#        def _asdict(self):
#            'Return a new OrderedDict which maps field names to their values'
#            return OrderedDict(zip(self._fields, self)) \n
#        def _replace(_self, **kwds):
#            'Return a new %(typename)s object replacing specified fields with new values'
#            result = _self._make(map(kwds.pop, %(field_names)r, _self))
#            if kwds:
#                raise ValueError('Got unexpected field names: %%r' %% kwds.keys())
#            return result \n
#        def __getnewargs__(self):
#            'Return self as a plain tuple.  Used by copy and pickle.'
#            return tuple(self) \n\n''' % locals()
#    for i, name in enumerate(field_names):
#        template += "        %s = _property(_itemgetter(%d), doc='Alias for field number %d')\n" % (name, i, i)
#    if verbose:
#        print(template)
#
#    # Execute the template string in a temporary namespace and
#    # support tracing utilities by setting a value for frame.f_globals['__name__']
#    namespace = dict(_itemgetter=_itemgetter, __name__='namedtuple_%s' % typename,
#                     OrderedDict=OrderedDict, _property=property, _tuple=tuple)
#    try:
#        exec(template, namespace)
#    except SyntaxError as e:
#        raise SyntaxError(e.msg + ':\n\n' + template)
#    result = namespace[typename]
#
#    # For pickling to work, the __module__ variable needs to be set to the frame
#    # where the named tuple is created.  Bypass this step in enviroments where
#    # sys._getframe is not defined (Jython for example) or sys._getframe is not
#    # defined for arguments greater than 0 (IronPython).
#    try:
#        result.__module__ = _sys._getframe(1).f_globals.get('__name__', '__main__')
#    except (AttributeError, ValueError):
#        pass
#
#    return result


@functools.total_ordering
class TimeDelta:
    def __init__(self, days = 0):
        self._days = days
        
    def _reduce_init_arg(self, value, limit = 1000000000):
        if isinstance(value, (str, float, decimal.Decimal)):
            return fractions.Fraction(value).limit_denominator(limit)
        elif isinstance(value, (int, fractions.Fraction)):
            return fractions.Fraction(value)
        else:
            raise TypeError("Illegal type for {} initialization: {}.".format(type(self).__name__, type(value).__name__))

    def __repr__(self):
        class_name = type(self).__name__
        value_str = repr(self._days)
        return "{}(days = {})".format(class_name, value_str)

    # Binary arithmetic operations
    def __add__(self, other):
        if isinstance(other, TimeDelta):
            return type(self)(days = self._days + other._days)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, TimeDelta):
            return type(self)(days = self._days - other._days)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, numbers.Real):
            return type(self)(days = self._days * other)
        return NotImplemented
    
    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, TimeDelta):
            return float(self._days / other._days)
        elif isinstance(other, numbers.Real):
            return type(self)(days = self._days / other)
        return NotImplemented

    def __floordiv__(self, other):
        if isinstance(other, TimeDelta):
            return self._days // other._days
        elif isinstance(other, numbers.Real):
            return type(self)(days = self._days // other)
        return NotImplemented

    def __mod__(self, other):
        if isinstance(other, TimeDelta):
            return type(self)(self._days % other._days)
        elif isinstance(other, numbers.Real):
            return type(self)(days = self._days % other)
        return NotImplemented
    
    def __divmod__(self, other):
        if isinstance(other, TimeDelta):
            return (self._days // other._days, type(self)(days = self._days % other._days))
        elif isinstance(other, numbers.Real):
            return (type(self)(days = self._days // other), type(self)(days = self._days % other))
        return NotImplemented

    # Unary arithmetic operations
    def __neg__(self):
        return type(self)(days = -self._days)

    def __pos__(self):
        return self

    def __abs__(self):
        if self.td.value < 0:
            return -self
        else:
            return self

    # TODO: write __ceil__, __floor__ and __trunc__. What about __round__ ?
    
    # Comparisons of TimeDelta objects with other.
    def __eq__(self, other):
        if isinstance(other, TimeDelta):
            return self._days == other._days
        return False

    def __lt__(self, other):
        if isinstance(other, TimeDelta):
            return self._days < other._days
        raise TypeError("can't compare '%s' to '%s'" % (type(self).__name__ , type(other).__name__))

    def __hash__(self):
        return hash(self._days)

    def __bool__(self):
        return (self._days != 0)

    def in_days(self, as_fraction = False):
        if as_fraction:
            return self._days
        else:
            return float(self._days)


    # pickle support
#    def __reduce__(self):
#        return (self.__class__, (self._days,))

class BasicTD(TimeDelta):
    def __init__(self, days = 0):
        TimeDelta.__init__(self, self._reduce_init_arg(days))
        
    def __str__(self):
        integ, frac = divmod(self._days, 1)
        days_str = '{} day{}'.format(integ, 's' if integ in (1, -1) else '')
        time_str = '{} of a day'.format(str(frac))
        if integ == 0:
            if frac == 0:
                return '0 days'
            else:
                return time_str
        else:
            if frac == 0:
                return days_str
            else:
                return '{} and {}'.format(days_str, time_str)

    @property
    def days(self):
        return self._days
    
class WesternTD(TimeDelta):
    def __init__(self, days = 0, hours = 0, minutes = 0, seconds = 0, weeks = 0):
        days = self._reduce_init_arg(days)
        hours = self._reduce_init_arg(hours)
        minutes = self._reduce_init_arg(minutes)
        seconds = self._reduce_init_arg(seconds)
        weeks = self._reduce_init_arg(weeks)
        TimeDelta.__init__(self, weeks * 7 + days +
                                 hours / 24 + minutes / 1440 + seconds / 86400)
        self._intdays = int(self._days)
        frac = self._days - self._intdays
        self._hours = int(frac * 24)
        frac -= self._hours * 24
        self._minutes = int(frac * 60)
        frac -= self._minutes * 60
        self._seconds = frac * 60

    def __str__(self):
        days_str = '{} day{}'.format(self._intdays, 's' if self._intdays in (1, -1) else '')
        if int(self._seconds) == self._seconds:
            time_str = '{:02d}:{:02d}:{:02d}'.format(self._hours, self._minutes, int(self._seconds))
        else:
            time_str = '{:02d}:{:02d}:{:02.3f}'.format(self._hours, self._minutes, float(self._seconds))
        if self._hours == 0 and self._minutes == 0 and self._seconds == 0:
            if self._days == 0:
                return '0 days'
            else:
                return days_str
        else:
            if self._days == 0:
                return time_str
            else:
                return '{}, {}'.format(days_str, time_str)
        
    def in_weeks(self, as_fraction = False):
        value = self._days / 7
        if as_fraction:
            return value
        else:
            return float(value)

    def in_hours(self, as_fraction = False):
        value = self._days * 24
        if as_fraction:
            return value
        else:
            return float(value)

    def in_minutes(self, as_fraction = False):
        value = self._days * 1440
        if as_fraction:
            return value
        else:
            return float(value)
    
    def in_seconds(self, as_fraction = False):
        value = self._days * 86400
        if as_fraction:
            return value
        else:
            return float(value)
    
    # Read-only field accessors
    @property
    def days(self):
        return self._intdays

    @property
    def hours(self):
        return self._hours

    @property
    def minutes(self):
        return self._minutes

    @property
    def seconds(self):
        return float(self._seconds)

