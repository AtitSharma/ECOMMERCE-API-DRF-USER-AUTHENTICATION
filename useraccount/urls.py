from django.urls import path,include
from .views import (RegisterView,CustomGetToken,
                    UserLogin,UserPasswordChangeView,
                    UserPasswordReset,VerifyUser)
# from django.contrib.auth import get_user_model
app_name="user"

urlpatterns = [
    path("register/",RegisterView.as_view(),name="register"),
    path("login/",UserLogin.as_view(),name="login"),
    path("gettoken/",CustomGetToken.as_view(),name="get_token"),
    path("password-change/",UserPasswordChangeView.as_view(),name="password_change"),
    path("password-reset/",UserPasswordReset.as_view(),name="reset_pass"),
    path("verify/",VerifyUser.as_view(),name="verifyyy"),
   
    
    
]
