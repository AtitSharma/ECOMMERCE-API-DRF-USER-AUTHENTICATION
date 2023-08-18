"""
URL configuration for api_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView,TokenVerifyView
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView




urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

   # Optional
    path('admin/', admin.site.urls),
    path("users/",include("useraccount.urls",namespace="user")),
    path("product/",include("product_details.urls",namespace="product_detail")),
    # path("gettoken/",TokenObtainPairView.as_view(),name="get_token"),
    # path("gettoken/",CustomGetToken.as_view(),name="get_token"),
    path("refreshtoken/",TokenRefreshView.as_view(),name="refresh_token"),
    path("verifytoken/",TokenVerifyView.as_view(),name="verify_token"),
    path('auth/',include('rest_framework.urls',namespace="rest_framework"))
]
