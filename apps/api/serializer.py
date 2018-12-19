from rest_framework import serializers
from apps.storage.models import Fact

class FactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fact
        exclude = ('id',)
        read_only_fields = ('__all__',)

    uuid = serializers.CharField()
    hash = serializers.CharField()
    actor = serializers.ListField()
    type = serializers.CharField()
    result = serializers.JSONField()
    source = serializers.CharField()
    handler = serializers.CharField()
    meta = serializers.JSONField()
    description = serializers.CharField()
    is_active = serializers.BooleanField()
    created_at = serializers.CharField()