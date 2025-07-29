import os

def load_config(file_path):
    """
    Читает BOT_TOKEN и CHAT_ID из указанного файла конфигурации.
    Формат файла: 
        1 строка: BOT_TOKEN=значение
        2 строка: CHAT_ID=значение
        3 строка: пустая
    Возвращает кортеж (bot_token, chat_id).
    
    Args:
        file_path (str): Путь к файлу конфигурации.
    
    Raises:
        SystemExit: Если файл не найден, недоступен или имеет неверный формат.
    """
    if not os.path.exists(file_path):
        print(f"Ошибка: Файл {file_path} не найден или недоступен. Проверьте путь и права доступа.")
        exit(1)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
            # Проверяем, что файл содержит хотя бы 2 строки
            if len(lines) < 2:
                print(f"Ошибка: Файл {file_path} должен содержать как минимум 2 строки (BOT_TOKEN и CHAT_ID)")
                exit(1)
                
            # Читаем первую строку (BOT_TOKEN)
            bot_token_line = lines[0].strip()
            if not bot_token_line.startswith('BOT_TOKEN='):
                print(f"Ошибка: Первая строка должна начинаться с 'BOT_TOKEN='")
                exit(1)
            bot_token = bot_token_line.split('=', 1)[1].strip().replace('\n', '').replace('\r', '').replace('\ufeff', '')
            
            # Проверяем токен на пробелы
            if any(char in bot_token for char in ' \t\n\r'):
                print("Ошибка: Токен содержит пробелы или невидимые символы. Проверьте файл конфигурации")
                exit(1)
            
            # Читаем вторую строку (CHAT_ID)
            chat_id_line = lines[1].strip()
            if not chat_id_line.startswith('CHAT_ID='):
                print(f"Ошибка: Вторая строка должна начинаться с 'CHAT_ID='")
                exit(1)
            chat_id = chat_id_line.split('=', 1)[1].strip().replace('\n', '').replace('\r', '').replace('\ufeff', '')
            
            return bot_token, chat_id
            
    except PermissionError:
        print(f"Ошибка: Нет прав доступа к файлу {file_path}. Проверьте, подключён ли сетевой диск.")
        exit(1)
    except Exception as e:
        print(f"Ошибка при чтении конфигурации: {e}")
        exit(1)