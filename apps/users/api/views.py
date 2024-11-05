from .serializers import RegistrationSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import LoginSerializer, ProfileSerializer, ReviewSerializer
from apps.users.models import Profile, Review
from django.contrib.auth.models import User
import re
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

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
    
    # def list(self, request, *args, **kwargs):
    #     response = super().list(request, *args, **kwargs)
        
    #     customized_data = []
    #     for item in response.data:
    #         customized_data.append({
    #             "user": {
    #                 "pk": item["user"],
    #                 "username": item["username"],
    #                 "first_name": item["first_name"],
    #                 "last_name": item["last_name"]
    #             },
    #             "file": item["file"],
    #             "location": item["location"],
    #             "tel": item["tel"],
    #             "description": item["description"],
    #             "working_hours": item["working_hours"],
    #             "type": item["type"]
    #         })
    #     return Response(customized_data, status=status.HTTP_200_OK)


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

        if data.get('email'):
            # Überprüfe, ob die E-Mail-Adresse bereits verwendet wird (außer vom aktuellen Benutzer)
            if User.objects.filter(email=data.get('email')).exclude(pk=profile.user.pk).exists():
                return Response({"detail": "Diese E-Mail-Adresse wird bereits verwendet."}, status=status.HTTP_400_BAD_REQUEST)

            # Überprüfe das Format der E-Mail-Adresse
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data.get('email')):
                return Response({"detail": "E-Mail-Format ist ungültig."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProfileSerializer(profile, data=data, partial=True)
        if serializer.is_valid():
            profile.user.email = data.get('email', profile.user.email)
            profile.user.save()
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


class ReviewView(generics.GenericAPIView):
    """
    Create a review for a business user.

    - **POST**: Creates a review for a business user.
    - **GET**: Retrieves all reviews for a business user, with filtering by `business_user_id`.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business_user_id', 'reviewer_id']
    ordering_fields = ['updated_at', 'rating']

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
