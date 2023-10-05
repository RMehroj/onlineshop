from django.urls import path

from . import views

urlpatterns = [
    path(
        'login/',
        views.LoginView.as_view(),
        name='login'
    ),
    path(
        'signup/',
        views.RegisterView.as_view(),
        name='signup'
    ),
    path(
        "profile/",
        views.UserVerifyView.as_view(),
        name="user_verify",
    ), 
]
