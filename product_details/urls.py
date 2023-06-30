
from django.urls import path
from .views import ProductDetailsView,ProductUpdateDelete


app_name="product"

urlpatterns = [
    path("product-details/",ProductDetailsView.as_view(),name="productdetail"),
    path("product-cd/<int:pk>/",ProductUpdateDelete.as_view(),name="product_ud"),
    
    
]
