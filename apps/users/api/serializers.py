import re
from rest_framework import serializers, status
from apps.users.models import Profile
from django.contrib.auth.models import User
from apps.users.models import Review

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', \
                   'description', 'working_hours', 'type', 'email', 'created_at']

    def get_username(self, obj):
        return obj.user.username

    def get_email(self, obj):
        return obj.user.email   

    def get_created_at(self, obj):
        return obj.user.date_joined
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "Falsche Anmeldedaten."})

        if not user.check_password(password):
            raise serializers.ValidationError({"detail": "Falsche Anmeldedaten."})

        data['user'] = user
        return data


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'repeated_password', 'type')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, data):
        pw = data['password']
        repeated_pw = data['repeated_password']
        errors = {}

        if User.objects.filter(username=data['username']).exists():
            errors.setdefault('username', []).append("Dieser Benutzername ist bereits vergeben.")

        if User.objects.filter(email=data['email']).exists():
            errors.setdefault('email', []).append("Diese E-Mail-Adresse wird bereits verwendet.")

        if not data['email']:
            errors.setdefault('email', []).append("E-Mail ist erforderlich.")

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data['email']):
            errors.setdefault('email', []).append("E-Mail-Format ist ungültig.")

        if pw != repeated_pw:
            errors.setdefault('password', []).append("Das Passwort ist nicht gleich mit dem wiederholten Passwort")
        
        if errors:
            raise serializers.ValidationError(errors, code=400)

        return data 
    

    def create(self, validated_data):
        user = User(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()

        Profile.objects.create(user=user, type=validated_data['type'])

        return user
    

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']

    def validate(self, data):
        user = self.context['request'].user

        # Überprüfen, ob der Nutzer ein "customer" ist
        if user.profile.type != 'customer':
            raise serializers.ValidationError(
                detail={"error": "Nur Kunden können Bewertungen abgeben."},
                code=status.HTTP_403_FORBIDDEN)

        # Überprüfen, ob der aktuelle Nutzer der Reviewer ist
        if data['reviewer'].id != self.context['request'].user.id:
            raise serializers.ValidationError(
                detail={"error": "Der Reviewer muss der aktuelle Nutzer sein."},
                code=status.HTTP_403_FORBIDDEN)

        # Überprüfen, ob bereits eine Bewertung für diesen Geschäftsnutzer existiert
        if Review.objects.filter(business_user=data['business_user'], reviewer=data['reviewer']).exists():
            raise serializers.ValidationError(
                detail={"error": "Du hast diesen User schon einmal bewertet."},
                code=status.HTTP_400_BAD_REQUEST)

        return data
    

        
