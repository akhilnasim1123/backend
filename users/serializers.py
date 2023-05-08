from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

from .models import *


User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'phone_number','email', 'password')

  def validate(self, data):
    user = User(**data)
    password = data.get('password')

    try:
      validate_password(password, user)
    except exceptions.ValidationError as e:
      serializer_errors = serializers.as_serializer_error(e)
      raise exceptions.ValidationError(
        {'password': serializer_errors['non_field_errors']}
      )

    return data
  def create(self, validated_data):
    user = User.objects.create_user(
      first_name=validated_data['first_name'],
      last_name=validated_data['last_name'],
      phone_number=validated_data['phone_number'],
      email=validated_data['email'],
      password=validated_data['password'],
    )

    return user
  
# class UserChangePasswordSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = User
#     fields = ('first_name', 'last_name', 'phone_number','email', 'password')

#   def validate(self, data):
#     user = User(**data)
#     password = data.get('password')

#     try:
#       validate_password(password, user)
#     except exceptions.ValidationError as e:
#       serializer_errors = serializers.as_serializer_error(e)
#       raise exceptions.ValidationError(
#         {'password': serializer_errors['non_field_errors']}
#       )

#     return data
#   def save(self, validated_data):
#     user = User.objects.create_user(
#       first_name=validated_data['first_name'],
#       last_name=validated_data['last_name'],
#       phone_number=validated_data['phone_number'],
#       email=validated_data['email'],
#       password=validated_data['password'],
#     )

#     return user



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User    
        fields = ('first_name', 'last_name', 'phone_number','email','is_active','is_superuser','image_url','wordCount','premium','subscriptionType','monthlyCount','email_verified')

# class ContentSerializer(serializers.)

class BlogIdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogIdea    
        fields = ('title','blog_ideas','unique_id')

class BlogSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogSection   
        fields = ('title','body','date_created')

class BlogCollectionSerializer(serializers.ModelSerializer):
   class Meta:
      model = BlogCollection
      fields = ('title','blog','keywords','accuracy','wordCount','unique_id')

class BlogIdeaSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogIdeaSave  
        fields = ('title','blog_ideas','keywords','wordCount','unique_id','idea','idea_key')


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryDetails  
        fields = ('title','story','audience','keywords','wordCount','unique_id')

class PrimeSerializer(serializers.ModelSerializer):
   class Meta:
      model = Prime
      fields = "__all__"

class PrimeNameSerializer(serializers.ModelSerializer):
   class Meta:
      model = Prime
      fields = ('prime',)

class UserPasswordsSerializer(serializers.ModelSerializer):
   class Meta:
      model = UserAccount
      fields = ('password',)

class PremiumSubscriptionSerializer(serializers.ModelSerializer):
   class Meta:
      model = PremiumSubscription
      fields = "__all__"
class CurrentSubSerializer(serializers.ModelSerializer):
   class Meta:
      model = CurrentSub
      fields = "__all__"
