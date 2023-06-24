
from django.urls import path
from .views import ProductDetailsView


app_name="product"

urlpatterns = [
    path("product-details/",ProductDetailsView.as_view(),name="productdetail")
    
]
