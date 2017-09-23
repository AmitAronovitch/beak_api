import sys

# decorators

def public(f):
    all = sys.modules[f.__module__].__dict__.setdefault('__all__', [])
    if f.__name__ not in all: 
        all.append(f.__name__)
    return f

def rename(name, scope=None):
    def renamed(func):
        func.__name__ = name
        if scope is not None:
            scope[name] = func
        return func
    return renamed
