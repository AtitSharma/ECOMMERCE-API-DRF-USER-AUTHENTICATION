from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate,login
# from rest_framework.authtoken.models import Token
from useraccount.models import Token
# from datetime import timedelta,datetime
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.http import JsonResponse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str



class RegisterSerializer(serializers.Serializer):
    '''
        THIS IS TO REGISTER A NEW USER 
    '''
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
    
    '''
        THIS IS TO LOGIN USER AND PROVIDE CUSTOM TOKEN TO USER
    '''
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()  
    
    
      
    def validate(self, attrs):
        username=User.objects.filter(username=attrs["username"],email=attrs["email"])
        if username:
            user=authenticate(username=attrs["username"],password=attrs["password"])
            if user:
                token= Token.objects.create(user=user)  
                attrs["token"]=token.key
                attrs["user"]=user
                return attrs
        raise serializers.ValidationError("Unable to login")
    
    



class CustomJWTtokenCreaterSerializer(TokenObtainPairSerializer):
    '''
        THIS WILL  CREATE A TOKEN FOR THE USER
    '''
    def validate(self,attrs): 
        # print(self.context) REQUEST IS INSIDE CONTEXT 
        data = super().validate(attrs)
        # refresh = self.get_token(self.user)
        data["user"]=str(self.user)
        # data["refresh"] = str(refresh)
        # data["access"] = str(refresh.access_token)
        return data
    
    
    @classmethod
    def get_token(cls, user):
        
        
        '''
            THIS IS TO ADD PAYLOAD IN TOKEN
        '''
        
        token=super().get_token(user)
        token['username']=user.username
        return token
    
    
class UserPasswordChangeSerializer(serializers.Serializer):
    '''
    This IS TO CHANGE USER PASSWORD ON THE BASIS OF THEIR old-password and New-password
    
    '''
    old_password=serializers.CharField()
    new_password1=serializers.CharField()
    new_password2=serializers.CharField()
    
    def validate(self, attrs):
        request=self.context.get("request")
        user=request.user
        new_password1=attrs["new_password1"]
        new_password2=attrs["new_password2"]
        old_password=attrs["old_password"]
        if new_password2!=new_password1:
            raise serializers.ValidationError("Both password Didnt Matched !!!! ")
        elif new_password2 == old_password:
            raise serializers.ValidationError("New Password Should not be same as newpassword ")
        
        password_match=check_password(old_password,user.password)
        if not password_match:
            raise serializers.ValidationError("Please Provide Correct Password !!! ")  
        return attrs
    
    
    
    def create(self, validated_data):  
        request=self.context.get("request")
        user=request.user
        new_password2=validated_data["new_password2"]
        user.set_password(new_password2)
        user.save()
        return validated_data
        
        
class UserPasswordResetSerializer(serializers.Serializer):
    
    '''
    
        THIS IS TO RESET PASSWORD OF USER 
    '''
    email=serializers.CharField()
    
    def validate_email(self,value):
        user=User.objects.filter(email=value).first()
        if user:
            return value
        raise serializers.ValidationError(f"No such user with {value} email ")
    
    def create(self, validated_data):
        return validated_data
    
    
class VerifyUserSerializer(serializers.Serializer):
    
    '''
    
        CREATE NEW PASSWORD FROM TOKEN VARIFICATION 
    
    '''
    user_id=serializers.CharField()
    new_password1=serializers.CharField()
    new_password2=serializers.CharField()
    
    
    def validate_user_id(self,value):
        user_id=int(force_str(urlsafe_base64_decode(value)))
        user=User.objects.filter(pk=user_id).first()
        if user:
            return value
        raise serializers.ValidationError("No such user with such id")
    
    def validate(self, attrs):
        new_password1=attrs["new_password1"]
        new_password2=attrs["new_password2"]
        
        if new_password1 !=new_password2:
            raise serializers.ValidationError("Both password should match !!! ")
        return attrs
    
    def create(self, validated_data):
        new_password=validated_data["new_password2"]
        id=validated_data["user_id"]
        user_id=int(force_str(urlsafe_base64_decode(id)))
        user=User.objects.get(id=user_id)
        user.set_password(new_password)
        user.save()
        return validated_data
    

    
    
    
    
    
        
        
        
        
    

        
        
    
    
        
    
    


            
            
        
   
       