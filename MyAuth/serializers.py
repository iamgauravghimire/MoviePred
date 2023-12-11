from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile
from MoviePred.models import Genre

class UserProfileSerializer(serializers.ModelSerializer):
    genre_preferences = serializers.PrimaryKeyRelatedField(many=True, queryset = Genre.objects.all())
    class Meta:
        model = UserProfile
        fields = ( 'profile_picture', 'genre_preferences')
        

class UserRetrieveSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email','first_name', 'last_name', 'profile')
        

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
    required = True,
    validators = [UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators = [validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    user_profile = UserProfileSerializer(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name','user_profile')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name' : {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs
    
    def create(self, validated_data):
        profile_data = validated_data.pop('user_profile', {})
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name = validated_data['last_name']
        )
    
        user.set_password(validated_data['password'])
        user.save()


        userprofile = UserProfile.objects.create(user=user)
        userprofile.phone_number = profile_data.get('phone_number', userprofile.phone_number)
        userprofile.profile_picture = profile_data.get('profile_picture', userprofile.profile_picture)
        genres = profile_data.get('genre_preferences')
        if genres is not None:
            userprofile.genre_preferences.set(genres)
        userprofile.save()

        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True,validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct."})
        return value
    
    def update(self, instance, validated_data):
        user = self.context['request'].User

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You don't have the permission for this user."})
        instance.set_password(validated_data['password'])
        instance.save()

        return instance



class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'profile')
        extra_kwargs = {
            'first_name' : {'required' : True},
            'last_name' : {'required': True},
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({'email': "This email is already in use."})

        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})

        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You don't have permission for this user."})

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']

        instance.save()

        profile_data = validated_data.get('profile')
        if profile_data:
            profile = instance.profile
            profile.phone_number = profile_data.get('phone_number', profile.phone_number)
            profile.profile_picture = profile_data.get('profile_picture', profile.profile_picture)
            profile.genre_preferences.set(profile_data.get('genre_prefernces', profile.genre_preferences.all()))
            profile.save()


        return instance