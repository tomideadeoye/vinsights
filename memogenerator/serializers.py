from django.contrib.auth.models import User, Group
from rest_framework import serializers
from memogenerator.models import Company


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class CompanySerializers(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'website', 'pitch']

    name = serializers.CharField(max_length=100)
    website = serializers.CharField(max_length=100)
    # pitch = serializers.CharField(max_length=100)
