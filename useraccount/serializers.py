from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate,login
# from rest_framework.authtoken.models import Token
# from useraccount.models import Token
# from datetime import timedelta,datetime
# from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



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
    
    
# class LoginSerializer(serializers.Serializer):
#     username=serializers.CharField()
#     email=serializers.EmailField()
#     password=serializers.CharField()    
#     def validate(self, attrs):
#         username=User.objects.filter(username=attrs["username"],email=attrs["email"])
#         if username:
#             user=authenticate(username=attrs["username"],password=attrs["password"])
#             if user:
#                 token= Token.objects.create(user=user)               
#                 token.save()
#                 attrs["token"]=token.key
#                 attrs["user"]=user
#                 return attrs
#         raise serializers.ValidationError("Unable to login")
    
    



class CustomJWTtokenCreaterSerializer(TokenObtainPairSerializer):
    '''
        THIS WILL  CREATE A TOKEN FOR THE USER
    '''
    def validate(self,attrs): 
        # print(self.context) REQUEST IS INSIDE CONTEXT 
        request=self.context.get("request")
        username=attrs["username"]
        password=attrs["password"]
        user=authenticate(username=username,password=password)
        if user:  
            login(request=request,user=user)
        else:
            raise serializers.ValidationError("Incorrect Username or Password ")
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["user"]=str(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data


            
            
        
   
       