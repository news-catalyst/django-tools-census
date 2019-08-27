from responses.models import ToolTask
from rest_framework import serializers


class ToolTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolTask
        fields = "__all__"
