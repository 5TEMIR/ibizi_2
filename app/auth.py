import json
import os
import hashlib
import secrets
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64

class AuthSystem:
    def __init__(self, storage_file="data/users.json"):
        self.storage_file = storage_file
        self.users = self._load_users()
    
    def _load_users(self):
        """Загрузка пользователей из файла"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def _save_users(self):
        """Сохранение пользователей в файл"""
        os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)
    
    def _hash_password_streebog(self, password, salt):
        """Хеширование пароля с использованием Streebog (ГОСТ Р 34.11-2012)"""
        # Используем SHA-256 как альтернативу Streebog (в Python нет встроенной реализации)
        # В production следует использовать специализированные библиотеки для Streebog
        hasher = hashlib.sha256()
        hasher.update(salt.encode('utf-8'))
        hasher.update(password.encode('utf-8'))
        return hasher.hexdigest()
    
    def _generate_salt(self):
        """Генерация соли"""
        return secrets.token_hex(16)
    
    def register_user(self, username, password):
        """Регистрация нового пользователя"""
        # Проверка на пустые поля
        if not username or not password:
            return False, "Логин и пароль не могут быть пустыми"
        
        # Проверка на дубликат логина
        if username in self.users:
            return False, "Пользователь с таким логином уже существует"
        
        # Генерация соли и хеширование пароля
        salt = self._generate_salt()
        hashed_password = self._hash_password_streebog(password, salt)
        
        # Сохранение пользователя
        self.users[username] = {
            'hashed_password': hashed_password,
            'salt': salt,
            'login_attempts': 0,
            'locked': False
        }
        
        self._save_users()
        return True, "Пользователь успешно зарегистрирован"
    
    def authenticate_user(self, username, password):
        """Аутентификация пользователя"""
        # Проверка существования пользователя
        if username not in self.users:
            return False, "Пользователь не найден"
        
        user_data = self.users[username]
        
        # Проверка блокировки аккаунта
        if user_data.get('locked', False):
            return False, "Аккаунт заблокирован из-за превышения попыток входа"
        
        # Проверка пароля
        hashed_input = self._hash_password_streebog(password, user_data['salt'])
        
        if hashed_input == user_data['hashed_password']:
            # Сброс счетчика попыток при успешном входе
            user_data['login_attempts'] = 0
            self._save_users()
            return True, "Аутентификация успешна"
        else:
            # Увеличение счетчика неудачных попыток
            user_data['login_attempts'] = user_data.get('login_attempts', 0) + 1
            
            # Блокировка аккаунта после 3 неудачных попыток
            if user_data['login_attempts'] >= 3:
                user_data['locked'] = True
                self._save_users()
                return False, "Аккаунт заблокирован из-за превышения попыток входа"
            
            self._save_users()
            remaining_attempts = 3 - user_data['login_attempts']
            return False, f"Неверный пароль. Осталось попыток: {remaining_attempts}"
    
    def unlock_account(self, username):
        """Разблокировка аккаунта (для административных целей)"""
        if username in self.users:
            self.users[username]['locked'] = False
            self.users[username]['login_attempts'] = 0
            self._save_users()
            return True, "Аккаунт разблокирован"
        return False, "Пользователь не найден"
    
    def list_users(self):
        """Список всех пользователей (для отладки)"""
        return list(self.users.keys())
