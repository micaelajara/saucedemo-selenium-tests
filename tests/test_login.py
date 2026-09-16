from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


class TestLogin:
    def test_standard_user_logs_in_successfully(self, driver):
        login = LoginPage(driver)
        login.goto()
        login.login("standard_user", "secret_sauce")

        assert "inventory.html" in driver.current_url
        assert InventoryPage(driver).title == "Products"

    def test_locked_out_user_is_rejected_with_a_clear_error(self, driver):
        login = LoginPage(driver)
        login.goto()
        login.login("locked_out_user", "secret_sauce")

        assert driver.current_url.rstrip("/") == "https://www.saucedemo.com"
        assert "locked out" in login.error_message

    def test_wrong_password_is_rejected_with_a_generic_error(self, driver):
        login = LoginPage(driver)
        login.goto()
        login.login("standard_user", "not_the_password")

        assert "do not match" in login.error_message

    def test_empty_credentials_are_rejected_client_side(self, driver):
        login = LoginPage(driver)
        login.goto()
        login.submit()

        assert "Username is required" in login.error_message
