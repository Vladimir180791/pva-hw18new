import allure
import pytest
from pages.login_page import LoginPage

@allure.epic("Авторизация")
@allure.feature("Функциональность входа в систему")
class TestLogin:
    
    @pytest.fixture
    def login_page(self, driver, logger):
        """Фикстура для создания экземпляра LoginPage"""
        return LoginPage(driver, logger)
    
    @allure.story("Успешный вход в систему")
    @allure.title("Тест успешной авторизации с валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("""
    Этот тест проверяет успешный вход в систему с корректными учетными данными.
    Ожидается переход на главную страницу после авторизации.
    """)
    @pytest.mark.parametrize("username,password", [
        ("valid_user", "valid_password"),
        ("admin", "admin123")
    ])
    def test_successful_login(self, login_page, username, password):
        with allure.step("Открытие страницы логина"):
            login_page.open_login_page()
        
        with allure.step(f"Ввод учетных данных: {username}"):
            login_page.login(username, password)
        
        with allure.step("Проверка успешной авторизации"):
            assert "dashboard" in login_page.driver.current_url
            assert "Welcome" in login_page.driver.page_source
    
    @allure.story("Неуспешный вход в систему")
    @allure.title("Тест авторизации с неверными данными")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("username,password,expected_error", [
        ("invalid_user", "wrong_password", "Invalid credentials"),
        ("", "password", "Username is required"),
        ("user", "", "Password is required")
    ])
    def test_failed_login(self, login_page, username, password, expected_error):
        with allure.step("Открытие страницы логина"):
            login_page.open_login_page()
        
        with allure.step(f"Ввод неверных учетных данных: {username}"):
            login_page.login(username, password)
        
        with allure.step("Проверка отображения ошибки"):
            assert login_page.is_error_displayed()
            error_text = login_page.get_error_message()
            assert expected_error in error_text