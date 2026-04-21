# Module 1.5 — Auto-Waiting & Assertions

## The #1 Pain Point in Selenium

Selenium's biggest headache: elements not ready when you try to interact.

```python
# Selenium — crashes if button hasn't loaded yet
driver.find_element(By.ID, "submit").click()  # ❌ NoSuchElementException!

# Selenium fix — manual waits EVERYWHERE
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "submit"))
)
element.click()  # 4 lines just to click a button!
```

## Playwright's Solution: Auto-Wait

Every Playwright action AUTOMATICALLY waits for the element to be ready.

```python
# Playwright — just click, it handles the rest
page.click("#submit")  # ✅ auto-waits up to 30s for element to be clickable
```

## What Playwright Checks Before Every Action

| Check | Meaning |
|-------|---------|
| Visible | Element is not hidden (display:none, visibility:hidden) |
| Stable | Element is not animating/moving |
| Enabled | Element is not disabled |
| Receives Events | No overlay/modal blocking it |
| Editable | For fill/type — element accepts input |

## expect() API — Built-in Assertions

```python
from playwright.sync_api import expect

# Assert element state
expect(locator).to_be_visible()
expect(locator).to_have_text("Hello")
expect(locator).to_be_checked()

# Assert page state
expect(page).to_have_url("https://example.com")
expect(page).to_have_title("My Page")
```

## Timeouts

| Level | How to set | Affects |
|-------|-----------|---------|
| Per-action | `page.click(selector, timeout=5000)` | Single action |
| Per-page | `page.set_default_timeout(10000)` | All actions on this page |
| Per-navigation | `page.set_default_navigation_timeout(60000)` | goto, back, forward, reload |
| Per-expect | `expect(loc).to_be_visible(timeout=5000)` | Single assertion |

Default timeout: 30000ms (30 seconds)

## Selenium Comparison

| Scenario | Selenium | Playwright |
|----------|----------|------------|
| Wait for element | WebDriverWait + EC (4+ lines) | Automatic (0 lines) |
| Assert text | assertEqual(element.text, "x") | expect(locator).to_have_text("x") |
| Assert visible | is_displayed() (no auto-retry) | expect(locator).to_be_visible() (auto-retry!) |
| Assert URL | assertEqual(driver.current_url, x) | expect(page).to_have_url(x) |
| Timeout config | Implicit/explicit/fluent waits | Simple per-action or global |