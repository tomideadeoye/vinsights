from rest_framework.viewsets import ViewSet
from rest_framework import permissions
from memogenerator import serializers
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from django.http import JsonResponse
from memogenerator.memo_creator import generate_mad_memo
from .serializers import CompanySerializers
from rest_framework.generics import ListCreateAPIView


class CompanyDataView(ListCreateAPIView):

    def post(self, request, *args, **kwargs):
        serializer_class = CompanySerializers
        company_data = JSONParser().parse(request)
        company_serializer = serializers.CompanySerializers(data=company_data)
        # if company_serializer.is_valid():company_name

        response = generate_mad_memo(
            company_data['name'], company_data['website'], company_data['pitch_uploaded'], company_data['emailTo'],)

        return JsonResponse({"data": response})
    # else:
    #     print(company_serializer.errors)response
    #     return Response('Yo.. there was an error .... these things happen')

    def get(self, request, *args, **kwargs):
        print("hello")
        return JsonResponse({'data': 'hello'})
