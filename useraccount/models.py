from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import uuid
from datetime import timedelta
from django.utils import timezone
# from useraccount.models import Token



class User(AbstractUser):
    username=models.CharField(max_length=100,unique=True)
    email=models.EmailField(max_length=20)
    
    
class Token(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    key=models.CharField(max_length=40, primary_key=True,unique=True)
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.key)
    
    def is_valid(self):
        expiration_time = self.created + timedelta(minutes=5)
        return timezone.now() <= expiration_time
    
    def save(self,*args,**kwargs):
        self.key=str(uuid.uuid4())

        super().save(*args,**kwargs)
    
    
    

    
    
    
    
    
    

    
    
    

    
    