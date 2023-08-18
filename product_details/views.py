from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from .serializers import ProductSerializer,CartSerializer,BuyProductSerializer,BuyProductFromCartSerailizer
from rest_framework.response import Response
from rest_framework import status
from .models import Products,Cart
from rest_framework_simplejwt.authentication import JWTAuthentication
from product_details.permissions import ProductDeleteUpdatePermission,CartUpdateDeletePermission
from rest_framework import serializers

'''SWAGGER SETTING'''
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes



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
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, *args, **kwargs):
        '''
            THIS IS TO GET ALL PRODUCTS !!!
        '''
        products=self.get_queryset()
        if not products:
            products=Products.objects.all()
        if products=="Error":
            return Response({"msg":"No such Product"})
        
        serializer = ProductSerializer(instance=products,many=True)
        return Response(serializer.data)
    
    
    def get_queryset(self):
        '''
            http://127.0.0.1:8000/product/product-details/?search=product2
            
            http://127.0.0.1:8000/product/product-details/?min_price=1&max_price=1000
        
            This view Catches product2 and give query else return None
        '''
        queried_data=self.request.GET        
        listed_data=list(queried_data)
        if ('min_price' or 'max_price') in listed_data:
            min_price=queried_data.get('min_price',None)
            max_price=queried_data.get("max_price",None) 
            if min_price==None:
                min_price=1 
            if max_price==None:
                max_price=min_price
                min_price=1
            # product=Products.objects.filter(price__gte=min_price) & Products.objects.filter(price__lte=max_price)
            product=Products.objects.filter(price__range=(min_price,max_price))
            return product
        
        if 'search' in listed_data:
            data=self.request.GET.get("search",None)
            
            if not data:
                return None
            query=Products.objects.filter(name__icontains=data)
            if not query:
                return "Error"
            return query
        return None
    
    

    
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
    
    
  

@extend_schema(
        operation_id="Add To Cart From Here!!!",
        description="Add to Cart From Here! !!! ",
        parameters=[
            OpenApiParameter(
                name="id",
                required=False,
                type=int,
                description="Type The Id Here"
                
            )
        ],
        request=CartSerializer,
        responses=CartSerializer(
            "success_reservation_response",
    )
    )
  
class AddToCart(APIView):
    # authentication_classes=[JWTAuthentication]
    

    def get_permissions(self):
        '''
            GIVE PERMISSION ACCOURDING TO DIFFRENT RESPONSE
        '''
        if self.request.method == "GET":
            self.permission_classes = [IsAuthenticated]
        elif self.request.method == "POST":
            self.permission_classes = [IsAuthenticated | IsAdminUser]
        return super().get_permissions()
    
    
    def get(self,request,*args,**kwargs):
        '''
            Provide cart details of request  user
        '''
        # self.authentication_classes=[JWTAuthentication]
        
        user=request.user.username
        cart=Cart.objects.filter(name=user)
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



@extend_schema(
        operation_id="Cart UpDate Delete From Here!!!",
        description="Cart UpDate Delete From Here! !!! ",
        parameters=[
            OpenApiParameter(
                name="id",
                required=False,
                type=int,
                description="Type The Id Here"
                
            )
        ],
        request=CartSerializer,
        responses=CartSerializer(
            "success_reservation_response",
    )
    ) 
class UpdateDeleteCartApiView(APIView):
        '''
            this is for object level because PK is given with url 
        
        '''
    
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
            elif self.request.method == "DELETE":
                self.permission_classes = [CartUpdateDeletePermission]
                # return [CartUpdateDeletePermission()]
            return super().get_permissions()
            
        
    
        def get(self,request,*args,**kwargs):
            '''
                Provide cart details of  Cart if  pk is given !!!
            '''
            self.authentication_classes=[]
            pk=self.kwargs.get("pk")

            cart=Cart.objects.filter(pk=pk)
            serializer=CartSerializer(cart, many=True)
            return Response(serializer.data)

            
            
        def delete(self, request, *args, **kwargs):
            
            '''
            
            DELETE THE PARICULAR CART 
            
            '''
            
            cart=self.get_object()
            cart.delete()
            return Response({"msg": "Deleted!!!"})
        
        
class BuyProduct(APIView):
    
    '''
        THIS VIEW WILL BUY THE PRODUCT
    
    '''
    @extend_schema(
        operation_id="Buy The product From Here !!!",
        description="Provide the Product Id  !!! ",
        request=BuyProductSerializer,
        responses=BuyProductSerializer(
            "success_reservation_response",
    )
    ) 
    def get(self,request,*args,**kwargs):
        pid=kwargs.get("pk")
        serailizer=BuyProductSerializer(data=request.data,context={"pid":pid})
        if serailizer.is_valid():
            if serailizer.buy_now():
                return Response({"msg":"Bought Successfully !!!"})
            else:
                return Response({"msg":"Prouct Not Available now !!!"})
        return Response(serailizer.errors)
    
    

class BuyProductFromCart(APIView):
    '''
    
        THIS VIEW IS USED TO BUY PRODUCT FROM CART
    '''
    
    
    
    @extend_schema(
        operation_id="Sell Product From Here !!!",
        description="Sell The Product From Here Guyzzz !!! ",
        parameters=[
            OpenApiParameter(
                name="id",
                required=False,
                type=int,
                description="Type The Id Here"
                
            )
        ],
        request=BuyProductFromCartSerailizer,
        responses=BuyProductFromCartSerailizer(
            "success_reservation_response",
    )
    ) 
    def post(self,request,*args,**kwargs):
        serializer=BuyProductFromCartSerailizer(data=request.data,context={"user":request.user.username})
        if serializer.is_valid():
            serializer.buy_now()
            return Response({"msg":" Bought Successfully "})
        return Response(serializer.errors)        
    
            

    



    
        
    

  

    
    