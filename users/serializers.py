from rest_framework import serializers
from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password", "city", "phone", "telegram_chat_id"]


    def create(self, validated_data):
        """Сохраняем пользователя и хэшируем пароль для БД"""
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля (чтение и обновление)"""
    class Meta:
        model = User
        fields = ["username", "email", "city", "phone", "telegram_chat_id", "date_joined"]
        read_only_fields = ["email", "date_joined"]  # email и дата — только чтение
