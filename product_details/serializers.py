from rest_framework import serializers
from product_details.models import Products



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
        
    
    
    


  
        
    
        

        
        