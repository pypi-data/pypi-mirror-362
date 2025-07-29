import telebot
import os
import logging

# Заданный путь к файлу конфигурации
CONFIG_PATH = r"\\ad.modniy.org\analitik\D\UpdExlc\CheckL\config_tg_bot.txt"

# Настройка логирования
def setup_logging(log_dir="logs"):
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "tg_bot_utils.log")
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8', mode='a'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger()

def load_config():
    """
    Читает BOT_TOKEN и CHAT_ID из жёстко заданного файла конфигурации.
    Возвращает кортеж (bot_token, chat_id).
    """
    logger = setup_logging()
    file_path = CONFIG_PATH
    if not os.path.exists(file_path):
        logger.error(f"Файл конфигурации {file_path} не найден.")
        return None, None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
            if len(lines) < 2:
                logger.error(f"Файл {file_path} должен содержать как минимум 2 строки (BOT_TOKEN и CHAT_ID)")
                return None, None
                
            bot_token_line = lines[0].strip()
            if not bot_token_line.startswith('BOT_TOKEN='):
                logger.error(f"Первая строка должна начинаться с 'BOT_TOKEN='")
                return None, None
            bot_token = bot_token_line.split('=', 1)[1].strip().replace('\n', '').replace('\r', '').replace('\ufeff', '')
            
            if any(char in bot_token for char in ' \t\n\r'):
                logger.error("Токен содержит пробелы или невидимые символы.")
                return None, None
            
            chat_id_line = lines[1].strip()
            if not chat_id_line.startswith('CHAT_ID='):
                logger.error(f"Вторая строка должна начинаться с 'CHAT_ID='")
                return None, None
            chat_id = chat_id_line.split('=', 1)[1].strip().replace('\n', '').replace('\r', '').replace('\ufeff', '')
            
            return bot_token, chat_id
            
    except Exception as e:
        logger.error(f"Ошибка при чтении конфигурации: {e}")
        return None, None

def send_checklist(message):
    """
    Отправляет сообщение в Telegram чат, используя конфигурацию CheckList.
    
    Args:
        message (str): Сообщение для отправки.
    """
    logger = setup_logging()
    bot_token, chat_id = load_config()
    
    if bot_token and chat_id:
        try:
            bot = telebot.TeleBot(bot_token)
            bot.send_message(chat_id, message)
            logger.info(f"Сообщение отправлено: {message}")
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения: {e}")
    else:
        logger.error("Не удалось загрузить конфигурацию для отправки сообщения.")