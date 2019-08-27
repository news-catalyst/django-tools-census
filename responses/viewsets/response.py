from responses.conf import settings
from responses.models import NewsOrgType, Response, Tool, ToolTask
from responses.serializers import ResponseSerializer
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
        news_org_type = NewsOrgType.objects.get_or_create(
            name=request.data['newsOrgType']
        )[0]

        tools_used = [Tool.objects.get_or_create(
            name=tool
        )[0] for tool in request.data["toolsUsed"]]

        most_important_tool = Tool.objects.get_or_create(
            name=request.data['mostImportantTool']
        )[0]

        tasks_used = [ToolTask.objects.get_or_create(
            name=task
        )[0] for task in request.data["tasksUsed"]]

        obj = Response.objects.create(
            job_title=request.data['jobTitle'],
            job_duties=request.data['jobDuties'],
            news_org_name=request.data['newsOrgName'],
            news_org_type=news_org_type,
            news_org_age=request.data['newsOrgAge'],
            most_important_tool=most_important_tool,
            tool_satisfaction=request.data['toolSatisfaction'],
            tool_recommendation=request.data['toolRecommendation'],
            tool_recommendation_why_not=request.data[
                'toolRecommendationWhyNot'
            ],
            stopped_using=request.data['stoppedUsing'],
            why_stopped_using=request.data['whyStoppedUsing'],
            org_struggle=request.data['orgStruggles'],
            org_struggle_other=request.data['orgStrugglesOther'],
            org_comparison=request.data['orgComparison'],
            org_communication=request.data['orgCommunication'],
            org_sustainability=request.data['orgSustainability'],
            talk_more=True if request.data['talkMore'] == 'Yes' else False,
            email=request.data['email']
        )

        obj.tools_used.set(tools_used)
        obj.tasks_used.set(tasks_used)

        return RestResponse(200)
