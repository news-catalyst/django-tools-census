import os

from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toolscensus.settings')

app = Celery('toolscensus')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(
    broker_url=os.getenv("REDIS_URL", "redis://127.0.0.1:6379"),
    task_serializer="json",
    timezone="America/New_York",
)

if settings.DEBUG:
    app.conf.update(task_always_eager=True)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
