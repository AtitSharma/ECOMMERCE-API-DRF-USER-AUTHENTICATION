from django.contrib import admin
from .models import Products,Cart
# Register your models here.

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display=['id',"name","details","price"]
    
    
    
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=["id","name","product","quantity","totalprice"]
