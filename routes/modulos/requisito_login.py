from functools import wraps
from flask import session, redirect, url_for

def login_requisito(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'usuario_logado' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapper

