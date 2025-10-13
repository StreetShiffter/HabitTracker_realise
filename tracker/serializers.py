from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели привычки"""
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('owner',)

    def validate(self, data):
        # Валидация на уровне сериализатора
        habit = Habit(**data)
        habit.clean()
        return data