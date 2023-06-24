from django.urls import path
from .views import RegisterView,UserLogin

app_name="user"

urlpatterns = [
    path("register/",RegisterView.as_view(),name="register"),
    path("login/",UserLogin.as_view(),name="login")
]
