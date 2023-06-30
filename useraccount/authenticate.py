from rest_framework.authentication import TokenAuthentication
from useraccount.models import Token




class CustomTokenAuthentication(TokenAuthentication):
    model=Token
    
    def authenticate_credentials(self, key):
        model=self.get_model()
        
        try:
            token=model.objects.get(key=key)
        except model.DoesNotExist:
            return None
        if not token.is_valid():
            return None
        return (token.user, token)
        

        
        
    
    


