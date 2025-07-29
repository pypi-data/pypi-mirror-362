import os
import contextvars
import functools
import time
import uuid
import requests
import asyncio
from . import __version__

# Context for current trace/span
current_trace_id = contextvars.ContextVar("trace_id")
current_span_id = contextvars.ContextVar("span_id")
current_parent_id = contextvars.ContextVar("parent_id", default=None)

AWS_ENDPOINT = os.getenv(
    "VERAS_ENDPOINT",
    "https://dyqv5r50u5.execute-api.ap-southeast-2.amazonaws.com/dev/api/v1/traces"
)


def to_serializable(obj):
    """
    Recursively convert objects to JSON-serializable forms, omitting any field that is None, empty list, or empty dict.
    """
    if isinstance(obj, dict):
        return {k: to_serializable(v) for k, v in obj.items()
                if v not in (None, [], {}) and not (isinstance(v, (list, dict)) and not v)}
    elif isinstance(obj, (list, tuple)):
        return [to_serializable(v) for v in obj if v not in (None, [], {})]
    elif hasattr(obj, '__dict__'):
        return to_serializable(vars(obj))
    elif isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    else:
        return str(obj)

# --- Context propagation helpers ---
def get_current_trace_context():
    """Get the current trace context for propagation across threads/processes."""
    return {
        "trace_id": current_trace_id.get(None),
        "span_id": current_span_id.get(None),
        "parent_id": current_parent_id.get(None),
    }

def set_current_trace_context(trace_id=None, span_id=None, parent_id=None):
    """Set the current trace context for propagation across threads/processes."""
    if trace_id is not None:
        current_trace_id.set(trace_id)
    if span_id is not None:
        current_span_id.set(span_id)
    if parent_id is not None:
        current_parent_id.set(parent_id)

