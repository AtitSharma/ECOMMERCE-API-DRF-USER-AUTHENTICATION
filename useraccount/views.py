# from django.shortcuts import render
# from rest_framework.decorators import api_view,permission_classes
from .serializers import RegisterSerializer,LoginSerializer
from rest_framework.response  import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
from useraccount.models import User,Token
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
# from rest_framework.authtoken.models import Token
# from useraccount.models import Token
from django.contrib.auth import authenticate,login
# from datetime import datetime
# from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomJWTtokenCreaterSerializer,UserPasswordChangeSerializer,UserPasswordResetSerializer,VerifyUserSerializer
from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from useraccount.authenticate import CustomTokenAuthentication
from rest_framework.generics import GenericAPIView

class RegisterView(APIView):
    permission_classes=[AllowAny]
    def post(self,request,*args, **kwargs):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"Register Successfully !!!"})    
        else:
            return Response({"msg":serializer.errors})
        
class UserLogin(APIView):
    permission_classes=[AllowAny]
    def post(self,request,*args,**kwargs):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.validated_data.get("user") 
            if user:
                token=serializer.validated_data.get("token")
                login(request,user)
                context = {
                        "msg": "Login successful!",
                        "token": str(token),       
                    }
                return Response(data=context,status=status.HTTP_200_OK)
            else:
                context={
                    "msg":"Login Faileed !!!",
                    "token":None
                }
                return Response(data=context,status=status.HTTP_200_OK)       
        else:
            return Response({"msg":serializer.errors})    
        
    def get(self,request,*args,**kwargs):
        context={
            "user":str(request.user),
            "token":str(request.auth),
            
        }
        return Response(data=context,status=status.HTTP_200_OK)
    
    

class CustomGetToken(TokenObtainPairView):
    serializer_class=CustomJWTtokenCreaterSerializer
    
    
    
class UserPasswordChangeView(APIView):
    authentication_classes=[JWTAuthentication]
    # authentication_classes=[]
    def post(self,request,*args,**kwargs):
        serializers=UserPasswordChangeSerializer(data=request.data,context={"request":request})
        if serializers.is_valid():
            serializers.save()
            return Response({"msg":"Password Change  Success !!! "})
            
        return Response(serializers.errors)
        
        
        
        
def send_mail_to_user(request,email):
    
    user=User.objects.get(email=email)
    user_id =user.id
    user_token=Token.objects.create(user=user)
    decoded_id=urlsafe_base64_encode(force_bytes(user_id))
    
    subject="Verifyyy"
    message=f"Verify Your Email in  http://localhost:8000/verify/{decoded_id}/{user_token}  Dont share this link to anyone"
    from_email=settings.EMAIL_HOST_USER
    recipient_list=[email] 
    send_mail(subject,message,from_email,recipient_list)
    
    
class UserPasswordReset(APIView):
    authentication_classes=[]
    permission_classes=[]
    def post(self,request,*args,**kwargs):
        serializer=UserPasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email=serializer.validated_data.get("email")
            send_mail_to_user(request,email)
            return Response({"msg":"Mail has been send to you email Verify !!! "})
        return Response(serializer.errors)
    
    
class VerifyUser(APIView): 
    '''
        This is to set new password after verification of token and userid
    
    '''  
    permission_classes=[IsAuthenticated]
    authentication_classes=[CustomTokenAuthentication]
    def post(self,request,*args,**kwargs):
        serializer=VerifyUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"Successfully Created New Password !!! "})
        return Response(serializer.errors)
    
    

    
    
    

        
        

    
        
        
    
    
        
        

    

    
    
    

 



        
        
    
        

        