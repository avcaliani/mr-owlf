from re import sub


def clean(value: str) -> str:
    """
    Clean up `value` data.
    :param value: String value
    :return: Cleaned data.
    """
    if value is None:
        return ''

    _value = value.lower()
    _value = sub(pattern='[^0-9a-z\s&]', repl='', string=value)
    _value = sub(pattern='\s{2,}', repl=' ', string=value)
    return _value.strip()
