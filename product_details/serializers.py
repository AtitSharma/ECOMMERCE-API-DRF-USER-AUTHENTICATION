from rest_framework import serializers
from product_details.models import Products



class ProductSerializer(serializers.Serializer):
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
    

        
        
    
        

        
        