# Module 1.3 — Navigation & Basic Interactions

## Selenium vs Playwright Comparison

| Action | Selenium | Playwright |
|--------|----------|------------|
| Go to URL | `driver.get(url)` | `page.goto(url)` |
| Click | `driver.find_element().click()` | `page.click(selector)` |
| Type (instant) | N/A | `page.fill(selector, text)` |
| Type (keystroke) | `element.send_keys(text)` | `page.type(selector, text)` |
| Clear + Type | `element.clear()` + `send_keys()` | `page.fill()` (auto clears!) |
| Press key | `ActionChains.send_keys()` | `page.press(selector, key)` |
| Dropdown | `Select(element).select_by_value()` | `page.select_option(selector, value)` |
| Checkbox | `element.click()` | `page.check()` / `page.uncheck()` |
| Hover | `ActionChains.move_to_element()` | `page.hover(selector)` |
| Back/Forward | `driver.back()` / `driver.forward()` | `page.go_back()` / `page.go_forward()` |

## Key Insight
- Selenium: find element FIRST, then act → `driver.find_element(By.ID, "x").click()`
- Playwright: act directly with selector → `page.click("#x")`
- Playwright auto-waits for element to be ready before acting!

## fill() vs type()
- `fill()` = instant replace (like Ctrl+A → paste) — use 99% of the time
- `type()` = simulates real keystrokes one by one — use when site reacts to each key

## goto() wait_until options
- `'commit'` — fastest, response received
- `'domcontentloaded'` — HTML parsed
- `'load'` — all resources loaded (default)
- `'networkidle'` — no network requests for 500ms (slowest but safest)