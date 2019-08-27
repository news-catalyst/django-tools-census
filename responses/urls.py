from django.urls import re_path, path

from .viewsets import ResponseViewSet

urlpatterns = [
    path("api/responses/", ResponseViewSet.as_view()),
]
