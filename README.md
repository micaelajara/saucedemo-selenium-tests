# saucedemo-selenium-tests

A Selenium + pytest Page Object Model suite for saucedemo.com: login (happy path, locked out user, wrong password, empty fields) and inventory sorting (price low/high, name Z-A, cart badge count).

**Run for real:** 8/8 tests passed locally against the live site (Chrome, headless), and again in GitHub Actions on push.

## Why this exists

I already have the same site covered with Playwright in [`saucedemo-playwright-ci`](https://github.com/micaelajara/saucedemo-playwright-ci). This isn't a random second project, it's the same test plan (same POM structure, same scenarios) rebuilt on a different tool, on purpose: to show the Page Object Model itself is the transferable skill, not the specific API of one framework.

## Selenium vs. Playwright (what actually differs)

| | Selenium | Playwright |
|---|---|---|
| Waiting for elements | Manual (explicit waits) unless the action itself retries | Auto-waiting built into every action |
| Driver setup | Selenium Manager resolves/downloads the browser driver (Selenium 4+) | Ships its own bundled browser binaries |
| Locators | `driver.find_element(By.ID, ...)` returns a live element right away | `page.locator(...)` is a lazy handle, resolved when acted on |
| Language ecosystem | Java, Python, JS, C#, Ruby, all first-class | Strongest in JS/TS and Python |

Practical consequence in this repo: `sort_by()` in `pages/inventory_page.py` calls Selenium's `Select` helper on a raw `<select>` element, where the Playwright version just calls `.selectOption()` directly on a Locator. Same intent (pick a dropdown option), different API shape, because Playwright's locators already carry the retry/wait logic that Selenium's plain `WebElement` doesn't.

That last point wasn't theoretical: it caused two real, reproducible flakes while building this suite. `add_item_to_cart_by_name()` clicked a button before it was interactable, silently missing the click and leaving the cart badge at "1" instead of "2". Logging in and immediately reading the inventory list sometimes ran against the still-loading login page and came back empty. Both are fixed with explicit `WebDriverWait` calls (`element_to_be_clickable`, `presence_of_element_located`), because in Selenium that wait is the test's job, not the driver's.

## Run it yourself

```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
pytest -v
```

## Stack

Selenium 4, pytest, Python, GitHub Actions.
