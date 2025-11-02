import os
from celery import Celery
import eventlet
eventlet.monkey_patch()

# Установите переменную окружения для настроек Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

# Загрузите конфигурацию из settings.py с префиксом CELERY_
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически обнаруживайте задачи в приложениях
app.autodiscover_tasks()
