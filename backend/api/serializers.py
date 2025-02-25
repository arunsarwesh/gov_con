from rest_framework import serializers
from . import models

class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Form
        fields = '__all__'

    def create(self, validated_data):
        return models.Form.objects.create(**validated_data)