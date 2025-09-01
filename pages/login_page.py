import allure
from .base_page import BasePage
from selenium.webdriver.common.by import By

class LoginPage(BasePage):
    # URL страницы логина
    URL = "https://example.com/login"
    
    # Локаторы
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    
    def __init__(self, driver, logger=None):
        super().__init__(driver, logger)
    
    @allure.step("Открытие страницы логина")
    def open_login_page(self):
        self.open(self.URL)
        return self
    
    @allure.step("Выполнение входа с username: {username}")
    def login(self, username, password):
        self.logger.info(f"Attempting login with username: {username}")
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        return self
    
    @allure.step("Получение сообщения об ошибке")
    def get_error_message(self):
        error_text = self.get_text(self.ERROR_MESSAGE)
        self.logger.warning(f"Error message displayed: {error_text}")
        return error_text
    
    @allure.step("Проверка отображения ошибки")
    def is_error_displayed(self):
        try:
            self.find_element(self.ERROR_MESSAGE, timeout=3)
            self.logger.debug("Error message is displayed")
            return True
        except:
            self.logger.debug("Error message is not displayed")
            return False