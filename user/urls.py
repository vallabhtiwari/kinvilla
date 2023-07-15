from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import CreateUserView, ResidentUpdateView

app_name = "user"
urlpatterns = [
    path("register/", CreateUserView.as_view(), name="user-register"),
    path(
        "login/", LoginView.as_view(template_name="user/login.html"), name="user-login"
    ),
    path(
        "logout/",
        LogoutView.as_view(template_name="user/logout.html"),
        name="user-logout",
    ),
    path("update/<int:pk>", ResidentUpdateView.as_view(), name="user-update"),
]
