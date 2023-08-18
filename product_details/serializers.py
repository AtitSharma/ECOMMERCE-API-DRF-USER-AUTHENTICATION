from rest_framework import serializers
from product_details.models import Products,Cart



class ProductSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    name=serializers.CharField()
    details=serializers.CharField()
    price=serializers.IntegerField()
    quantity=serializers.IntegerField()
    user=serializers.CharField(required=False)

    
    def create(self, validated_data):
        name=validated_data.get("name")
        details=validated_data.get("details")
        price=validated_data.get("price")
        user=self.context.get("user")
        quantity=validated_data.get("quantity")
        if user:
            return Products.objects.create(name=name,details=details,price=price,user=user,quantity=quantity)
        raise serializers.ValidationError("Provide Valid Token ")
    
    
    def update(self, instance, validated_data):
        '''
        THIS WILL WORK WHEN PUT request or PATCH REQUEST IS SENT
        '''
        instance.name=validated_data.get('name',instance.name)
        instance.details=validated_data.get("details",instance.details)
        instance.price=validated_data.get("price",instance.price)
        instance.quantity=validated_data.get("quantity",instance.quantity)
        instance.save()
        return instance
        
    
    
    
    
class CartSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    name=serializers.CharField(read_only=True)
    product_id=serializers.IntegerField()
    product=serializers.CharField(read_only=True)
    totalprice=serializers.IntegerField(read_only=True)
    quantity=serializers.IntegerField()
    
    
    
    def create(self, validated_data):
        quantity=validated_data.get("quantity")
        product_id=validated_data.get("product_id")
        product=Products.objects.get(id=product_id)
        price=Products.objects.get(id=product_id).price
        totalprice=quantity*price
        name=self.context.get("name")
        
        if name:
            return Cart.objects.create(name=name,product=product,quantity=quantity,totalprice=totalprice)
        raise serializers.ValidationError("Cannot Add to Cart")
    
    
    def validate_product_id(self, value):
        product=Products.objects.filter(id=value).first()
        if not product:
            raise serializers.ValidationError(" No product with such id ")
        
        return value
    
    
    def validate(self, attrs):
        quantity=attrs["quantity"]
        print(quantity)
        pid=attrs["product_id"]
        product=Products.objects.get(pk=pid)
        avaialble_quantity=product.quantity
        if avaialble_quantity>=quantity:
            return attrs
        raise serializers.ValidationError("Cannot add more quantity than available !! ")
            
        
        
        
        
    
    
    
    
    
class BuyProductSerializer(serializers.Serializer):

    
    def validate(self, attrs):
        pid=self.context.get("pid")
        product=Products.objects.filter(pk=pid).first()
        if not product:
            raise serializers.ValidationError("No product with such id")
        return product
    
    def buy_now(self):
        product=self.validated_data
        if product.quantity<1:
            return False
        product.quantity-=1
        product.save()
        return True
    
    

class BuyProductFromCartSerailizer(serializers.Serializer):
    cart_id=serializers.IntegerField()
    username=serializers.CharField()
    
    
    def validate(self, attrs):
        cart_id=attrs["cart_id"]
        username=attrs["username"]
        user=self.context.get("user")
        if username!=user:
            raise serializers.ValidationError("Cannot get other cart")
        cart=Cart.objects.filter(pk=cart_id,name=username).first()
        if cart:
            
            return attrs
        raise serializers.ValidationError("No such cart found with given credentials !!! ")
    
    
    def buy_now(self):
        cid=self.validated_data.get("cart_id")
        cart=Cart.objects.get(pk=cid)
        quantity=cart.quantity
        pid=cart.product.id
        product=Products.objects.get(id=pid)
        product.quantity=product.quantity-quantity
        product.save()
        cart.delete()
        
        

        
        
       
        
        
        
            

        
        
        
    
    
    
        
        
       
    
    

        



  
        
    
        

        
        