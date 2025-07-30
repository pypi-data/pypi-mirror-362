def python_to_luxon_format(python_format: str) -> str:
    format_mappings = {
        '%a': 'ccc',   # Weekday, short version, Sun-Sat
        '%A': 'cccc',  # Weekday, full version, Sunday-Saturday
        '%w': 'c',     # Weekday as a number, 0-6
        '%d': 'dd',    # Day of month, 01-31
        '%-d': 'd',    # Day of month, 1-31
        '%b': 'LLL',   # Month name, short version, Jan-Dec
        '%B': 'LLLL',  # Month name, full version, January-December
        '%m': 'MM',    # Month as a number, 01-12
        '%-m': 'M',    # Month as a number, 1-12
        '%y': 'yy',    # Year, short version, 00-99
        '%Y': 'yyyy',  # Year, full version, 0001-9999
        '%H': 'HH',    # Hour, 00-23
        '%-H': 'H',    # Hour, 0-23
        '%I': 'hh',    # Hour, 01-12
        '%-I': 'h',    # Hour, 1-12
        '%p': 'a',     # AM/PM
        '%M': 'mm',    # Minute, 00-59
        '%-M': 'm',    # Minute, 0-59
        '%S': 'ss',    # Second, 00-59
        '%-S': 's',    # Second, 0-59
        '%f': 'SSS',   # Microsecond, 000000-999999
        '%z': 'ZZ',    # UTC offset
        '%Z': 'ZZZZ',  # Time zone name
        '%j': 'o',     # Day of year, 001-366
        '%-j': 'o',    # Day of year, 1-366
        '%U': 'WW',    # Week number of year, Sunday as the first day of the week
        '%W': 'WW',    # Week number of year, Monday as the first day of the week
        '%c': 'fff',   # Locale’s appropriate date and time representation
        '%x': 'ff',    # Locale’s appropriate date representation
        '%X': 'tt',    # Locale’s appropriate time representation
        '%%': '%',     # A literal '%' character
    }

    luxon_format = python_format

    for python_spec, luxon_spec in format_mappings.items():
        luxon_format = luxon_format.replace(python_spec, luxon_spec)

    return luxon_format


# Example usage
# python_format = "%m/%d/%Y %H:%M:%S"
# luxon_format = python_to_luxon_format(python_format)
# print(luxon_format)  # Outputs: MM/dd/yyyy HH:mm:ss
