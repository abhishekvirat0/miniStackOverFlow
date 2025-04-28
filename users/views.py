import requests
from django.conf import settings
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer

User = get_user_model()


# Register API
class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


# Login API (OAuth2 Token)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def loginview(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

    data = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        'client_id': settings.OAUTH2_CLIENT_ID,
        'client_secret': settings.OAUTH2_CLIENT_SECRET,
    }

    token_url = request.build_absolute_uri('/o/token/')
    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        return Response(response.json())
    else:
        return Response({"error": "Invalid credentials or OAuth error"}, status=response.status_code)


# View own profile
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def userprofileview(request):
    user = request.user
    data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "reputation": user.reputation if hasattr(user, 'reputation') else 0
    }
    return Response(data)
