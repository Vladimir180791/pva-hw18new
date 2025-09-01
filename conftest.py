import pytest
import allure
import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    """Настройка логирования для всей сессии тестов"""
    from utils.logger import setup_logging
    setup_logging(log_level=logging.INFO)

@pytest.fixture(scope="function")
def driver():
    """Фикстура для инициализации и закрытия браузера"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    
    driver = webdriver.Chrome(
        ChromeDriverManager().install(),
        options=chrome_options
    )
    
    logging.info("Browser started")
    yield driver
    
    driver.quit()
    logging.info("Browser closed")

@pytest.fixture
def logger(request):
    """Фикстура для получения логгера с именем теста"""
    test_name = request.node.name
    return logging.getLogger(test_name)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для создания скриншотов при падении тестов"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        try:
            driver = item.funcargs.get('driver')
            if driver:
                # Создаем директорию для скриншотов если её нет
                screenshot_dir = "screenshots"
                if not os.path.exists(screenshot_dir):
                    os.makedirs(screenshot_dir)
                
                # Сохраняем скриншот
                screenshot_path = os.path.join(screenshot_dir, f"{item.name}.png")
                driver.save_screenshot(screenshot_path)
                
                # Добавляем в allure отчет
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=f"screenshot_{item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
                
                logging.warning(f"Screenshot saved: {screenshot_path}")
        except Exception as e:
            logging.error(f"Failed to take screenshot: {e}")

@pytest.fixture(scope="session", autouse=True)
def create_environment_file():
    """Создание файла environment.properties для Allure"""
    environment_dir = "allure-results"
    if not os.path.exists(environment_dir):
        os.makedirs(environment_dir)
    
    environment_file = os.path.join(environment_dir, "environment.properties")
    
    import sys
    import allure
    from selenium import __version__ as selenium_version
    
    env_vars = {
        "PYTHON_VERSION": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "PYTEST_VERSION": pytest.__version__,
        "ALLURE_VERSION": allure.__version__,
        "SELENIUM_VERSION": selenium_version,
        "OS": os.name,
        "TEST_ENV": "CI" if os.getenv("CI") else "LOCAL",
    }
    
    with open(environment_file, "w", encoding="utf-8") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
    
    logging.info("Environment file created for Allure report")