# --- Best-in-class span decorator: async/sync, arbitrary metadata, context propagation ---
def span(_func=None, **meta):
    """
    Decorator for tracing a function as a span. Supports async/sync, context propagation, and arbitrary metadata.
    """
    def decorator(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            trace_id = current_trace_id.get(None) or str(uuid.uuid4())
            parent_id = current_span_id.get(None)
            span_id = str(uuid.uuid4())
            token_trace = current_trace_id.set(trace_id)
            token_span = current_span_id.set(span_id)
            token_parent = current_parent_id.set(parent_id)
            start = time.time()
            status = "success"
            exc = None
            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                status = "error"
                exc = str(e)
                result = None
            end = time.time()
            serial_args = to_serializable(args)
            serial_kwargs = to_serializable(kwargs)
            serial_result = to_serializable(result)
            record = {
                "trace_id": trace_id,
                "span_id": span_id,
                "parent_id": parent_id,
                "function": func.__name__,
                "args": serial_args,
                "kwargs": serial_kwargs,
                "result": serial_result,
                "status": status,
                "exception": exc,
                "start_time": start,
                "end_time": end,
                "duration": end - start,
                "sdk_version": __version__,
            }
            # Merge in non-empty meta fields
            record.update({k: v for k, v in meta.items() if v not in (None, [], {}, "")})
            # Omit empty fields
            record = {k: v for k, v in record.items() if v not in (None, [], {}, "")}
            try:
                requests.post(AWS_ENDPOINT, json=record, timeout=2)
            except Exception:
                pass
            current_trace_id.reset(token_trace)
            current_span_id.reset(token_span)
            current_parent_id.reset(token_parent)
            return result

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            trace_id = current_trace_id.get(None) or str(uuid.uuid4())
            parent_id = current_span_id.get(None)
            span_id = str(uuid.uuid4())
            token_trace = current_trace_id.set(trace_id)
            token_span = current_span_id.set(span_id)
            token_parent = current_parent_id.set(parent_id)
            start = time.time()
            status = "success"
            exc = None
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                status = "error"
                exc = str(e)
                result = None
            end = time.time()
            serial_args = to_serializable(args)
            serial_kwargs = to_serializable(kwargs)
            serial_result = to_serializable(result)
            record = {
                "trace_id": trace_id,
                "span_id": span_id,
                "parent_id": parent_id,
                "function": func.__name__,
                "args": serial_args,
                "kwargs": serial_kwargs,
                "result": serial_result,
                "status": status,
                "exception": exc,
                "start_time": start,
                "end_time": end,
                "duration": end - start,
                "sdk_version": __version__,
            }
            # Merge in non-empty meta fields
            record.update({k: v for k, v in meta.items() if v not in (None, [], {}, "")})
            # Omit empty fields
            record = {k: v for k, v in record.items() if v not in (None, [], {}, "")}
            try:
                requests.post(AWS_ENDPOINT, json=record, timeout=2)
            except Exception:
                pass
            current_trace_id.reset(token_trace)
            current_span_id.reset(token_span)
            current_parent_id.reset(token_parent)
            return result

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    if _func is None:
        return decorator
    else:
        return decorator(_func)

# --- Best-in-class trace decorator: async/sync, arbitrary metadata, context propagation ---
def trace(_func=None, **meta):
    """
    Decorator for tracing a root function as a trace. Supports async/sync, context propagation, and arbitrary metadata.
    """
    def decorator(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            trace_id = str(uuid.uuid4())
            span_id = str(uuid.uuid4())
            token_trace = current_trace_id.set(trace_id)
            token_span = current_span_id.set(span_id)
            token_parent = current_parent_id.set(None)
            start = time.time()
            status = "success"
            exc = None
            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                status = "error"
                exc = str(e)
                result = None
            end = time.time()
            record = {
                "trace_id": trace_id,
                "span_id": span_id,
                "parent_id": None,
                "function": func.__name__,
                "args": to_serializable(args),
                "kwargs": to_serializable(kwargs),
                "result": to_serializable(result),
                "status": status,
                "exception": exc,
                "start_time": start,
                "end_time": end,
                "duration": end - start,
                "sdk_version": __version__,
            }
            # Merge in non-empty meta fields
            record.update({k: v for k, v in meta.items() if v not in (None, [], {}, "")})
            # Omit empty fields
            record = {k: v for k, v in record.items() if v not in (None, [], {}, "")}
            try:
                requests.post(AWS_ENDPOINT, json=record, timeout=2)
            except Exception:
                pass
            current_trace_id.reset(token_trace)
            current_span_id.reset(token_span)
            current_parent_id.reset(token_parent)
            return result

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            trace_id = str(uuid.uuid4())
            span_id = str(uuid.uuid4())
            token_trace = current_trace_id.set(trace_id)
            token_span = current_span_id.set(span_id)
            token_parent = current_parent_id.set(None)
            start = time.time()
            status = "success"
            exc = None
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                status = "error"
                exc = str(e)
                raise
            finally:
                end = time.time()
                record = {
                    "trace_id": trace_id,
                    "span_id": span_id,
                    "parent_id": None,
                    "function": func.__name__,
                    "args": to_serializable(args),
                    "kwargs": to_serializable(kwargs),
                    "result": to_serializable(result),
                    "status": status,
                    "exception": exc,
                    "start_time": start,
                    "end_time": end,
                    "duration": end - start,
                    "sdk_version": __version__,
                }
                # Merge in non-empty meta fields
                record.update({k: v for k, v in meta.items() if v not in (None, [], {}, "")})
                # Omit empty fields
                record = {k: v for k, v in record.items() if v not in (None, [], {}, "")}
                try:
                    requests.post(AWS_ENDPOINT, json=record, timeout=2)
                except Exception:
                    pass
                current_trace_id.reset(token_trace)
                current_span_id.reset(token_span)
                current_parent_id.reset(token_parent)
    
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    if _func is None:
        return decorator
    else:
        return decorator(_func) 