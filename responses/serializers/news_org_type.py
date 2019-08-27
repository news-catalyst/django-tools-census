from responses.models import NewsOrgType
from rest_framework import serializers


class NewsOrgTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsOrgType
        fields = "__all__"
