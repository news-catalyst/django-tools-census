from responses.models import Response
from rest_framework import serializers

from .news_org_type import NewsOrgTypeSerializer
from .tool import ToolSerializer
from .tool_task import ToolTaskSerializer


class ResponseSerializer(serializers.ModelSerializer):
    news_org_type = serializers.SerializerMethodField()
    tools_used = serializers.SerializerMethodField()
    most_important_tool = serializers.SerializerMethodField()
    tasks_used = serializers.SerializerMethodField()

    def get_news_org_type(self, obj):
        return NewsOrgTypeSerializer(obj.news_org_type).data

    def get_tools_used(self, obj):
        parsed_tools = []
        for tool in obj.tools_used.all():
            parsed_tools.append(ToolSerializer(tool).data)

        return parsed_tools

    def get_most_important_tool(self, obj):
        return ToolSerializer(obj.most_important_tool).data

    def get_tasks_used(self, obj):
        parsed_tasks = []
        for task in obj.tasks_used.all():
            parsed_tasks.append(ToolTaskSerializer(task).data)

        return parsed_tasks

    class Meta:
        model = Response
        fields = (
            "date_submitted",
            "job_title",
            "job_duties",
            "news_org_name",
            "news_org_type",
            "news_org_age",
            "tools_used",
            "most_important_tool",
            "tasks_used",
            "tool_satisfaction",
            "tool_recommendation",
            "tool_recommendation_why_not",
            "stopped_using",
            "why_stopped_using",
            "org_struggle",
            "org_struggle_other",
            "org_comparison",
            "org_communication",
            "org_sustainability",
            "talk_more",
            "email",
        )
