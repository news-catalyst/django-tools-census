from django.urls import re_path, path

from .views import Home
from .viewsets import ResponseViewSet

urlpatterns = [
    path("", Home.as_view()),
    path("api/responses/", ResponseViewSet.as_view()),
]
