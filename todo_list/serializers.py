from rest_framework import serializers
from .models import TodoItem

class TodoItemSerializer(serializers.ModelSerializer):
    created_at = serializers.DateField(required=False)
    class Meta:
        model = TodoItem
        fields = '__all__'