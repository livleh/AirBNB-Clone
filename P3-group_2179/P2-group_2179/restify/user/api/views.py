from django.http import JsonResponse 
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


#access contain information about user - jwt.io
#customized serializer to add username in the access token
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    #customize token claim 

    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        #username will now be encrypted into the token
        token['username'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

#setting up api
@api_view(['GET'])
def getRoutes(request):
    #routes is a list 

    routes = [
        '/api/token',
        #refresh will give u a new token based off the sent refresh token
        '/api/token/refresh'
    ]
    
    return Response(routes)