from rest_framework.permissions import BasePermission



class ProductDeleteUpdatePermission(BasePermission):
    
    '''
    
        THIS PERMISSION ALLOWS THE SUPER USER AND THE PRODUCT USER TO UPDATE AND DELETE THEIR PRODUCTS
        
    '''

    def has_object_permission(self, request, view, obj):
        if not obj:
            return False
        if request.user.is_superuser or request.user == obj.user:
            return True
        return False
    

class CartUpdateDeletePermission(BasePermission):
    
    '''
        THIS IS TO GIVE THOSE USER A PERMISSION TO UPDATE AND DELETE CART !!!
    '''
    
    def has_object_permission(self, request, view, obj):
        if not obj:
            return False
        if (request.user.is_superuser) or (request.user== obj.name):
            return True
        return False
    

    
    
    
        

            
            
        

         

         