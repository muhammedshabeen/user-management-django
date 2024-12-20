from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from user_app.models import *
from .serializers import RegisterSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "status":1,
                "message": "User registered successfully",
            })
        return Response({
            "status":0,
            "message":serializer.errors,
        })
        
class LoginView(APIView):
    
    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        print("EMAIL IS",email)
        
        if not email or not password:
            return Response({"detail": "Email and password are required."})

        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response({"detail": "Email and password are required."})

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "message": "Login successful.",
            "token": token.key,
            "user": {
                "id":user.id,
                "username":user.username
                },
        })
            