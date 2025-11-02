# ⏰ Habit Tracker

# 🔖 Описание проекта:

Данный проект является трекером привычек по книге "Атомные привычки", работающие на DJANGO REST FRAMEWORK.

*ЗАДАЧА*

В 2018 году Джеймс Клир написал книгу «Атомные привычки», которая посвящена приобретению новых полезных привычек и искоренению старых плохих привычек. Заказчик прочитал книгу, впечатлился и обратился с запросом реализовать трекер полезных привычек.
# 🔧 Установка компонентов:


1. Создайте проект и установите poetry:


```pip install --user poetry```


2. Установите инструменты для реализации сервиса:

![Python](https://img.shields.io/badge/Python-3.13-green?logo=python&logoColor=white)

[![Django](https://img.shields.io/badge/Django-3.2.0-%2311677A?logo=django&logoColor=white&style=flat&labelColor=black)]( https://www.djangoproject.com/ )
![Django REST Framework](https://img.shields.io/badge/DJANGO-REST_FRAMEWORK-ff69b4?style=for-the-badge&logo=django&logoColor=white)
[![django-filter](https://img.shields.io/badge/django--filter-4.0.0-blue?logo=django&logoColor=white&style=for-the-badge)](https://django-filter.readthedocs.io/)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
[![python-dotenv](https://img.shields.io/badge/python--dotenv-black?logo=envoy&logoColor=orange)]( https://pypi.org/project/python-dotenv/ )
[![psycopg2](https://img.shields.io/badge/psycopg2-%233178C6?logo=postgresql&logoColor=white)]( https://pypi.org/project/psycopg2/ )
[![IPython](https://img.shields.io/badge/IPython-%23779ECB?logo=ipython&logoColor=white&style=flat&labelColor=black)]( https://pypi.org/project/ipython/ )

![Redis](https://img.shields.io/badge/Redis-cache-8a2be2?logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-%2337814A.svg?style=for-the-badge&logo=celery&logoColor=white)
![Celery Beat](https://img.shields.io/badge/django--celery--beat-%2337814A.svg?style=for-the-badge&logo=celery&logoColor=white)
![Eventlet](https://img.shields.io/badge/Eventlet-%23009688.svg?style=for-the-badge)
![CORS](https://img.shields.io/badge/django--cors--headers-%23092E20.svg?style=for-the-badge)
![Spectacular](https://img.shields.io/badge/drf--spectacular-%235272B4.svg?style=for-the-badge&logo=openapi-initiative&logoColor=white)
![SimpleJWT](https://img.shields.io/badge/djangorestframework--simplejwt-%23092E20.svg?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?style=for-the-badge&logo=postgresql&logoColor=white)
![requests](https://img.shields.io/badge/requests-3498db?logo=python&logoColor=white)
![coverage](https://img.shields.io/badge/coverage-92%25-brightgreen?logo=codecov)

![Black](https://img.shields.io/badge/black-000000?style=flat&logo=python&logoColor=white)
![Mypy](https://img.shields.io/badge/mypy-checked-blue.svg?logo=python&logoColor=green)
![Flake8](https://img.shields.io/badge/flake8-checked-blue.svg?logo=python&logoColor=blue)
![JSON](https://img.shields.io/badge/json-5E5C5C?logo=json&logoColor=red)

КОМАНДЫ ДЛЯ ЗАПУСКА ФРЕЙМВОРКА И ПРИЛОЖЕНИЯ
```
poetry add django # Установка django
poetry add djangorestframework # Установка django rest framework
poetry add django-filter # Установка фильтратора DRF
poetry add dotenv # Установка библиотеки для работы с чувствительными данными
poetry add ipython # Установка библиотеки для работы с чувствительными данными
poetry add psycopg2 # Установка инструмента для работы с ORM

poetry add --dev flake8 mypy isort black # Установка всех dev зависимостей 

django-admin startproject config . # Старт нового проекта
django-admin startproject myproject # Старт нового приложения

python manage.py createsuperuser # дать суперпользователя для админки.
При выполнении этой команды необходимо указать имя пользователя и пароль.
Адрес электронной почты является опциональным параметром.

python manage.py shell -i ipython #Запуск DJANGO SHELL

```

# ✒️ Использование API

⚠️️ ВАЖНО ⚠️
```
python manage.py runserver 8080 # Запуск сервера
CTRL+С # Отключение сервера
```

🔝 РАБОТА с CELERY 
*Запуск команд воркера Celery*
```
poetry run celery -A config worker -l INFO -P eventlet
poetry run celery -A config beat -l INFO
poetry run celery -A my_project worker —loglevel=info
poetry run celery -A my_project beat —loglevel=info
```

*Запуск команд планера Celery*
```
poetry run celery -A config worker -pool=eventlet -l INFO
```

Далее работа в *setting.py*
```
INSTALLED_APPS = [
    # ... другие приложения ...
    'django_celery_beat',
]
```
💡ВАЖНО💡
ВЫПОЛНИТЕ МИГРАЦИИ ДО РАБОТЫ С ПЛАНЕРОМ + запустите REDIS 
```
poetry run python manage.py migrate
```

### 🌐 Пример страниц:
*Главная страница*
![Главная страница с указанием страницы](./media/postman.jpg)


*Работа бота*

![<Бот телеграм>](./media/telegram.jpg)


📡 API Документация
API доступно по адресу: http://localhost:8000/swagger/#/

Postman коллекция
Для удобства тестирования API предоставлена коллекция Postman:

📥 Скачать Postman Collection

Или импортируйте по ссылке (если опубликовано в Postman Cloud):

🔗 Открыть в Postman

💡 Совет: Импортируйте коллекцию в Postman → "Import" → "Link" или "File". 
### 📶 Работа с запросами

```
http://localhost:8000/tracker/ - основа
http://localhost:8000/tracker/?ordering=time - сортировка по времени 

Регистрация:
http://localhost:8000/users/register/ - post(json-raw)

Вход и получение токена post:
http://localhost:8000/users/login/ в body отправить json (json-raw)

Просмотр профиля get:
http://localhost:8000/users/profile/ (headers) Accept -Bearer  токен 

Редактирование профиля patch:
http://localhost:8000/users/profile/ (json-raw) patch + (headers) Accept -Bearer токен (ТОЛЬКО ВЛАДЕЛЬЦАМ)

Редактирование профиля полностью( нужны важные поля входа в аккаунт) put:
http://localhost:8000/users/profile/ (json-raw) patch + (headers) Accept - Bearer токен  (ТОЛЬКО ВЛАДЕЛЬЦАМ)

Удаление профиля delete:
http://localhost:8000/users/profile/delete (headers) Bearer  токен (ТОЛЬКО ВЛАДЕЛЬЦАМ)

Просмотр списков пользователя get:
http://localhost:8000/users/list/(headers) Accept - Bearer  токен (ТОЛЬКО АДМИНАМ)

Отправка refresh токена post:
http://localhost:8000/users/list/(headers) Content-Type - application/json/ 
в body отправить json
{"refresh":"токен"} 
```
### ТЕСТЫ 

Для запусков тестов воспользуйтесь командами:

*Пропишите приложение "tracker" или "users" для формирования тестов конкретного приложения*
```
coverage run --source='tracker/' manage.py test tracker.tests 
coverage report
coverage html
```
*Или же покрытие разом двух приложений*
```
coverage run --source='.' manage.py test tracker.tests users.tests
```

![Итоги тестов](./media/test.jpg)

Отчет тестов создастся по пути *HabitTracker\htmlcov\index.html*


Для начала работы убедитесь что папка .ssh создана по пути C:\Users\ВАШ_ПОЛЬЗОВАТЕЛЬ\.ssh

- СОЗДАЕМ Виртуальную Машину(ВМ) с именем админа и сгенерированным ssh + архив скачается на пк(сохраните по пути users/User/.ssh/)
![Подключение к ВМ](./media/BM_SSH.jpg)

- Далее распаковываем архив с ключом(достать ключи в папку вручную)
- Открываем приватный ключ в powershell
```
Get-Content -Path "C:\Users\ВАШЕИМЯЮЗЕРА\.ssh\ssh2025"
```

Будет примерно такой ключ - скопировать весь и сохранить в txt(для подстраховки)

![Подключение к ВМ](./media/docker_3.jpg)

можно проверить этот ключ для подключения к серверу через *Yandex Cloud Shell*(имя админа + ключ)

![Подключение к ВМ](./media/вм.jpg)
![Подключение к ВМ](./media/вм2.jpg)

!!! ВАЖНО - При переустановке windows желательно забрать всю папку .ssh из системы !!!

-Сгенерируй ключ из приватного и сравни с ключом на ВМ в разделе МЕТАДАННЫЕ:
```ssh-keygen -y -f "$env:USERPROFILE\.ssh\ssh2025"```
	ИТОГ: это твой ключ только для соединеия твоего ПК и твоего СЕРВЕРА

🔥 МОЖНО СДЕЛАТЬ ПРОЩЕ, ЕСЛИ СОЗДАТЬ ПАРУ КЛЮЧЕЙ НА ПК и создать ВМ отдав публичную часть 🔥
```
# Создаём ключ без пароля (обязательно для автоматизации)
ssh-keygen -t ed25519 -C "yandex-cloud-vm" -f "$env:USERPROFILE\.ssh\yandex_cloud_vm" -N '""'

#Получаем приватный ключ
Get-Content "$env:USERPROFILE\.ssh\yandex_cloud_vm"

#Получаем публичный ключ
Get-Content "$env:USERPROFILE\.ssh\yandex_cloud_vm.pub"

```

1. 🧱 Настрой фаервол (UFW)
```
# Разрешить SSH (обязательно ДО включения!)
sudo ufw allow 22/tcp

# Разрешить веб-трафик
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Включить фаервол
sudo ufw --force enable

# Проверить
sudo ufw status
```

2. 🔄 Обнови систему ВМ(&& - команда "если выполнилась предыдущая - начинай следущую") - если обновил, то пропусти шаг:
```sudo apt update && sudo apt upgrade -y```

или отдельно построчно
```
sudo apt update
#################################################
sudo apt upgrade

# Активация, если inactive:
sudo ufw enable
```
======================================================================================================================

СОЗДАЕМ КЛЮЧИ ДЛЯ работы ручоного деплоя и CI/CD

❗❗❗РАБОТА НА СВОЕМ ПК В POWERSHELL❗❗❗

☁️СОЗДАНИЕ КЛЮЧА ДЛЯ Github Actions
1. 🔐 Создаем пары ключей с названием *github-actions-deploy* для Github Action (просто жмем везде enter или y)
через полный путь или переменную:
```
ssh-keygen -t ed25519 -C "github-actions-deploy" -f "C:\Users\ВАШЕ_ИМЯ_ПОЛЬЗОВАТЕЛЯ\.ssh\id_ed25519_github_actions"
#####################################################################################################################
ssh-keygen -t ed25519 -C "github-actions-deploy" -f "$env:USERPROFILE\.ssh\id_ed25519_github_actions"
```
Получаем в случае успеха:
![Получение ключа](./media/ssh.jpg)

2. 📄 Копируем приватный ключ *id_ed25519_github_actions* - он пойдет в проект в раздел Github Secrets:
```type ~/.ssh/id_ed25519_github_actions```
✅ Скопируй ВЕСЬ этот текст — он понадобится как значение для секрета SSH_KEY в GitHub.

3. 🔑 Скопируй публичный ключ — он пойдёт на сервер твоей ВМ:
```type ~/.ssh/id_ed25519_github_actions.pub```

💾СОЗДАНИЕ КЛЮЧА ДЛЯ Github репозитория (для ручного деплоя)⚠️Этот пункт можно выполнить на сервере и скопировать публичный для репозитория⚠️
1. 🔐 Создаем пары ключей с названием *deploy_github* для Github репозитория (просто жмем везде enter или y)
через полный путь или переменную
```
ssh-keygen -t ed25519 -C "deploy_github" -f "C:\Users\ВАШЕ_ИМЯ_ПОЛЬЗОВАТЕЛЯ\.ssh\id_ed25519_deploy_github"
#####################################################################################################################
ssh-keygen -t ed25519 -C "deploy_github" -f "$env:USERPROFILE\.ssh\id_ed25519_deploy_github"
```

2. 📄 Копируем приватный ключ *id_ed25519_deploy_github* - он пойдет в проект в раздел Github Secrets:
```type ~/.ssh/id_ed25519_deploy_github```
✅ Скопируй ВЕСЬ этот текст — он понадобится для твоего сервера

3. 🔑 Скопируй публичный ключ — он пойдёт в раздел SSH ключей твоего репозитория:
```type ~/.ssh/id_ed25519_deploy_github.pub```

🔎ОПЦИОНАЛЬНО: 
 Убедись в корректности Git-настроек (опционально)
```
git config --global user.name
git config --global user.email
```
→ Убедись, что email совпадает с тем, что в ключах.

❗❗❗РАБОТА НА СВОЕМ ПК В POWERSHELL - ПОДКЛЮЧЕНИЕ К ВМ❗❗❗
1. 🔓Подключаемся к своей ВМ(явно указываем приватный ключ или не указываем работаем через Cloud Shell):
```
# Если создал пару ключей на пк и отдал ВМ публичный
ssh -i "C:\Users\Support\.ssh\ssh2025" test@158.160.27.139

# Если создал пару ключей на YC, скачал и распаковал ключи на пк
ssh -i "C:\Users\Support\.ssh\ssh2025" test@158.160.27.139
```

НА ЭТОМ ЭТАПЕ МОЖЕМ ПОДГОТОВИТЬ ПАПКУ ДЛЯ ДЕПЛОЯ:
```
mkdir -p ~/HabitTracker # Создаем папку для деплоя
nano ~/HabitTracker/.env # Создать файл с конфигурациями
# вносим измененеия и выполняем CTRL+O > Enter > CTRL+X
```

🌟ИЛИ СДЕЛАТЬ SSH-конфиг (гибкий и профессиональный):
В PowerShell выполни

Шаг 1: Создай файл config
```
notepad "$env:USERPROFILE\.ssh\config"
```
Если Notepad спросит — создать файл — нажми Да.


Шаг 2: Вставь настройки
```
Host yandex-vm
    HostName 158.160.27.139
    User test
    IdentityFile ~/.ssh/ssh2025
    IdentitiesOnly yes
```
💡 HostName 158.160.27.139 - ip твоего хоста+
💡 User test - test это имя админа на серваке
💡 yandex-vm — это псевдоним, который ты сам придумал. Можно назвать как угодно. 

Шаг 3: Сохрани и установи права (важно!)
Закрой Notepad. Затем в PowerShell:
```
# Установи правильные права на config
icacls "$env:USERPROFILE\.ssh\config" /inheritance:r
icacls "$env:USERPROFILE\.ssh\config" /grant:r "$env:USERNAME:(R)"
```
Шаг 4: Подключайся!
```
ssh yandex-vm
```
Или, если хочешь по IP — добавь ещё один блок в config:

```
Host 158.160.27.139
    User test
    IdentityFile ~/.ssh/ssh2025
    IdentitiesOnly yes
```

После этого заработает и:
```
ssh test@158.160.27.139
```

2. 🔄 Обнови систему ВМ(&& - команда "если выполнилась предыдущая - начинай следущую") - если обновил, то пропусти шаг:
```sudo apt update && sudo apt upgrade -y```

или отдельно построчно
```
sudo apt update
#################################################
sudo apt upgrade
```

3. 🤔 Узнаем имя админа и путь папки копирования на сервер(DEPLOY_DIR будет в Github Secret):
```
whoami
echo $HOME
 
```

4. 🧠 Создай постоянного пользователя например, admin
```
export USERNAME=admin

#Создаем нового юзера и добавляем в группу studo 
sudo adduser --gecos "" --disabled-password "$USERNAME"
sudo usermod -aG sudo "$USERNAME"

# Надёжное создание .ssh
sudo mkdir -p /home/"$USERNAME"/.ssh
sudo chown "$USERNAME":"$USERNAME" /home/"$USERNAME"/.ssh
sudo chmod 700 /home/"$USERNAME"/.ssh

# Добавление ключа
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... github-actions-deploy" | sudo tee /home/"$USERNAME"/.ssh/authorized_keys > /dev/null
sudo chown "$USERNAME":"$USERNAME" /home/"$USERNAME"/.ssh/authorized_keys
sudo chmod 600 /home/"$USERNAME"/.ssh/authorized_keys

# Права на домашнюю папку (обязательно!)
sudo chmod 755 /home/"$USERNAME"
```

✅ Теперь у тебя есть пользователь с правами sudo.

🧩 Или используем готового админа
```
# 1. Убедитесь, что вы test
whoami  # должно быть: test

# 2. Создайте .ssh (если нет)
mkdir -p ~/.ssh

# 3. Добавьте ключ (пример)
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... github-actions-deploy" >> ~/.ssh/authorized_keys

# 4. Права
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```
🔒 ВАЖНО - Без этих прав SSH откажет в подключении, даже если ключ верный! 🔒 

6. ✏️ Возмем приватный длиный ключ для ручного деплоя *id_ed25519_deploy_github* и выполни команду:
```
# Создать файл приватного ключа
export USERNAME=ВАШЕИМЯ АДМИНА

sudo -u $USERNAME nano /home/$USERNAME/.ssh/id_ed25519_deploy_github
#ИЛИ ОТ АВТОРИЗОВАННОГО
nano ~/.ssh/id_ed25519_github_deploy
```
Копируем приватный ключ в открытой панели и сохраняем *Ctrl+O > Enter > Ctrl+X*
при повторном вводе команды, должен открытся заполненный файл

7.🤖 Установи права:
```
sudo chmod 600 /home/$USERNAME/.ssh/id_ed25519_github_deploy
sudo chown $USERNAME:$USERNAME /home/$USERNAME/.ssh/id_ed25519_github_deploy

#Если авторизованы
chmod 600 ~/.ssh/id_ed25519_github_deploy
```

8. 🧷 Создай SSH-конфиг для GitHub:
```
sudo -u $USERNAME tee /home/$USERNAME/.ssh/config > /dev/null <<EOF
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_github_deploy
  IdentitiesOnly yes
EOF

sudo chmod 600 /home/$USERNAME/.ssh/config
sudo chown $USERNAME:$USERNAME /home/$USERNAME/.ssh/config
```

Можно прочитать его на корректность заполнения
```cat /home/$USERNAME/.ssh/config```
 Получится так:
![Получение ключа](./media/вм3.jpg)

9. 📝 Добавляем публичный ключ *deploy_github* на Github репозиторий в настройках SSH ключей и выполняем:
```sudo -u $USERNAME ssh -T git@github.com```

При успешном выполнении будет приветствие


10.🔌 Настройка Secrets(информацию достанешь в консоли )
Создай:
```
#SSH_KEY = содержимое приватного ключа Ключа №1 (id_ed25519_github_actions)
#SSH_USER 
whoami 

#ip вашего сервера
#SECRET_IP\SERVER_IP
hostname -I

#DEPLOY_DIR 
echo $HOME

#SSH_KNOW_HOST - отпечаток сервера(нужен редко)
ssh-keyscan -t ed25519 ваш_ip_сервера


DOCKER_USERNAME(ваш юзернейм на dockerhub)
DOCKER_PASSWORD(подготовить ваш access token)
```

В личном кабинете при создании токена для docker обязательно указать такие настройки:
![Подключение к DH](./media/docker_pass.jpg)

SSH_KNOW_HOST увидите вывод:
![Подключение к DH](./media/docker4.jpg)
скопируй все без строк хэштега и добавь в secrets SSH_KNOWN_HOST

1. В dockerhub в настройках профиля ищем *Account settings*:
![Подключение к DH](./media/docker.jpg)

2.Ищем строку *Personal access tokens*
![Подключение к DH](./media/docker2.jpg)

3. Выбираем *generate new token*

4. Скопируйте токен (ОН ДОСТУПЕН ОДИН РАЗ)
5. Добавьте в Github secrets


НАСТРОЙКА В ПРОЕКТЕ
1. Создаем путь и файл в корне *.github/workflows/ci.yml*
ВАЖНО ДЛЯ ТЕСТОВ ИСПОЛЬЗОВАНИЕ ОТДЕЛЬНОЙ СУБД в Settings (если в проекте используется postgres):
```
# Настройки для тестирования, включая CI/CD
if "test" in sys.argv:
    ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1"]

    # Дополнительные настройки для тестов
    PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.MD5PasswordHasher",  # Быстрее для тестов
    ]

    # 🗃️ База данных - для тестов стоковая
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

    LANGUAGE_CODE = "ru-ru"
    TIME_ZONE = "UTC"
    USE_I18N = True
    USE_TZ = True

    # 📦 Статика
    STATIC_URL = "/static/"
    STATICFILES_DIRS = []

    # 📧 Email
    EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

    # ПРОИЗВОЛЬНЫЙ КЛЮЧ ДЛЯ ТЕСТОВ
    SECRET_KEY = "ci-test-secret-key-unsafe-but-ok"
    DEBUG = True
    ROOT_URLCONF = "config.urls"

    # 🔑 Указываем, что кастомная модель User — основная
    AUTH_USER_MODEL = "users.User"

    # 🖼️ TEMPLATES — обязательно для админки
    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]
```
2. При пуше подтверждаем пуш workflows:
```
git add .
git commit -m "Test CI"
git remote set-url origin git@github.com:StreetShiffter/DJANGO_REST_HW.git
git push
```

ВНИМАНИЕ: команда *docker-compose up -d --build* на сервере работает без тире *docker compose up -d --build* 

https://app.docker.com/accounts/streetshiffter/settings/personal-access-tokens

📄 Лицензия
Этот проект лицензирован по MIT License — подробнее см. файл LICENSE.