import time
import functools


class Max_retries_reach( Exception ):
    pass


def retry_on_exception( f=None, *, exceptions=( Exception, ), max_retries=5 ):
    def _decorate( function, exceptions=exceptions, max_retries=max_retries ):
        @functools.wraps( function )
        def retry_function(
                *args, retries=0, max_retries=max_retries, exception=None,
                exceptions=exceptions,
                **kw ):
            try:
                return function( *args, **kw )
            except Exception as e:
                if exception and not e.__cause__:
                    e.__cause__ = exception
                exception = e

                retries += 1
                if retries <= max_retries:
                    if isinstance( e, exceptions ):
                        return retry_function(
                            *args, retries=retries,
                            max_retries=max_retries, exception=exception,
                            **kw )
                    else:
                        raise exception
                else:
                    raise exception
        return retry_function
    if f:
        return _decorate( f, exceptions=exceptions, max_retries=max_retries )
    return _decorate


def delay( f=None, *, seconds=None ):
    def _decorate( function ):
        @functools.wraps( function )
        def delay_function( *args, **kw ):
            time.sleep( seconds )
            return function( *args, **kw )
        return delay_function
    if f:
        return _decorate( f )
    return _decorate
