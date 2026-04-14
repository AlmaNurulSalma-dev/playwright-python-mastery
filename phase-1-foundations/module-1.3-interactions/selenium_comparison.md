# Selenium vs Playwright — Interactions Comparison

## Setup & Navigation

| Action | Selenium | Playwright |
|--------|----------|------------|
| Import | `from selenium import webdriver` | `from playwright.sync_api import sync_playwright` |
| Launch | `driver = webdriver.Chrome()` | `browser = p.chromium.launch()` |
| Navigate | `driver.get(url)` | `page.goto(url)` |
| Back | `driver.back()` | `page.go_back()` |
| Forward | `driver.forward()` | `page.go_forward()` |
| Refresh | `driver.refresh()` | `page.reload()` |
| Current URL | `driver.current_url` | `page.url` |
| Page title | `driver.title` | `page.title()` |
| Page source | `driver.page_source` | `page.content()` |
| Close | `driver.quit()` | `browser.close()` |

## Finding Elements

```python
# Selenium — ALWAYS two steps: find first, then act
element = driver.find_element(By.ID, "username")
element.click()

# Playwright — one step: act directly with selector
page.click("#username")
```

| Find by | Selenium | Playwright |
|---------|----------|------------|
| ID | `By.ID, "username"` | `"#username"` |
| Class | `By.CLASS_NAME, "btn"` | `".btn"` |
| CSS | `By.CSS_SELECTOR, "input[type='text']"` | `"input[type='text']"` |
| XPath | `By.XPATH, "//div[@class='quote']"` | `"xpath=//div[@class='quote']"` |
| Text | N/A (use XPath) | `"text=Login"` or `"a:text('Next')"` |
| Tag | `By.TAG_NAME, "button"` | `"button"` |

## Click

```python
# Selenium
driver.find_element(By.ID, "submit").click()

# Playwright
page.click("#submit")
```

```python
# Selenium — double click
from selenium.webdriver.common.action_chains import ActionChains
ActionChains(driver).double_click(element).perform()

# Playwright
page.dblclick("#element")
```

```python
# Selenium — right click
ActionChains(driver).context_click(element).perform()

# Playwright
page.click("#element", button="right")
```

## Text Input

```python
# Selenium — clear + type (manual)
element = driver.find_element(By.ID, "username")
element.clear()
element.send_keys("admin")

# Playwright — fill auto-clears
page.fill("#username", "admin")
```

```python
# Selenium — type character by character (not built-in, needs loop or send_keys)
element.send_keys("admin")  # sends all at once, not truly char-by-char

# Playwright — true character-by-character typing
page.type("#username", "admin", delay=100)  # 100ms between each keystroke
```

## Keyboard

```python
# Selenium
from selenium.webdriver.common.keys import Keys
element.send_keys(Keys.ENTER)
element.send_keys(Keys.TAB)
ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()

# Playwright
page.press("#element", "Enter")
page.press("#element", "Tab")
page.press("#element", "Control+a")
```

## Dropdowns

```python
# Selenium — needs special Select class
from selenium.webdriver.support.ui import Select
select = Select(driver.find_element(By.ID, "dropdown"))
select.select_by_value("1")
select.select_by_visible_text("Option 1")
select.select_by_index(1)

# Playwright — one method, no special class
page.select_option("#dropdown", value="1")
page.select_option("#dropdown", label="Option 1")
page.select_option("#dropdown", index=1)
```

## Checkboxes

```python
# Selenium — DANGEROUS! click() toggles state
checkbox = driver.find_element(By.ID, "agree")
checkbox.click()  # if already checked → UNCHECKS it!
# Need manual check:
if not checkbox.is_selected():
    checkbox.click()

# Playwright — SAFE! check() is idempotent
page.check("#agree")    # already checked? does nothing
page.uncheck("#agree")  # already unchecked? does nothing
```

## Hover

```python
# Selenium — needs ActionChains
from selenium.webdriver.common.action_chains import ActionChains
element = driver.find_element(By.CSS_SELECTOR, ".menu")
ActionChains(driver).move_to_element(element).perform()

# Playwright
page.hover(".menu")
```

## File Upload

```python
# Selenium
driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys("/path/to/file.pdf")

# Playwright
page.set_input_files("input[type='file']", "path/to/file.pdf")
```

## Drag and Drop

```python
# Selenium
source = driver.find_element(By.ID, "draggable")
target = driver.find_element(By.ID, "droppable")
ActionChains(driver).drag_and_drop(source, target).perform()

# Playwright
page.drag_and_drop("#draggable", "#droppable")
```

## Waiting

```python
# Selenium — MANUAL waits everywhere!
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "submit"))
)
element.click()

# Playwright — AUTO-WAIT built in!
page.click("#submit")  # automatically waits up to 30s for element to be clickable
```

## Overall Pattern

```python
# ═══════════════════════════════════════
# SELENIUM: Find → Store → Act
# ═══════════════════════════════════════
element = driver.find_element(By.ID, "username")  # find
element.clear()                                     # act 1
element.send_keys("admin")                          # act 2

submit = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
submit.click()

# ═══════════════════════════════════════
# PLAYWRIGHT: Just Act (selector inline)
# ═══════════════════════════════════════
page.fill("#username", "admin")            # find + clear + type in one
page.click("input[type='submit']")         # find + click in one
```

## Lines of Code Comparison

| Task | Selenium | Playwright |
|------|----------|------------|
| Login form | ~8 lines | ~3 lines |
| Dropdown select | ~3 lines + import | ~1 line |
| Hover | ~3 lines + import | ~1 line |
| Checkbox (safe) | ~3 lines | ~1 line |
| Wait + click | ~4 lines + imports | ~1 line |

## Verdict

Playwright wins on:
- **Less code** — no find-then-act, just act
- **Auto-wait** — no manual WebDriverWait
- **Smarter methods** — check() vs click() for checkboxes
- **Built-in features** — no ActionChains import needed
- **Text selectors** — find by visible text natively