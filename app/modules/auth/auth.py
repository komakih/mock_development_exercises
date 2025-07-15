from functools import wraps
from flask_login import current_user
from flask import abort

def require_permission(permission_name):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.has_permission(permission_name):
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return decorator