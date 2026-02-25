from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

# get_user_model().objects.create_user

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'bio', 'token']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            bio=validated_data.get('bio', '')
        )
        token, _ = Token.objects.get_or_create(user=user)
        user.token = token.key
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        token, _ = Token.objects.get_or_create(user=user)
        return {
            'user': user,
            'token': token.key
        }


class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(
        source='followers.count',
        read_only=True
    )
    following_count = serializers.IntegerField(
        source='following.count',
        read_only=True
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'bio',
            'profile_picture',
            'followers_count',
            'following_count'
        ]