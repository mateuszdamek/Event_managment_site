from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError

# ? UserModel is the user model that is used in the project


UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        if not (username or email):
            raise serializers.ValidationError('Username or email is required.')

        user = None
        if username:
            user = authenticate(username=username, password=password)
        elif email:
            user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid username or password.')

        attrs['user'] = user
        return attrs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_ID', 'username', 'email')


"""
#? UserSerializer but without register authentication
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_ID", "username", "email"]


#! Might not be needed and just should fetched with user
class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ["user_ID", "role"]
"""


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "event_ID",
            "title",
            "date",
            "description",
            "start_date",
            "end_date",
            "location",
            "organizer_ID",
            "parent_event_ID",
            "status",
        ]


class EventSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event_Submission
        fields = [
            "submission_ID",
            "event_ID",
            "title",
            "description",
            "submitter_ID",
            "status",
        ]


class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event_Registration
        fields = ["registration_ID", "event_ID", "user_ID", "registration_Date"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_ID", "name"]


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Event_Category
        fields = ["event_ID", "category_ID"]
        # * Creating pk for two fields
        constraints = [
            models.UniqueConstraint(
                fields=["event_ID", "category_ID"], name="EventCategory_pk"
            )
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["tag_ID", "name"]


class EventTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event_Tag
        fields = ["event_ID", "tag_ID"]
        # * Creating pk for two fields
        constraints = [
            models.UniqueConstraint(fields=["event_ID", "tag_ID"], name="EventTag_pk")
        ]
