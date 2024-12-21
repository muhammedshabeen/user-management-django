from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from user_app.models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated


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
            

class ProfileView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        user = request.user
        serialzier = ProfileEditSerializer(user)
        return Response({
            "status":1,
            "message":"success",
            "data":serialzier.data
        })
    
    def put(self,request):
        user = request.user
        serializer = ProfileEditSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "status":1,
                "message": "Profile updated successfully.",
                "data": serializer.data
            })

        return Response({
            "status":0,
            "message": "Profile update failed.",
            "errors": serializer.errors
        })
        
class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        password1 = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if not password1 == confirm_password:
            return Response({
                "status":0,
                "message": "Passwords mismatched"
                })

        if len(confirm_password) < 8:
            return Response({
                "status":0,
                "message": "Password must be at least 8 characters long."
                             })
        
        if not any(char.isupper() for char in confirm_password):
            return Response({
                "status":0,
                "message": "Password must contain at least one uppercase letter."
                })
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', confirm_password):
            return Response({
                "status":0,
                "message": "Password must contain at least one special character."
                })

        user.set_password(confirm_password)
        user.save()

        Token.objects.filter(user=user).delete()
        
        return Response({
            "status":1,
            "message": "Password updated successfully."
            })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response({
            "status":1,
            "message": "Logged out successfully."
            })
        
class UserLists(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        users = CustomUser.objects.exclude(is_superuser=True)
        serializer = RegisterSerializer(users,many=True)
        return Response({
            "status":1,
            "message":"success",
            "data":serializer.data
        })