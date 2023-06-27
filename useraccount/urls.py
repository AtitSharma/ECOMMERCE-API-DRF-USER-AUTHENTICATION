from django.urls import path
from .views import RegisterView,CustomGetToken

app_name="user"

urlpatterns = [
    path("register/",RegisterView.as_view(),name="register"),
    # path("login/",UserLogin.as_view(),name="login"),
    path("login/",CustomGetToken.as_view(),name="get_token"),
    
]
