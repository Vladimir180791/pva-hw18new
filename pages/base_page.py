import allure
import logging

class BasePage:
    def __init__(self, driver, logger=None):
        self.driver = driver
        self.logger = logger or logging.getLogger(__name__)
    
    @allure.step("Открытие страницы: {url}")
    def open(self, url):
        self.logger.info(f"Opening URL: {url}")
        self.driver.get(url)
        self.logger.debug(f"Page title: {self.driver.title}")
        return self
    
    @allure.step("Поиск элемента: {locator}")
    def find_element(self, locator, timeout=10):
        self.logger.debug(f"Looking for element: {locator}")
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            self.logger.debug(f"Element found: {locator}")
            return element
        except Exception as e:
            self.logger.error(f"Element not found: {locator} - {str(e)}")
            raise
    
    @allure.step("Клик по элементу: {locator}")
    def click(self, locator):
        self.logger.info(f"Clicking on element: {locator}")
        element = self.find_element(locator)
        element.click()
        return self
    
    @allure.step("Ввод текста '{text}' в элемент: {locator}")
    def type_text(self, locator, text):
        self.logger.info(f"Typing text '{text}' into element: {locator}")
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        return self
    
    @allure.step("Получение текста элемента: {locator}")
    def get_text(self, locator):
        self.logger.debug(f"Getting text from element: {locator}")
        element = self.find_element(locator)
        text = element.text
        self.logger.debug(f"Text received: {text}")
        return text