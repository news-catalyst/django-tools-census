import json

from celery import shared_task
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from responses.models import NewsOrgType, Response, Tool, ToolTask
from responses.utils.aws import defaults, get_bucket


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


@shared_task(acks_late=True)
def publish_survey_data():
    responses = Response.objects.all()
    tools = Tool.objects.all()
    tasks = ToolTask.objects.all()

    time_series = [
        response.date_submitted.isoformat() for response in responses
    ]

    news_org_type_counts = list(
        responses.values('news_org_type__name').annotate(
            num=Count('news_org_type__name')
        )
    )

    news_org_name_counts = list(responses.values('news_org_name').annotate(
        num=Count('news_org_name')
    ))

    org_struggle_counts = list(responses.values('org_struggle').annotate(
        num=Count('org_struggle')
    ))

    org_comparison_counts = list(responses.values('org_comparison').annotate(
        num=Count('org_comparison')
    ))

    org_communication_counts = list(responses.values('org_communication').annotate(
        num=Count('org_communication')
    ))

    org_sustainability_counts = list(responses.values('org_sustainability').annotate(
        num=Count('org_sustainability')
    ))

    number_of_tools = tools.count()

    tool_counts = list(tools.values('name').annotate(num=Count('response')))
    task_counts = list(tasks.values('name').annotate(num=Count('response')))

    data = {
        "time_series": time_series,
        "org_struggle_counts": org_struggle_counts,
        "org_comparison_counts": org_comparison_counts,
        "org_communication_counts": org_communication_counts,
        "org_sustainability_counts": org_sustainability_counts,
        "news_org_type_counts": news_org_type_counts,
        "news_org_name_counts": news_org_name_counts,
        "number_of_tools": number_of_tools,
        "tool_counts": tool_counts,
        "task_counts": task_counts
    }

    with open('data.json', 'w') as f:
        json.dump(data, f, cls=DjangoJSONEncoder)

    # key = "news-tools-census/responses/data.json"
    # bucket = get_bucket()
    # bucket.put_object(
    #     Key=key,
    #     ACL=defaults.ACL,
    #     Body=json.dumps(data),
    #     CacheControl=defaults.CACHE_HEADER,
    #     ContentType="application/json",
    # )
