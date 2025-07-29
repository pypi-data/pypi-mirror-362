import logging
import sys
import os
from logging.handlers import RotatingFileHandler

def configure_logger(
    logger_name,
    level=logging.INFO,
    console=True,
    log_file=None,
    log_format=None,
    max_file_size=10485760,  # 10 МБ по умолчанию
    backup_count=5,
    propagate=False
):
    """
    Настраивает логгер с указанными параметрами.
    
    Args:
        level: Уровень логирования (по умолчанию INFO)
        console: Логировать в консоль (True или False)
        log_file: Путь к файлу лога (или None, если не нужно логировать в файл)
        log_format: Формат лога (или None для использования стандартного формата)
        max_file_size: Максимальный размер файла лога перед ротацией
        backup_count: Количество файлов резервных копий
        propagate: Передавать ли сообщения родительским логгерам
        module_name: Имя модуля для создания дочернего логгера (или None для основного логгера)
    
    Returns:
        Настроенный логгер
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    logger.propagate = propagate
    
    # Устанавливаем формат
    if log_format is None:
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)
    
    # Добавляем обработчик для консоли, если нужно
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # Добавляем обработчик для файла, если нужно
    if log_file:
        # Создаем директорию, если она не существует
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # Используем RotatingFileHandler для автоматической ротации файлов
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_file_size,
            backupCount=backup_count
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger