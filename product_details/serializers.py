from rest_framework import serializers
from product_details.models import Products
from rest_framework.authtoken.models import Token


class ProductSerializer(serializers.Serializer):
    name=serializers.CharField()
    details=serializers.CharField()
    price=serializers.IntegerField()
    user=serializers.CharField(required=False)
    
    def create(self, validated_data):
        name=validated_data.get("name")
        details=validated_data.get("details")
        price=validated_data.get("price")
        token= self.context.get("token")
        token=Token.objects.filter(key=token).first()
        if token:
            user=token.user    
            return Products.objects.create(name=name,details=details,price=price,user=user)
        return serializers.ValidationError("Provide Valid Token ")
    
    def validate(self, attrs):
        token= self.context.get("token")
        if Token.objects.filter(key=token).exists():
            return attrs
        return serializers.ValidationError("Provide a token ")
        
        
    
        

        
        