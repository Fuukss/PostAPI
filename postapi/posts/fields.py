import json
from rest_framework import serializers

class JSONListField(serializers.Field):
    """
    Field that accepts a list as input and stores it as a JSON string,
    and converts the JSON string back to a list upon output.
    """
    def to_internal_value(self, data):
        if not isinstance(data, list):
            raise serializers.ValidationError("Expected a list of strings.")
        return data

    def to_representation(self, value):
        if isinstance(value, str):
            try:
                return json.loads(value)
            except Exception:
                return []
        return value
