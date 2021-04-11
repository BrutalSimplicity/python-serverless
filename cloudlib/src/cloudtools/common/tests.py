import functools

def mock_decorator(f):
    @functools.wraps(f)
    def _wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return _wrapper
