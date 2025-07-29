import socket
import re
import os
from analitiks.logger_utils import setup_logging  # ❗ импорт из общей библиотеки

def read_file_contents(file_path, log_file_name="connection_utils.log"):
    """
    Читает содержимое файла и заменяет хост на localhost в строке подключения, если он совпадает с текущим хостом или IP.
    
    Args:
        file_path (str): Путь к файлу.
        log_file_name (str): Имя лог-файла для записи.
    
    Returns:
        str: Обработанное содержимое файла или сообщение об ошибке.
    """
    logger = setup_logging(log_file_name=log_file_name)

    try:
        with open(file_path, 'r') as file:
            file_contents = file.read()

        current_host = socket.gethostname().lower()
        current_fqdn = socket.getfqdn().lower()
        try:
            current_ip = socket.gethostbyname(socket.gethostname())
        except socket.gaierror:
            current_ip = None

        host_match = re.search(r'@([^\s:\/]+)(?::\d+)?/', file_contents)
        if host_match:
            connection_host = host_match.group(1).lower()

            if (current_host == connection_host or 
                current_fqdn == connection_host or 
                (current_ip and current_ip == connection_host)):
                logger.info(f"Заменен хост {connection_host} на localhost в файле {os.path.basename(file_path)}")
                file_contents = re.sub(r'@' + re.escape(connection_host) + r'(:?\d*/|/)', '@localhost\\1', file_contents)

        return file_contents
    except FileNotFoundError:
        logger.error(f"Файл '{file_path}' не найден.")
        return f"Файл '{file_path}' не найден."
    except Exception as e:
        logger.error(f"Ошибка при чтении файла '{file_path}': {str(e)}")
        return f"Ошибка при чтении файла '{file_path}': {str(e)}"
