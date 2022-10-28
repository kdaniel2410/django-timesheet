from django.urls import path
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm

urlpatterns = [
    path("login/", LoginView.as_view(), name="registration_login"),
    path(
        "logout/",
        LogoutView.as_view(),
        name="registration_logout",
    ),
    path(
        "register/",
        CreateView.as_view(
            form_class=UserCreationForm,
            template_name="registration/register.html",
            success_url="/",
        ),
        name="registration_register",
    ),
]
