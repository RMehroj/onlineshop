from django.urls import path

from . import views

urlpatterns = [
    # path('',
    #      views.Index.as_view(),
    #      name='homepage'
    #      ), 
    # path(
    #     'user',
    #     views.user,
    #     name='store'
    #     ), 
    path(
        'signup/',
        views.SignupAPIView.as_view(),
        name='signup'
        ), 
    path(
        'login/',
        views.Login.as_view(),
        name='login'
        ), 
    path(
        'logout/',
        views.logout,
        name='logout'
        ),
]
