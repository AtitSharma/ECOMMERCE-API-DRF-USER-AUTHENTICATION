from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.authentication import TokenAuthentication
from .models import Products
from rest_framework_simplejwt.authentication import JWTAuthentication

class ProductDetailsView(APIView):
    
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    
    def post(self,request,*args,**kwargs):
        serializer=ProductSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid():
            serializer.save()
            context={
                "msg":"Succesfully Saved the product !!!"
            }
            return Response(data=context,status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, *args, **kwargs):
        token=request.headers.get("Authorization")
        token=token.split()
        products = Products.objects.all()
        serializer = ProductSerializer(instance=products,context={'token': token[-1]},many=True)
        return Response(serializer.data)
        
    
    
    