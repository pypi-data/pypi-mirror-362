import functools
import logging
import time
import inspect

# Setup default logger
logger = logging.getLogger("autopylog")
logger.setLevel(logging.INFO)

# StreamHandler for console output
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def log_this(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        arg_names = inspect.getfullargspec(func).args
        arg_str = ', '.join(f"{name}={val!r}" for name, val in zip(arg_names, args))
        kwarg_str = ', '.join(f"{k}={v!r}" for k, v in kwargs.items())
        params = ', '.join(filter(None, [arg_str, kwarg_str]))

        logger.info(f"Calling: {func_name}({params})")
        start = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start
            logger.info(f"Returned: {result!r} in {duration:.4f}s")
            return result
        except Exception as e:
            logger.error(f"Exception in {func_name}: {e}")
            raise
    return wrapper
