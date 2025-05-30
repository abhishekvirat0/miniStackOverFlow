import requests
import logging
from django.conf import settings
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer
logger = logging.getLogger(__name__)
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
    try:
        response = requests.post(token_url, data=data)

        # Log the response status and body
        logger.debug(f"Token response status: {response.status_code}")
        logger.debug(f"Token response body: {response.text}")

        if response.status_code == 200:
            return Response(response.json())
        else:
            return Response({"error": "Invalid credentials or OAuth error"}, status=response.status_code)
    except Exception as e:
        logger.error(f"Error in token request: {str(e)}", exc_info=True)
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
