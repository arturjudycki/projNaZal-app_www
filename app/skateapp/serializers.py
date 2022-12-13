from rest_framework import serializers
from django.contrib.auth.models import User as AuthUser
from .models import User_detail, Competition, Registration
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.password_validation import validate_password
import datetime

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        # validators=[UniqueValidator(queryset=AuthUser.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = AuthUser
        fields = ('id', 'username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }
        read_only_fields = ['id']
        validators = [UniqueTogetherValidator(queryset=AuthUser.objects.all(),fields=['username', 'email'])]


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user_auth = AuthUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user_auth.set_password(validated_data['password'])

        user_skateapp = User_detail.objects.create(
            user=user_auth
        )

        user_auth.save()
        user_skateapp.save()

        return user_auth

class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ['id', 'city', 'street', 'date', 'description']
        read_only_fields = ['id']

    def validate_city(self, value):

        if not value.istitle():
            raise serializers.ValidationError(
                "Miasto musi zaczynać się z wielkiej litery",
            )
        return value

    def validate_date(self, value):
        if value < datetime.date.today():
            raise serializers.ValidationError(
                "Data nie może być z przeszłości.",
            )
        return value

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['id', 'status', 'id_competition', 'id_user']
        read_only_fields = ['id']

class User_detail_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User_detail
        fields = ['id', 'age', 'gender', 'stance', 'user']
        read_only_fields = ['id']