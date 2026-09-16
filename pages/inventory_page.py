from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

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
        # Unlike Playwright's Locator, a Selenium WebElement doesn't retry or
        # wait on its own: click() fires immediately, even if the button
        # isn't interactable yet. Waiting for it explicitly is what makes
        # two adds in a row reliable instead of occasionally silently
        # missing a click.
        for item in self.driver.find_elements(By.CLASS_NAME, "inventory_item"):
            if name in item.find_element(By.CLASS_NAME, "inventory_item_name").text:
                button = item.find_element(By.TAG_NAME, "button")
                self.wait.until(EC.element_to_be_clickable(button))
                button.click()
                return
        raise ValueError(f"Item not found: {name}")

    @property
    def cart_badge_text(self):
        return self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
