from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet
from .apps import TrackerConfig

app_name = TrackerConfig.name

router = DefaultRouter()
router.register(r'tracker', HabitViewSet, basename='tracker')

urlpatterns = [
    path('', include(router.urls)),
]