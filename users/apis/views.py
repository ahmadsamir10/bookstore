from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import status
from users.apis.serializers import RegisterSerializer, LoginSerializer
from rest_framework.throttling import AnonRateThrottle


# Register Throttling Handler
class RegistrationThrottle(AnonRateThrottle):
    """
    Custom Throttle class for the registration endpoint.
    Limits the number of requests to the registration endpoint for anonymous users.
    """
    scope = 'registration'


# Register View
class RegisterView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [RegistrationThrottle]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Register Throttling Handler
class LoginThrottle(AnonRateThrottle):
    """
    Custom Throttle class for the loin endpoint.
    Limits the number of requests to the login endpoint for anonymous users.
    """
    scope = 'login'


# Login View
class LoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [RegistrationThrottle]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
