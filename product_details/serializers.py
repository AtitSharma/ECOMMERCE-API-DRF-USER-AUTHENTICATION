from rest_framework import serializers
from product_details.models import Products,Cart



class ProductSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    name=serializers.CharField()
    details=serializers.CharField()
    price=serializers.IntegerField()
    user=serializers.CharField(required=False)
    
    def create(self, validated_data):
        name=validated_data.get("name")
        details=validated_data.get("details")
        price=validated_data.get("price")
        user=self.context.get("user")
        if user:
            return Products.objects.create(name=name,details=details,price=price,user=user)
        return serializers.ValidationError("Provide Valid Token ")
    
    def update(self, instance, validated_data):
        '''
        THIS WILL WORK WHEN PUT request or PATCH REQUEST IS SENT
        '''
        instance.name=validated_data.get('name',instance.name)
        instance.details=validated_data.get("details",instance.details)
        instance.price=validated_data.get("price",instance.price)
        instance.save()
        return instance
        
    
    
    
    
class CartSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    name=serializers.CharField(read_only=True)
    product_id=serializers.IntegerField()
    product=serializers.CharField(read_only=True)
    totalprice=serializers.IntegerField(read_only=True)
    quantity=serializers.IntegerField(read_only=True)
    
    
    
    def create(self, validated_data):
        quantity=1
        product_id=validated_data.get("product_id")
        product=Products.objects.get(id=product_id)
        price=Products.objects.get(id=product_id).price
        totalprice=quantity*price
        name=self.context.get("name")
        
        if name:
            return Cart.objects.create(name=name,product=product,quantity=quantity,totalprice=totalprice)
        return serializers.ValidationError("Cannot Add to Cart")
    
    
    def validate_product_id(self, value):
        product=Products.objects.filter(id=value).first()
        if not product:
            return serializers.ValidationError(" No product with such id ")
        
        return value
    
    

        



  
        
    
        

        
        