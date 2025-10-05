#!/usr/bin/env python3
import os
import sys
from app.auth import AuthSystem
from app.brute_force import BruteForceAttacker, create_test_passwords_file
from app.utils import get_input, print_menu

def main():
    auth_system = AuthSystem()
    attacker = BruteForceAttacker(auth_system)
    
    # Создание тестового файла паролей
    create_test_passwords_file()
    
    while True:
        print_menu()
        choice = get_input("Выберите действие: ")
        
        if choice == "1":
            # Регистрация
            username = get_input("Введите логин: ")
            password = get_input("Введите пароль: ", password=True)
            
            success, message = auth_system.register_user(username, password)
            print(f"Результат: {message}")
        
        elif choice == "2":
            # Вход
            username = get_input("Введите логин: ")
            password = get_input("Введите пароль: ", password=True)
            
            success, message = auth_system.authenticate_user(username, password)
            print(f"Результат: {message}")
            
            if success:
                print(f"Добро пожаловать, {username}!")
        
        elif choice == "3":
            # Brute-force атака
            print("\n--- BRUTE-FORCE АТАКА ---")
            print("1. Атака по словарю")
            print("2. Полный перебор")
            
            attack_type = get_input("Выберите тип атаки: ")
            username = get_input("Введите логин для атаки: ")
            
            if attack_type == "1":
                success, password = attacker.dictionary_attack(username)
            elif attack_type == "2":
                max_len = int(get_input("Максимальная длина пароля (по умолчанию 4): ") or "4")
                success, password = attacker.brute_force_attack(username, max_length=max_len)
            else:
                print("Неверный выбор")
        
        elif choice == "4":
            # Разблокировка аккаунта
            username = get_input("Введите логин для разблокировки: ")
            success, message = auth_system.unlock_account(username)
            print(f"Результат: {message}")
        
        elif choice == "5":
            # Список пользователей
            users = auth_system.list_users()
            print(f"Зарегистрированные пользователи: {users}")
        
        elif choice == "6":
            print("Выход из системы...")
            break
        
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
