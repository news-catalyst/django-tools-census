from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Calls all bootstrap commands"

    def handle(self, *args, **options):
        print("Bootstrapping responses")
        call_command("bootstrap_news_org_types")
        call_command("bootstrap_tool_tasks")
