from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from .serializers import ProductSerializer,CartSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Products,Cart
from rest_framework_simplejwt.authentication import JWTAuthentication
from product_details.permissions import ProductDeleteUpdatePermission,CartUpdateDeletePermission

class ProductDetailsView(APIView):
    '''
    
    GIVES ALL PRODUCT DETAILS !!!
        
    '''
    
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    
    
    def post(self,request,*args,**kwargs):
        '''
            THIS IS TO ADD PRODUCT 
        '''
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
        '''
            THIS IS TO GET ALL PRODUCTS !!!
        '''
        products = Products.objects.all()
        serializer = ProductSerializer(instance=products,many=True)
        return Response(serializer.data)
        
    
    
class ProductUpdateDelete(APIView):
    '''
        THIS IS TO UPDATE AND DELETE PRODUCT 
    '''
    authentication_classes=[JWTAuthentication]
    permission_classes=[ProductDeleteUpdatePermission]
    
    

    
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
        '''
        
            THIS IS TO UPDATE PRODUCTS
            
        '''
        product=self.get_object()
        serilaizer=ProductSerializer(product,data=request.data)
        if serilaizer.is_valid():
            serilaizer.save()
            return Response(serilaizer.data)
        return Response(serilaizer.errors)
    
    
  
  
  
class AddToCart(APIView):

    
    def get_object(self):
        '''
            THIS VIEW WILL RETURN THE PARTICULAR CART
        '''
        product = Cart.objects.filter(pk=self.kwargs.get('pk')).first()
        self.check_object_permissions(self.request, product) # This will run our CustomPermission
        return product
    
    def get_permissions(self):
        '''
            GIVE PERMISSION ACCOURDING TO DIFFRENT RESPONSE
        '''
        if self.request.method == "GET":
            self.permission_classes = [AllowAny]
        elif self.request.method == "POST":
            self.permission_classes = [IsAuthenticated | IsAdminUser]
        elif self.request.method == "DELETE":
            self.permission_classes = [CartUpdateDeletePermission]
        return super().get_permissions()
    
    
    def get(self,request,*args,**kwargs):
        '''
            Provide cart details of all Cart if no pk is given otherwise It gives accordingly !!!
        '''
        self.authentication_classes=[]
        pk=self.kwargs.get("pk")

        if pk:
            cart=Cart.objects.filter(pk=pk).first()
            if cart:
                serializer=CartSerializer(cart)
                return Response(serializer.data)
            return Response({"msg":"No Cart With Such id"})
        else:
            cart=Cart.objects.all()
            serializer=CartSerializer(cart,many=True)
            return Response(serializer.data)
            
    
    
    def post(self,request,*args,**kwargs):
        """
            ADD the items in the CART on the basis of product id !!!
        """
        serializer=CartSerializer(data=request.data,context={"name":request.user.username})
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"Successfully add to cart"})
        return Response(serializer.errors)


    def delete(self, request, *args, **kwargs):
        '''
        DELETE THE PARICULAR CART 
        
        '''
        
        cart=self.get_object()
        cart.delete()
        return Response({"msg": "Deleted!!!"})
        
    
    
    
    
        
        
    

    


    
        
    

  

    
    