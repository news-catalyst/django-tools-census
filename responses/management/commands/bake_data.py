from django.core.management.base import BaseCommand
from responses.tasks import publish_survey_data

class Command(BaseCommand):
    help = "Bakes data"

    def handle(self, *args, **options):
      publish_survey_data.delay()
