from functools import wraps


def synchronized(method):
    """
    Decorator to make underlying methods thread safe given an instance wide lock
    """

    @wraps(method)
    def synchronized_method(self, *args, **kwargs):
        with self._lock:
            return method(self, *args, **kwargs)

    return synchronized_method
