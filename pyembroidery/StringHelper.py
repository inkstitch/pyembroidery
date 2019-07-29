def is_string(thing):
    try:
        return isinstance(thing, basestring)
    except NameError:
        return isinstance(thing, str)
