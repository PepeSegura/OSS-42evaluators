from django.urls import path
from .views import (
    landing,

    index,
    cursus,
    cluster_view,
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

)

urlpatterns = [
    path('', landing, name='landing'),
    path('login/42/', login_42, name='login_42'),
    path('auth/callback/', auth_callback, name='auth_callback'),
    path('check_login_status/', check_login_status, name='check_login_status'),
    path('logout/', logout_view, name='logout'),

    path('index', index, name='index'),
    path('projects/', projects, name='Projects'),
    path('cursus/', cursus, name='cursus'),
    path('all-projects/', allprojects, name='allprojects'),

    path('clusters/', cluster_view, name='clusters'),
    path('peers/', peers, name='peers'),
    path('add/', add_friend, name='add'),

    path('about/', about, name='about'),
    path('calculator/', calculator, name='calculator'),
]


