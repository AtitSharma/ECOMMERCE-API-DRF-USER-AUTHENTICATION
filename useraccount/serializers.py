from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from datetime import timedelta,datetime



class RegisterSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=100)
    password1=serializers.CharField(min_length=5,max_length=100)
    password2=serializers.CharField(min_length=5,max_length=100)
    email=serializers.EmailField()
    
    
    def validate_username(self,value):
        user=User.objects.filter(username=value)
        if user:
            raise serializers.ValidationError(f"{user} Already Exitssss !!")
        return value
    
    def validate_email(self,value):
        email=User.objects.filter(email=value)
        if email:
            raise serializers.ValidationError(f"User With Email {email} Already Exitssss!!")
        return value     
    
    def create(self, validated_data):
        username=validated_data.get("username")
        password=validated_data.get("password2")
        email=validated_data.get("email")
        return User.objects.create_user(username=username,password=password,email=email)

    
    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError("Password Dont Match !!!")
        return attrs
    
    
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()    
    def validate(self, attrs):
        username=User.objects.filter(username=attrs["username"],email=attrs["email"])
        if username:
            user=authenticate(username=attrs["username"],password=attrs["password"])
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                token.save()
                attrs["token"]=token.key
                attrs["user"]=user
                return attrs
        return serializers.ValidationError("Unable to login")
    
    

    
            
            
            
        
   
       