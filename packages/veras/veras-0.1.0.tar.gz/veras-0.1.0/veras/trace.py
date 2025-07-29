import os
import contextvars
import functools
import time
import uuid
import requests

# Context for current trace/span
current_trace_id = contextvars.ContextVar("trace_id")
current_span_id = contextvars.ContextVar("span_id")
current_parent_id = contextvars.ContextVar("parent_id", default=None)

AWS_ENDPOINT = os.getenv(
    "VERAS_ENDPOINT",
    "https://dyqv5r50u5.execute-api.ap-southeast-2.amazonaws.com/dev/api/v1/traces"
)


def trace(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        trace_id = str(uuid.uuid4())
        span_id = str(uuid.uuid4())
        current_trace_id.set(trace_id)
        current_span_id.set(span_id)
        current_parent_id.set(None)
        start = time.time()
        status = "success"
        exc = None
        result = None
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            status = "error"
            exc = str(e)
            raise
        finally:
            end = time.time()
            trace_data = {
                "trace_id": trace_id,
                "span_id": span_id,
                "parent_id": None,
                "function": func.__name__,
                "args": repr(args),
                "kwargs": repr(kwargs),
                "status": status,
                "exception": exc,
                "start_time": start,
                "end_time": end,
                "duration": end - start,
            }
            try:
                requests.post(AWS_ENDPOINT, json=trace_data)
            except Exception:
                pass  # Don't break user code if sending fails
    return wrapper

def span(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        trace_id = current_trace_id.get(None)
        parent_id = current_span_id.get(None)
        span_id = str(uuid.uuid4())
        current_span_id.set(span_id)
        current_parent_id.set(parent_id)
        start = time.time()
        status = "success"
        exc = None
        result = None
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            status = "error"
            exc = str(e)
            raise
        finally:
            end = time.time()
            span_data = {
                "trace_id": trace_id,
                "span_id": span_id,
                "parent_id": parent_id,
                "function": func.__name__,
                "args": repr(args),
                "kwargs": repr(kwargs),
                "status": status,
                "exception": exc,
                "start_time": start,
                "end_time": end,
                "duration": end - start,
            }
            try:
                requests.post(AWS_ENDPOINT, json=span_data)
            except Exception:
                pass
    return wrapper 