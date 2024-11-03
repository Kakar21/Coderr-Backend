from .serializers import RegistrationSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import LoginSerializer, ProfileSerializer
from apps.users.models import Profile
from rest_framework.permissions import IsAuthenticated

class ProfileList(generics.ListAPIView):
    """
    List user based on type profiles.
    
    - **GET**: Returns all user profiles.
    """
    serializer_class = ProfileSerializer

    def get_queryset(self):
        queryset = Profile.objects.all()
        profile_type = self.kwargs.get('type', None)
        if profile_type:
            queryset = queryset.filter(type=profile_type)
        return queryset


class ProfileDetail(APIView):
    """
    Update a specific user profile.

    - **GET**: Retrieves a profile.
    - **PATCH**: Updates a profile.
    """
    def patch(self, request, pk):
        try:
            profile = Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Response({"detail": "Nutzer nicht gefunden."}, status=status.HTTP_404_NOT_FOUND)

        if profile.user != request.user:
            return Response({"detail": "Nicht berechtigt."}, status=status.HTTP_403_FORBIDDEN)

        # Exclude fields that should not be updated
        data = request.data.copy()
        data.pop('user', None)
        data.pop('username', None)
        data.pop('type', None)
        data.pop('created_at', None)

        serializer = ProfileSerializer(profile, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk):
        profile = Profile.objects.get(pk=pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

        

class LoginView(ObtainAuthToken):
    """
    Log in a user with username and password, returning a token.

    - **POST**: Logs in a user with username and password, returning a token.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        data = {}
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.id,
            }
            return Response(data, status=200)
        else:
            return Response(serializer.errors, status=400)


class RegistrationView(APIView):
    """
    Register a new user and return a token.

    - **POST**: Registers a new user and returns a token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():

            saved_user = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_user)
            data = {
                'token': token.key,
                'username': saved_user.username,
                'email': saved_user.email,
                'user_id': saved_user.id,
            }
            
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


