import os
import logging
import getpass

# Фиксированная директория для логов
LOG_DIR = r"\\ad.modniy.org\analitik\D\UpdExlc\Python_lib\analitiks\logs"

class UsernameFilter(logging.Filter):
    """Custom filter to add username to log records."""
    def __init__(self, username):
        super().__init__()
        self.username = username

    def filter(self, record):
        print(f"[DEBUG] Applying UsernameFilter with username: {self.username}")  # Отладочный вывод
        record.username = getattr(record, 'username', self.username)
        return True

def setup_logging(log_file_name="library.log"):
    """
    Настраивает логирование с сохранением в фиксированную папку logs/ и добавлением в файл (без перезаписи).
    Включает имя пользователя в сообщения лога.
    
    Args:
        log_file_name (str): Имя лог-файла. По умолчанию — 'library.log'.
    
    Returns:
        logging.Logger: Готовый логгер.
    """
    # Создаем директорию, если она не существует
    os.makedirs(LOG_DIR, exist_ok=True)
    log_path = os.path.join(LOG_DIR, log_file_name)

    # Проверяем права на запись
    if not os.access(LOG_DIR, os.W_OK):
        raise OSError(f"Нет прав на запись в директорию: {LOG_DIR}")

    # Получаем имя текущего пользователя
    username = getpass.getuser()

    # Создаем логгер с уникальным именем
    logger = logging.getLogger(f"LibraryLogger::{log_file_name}")
    logger.setLevel(logging.INFO)
    logger.propagate = False  # Чтобы избежать дублирования логов в root-логгере

    # Очистим обработчики только если они уже были добавлены
    if logger.hasHandlers():
        print(f"[DEBUG] Clearing existing handlers for logger: {logger.name}")  # Отладочный вывод
        logger.handlers.clear()

    # Форматтер с добавлением имени пользователя
    formatter = logging.Formatter(
        '%(asctime)s - %(username)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        defaults={'username': username}  # Устанавливаем значение по умолчанию для username
    )

    # Файл-лог (добавление в конец файла, а не перезапись)
    file_handler = logging.FileHandler(log_path, encoding='utf-8', mode='a')
    file_handler.setFormatter(formatter)
    file_handler.addFilter(UsernameFilter(username))
    logger.addHandler(file_handler)

    # Консоль (для удобства отладки)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.addFilter(UsernameFilter(username))
    logger.addHandler(console_handler)

    print(f"[DEBUG] Logger {logger.name} configured with handlers: {[h.__class__.__name__ for h in logger.handlers]}")  # Отладочный вывод
    return logger