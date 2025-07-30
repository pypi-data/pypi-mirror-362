import math

def expotower(*args):
    if not args:
        raise ValueError("expotower requires at least one argument")
    result = args[-1]
    for num in reversed(args[:-1]):
        result = num ** result
    return result

def log10_estimate(*args):
    result = args[-1]
    for num in reversed(args[:-1]):
        result = math.log10(num) * result
    return result

def repeat(base, height):
    if height < 1:
        raise ValueError("Height must be >= 1")
    return expotower(*([base] * height))
