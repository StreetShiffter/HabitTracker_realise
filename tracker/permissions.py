from rest_framework import permissions


class IsOwnerOrReadOnlyForPublic(permissions.BasePermission):
    """Переопределение прав между админом и юзером"""

    def has_object_permission(self, request, view, obj):
        # Любой может читать публичные привычки
        if request.method in permissions.SAFE_METHODS and obj.is_public:
            return True

        # Владелец или админ может читать свои привычки
        if request.method in permissions.SAFE_METHODS:
            return obj.owner == request.user or request.user.is_staff

        # Изменение/удаление — только владелец
        return obj.owner == request.user