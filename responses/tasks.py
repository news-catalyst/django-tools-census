from celery import shared_task
from responses.models import NewsOrgType, Response, Tool, ToolTask


@shared_task(acks_late=True)
def add_survey_response(response):
    news_org_type = NewsOrgType.objects.get_or_create(
        name=response['newsOrgType']
    )[0]

    tools_used = [Tool.objects.get_or_create(
        name=tool
    )[0] for tool in response["toolsUsed"]]

    most_important_tool = Tool.objects.get_or_create(
        name=response['mostImportantTool']
    )[0]

    tasks_used = [ToolTask.objects.get_or_create(
        name=task
    )[0] for task in response["tasksUsed"]]

    obj = Response.objects.create(
        job_title=response['jobTitle'],
        job_duties=response['jobDuties'],
        news_org_name=response['newsOrgName'],
        news_org_type=news_org_type,
        news_org_age=response['newsOrgAge'],
        most_important_tool=most_important_tool,
        tool_satisfaction=response['toolSatisfaction'],
        tool_recommendation=response['toolRecommendation'],
        tool_recommendation_why_not=response[
            'toolRecommendationWhyNot'
        ],
        stopped_using=response['stoppedUsing'],
        why_stopped_using=response['whyStoppedUsing'],
        org_struggle=response['orgStruggles'],
        org_struggle_other=response['orgStrugglesOther'],
        org_comparison=response['orgComparison'],
        org_communication=response['orgCommunication'],
        org_sustainability=response['orgSustainability'],
        talk_more=True if response['talkMore'] == 'Yes' else False,
        email=response['email']
    )

    obj.tools_used.set(tools_used)
    obj.tasks_used.set(tasks_used)
