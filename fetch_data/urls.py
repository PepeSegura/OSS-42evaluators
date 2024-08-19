from django.urls import path
from .views import (
    landing,

    index,
    cursus,
    clusterMap,
    projects,
    allprojects,

    login_42,
    peers,
    add_friend,
    auth_callback,
    check_login_status,
    logout_view,

    about,
    calculator,

    leaderboard_view,
)

urlpatterns = [
    path('', landing, name='landing'),

    path('index', index, name='index'),
    path('cursus/', cursus, name='Cursus'),
    path('clusters/', clusterMap, name='clusters'),
    path('projects/', projects, name='Projects'),
    path('all-projects/', allprojects, name='allprojects'),

    path('login/42/', login_42, name='login_42'),
    path('peers/', peers, name='peers'),
    path('add/', add_friend, name='add'),
    path('auth/callback/', auth_callback, name='auth_callback'),
    path('check_login_status/', check_login_status, name='check_login_status'),
    path('logout/', logout_view, name='logout'),

    path('about/', about, name='about'),
    path('calculator/', calculator, name='calculator'),
    
    path('leaderboard', leaderboard_view, name='leaderboard_view'),
]


