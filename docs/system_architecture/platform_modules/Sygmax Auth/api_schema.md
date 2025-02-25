# Sygmax Auth API Schema Draft

## Тырикова Евгения
- В Django для работы с JWT часто используется библиотека djangorestframework-simplejwt

- Вставка в файл settings.py:
```
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework_simplejwt',
]

    REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
```

- Генерация эндпоинта для токена:
``` from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```
### Регистрация аккауинта:
```
from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest
from bcrypt import gensalt, hashpw
import jwt
import requests
import time

app = Flask(__name__)

# Конфигурация
SECRET_KEY = "your_jwt_secret_key"
WORKSPACE_SERVICE_URL = "http://workspace-service/api/workspaces"

# Мок базы данных
users_db = {}
user_roles_db = {}

@app.route('/auth/register', methods=['POST'])
def register_user():
    try:
        # Получение данных из запроса
        data = request.json
        email = data.get("email")
        password = data.get("password")
        name = data.get("name")

        if not email or not password or not name:
            raise BadRequest("Email, password, and name are required.")

        # Проверка, существует ли пользователь
        if email in users_db:
            return jsonify({"error": "User with this email already exists."}), 400

        # Хеширование пароля
        hashed_password = hashpw(password.encode('utf-8'), gensalt())

        # Создание записи пользователя
        user_id = len(users_db) + 1
        users_db[email] = {
            "id": user_id,
            "email": email,
            "password": hashed_password,
            "name": name
        }

        # Назначение роли Admin
        user_roles_db[user_id] = "Admin"

        # Создание персонального воркспейса
        workspace_payload = {"user_id": user_id, "workspace_name": f"{name}'s Workspace"}
        for attempt in range(2):  # Два попытки
            response = requests.post(WORKSPACE_SERVICE_URL, json=workspace_payload)
            if response.status_code == 201:  # Успешное создание воркспейса
                workspace_id = response.json().get("workspace_id")
                users_db[email]["default_workspace_id"] = workspace_id
                break
            else:
                time.sleep(2)  # Ожидание перед повторной попыткой
        else:
            # Если обе попытки провалились, откат регистрации
            del users_db[email]
            del user_roles_db[user_id]
            return jsonify({"error": "Failed to create workspace. Registration rolled back."}), 500

        # Генерация JWT
        token = jwt.encode({"user_id": user_id, "email": email}, SECRET_KEY, algorithm="HS256")

        return jsonify({"message": "User registered successfully.", "token": token}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

```

### Вход ы систему:
```
from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest, Unauthorized
from bcrypt import checkpw
import jwt
import requests

app = Flask(__name__)

# Конфигурация
SECRET_KEY = "your_jwt_secret_key"
PROFILE_SERVICE_URL = "http://profile-service/api/profiles"
WORKSPACE_SERVICE_URL = "http://workspace-service/api/workspaces"

# Мок базы данных
users_db = {
    "user@example.com": {
        "id": 1,
        "email": "user@example.com",
        "password": b"$2b$12$eImiTXuWVxfM37uY4JANjQWz8h3Zx9Q2o5l5f9J8J8J8J8J8J8J8J",  # bcrypt hash for "securepassword"
        "name": "John Doe"
    }
}

@app.route('/auth/login', methods=['POST'])
def login_user():
    try:
        # Получение данных из запроса
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise BadRequest("Email and password are required.")

        # Проверка существования пользователя
        user = users_db.get(email)
        if not user:
            raise Unauthorized("Invalid email or password.")

        # Проверка пароля
        if not checkpw(password.encode('utf-8'), user["password"]):
            raise Unauthorized("Invalid email or password.")

        # Генерация JWT
        user_id = user["id"]
        token = jwt.encode({"user_id": user_id, "email": email}, SECRET_KEY, algorithm="HS256")

        # Запрос данных профиля из Profile Service
        profile_response = requests.get(f"{PROFILE_SERVICE_URL}/{user_id}")
        if profile_response.status_code != 200:
            raise Exception("Failed to fetch profile data.")
        profile_data = profile_response.json()

        # Запрос списка воркспейсов из Workspace Service
        workspace_response = requests.get(f"{WORKSPACE_SERVICE_URL}/{user_id}/workspaces")
        if workspace_response.status_code != 200:
            raise Exception("Failed to fetch workspace data.")
        workspaces = workspace_response.json()

        # Формирование ответа
        return jsonify({
            "token": token,
            "profile": {
                "full_name": profile_data.get("full_name"),
                "email": profile_data.get("email"),
                "avatar": profile_data.get("avatar")
            },
            "workspaces": workspaces
        }), 200

    except Unauthorized as e:
        return jsonify({"error": str(e)}), 401
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

```

### Удаление аккауинта:
```
from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

# Конфигурация
AUTH_SERVICE_SECRET = "your_auth_service_secret"
WORKSPACE_SERVICE_URL = "http://workspace-service/api/workspaces"
PROFILE_SERVICE_URL = "http://profile-service/api/profiles"

# Мок базы данных
users_db = {
    "user@example.com": {
        "id": 1,
        "password": "hashed_password",
        "2fa_enabled": True,
        "workspaces": [101, 102],  # ID воркспейсов
        "member_of_workspaces": [201, 202]  # ID воркспейсов, где он член
    }
}

@app.route('/auth/delete-account', methods=['DELETE'])
def delete_account():
    try:
        # Получение данных из запроса
        data = request.json
        email = data.get("email")
        password = data.get("password")
        otp = data.get("otp")  # Одноразовый пароль для 2FA

        if not email or not password:
            return jsonify({"error": "Email and password are required."}), 400

        # Проверка существования пользователя
        user = users_db.get(email)
        if not user:
            return jsonify({"error": "User not found."}), 404

        # Проверка пароля (упрощенная проверка, в реальном приложении используйте bcrypt/argon2)
        if password != "hashed_password":  # Здесь должна быть проверка хэша
            return jsonify({"error": "Invalid password."}), 401

        # Проверка 2FA (если включена)
        if user.get("2fa_enabled"):
            if not otp or otp != "123456":  # Здесь должна быть проверка OTP
                return jsonify({"error": "Invalid or missing OTP for 2FA."}), 401

        # Удаление воркспейсов пользователя
        for workspace_id in user["workspaces"]:
            response = requests.delete(f"{WORKSPACE_SERVICE_URL}/{workspace_id}")
            if response.status_code != 204:
                return jsonify({"error": f"Failed to delete workspace {workspace_id}."}), 500

        # Исключение пользователя из воркспейсов, где он член
        for workspace_id in user["member_of_workspaces"]:
            response = requests.post(f"{WORKSPACE_SERVICE_URL}/{workspace_id}/remove-member", json={"user_id": user["id"]})
            if response.status_code != 200:
                return jsonify({"error": f"Failed to remove user from workspace {workspace_id}."}), 500

        # Удаление персональных настроек (Profile Service)
        response = requests.delete(f"{PROFILE_SERVICE_URL}/{user['id']}")
        if response.status_code != 204:
            return jsonify({"error": "Failed to delete user profile."}), 500

        # Удаление учетной записи (Auth Service)
        del users_db[email]

        # Возврат подтверждения удаления
        return jsonify({"message": "Account deleted successfully."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

```

## Воронов Даниил

