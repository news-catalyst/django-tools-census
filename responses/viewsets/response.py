from responses.conf import settings
from responses.models import Response
from responses.serializers import ResponseSerializer
from responses.tasks import add_survey_response
from responses.utils.importers import import_class
from rest_framework.views import APIView
from rest_framework.response import Response as RestResponse

authentication = import_class(settings.API_AUTHENTICATION_CLASS)
permission = import_class(settings.API_PERMISSION_CLASS)


class ResponseViewSet(APIView):
    serializer_class = ResponseSerializer

    def get(self, request):
        responses = Response.objects.all()
        data = ResponseSerializer(responses, many=True).data

        return RestResponse(data)

    def post(self, request):
        add_survey_response.delay(request.data)
        return RestResponse(200)
