import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@pytest.fixture
def logged_in_driver(driver):
    login = LoginPage(driver)
    login.goto()
    login.login("standard_user", "secret_sauce")
    return driver


class TestInventorySorting:
    def test_sorts_by_price_low_to_high(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.sort_by("lohi")

        prices = inventory.item_prices_as_numbers()
        assert prices == sorted(prices)

    def test_sorts_by_price_high_to_low(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.sort_by("hilo")

        prices = inventory.item_prices_as_numbers()
        assert prices == sorted(prices, reverse=True)

    def test_sorts_by_name_z_to_a(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.sort_by("za")

        names = inventory.item_names()
        assert names == sorted(names, reverse=True)

    def test_cart_badge_reflects_number_of_items_added(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory.add_item_to_cart_by_name("Sauce Labs Bike Light")

        assert inventory.cart_badge_text == "2"
