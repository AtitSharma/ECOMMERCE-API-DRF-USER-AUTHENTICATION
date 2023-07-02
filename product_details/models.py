from django.db import models
from django.conf import settings

class Products(models.Model):
    name=models.CharField(max_length=200)
    details=models.CharField(max_length=200)
    price=models.IntegerField()
    
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.name)
    
    
class Cart(models.Model):
    name=models.CharField(max_length=100)
    product=models.ForeignKey(Products,on_delete=models.CASCADE,related_name="cart")
    quantity=models.IntegerField()
    totalprice=models.IntegerField()
    
    
    def __str__(self):
        return str(self.name)
    
