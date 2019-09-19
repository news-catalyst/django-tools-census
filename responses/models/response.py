from django.db import models
from .news_org_type import NewsOrgType
from .tool import Tool
from .tool_task import ToolTask


class Response(models.Model):
    date_submitted = models.DateTimeField(auto_now_add=True)
    job_title = models.CharField(max_length=500)
    job_duties = models.TextField()
    news_org_name = models.CharField(max_length=500, null=True, blank=True)
    news_org_type = models.ForeignKey(NewsOrgType, on_delete=models.PROTECT)
    news_org_age = models.CharField(max_length=100)
    tools_used = models.ManyToManyField(Tool)
    most_important_tool = models.ForeignKey(
        Tool, on_delete=models.PROTECT, related_name="most_important_tool"
    )
    tasks_used = models.ManyToManyField(ToolTask)
    tool_satisfaction = models.CharField(max_length=100)
    tool_recommendation = models.CharField(max_length=100)
    tool_recommendation_why_not = models.TextField(null=True, blank=True)
    stopped_using = models.CharField(max_length=500, null=True, blank=True)
    why_stopped_using = models.TextField(null=True, blank=True)
    org_struggle = models.CharField(max_length=100)
    org_struggle_other = models.TextField(null=True, blank=True)
    org_comparison = models.CharField(max_length=100)
    org_communication = models.CharField(max_length=100)
    org_sustainability = models.CharField(max_length=100)
    talk_more = models.BooleanField(default=False)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return "{} {}".format(
            self.date_submitted.strftime('%Y-%m-%d %H:%M'),
            self.job_title
        )
