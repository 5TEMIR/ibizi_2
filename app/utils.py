import getpass

def get_input(prompt, password=False):
    """Безопасный ввод данных"""
    if password:
        return getpass.getpass(prompt)
    else:
        return input(prompt)

def print_menu():
    """Отображение меню"""
    print("\n" + "="*50)
    print("СИСТЕМА АУТЕНТИФИКАЦИИ")
    print("="*50)
    print("1. Регистрация")
    print("2. Вход")
    print("3. Запуск brute-force атаки")
    print("4. Разблокировка аккаунта")
    print("5. Список пользователей")
    print("6. Выход")
    print("="*50)
