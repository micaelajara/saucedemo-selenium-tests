from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class InventoryPage:
    def __init__(self, driver):
        self.driver = driver

    @property
    def title(self):
        return self.driver.find_element(By.CLASS_NAME, "title").text

    def sort_by(self, option_value):
        dropdown = self.driver.find_element(By.CSS_SELECTOR, '[data-test="product-sort-container"]')
        Select(dropdown).select_by_value(option_value)

    def item_names(self):
        return [e.text for e in self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")]

    def item_prices_as_numbers(self):
        texts = [e.text for e in self.driver.find_elements(By.CLASS_NAME, "inventory_item_price")]
        return [float(t.replace("$", "")) for t in texts]

    def add_item_to_cart_by_name(self, name):
        for item in self.driver.find_elements(By.CLASS_NAME, "inventory_item"):
            if name in item.find_element(By.CLASS_NAME, "inventory_item_name").text:
                item.find_element(By.TAG_NAME, "button").click()
                return
        raise ValueError(f"Item not found: {name}")

    @property
    def cart_badge_text(self):
        return self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
