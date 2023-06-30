from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.authentication import TokenAuthentication
from .models import Products
from rest_framework_simplejwt.authentication import JWTAuthentication
from product_details.permissions import ProductDeletePermission

class ProductDetailsView(APIView):
    '''
    
    GIVES ALL PRODUCT DETAILS !!!
        
    '''
    
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    # authentication_classes=[TokenAuthentication]
    
    
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
        products = Products.objects.all()
        serializer = ProductSerializer(instance=products,many=True)
        return Response(serializer.data)
        
    
    
class ProductUpdateDelete(APIView):
    '''
        THIS IS TO UPDATE AND DELETE PRODUCT 
    '''
    authentication_classes=[JWTAuthentication]
    permission_classes=[ProductDeletePermission]
    
    def get_object(self):
        '''
            THIS VIEW WILL RETURN THE PARTICULAR PRODUCT 
        '''
        product = Products.objects.filter(pk=self.kwargs.get('pk')).first()
        self.check_object_permissions(self.request, product) # This will run our CustomPermission
        return product
        
    
    
    def delete(self,request,*args,**kwargs):
        '''
        
            THIS WILL DELETE OUR PRODUCT 
        '''
        product = self.get_object() #This gets the particular product
        product.delete()
        return Response({"msg":"Deleted Successfully !!! "})

    
    def put(self,request,*args,**kwargs):
        product=self.get_object()
        serilaizer=ProductSerializer(product,data=request.data)
        if serilaizer.is_valid():
            serilaizer.save()
            return Response(serilaizer.data)
        return Response(serilaizer.errors)

        
    
    
    