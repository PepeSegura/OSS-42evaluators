from .login_views import landing, login_42, auth_callback, check_login_status, logout_view
from .others_views import about, calculator
from .main_views import index, cursus, clusterMap, projects, allprojects, peers, leaderboard_view, add_friend

__all__ = [
    'landing',

    'login_42',
    'auth_callback',
    'check_login_status',
    'logout_view',

    'index',
    'cursus',
    'clusterMap',
    'projects',
    'allprojects',
    'peers',
    'add_friend',

    'about',
    'calculator',

    leaderboard_view,
]
