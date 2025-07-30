from functools import wraps
from flask import current_app, request
from flask_login import current_user
from flask_login.config import EXEMPT_METHODS

def root_required(func):
    """
    If you decorate a view with this, it will ensure that the current user is
    logged in and authenticated before calling the actual view. (If they are
    not, it calls the :attr:`LoginManager.unauthorized` callback.) For
    example::
 
    @app.route('/post')
    @root_required
        def post():
            pass
     
    If there are only certain times you need to require that your user is
    logged in, you can do so with::
     
    if not current_user.id == 0: #.is_authenticated:
        return current_app.login_manager.unauthorized()
     
    ...which is essentially the code that this function adds to your views.
 
    """

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS or current_app.config.get("LOGIN_DISABLED"):
            pass
        elif not current_user.id == 1:
            return current_app.login_manager.unauthorized()
        return current_app.ensure_sync(func)(*args, **kwargs)
 
    return decorated_view

def role_required(role):
    """
    If you decorate a view with this, it will ensure that the current user is
    logged in and authenticated before calling the actual view. (If they are
    not, it calls the :attr:`LoginManager.unauthorized` callback.) For
    example::
 
    @app.route('/post')
    @role_required('admin')
        def post():
            pass
     
    """
    def specified_role_required(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if request.method in EXEMPT_METHODS or current_app.config.get("LOGIN_DISABLED"):
                pass
            else:
                if not check_user_role(role): return current_app.login_manager.unauthorized()
            return current_app.ensure_sync(func)(*args, **kwargs)
 
        return decorated_view
    return specified_role_required

def check_user_role(role):
    """Checks if the user has a certain role

    Args:
        role: str | list[str] | bool | None
            If str, than role name to check, or list of str, set of roles to check. If True, just requires user to be
            authenticated, if False no role required and if None it should be
            anonymous user

    TODO use this function from within role_required decorator
    """
    if role is None:
        return not current_user.is_authenticated
    elif role is True:
        return current_user.is_authenticated
    elif role is False:
        return True
    elif isinstance(role, str) or isinstance(role, list):
        if not current_user.is_authenticated: return False
        roles = [role] if isinstance(role, str) else role
        if current_app.config.get('IAM_ADMIN_FULL_ACCESS'):
            roles.append('admin')
            
        for role_name in roles:
            role = current_app.extensions['IAM'].models.Role.query.filter_by(name=role_name).first()
            if role:
                assigned_role = current_app.extensions['IAM'].models.RoleRegistration.query.filter_by(
                    user_id=current_user.id
                ).filter_by(role_id=role.id).first()
                if assigned_role: return True
        return current_user.role in roles
    else:
        raise TypeError('role_name should be str, bool or None')
