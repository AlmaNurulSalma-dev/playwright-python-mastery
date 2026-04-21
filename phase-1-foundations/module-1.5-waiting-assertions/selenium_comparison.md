# Selenium vs Playwright — Waiting & Assertions

## The Biggest Difference

Selenium: YOU manage all the waiting manually.
Playwright: Waiting is BUILT IN to every action.

## Waiting Comparison

### Selenium — Manual waits everywhere

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://example.com")

# Wait for element to be clickable — 4 lines + 3 imports!
element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "submit"))
)
element.click()

# Wait for element to be visible
element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".result"))
)
print(element.text)
```

### Playwright — Auto-wait built in

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")

    # Auto-waits for clickable — 1 line, 0 extra imports!
    page.click("#submit")

    # Auto-waits for visible
    print(page.locator(".result").text_content())
```

## Selenium's 3 Types of Waits

| Type | Selenium | Playwright |
|------|----------|------------|
| Implicit wait | `driver.implicitly_wait(10)` | Not needed — auto-wait |
| Explicit wait | `WebDriverWait(driver, 10).until(EC....)` | Not needed — auto-wait |
| Hard wait | `time.sleep(3)` | `page.wait_for_timeout(3000)` (avoid both!) |

## Assertions Comparison

### Selenium — No built-in retry assertions

```python
# Instant check — no retry!
assert driver.title == "My Page"              # ❌ fails if page still loading
assert element.text == "Hello"                # ❌ fails if text not updated yet
assert element.is_displayed()                 # ❌ fails if still animating

# Must combine with WebDriverWait for retry
WebDriverWait(driver, 10).until(
    EC.title_is("My Page")
)
```

### Playwright — expect() with auto-retry

```python
from playwright.sync_api import expect

# Auto-retry up to 5s!
expect(page).to_have_title("My Page")         # ✅ retries until match
expect(locator).to_have_text("Hello")         # ✅ retries until match
expect(locator).to_be_visible()               # ✅ retries until visible
```

## Selenium Expected Conditions vs Playwright expect()

| Selenium EC | Playwright expect() |
|-------------|-------------------|
| `EC.title_is("x")` | `expect(page).to_have_title("x")` |
| `EC.url_contains("x")` | `expect(page).to_have_url(re.compile("x"))` |
| `EC.visibility_of_element_located(loc)` | `expect(locator).to_be_visible()` |
| `EC.invisibility_of_element_located(loc)` | `expect(locator).to_be_hidden()` |
| `EC.element_to_be_clickable(loc)` | Not needed — auto-wait on click() |
| `EC.text_to_be_present_in_element(loc, "x")` | `expect(locator).to_have_text("x")` |
| `EC.element_to_be_selected(loc)` | `expect(locator).to_be_checked()` |
| No equivalent | `expect(locator).to_have_count(n)` |
| No equivalent | `expect(locator).to_have_attribute(name, val)` |
| No equivalent | `expect(locator).to_have_css(prop, val)` |

## Timeout Comparison

| Setting | Selenium | Playwright |
|---------|----------|------------|
| Global action timeout | `driver.implicitly_wait(10)` | `page.set_default_timeout(10000)` |
| Per-action timeout | Set in WebDriverWait | `page.click(sel, timeout=5000)` |
| Navigation timeout | `driver.set_page_load_timeout(30)` | `page.set_default_navigation_timeout(30000)` |
| Assertion timeout | No built-in | `expect.set_options(timeout=5000)` |
| Units | Seconds | Milliseconds |

## Lines of Code Comparison

| Task | Selenium | Playwright |
|------|----------|------------|
| Wait + click | 4 lines + 3 imports | 1 line |
| Wait + get text | 4 lines + 3 imports | 1 line |
| Assert title with retry | 3 lines + imports | 1 line |
| Assert visible with retry | 3 lines + imports | 1 line |
| Configure timeout | 1 line | 1 line |