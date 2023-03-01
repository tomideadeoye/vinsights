from rest_framework import serializers
from memogenerator.models import Company


class CompanySerializers(serializers.Serializer):
    class Meta:
        model = Company
        fields = ['name', 'website', 'emailTo', 'pitch_uploaded', ]

    name = serializers.CharField(max_length=100)
    website = serializers.CharField(max_length=100)
    emailTo = serializers.CharField(max_length=100)
    pitch_uploaded = serializers.FileField()
