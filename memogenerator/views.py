from django.contrib.auth.models import User, Group
from rest_framework.decorators import api_view
from rest_framework import viewsets, generics, views
from rest_framework import permissions
from memogenerator import serializers
# from vinsight.memogenerator.memo_creator import MemoCreator
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from django.http import JsonResponse
from memogenerator.memo_creator import generate_mad_memo


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET', 'POST'])
class SendEmailTest(generics.ListCreateAPIView):
    print("hellosfgf")

    # MemoCreator.memoCreate()
    # queryset = User.objects.all()
    # serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


class FileUploadView(views.APIView):

    test_data = {
        "name": "test",
        "email": ""
    }

    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        file_obj = request.data
        print(file_obj)
        return Response(self.test_data)


class DataConsumer(views.APIView):
    def get(self, request, *args, **kwargs):
        print("get")
        return Response(request.data)

    def post(self, request, *args, **kwargs):
        company_data = JSONParser().parse(request)
        company_serializer = serializers.CompanySerializers(data=company_data)
        print(company_serializer)
        # if company_serializer.is_valid():company_name

        response = generate_mad_memo(
            company_data['name'], company_data['website'], company_data['pitch'])

        return JsonResponse({'data': response})
        # else:
        #     print(company_serializer.errors)response
        #     return Response('Yo.. there was an error .... these things happen')
