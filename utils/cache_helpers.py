import functools
import hashlib
import time
from django.core.cache import cache
from rest_framework.response import Response

def _get_request_from_args(args):
    """
    Accepts args from a decorated function and returns the request object.
    Works for FBV (request, ...) and CBV (self, request, ...).
    """
    if not args:
        return None
    if hasattr(args[0], "META"):
        return args[0]
    if len(args) > 1 and hasattr(args[1], "META"):
        return args[1]
    return None

def make_cache_key(request, namespace="resp", time_window_seconds=300):
    # cache_bust param -> bypass cache
    qs = request.META.get("QUERY_STRING", "")
    qs_lower = qs.lower()
    if "cache_bust=true" in qs_lower:
        return None

    # explicit version param 'v' (first occurrence)
    version = ""
    for part in qs.split("&"):
        if part.startswith("v="):
            version = part.split("=", 1)[1]
            break

    # user role slice
    user_role = "anon"
    try:
        if getattr(request, "user", None) and request.user.is_authenticated:
            user_role = "staff" if request.user.is_staff else "auth"
    except Exception:
        user_role = "anon"

    # time bucketing for time-based busting
    bucket = int(time.time() / time_window_seconds)

    key_raw = f"{namespace}:{request.method}:{request.path}?{qs}:v={version}:role={user_role}:tw={bucket}"
    return "cache:" + hashlib.sha256(key_raw.encode("utf-8")).hexdigest()

def cache_response(ttl=60):
    """
    Decorator for caching view responses (works for FBV and CBV).
    Stores `response.data` (JSON-serializable) in Redis via Django cache.
    """
    def decorator(view_func):
        @functools.wraps(view_func)
        def _wrapped(*args, **kwargs):
            request = _get_request_from_args(args)
            if request is None:
                # fallback: just call the view
                return view_func(*args, **kwargs)

            key = make_cache_key(request)
            if key is None:
                # cache_bust requested
                return view_func(*args, **kwargs)

            cached = cache.get(key)
            if cached is not None:
                # return cached JSON payload as Response
                return Response(cached)

            # not cached: call the view
            response = view_func(*args, **kwargs)

            # cache only successful JSON responses
            try:
                if hasattr(response, "status_code") and response.status_code == 200:
                    # response.data should be JSON-serializable
                    cache.set(key, response.data, ttl)
            except Exception as e:
                # do not fail the request because of cache errors
                print("cache set error:", e)

            return response
        return _wrapped
    return decorator
