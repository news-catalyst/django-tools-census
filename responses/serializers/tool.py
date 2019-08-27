from responses.models import Tool
from rest_framework import serializers


class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = "__all__"
