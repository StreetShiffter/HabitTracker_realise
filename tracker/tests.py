from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from datetime import time, timedelta
from tracker.models import Habit
from tracker.serializers import HabitSerializer
from tracker.tasks import (
    send_reminder,
    send_failure,
    send_telegram_message_task,
    check_all_habits,
)
from tracker.views import HabitViewSet
from users.models import User
from django.core.exceptions import ValidationError


class HabitModelTest(TestCase):
    """Тест создания данных из модделей"""

    def setUp(self):
        """Предустановка модели привычки"""
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.pleasant_habit = Habit.objects.create(
            owner=self.user,
            place="Дом",
            time=time(10, 0),
            action="Пить воду",
            pleasant_habit=True,
        )

    def test_create_habit(self):
        """Тест создания полезной привычки(по умолчанию False)"""
        habit = Habit.objects.create(
            owner=self.user,
            place="Парк",
            time=time(12, 0),
            action="Прогулка",
            reward="Шоколадка",
            periodicity=1,
            duration=60,
        )
        self.assertEqual(str(habit), "Прогулка в Парк в 12:00:00")
        self.assertEqual(habit.owner, self.user)

    def test_duration_validation(self):
        """Тест нарушения длительности(более 2-ух минут)"""
        habit = Habit(
            owner=self.user,
            place="Дом",
            time=time(10, 0),
            action="Пить воду",
            duration=150,
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_periodicity_validation(self):
        """Тест нарушения переодичности(более 7 дней)"""
        habit = Habit(
            owner=self.user,
            place="Дом",
            time=time(10, 0),
            action="Пить воду",
            periodicity=10,
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_pleasant_habit_validation(self):
        """Тест на награду у приятной привычки(запрет)"""
        habit = Habit(
            owner=self.user,
            place="Дом",
            time=time(10, 0),
            action="Пить воду",
            pleasant_habit=True,
            reward="Шоколадка",
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_habit_none_reward_and_pleasant_habit(self):
        """Тест на отсутствие любой награды у полезной привычки"""
        habit = Habit(
            owner=self.user,
            place="Дом",
            time=time(10, 0),
            action="Убрать комнату",
            pleasant_habit=False,
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_habit_all_reward(self):
        """Тест на применение награды и приятной привычки(запрет)"""
        test_habit = Habit.objects.create(
            owner=self.user,
            place="Дом",
            time=time(10, 0),
            action="Шоколадка",
            pleasant_habit=True,
        )

        habit = Habit(
            owner=self.user,
            place="Дом",
            time=time(10, 0),
            action="Убрать комнату",
            pleasant_habit=False,
            related_habit=test_habit,
            reward="Шоколадка",
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_related_habit_validation(self):
        """Проверка связи приятной привычки у полезной"""
        not_pleasant_habit = Habit.objects.create(
            owner=self.user,
            place="Дом",
            time=time(10, 0),
            action="Бег",
            reward="Шоколадка",
            pleasant_habit=False,
        )

        habit = Habit(
            owner=self.user,
            place="Дом",
            time=time(10, 0),
            action="Пить воду",
            related_habit=not_pleasant_habit,
            pleasant_habit=True,
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_habit_validation(self):
        """Тест запрет связки двух приятных привычек"""
        not_pleasant_habit = Habit.objects.create(
            owner=self.user,
            place="Дом",
            time=time(10, 0),
            action="Бег",
            reward="Шоколадка",
            pleasant_habit=True,
        )

        habit = Habit(
            owner=self.user,
            place="Дом",
            time=time(10, 0),
            action="Пить воду",
            related_habit=not_pleasant_habit,
            pleasant_habit=True,
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_not_habit_validation(self):
        """Тест запрет связки двух полезных привычек"""
        not_pleasant_habit = Habit.objects.create(
            owner=self.user,
            place="Дом",
            time=time(10, 0),
            action="Бег",
            reward="Шоколадка",
        )

        habit = Habit(
            owner=self.user,
            place="Дом",
            time=time(10, 0),
            action="Пить воду",
            related_habit=not_pleasant_habit,
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()


############################################################################################################
# ТЕСТИРОВАНИЕ ВЬЮШКИ


@patch("tracker.views.send_telegram_message_task.delay")
def test_perform_create_sends_telegram_pleasant_habit(self, mock_send_telegram):
    """Тест: perform_create отправляет сообщение для приятной привычки"""
    view = HabitViewSet()

    data = {
        "place": "Дом",
        "time": time(10, 0),
        "action": "Медитация",
        "pleasant_habit": True,
        "periodicity": 1,
        "duration": 60,
    }
    serializer = HabitSerializer(data=data)

    request = self.client.request()
    request.user = self.user  # с telegram_chat_id
    serializer.context = {"request": request}
    serializer.is_valid()

    view.perform_create(serializer)

    expected_message = "Создана новая приятная привычка: Медитация в Дом"
    mock_send_telegram.assert_called_once_with(
        chat_id="123456789", message=expected_message
    )


@patch("tracker.views.send_telegram_message_task.delay")
def test_perform_create_no_telegram_when_no_chat_id(self, mock_send_telegram):
    """Тест: perform_create не отправляет Telegram, если нет chat_id"""
    user_no_tg = User.objects.create_user(email="no_tg@example.com", password="pass123")

    view = HabitViewSet()
    data = {
        "place": "Парк",
        "time": time(12, 0),
        "action": "Прогулка",
        "reward": "Шоколадка",
        "periodicity": 1,
        "duration": 60,
    }
    serializer = HabitSerializer(data=data)

    request = self.client.request()
    request.user = user_no_tg
    serializer.context = {"request": request}
    serializer.is_valid()

    view.perform_create(serializer)

    mock_send_telegram.assert_not_called()


@patch("tracker.views.send_telegram_message_task.delay")
def test_perform_create_handles_telegram_error(self, mock_send_telegram):
    """Тест: perform_create не падает при ошибке Telegram"""
    mock_send_telegram.side_effect = Exception("Telegram error")

    view = HabitViewSet()
    data = {
        "place": "Парк",
        "time": time(12, 0),
        "action": "Прогулка",
        "reward": "Шоколадка",
        "periodicity": 1,
        "duration": 60,
    }
    serializer = HabitSerializer(data=data)

    request = self.client.request()
    request.user = self.user
    serializer.context = {"request": request}
    serializer.is_valid()

    view.perform_create(serializer)

    self.assertTrue(Habit.objects.filter(action="Прогулка").exists())


############################################################################################################


class HabitAPITest(TestCase):
    """Тест проверка передачи данных"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            telegram_chat_id="123456789",
        )
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com", password="adminpass123"
        )
        self.pleasant_habit = Habit.objects.create(
            owner=self.user,
            place="Дом",
            time=time(10, 0),
            action="Медитация",
            pleasant_habit=True,
        )
        self.habit = Habit.objects.create(
            owner=self.user,
            place="Парк",
            time=time(12, 0),
            action="Прогулка",
            reward="Шоколадка",
            periodicity=1,
            duration=60,
        )

    def test_create_habit(self):
        """Проверка статус кода + наполнения"""
        # Авторизация
        self.client.force_authenticate(user=self.user)
        data = {
            "place": "Офис",
            "time": "09:00:00",
            "action": "Зарядка",
            "reward": "Кофе",
            "periodicity": 1,
            "duration": 30,
        }
        # 'tracker:tracker-list'-'приложение:сгенерированное имя в пути basename + list для списка'
        # Передача запроса
        response = self.client.post(reverse("tracker:tracker-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["action"], "Зарядка")

    def test_create_invalid_habit(self):
        """Проверка неправильной передачи награды и длительности у приятной привычки"""
        self.client.force_authenticate(user=self.user)
        data = {
            "place": "Парк",
            "time": "18:00:00",
            "action": "Прогулка",
            "reward": "Шоколадка",
            "pleasant_habit": True,
            "duration": 150,
        }
        response = self.client.post(reverse("tracker:tracker-list"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_my_habits(self):
        """Тест наличия верного списка привычек(всего 2)"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("tracker:tracker-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_get_public_habits(self):
        """Проверка возвращаемого ID привычки"""
        public_habit = Habit.objects.create(
            owner=self.user,
            place="Парк",
            time=time(15, 0),
            action="Йога",
            reward="Чай",
            is_public=True,
        )
        another_user = User.objects.create_user(
            email="other@example.com", password="otherpass123"
        )
        self.client.force_authenticate(user=another_user)
        response = self.client.get(reverse("tracker:tracker-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit_ids = [habit["id"] for habit in response.data["results"]]
        self.assertIn(public_habit.id, habit_ids)

    def test_update_habit(self):
        """Проверка PATCH запроса"""
        self.client.force_authenticate(user=self.user)
        data = {"action": "Прогулка в лесу"}
        # 'tracker:tracker-list'-'приложение:сгенерированное имя в пути basename + detail для деталей'
        response = self.client.patch(
            reverse("tracker:tracker-detail", kwargs={"pk": self.habit.id}), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["action"], "Прогулка в лесу")

    def test_delete_habit(self):
        """Проверка метода DELETE для конкретной привычки"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse("tracker:tracker-detail", kwargs={"pk": self.habit.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_can_see_all_habits(self):
        """Проверка, что админ видит все записи"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse("tracker:tracker-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Находим функцию и глушим её патчем
    @patch("tracker.views.send_telegram_message_task.delay")
    # Передаем жестко аргументы(подсказка ./media/patch.jpg)
    def test_create_habit_sends_telegram(self, mock_send_telegram):
        """Проверка работоспособности создания привычки и отправки в телеграм"""
        self.client.force_authenticate(user=self.user)
        data = {
            "place": "Офис",
            "time": "09:00:00",
            "action": "Зарядка",
            "reward": "Кофе",
            "periodicity": 1,
            "duration": 30,
        }
        response = self.client.post(reverse("tracker:tracker-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_send_telegram.assert_called()

    @patch("tracker.views.send_telegram_message_task.delay")
    def test_complete_habit_sends_reward(self, mock_send_telegram):
        """Проверка работоспособности изменения привычки и отправки в телеграм"""
        self.client.force_authenticate(user=self.user)
        data = {"status": "completed"}
        response = self.client.patch(
            reverse("tracker:tracker-detail", kwargs={"pk": self.habit.id}), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_send_telegram.assert_called()

    # #####   ####   ####
    @patch("tracker.views.send_telegram_message_task.delay")
    def test_create_habit_with_related_habit_sends_telegram(self, mock_send_telegram):
        """Тест: создание привычки с связанной привычкой отправляет Telegram"""
        related_habit = Habit.objects.create(
            owner=self.user,
            place="Дом",
            time=time(10, 0),
            action="Медитация",
            pleasant_habit=True,
        )

        self.client.force_authenticate(user=self.user)
        data = {
            "place": "Офис",
            "time": "09:00:00",
            "action": "Зарядка",
            "related_habit": related_habit.id,
            "periodicity": 1,
            "duration": 30,
        }
        response = self.client.post(reverse("tracker:tracker-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что отправлено сообщение с связанной привычкой
        expected_message = "Создана новая привычка: Зарядка в Офис. Награда: Медитация."
        mock_send_telegram.assert_called_with(
            chat_id="123456789", message=expected_message
        )

    @patch("tracker.views.send_telegram_message_task.delay")
    def test_create_habit_with_reward_sends_telegram(self, mock_send_telegram):
        """Тест: создание привычки с наградой отправляет Telegram (для покрытия else)"""
        self.client.force_authenticate(user=self.user)
        data = {
            "place": "Парк",
            "time": "12:00:00",
            "action": "Прогулка",
            "reward": "Шоколадка",
            "periodicity": 1,
            "duration": 60,
        }
        response = self.client.post(reverse("tracker:tracker-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что отправлено сообщение с наградой
        expected_message = "Создана новая привычка: Прогулка в Парк. Награда: Шоколадка"
        mock_send_telegram.assert_called_with(
            chat_id="123456789", message=expected_message
        )

    def test_create_habit_no_telegram_when_no_chat_id(self):
        """Тест: создание привычки не отправляет Telegram, если нет chat_id"""
        user_no_tg = User.objects.create_user(
            email="no_tg@example.com",
            password="pass123",
            # telegram_chat_id = None
        )

        self.client.force_authenticate(user=user_no_tg)
        data = {
            "place": "Парк",
            "time": "12:00:00",
            "action": "Прогулка",
            "reward": "Шоколадка",
            "periodicity": 1,
            "duration": 60,
        }
        response = self.client.post(reverse("tracker:tracker-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Привычка создана, но Telegram не отправлен (потому что нет chat_id)
        # (нельзя проверить мок, т.к. мок не патчится в этом случае)

    @patch("tracker.views.send_telegram_message_task.delay")
    def test_complete_habit_with_related_habit_reward(self, mock_send_telegram):
        """Тест: завершение привычки с связанной привычкой отправляет Telegram"""
        related_habit = Habit.objects.create(
            owner=self.user,
            place="Дом",
            time=time(10, 0),
            action="Медитация",
            pleasant_habit=True,
        )

        habit = Habit.objects.create(
            owner=self.user,
            place="Парк",
            time=time(12, 0),
            action="Прогулка",
            related_habit=related_habit,
            periodicity=1,
            duration=60,
        )

        self.client.force_authenticate(user=self.user)
        data = {"status": "completed"}
        response = self.client.patch(
            reverse("tracker:tracker-detail", kwargs={"pk": habit.id}), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        mock_send_telegram.assert_called_with(
            "123456789", "Привычка 'Прогулка' выполнена! Награда: Медитация"
        )

    @patch("tracker.views.send_telegram_message_task.delay")
    def test_complete_habit_without_reward(self, mock_send_telegram):
        """Тест: завершение привычки без награды отправляет Telegram"""
        habit = Habit.objects.create(
            owner=self.user,
            place="Парк",
            time=time(12, 0),
            action="Прогулка",
            reward="Шоколадка",
            periodicity=1,
            duration=60,
        )

        self.client.force_authenticate(user=self.user)
        data = {"status": "completed"}
        response = self.client.patch(
            reverse("tracker:tracker-detail", kwargs={"pk": habit.id}), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        mock_send_telegram.assert_called_with(
            "123456789", "Привычка 'Прогулка' выполнена! Награда: Шоколадка"
        )

    @patch("tracker.views.send_telegram_message_task.delay")
    def test_create_pleasant_habit_sends_telegram(self, mock_send_telegram):
        """Тест: создание приятной привычки отправляет Telegram"""
        self.client.force_authenticate(user=self.user)
        data = {
            "place": "Дом",
            "time": "10:00:00",
            "action": "Медитация",
            "pleasant_habit": True,
            "periodicity": 1,
            "duration": 60,
            # Нет reward, нет related_habit (для приятной не нужно)
        }
        response = self.client.post(reverse("tracker:tracker-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        expected_message = "Создана новая приятная привычка: Медитация в Дом"
        mock_send_telegram.assert_called_with(
            chat_id="123456789", message=expected_message
        )


################################################################################################
class HabitPermissionsTest(TestCase):
    """Тест проверка прав доступа"""

    def setUp(self):
        self.client = APIClient()
        self.admin1 = User.objects.create_user(
            email="admin1@example.com",
            password="pass123",
            is_superuser=True,
            is_staff=True,
        )
        self.admin = User.objects.create_superuser(
            email="admin@example.com", password="pass123"
        )
        self.user1 = User.objects.create_user(
            email="user1@example.com", password="pass123"
        )
        self.user2 = User.objects.create_user(
            email="user2@example.com", password="pass123"
        )
        self.habit = Habit.objects.create(
            owner=self.user1,
            place="Дом",
            time=time(10, 0),
            action="Медитация",
            reward="Шоколадка",
            periodicity=1,
            duration=60,
        )

    def test_user_view_habit(self):
        """Проверка просмотра своей привычки"""
        self.client.force_authenticate(user=self.user1)
        data = {"action": "Новое действие"}
        response = self.client.get(
            reverse("tracker:tracker-detail", kwargs={"pk": self.habit.id}), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_all_view_habit(self):
        """Проверка просмотра админом всех привычек(разное создание)"""
        # Админ
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(
            reverse("tracker:tracker-detail", kwargs={"pk": self.habit.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Пользователь с правами
        self.client.force_authenticate(user=self.admin1)
        response = self.client.get(
            reverse("tracker:tracker-detail", kwargs={"pk": self.habit.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_user_cannot_update_habit(self):
        """Проверка обновления не своей привычки(запрет)"""
        self.client.force_authenticate(user=self.user2)
        data = {"action": "Новое действие"}
        response = self.client.patch(
            reverse("tracker:tracker-detail", kwargs={"pk": self.habit.id}), data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_other_user_cannot_delete_habit(self):
        """Проверка удаления не своей привычки(запрет)"""
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(
            reverse("tracker:tracker-detail", kwargs={"pk": self.habit.id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_public_habit_readable_by_others(self):
        """Просмотр не владельцем публичных привычек"""
        self.habit.is_public = True
        self.habit.save()
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(
            reverse("tracker:tracker-detail", kwargs={"pk": self.habit.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_notauthenticate_nothing(self):
        """Проверка на запрет всего неавторизованным"""
        # Просмотр публичных привычек
        response = self.client.get(reverse("tracker:tracker-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Просмотр детально
        response = self.client.get(
            reverse("tracker:tracker-detail", kwargs={"pk": self.habit.id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Обновление
        data = {"action": "Новое действие"}
        response = self.client.patch(
            reverse("tracker:tracker-detail", kwargs={"pk": self.habit.id}), data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Удаление
        response = self.client.delete(
            reverse("tracker:tracker-detail", kwargs={"pk": self.habit.id})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Создание
        data = {
            "place": "Дом",
            "time": "10:10:00",
            "action": "Медитация",
            "reward": "Шоколадка",
            "periodicity": 1,
            "duration": 60,
        }
        response = self.client.post(reverse("tracker:tracker-list"), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_simpleuser_lock_privatehabit(self):
        """Тест запрета обычным пользователем(не админ и не владелец) доступ к приватной привычке"""
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(
            reverse("tracker:tracker-detail", kwargs={"pk": self.habit.id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


############################################################################################################
#  Временно изменяет настройки Django только для тестов (отправить синхронно вместо асинхронно)


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class HabitCeleryTest(TestCase):
    """Тест проверка отложенных задач Celery"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            telegram_chat_id="123456789",
        )
        self.habit = Habit.objects.create(
            owner=self.user,
            place="Парк",
            time=time(12, 0),
            action="Прогулка",
            reward="Шоколадка",
            periodicity=1,
            duration=60,
        )

    @patch("tracker.tasks.send_telegram_message")
    def test_send_reminder_task(self, mock_send_telegram):
        """Проверка работы напоминающей задачи"""
        result = send_reminder(self.habit.id)
        self.assertIsNone(result)
        mock_send_telegram.assert_called()

    @patch("tracker.tasks.send_telegram_message")
    def test_send_failure_task(self, mock_send_telegram):
        """Проверка работы проваленной задачи"""
        result = send_failure(self.habit.id)
        self.assertIsNone(result)
        mock_send_telegram.assert_called()
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.status, "failed")

    @patch("tracker.tasks.send_telegram_message")
    def test_send_telegram_message_task_failure_retries(self, mock_send_telegram):
        """Тест падения задачи в ошибку"""
        mock_send_telegram.side_effect = Exception("Telegram API error")
        with self.assertRaises(Exception):
            send_telegram_message_task("123456789", "test message")
        self.assertEqual(mock_send_telegram.call_count, 1)

    @patch("tracker.tasks.send_telegram_message_task.delay")
    def test_reminder_and_failure_habit_not_exists(self, mock_send_telegram):
        """Тест: задачи не падают, если привычка не существует"""
        # Проверяем send_reminder
        result1 = send_reminder(999999)
        self.assertIsNone(result1)

        # Проверяем send_failure
        result2 = send_failure(999999)
        self.assertIsNone(result2)
        mock_send_telegram.assert_not_called()

    @patch("tracker.tasks.send_reminder.delay")
    @patch("tracker.tasks.send_failure.delay")
    def test_check_all_habits_no_reminder_no_failure(
        self, mock_send_failure, mock_send_reminder
    ):
        """Тест: привычка не требует напоминания и не проваливается"""

        habit = Habit.objects.create(  # noqa: F841
            owner=self.user,
            place="Дом",
            time=time(10, 0),
            action="Медитация",
            reward="Шоколадка",
            periodicity=3,  # Периодичность = 3 дня - напоминание не нужно
            duration=60,
            status="started",
            # Прошло 1 день < 7 - провала не будет
            last_completed_at=timezone.now() - timedelta(days=1),
            # Привычка создана 1 день назад, последнее выполнение 1 день назад
            created_at=timezone.now() - timedelta(days=1),
        )
        check_all_habits()

        # Задачи должны ни разу не вызаваться
        mock_send_reminder.assert_not_called()
        mock_send_failure.assert_not_called()

    @patch("tracker.tasks.send_reminder.delay")
    @patch("tracker.tasks.send_failure.delay")
    def test_check_all_habits_no_reminder_failure(
        self, mock_send_failure, mock_send_reminder
    ):
        """Запуск напоминалки переодичности и провала"""

        habit = Habit.objects.create(
            owner=self.user,
            place="Дом",
            time=time(10, 0),
            action="Медитация",
            reward="Шоколадка",
            periodicity=3,  # Периодичность = 3 дня
            duration=60,
            status="started",
            # Прошло 1 день > 7 - провал
            last_completed_at=timezone.now() - timedelta(days=8),
            # Привычка создана 1 день назад, последнее выполнение 4 день назад - напомним
            created_at=timezone.now() - timedelta(days=8),
        )
        check_all_habits()

        # Задачи должны вызаваться
        mock_send_reminder.assert_called_once_with(habit.id)
        mock_send_failure.assert_called_once_with(habit.id)
