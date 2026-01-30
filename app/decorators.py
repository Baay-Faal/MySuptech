"""
Décorateurs personnalisés pour Flask-Login.
Contient des decorateurs pour vérifier les rôles.
"""

from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def role_required(*roles):
    """
    Décorateur pour vérifier que l'utilisateur a l'un des rôles spécifiés.
    
    Usage:
        @app.route('/admin')
        @login_required
        @role_required('admin')
        def admin_page():
            return "Admin page"
        
        @app.route('/staff')
        @login_required
        @role_required('admin', 'prof')
        def staff_page():
            return "Admin or Professor"
    """
    def decorator(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Vous devez être connecté.', 'danger')
                return redirect(url_for('login'))
            
            if current_user.role not in roles:
                flash(f'Accès refusé. Rôle requis: {", ".join(roles)}', 'danger')
                return redirect(url_for('dashboard'))
            
            return fn(*args, **kwargs)
        
        return decorated_function
    return decorator
