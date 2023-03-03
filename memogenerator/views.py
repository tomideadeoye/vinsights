from rest_framework import permissions
from memogenerator import serializers
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.response import Response
from django.http import JsonResponse
from memogenerator.memo_creator import generate_mad_memo
from rest_framework import viewsets, status
from memogenerator.models import Company


class CompanyDataView(viewsets.ModelViewSet):
    print('test')
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    queryset = Company.objects.all()
    serializer_class = serializers.CompanySerializers

    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.save()

        # Extract data from the request
        name = serializer.validated_data['name']
        emailTo = serializer.validated_data['emailTo']
        website = serializer.validated_data['website']
        pitch_uploaded = request.FILES['pitch_uploaded']

        print(pitch_uploaded)

        # do something with the data
        response = generate_mad_memo(
            name,
            website,
            pitch_uploaded,
            emailTo,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(response,
                        status=status.HTTP_201_CREATED,
                        headers=headers)
