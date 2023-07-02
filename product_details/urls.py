
from django.urls import path
from .views import ProductDetailsView,ProductUpdateDelete,AddToCart


app_name="product"

urlpatterns = [
    path("product-details/",ProductDetailsView.as_view(),name="productdetail"),
    path("product-cd/<int:pk>/",ProductUpdateDelete.as_view(),name="product_ud"),
    path("add-to-cart/<int:pk>/",AddToCart.as_view(),name="cart_delete_update"),
    path("add-to-cart/",AddToCart.as_view(),name="addcart"),
    
    
]
