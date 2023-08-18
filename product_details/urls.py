
from django.urls import path
from .views import (ProductDetailsView,
                    ProductUpdateDelete,
                    AddToCart,BuyProductFromCart,
                    UpdateDeleteCartApiView,
                    BuyProduct)


app_name="product"

urlpatterns = [
    path("product-details/",ProductDetailsView.as_view(),name="productdetail"),
    path("product-ud/<int:pk>/",ProductUpdateDelete.as_view(),name="product_ud"),
    path("add-to-cart/<int:pk>/",UpdateDeleteCartApiView.as_view(),name="cart_delete_update"),
    path("add-to-cart/",AddToCart.as_view(),name="addcart"),
    path("buy-product/<int:pk>/",BuyProduct.as_view(),name="buy_product"),
    path("buy-product-cart/",BuyProductFromCart.as_view(),name="buyfromcart")
    
    
]
