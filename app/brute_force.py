import time
import itertools
import string
import os

class BruteForceAttacker:
    def __init__(self, auth_system):
        self.auth_system = auth_system
    
    def dictionary_attack(self, username, dictionary_file="data/passwords.txt"):
        """Атака по словарю"""
        print(f"Запуск атаки по словарю для пользователя: {username}")
        
        try:
            with open(dictionary_file, 'r', encoding='utf-8') as f:
                passwords = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Файл словаря {dictionary_file} не найден")
            return False, None
        
        for i, password in enumerate(passwords):
            success, message = self.auth_system.authenticate_user(username, password)
            print(f"Попытка {i+1}: {password} - {message}")
            
            if success:
                print(f"Пароль найден: {password}")
                return True, password
            
            # Задержка для имитации реальной атаки
            time.sleep(0.1)
            
            # Проверка блокировки аккаунта
            if "заблокирован" in message:
                print("Аккаунт заблокирован. Атака остановлена.")
                return False, None
        
        print("Пароль не найден в словаре")
        return False, None
    
    def brute_force_attack(self, username, max_length=4, charset=None):
        """Полный перебор (brute force)"""
        if charset is None:
            charset = string.ascii_lowercase + string.digits
        
        print(f"Запуск brute-force атаки для пользователя: {username}")
        print(f"Длина пароля до: {max_length}, символы: {charset}")
        
        for length in range(1, max_length + 1):
            print(f"Проверка паролей длины {length}...")
            
            for password_tuple in itertools.product(charset, repeat=length):
                password = ''.join(password_tuple)
                success, message = self.auth_system.authenticate_user(username, password)
                
                print(f"Попытка: {password} - {message}")
                
                if success:
                    print(f"Пароль найден: {password}")
                    return True, password
                
                time.sleep(0.05)
                
                if "заблокирован" in message:
                    print("Аккаунт заблокирован. Атака остановлена.")
                    return False, None
        
        print("Пароль не найден")
        return False, None

def create_test_passwords_file():
    """Создание тестового файла с паролями"""
    os.makedirs("data", exist_ok=True)
    with open("data/passwords.txt", "w", encoding="utf-8") as f:
        f.write("123456\n")
        f.write("password\n")
        f.write("qwerty\n")
        f.write("admin\n")
        f.write("letmein\n")
        f.write("welcome\n")
        f.write("monkey\n")
        f.write("sunshine\n")
        f.write("password1\n")
        f.write("123456789\n")
