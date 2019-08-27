import csv
import os

from django.core.management.base import BaseCommand
from responses.models import NewsOrgType


class Command(BaseCommand):
    help = "Bootstraps initial news org types"

    def handle(self, *args, **options):
        print("Bootstrapping news org types")
        cmd_path = os.path.dirname(os.path.realpath(__file__))
        data_path = os.path.join(cmd_path, '../data/news_org_types.csv')

        with open(data_path) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                NewsOrgType.objects.update_or_create(name=row[0])
