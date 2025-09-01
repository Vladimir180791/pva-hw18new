import logging
import os

def setup_logging(log_dir="logs", log_level=logging.INFO):
    """
    Настройка конфигурации логирования для всего проекта
    """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, "tests.log")

    # Форматтер для всех обработчиков
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Обработчик для консоли
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # Обработчик для файла
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    # Базовая конфигурация
    logging.basicConfig(
        level=log_level,
        handlers=[console_handler, file_handler]
    )

    return logging.getLogger(__name__)

# Глобальная настройка логирования при импорте модуля
logger = logging.getLogger(__name__)