from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from .serializers import RegisterSerializer,LoginSerializer
from rest_framework.response  import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate,login
from datetime import datetime



class RegisterView(APIView):
    permission_classes=[AllowAny]
    def post(self,request,*args,**kwargs):
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
        
        
    
        

        