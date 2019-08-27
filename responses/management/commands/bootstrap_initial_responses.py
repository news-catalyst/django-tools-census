import csv
import os

from django.core.management.base import BaseCommand
from responses.models import NewsOrgType, Response, Tool, ToolTask


class Command(BaseCommand):
    help = "Parses initial responses from Google spreadsheet"

    def parse_response(self, response):
        news_org_type = self.parse_news_org_type(response["newsOrgType"])
        tools_used = self.parse_tools(response["toolsUsed"])
        most_important_tool = self.parse_most_important_tool(
            response["mostImportantTool"]
        )
        tasks_used = self.parse_tool_tasks(response["tasksUsed"])
        stopped_using = self.parse_boolean(response["stoppedUsing"])
        talk_more = self.parse_boolean(response["talkMore"])

        obj = Response.objects.update_or_create(
            job_title=response["jobTItle"],
            job_duties=response["jobDuties"],
            news_org_type=news_org_type,
            news_org_age=response["newsOrgAge"],
            most_important_tool=most_important_tool,
            tool_satisfaction=response["toolSatisfaction"],
            tool_recommendation=response["toolRecommendation"],
            stopped_using=stopped_using,
            why_stopped_using=response["whyStoppedUsing"],
            org_struggle=response["orgStruggles"],
            org_comparison=response["orgComparison"],
            org_communication=response["orgCommunication"],
            org_sustainability=response["orgSustainability"],
            talk_more=talk_more,
            email=response["email"],
        )[0]

        obj.tools_used.set(tools_used)
        obj.tasks_used.set(tasks_used)

    def parse_news_org_type(self, news_org_type):
        return NewsOrgType.objects.update_or_create(name=news_org_type)[0]

    def parse_tools(self, tools):
        parsed_tools = []
        for tool in tools.split(","):
            parsed_tools.append(Tool.objects.update_or_create(name=tool)[0])

        return parsed_tools

    def parse_most_important_tool(self, tool):
        return Tool.objects.update_or_create(name=tool)[0]

    def parse_tool_tasks(self, tool_tasks):
        parsed_tasks = []
        for task in tool_tasks.split(","):
            parsed_tasks.append(
                ToolTask.objects.update_or_create(name=task)[0]
            )

        return parsed_tasks

    def parse_boolean(self, answer):
        if answer == "Yes":
            return True

        return False

    def handle(self, *args, **options):
        print("Bootstrapping tool tasks")
        cmd_path = os.path.dirname(os.path.realpath(__file__))
        data_path = os.path.join(cmd_path, "../data/news_tools_census.tsv")

        with open(data_path) as f:
            reader = csv.DictReader(f, dialect="excel-tab")

            for row in reader:
                self.parse_response(row)
