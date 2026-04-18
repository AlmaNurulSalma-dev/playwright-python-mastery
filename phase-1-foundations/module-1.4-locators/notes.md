# Module 1.4 — Locators (The Modern Way)

## Why Locators?

Playwright has TWO ways to find elements:

1. **Selectors in actions** (old way): `page.click("#submit")`
2. **Locators** (modern way): `page.locator("#submit").click()`

Locators are RECOMMENDED because:
- Reusable — store in variable, use multiple times
- Chainable — filter, narrow down
- Lazy — don't search until action is performed
- Strict — error if multiple matches (prevents bugs)
- Auto-wait — built-in waiting before every action

for locator inside ():
"#username"                    # CSS selector
".quote"                       # CSS selector
"xpath=//h1"                   # XPath selector
"a:text('Next')"              # Text selector
"input[type='submit']"        # Attribute selector

## Locator Hierarchy (Most to Least Recommended)

| Priority | Method | Why |
|----------|--------|-----|
| 1st ⭐ | `get_by_role()` | Accessibility-first, resilient to HTML changes |
| 2nd | `get_by_text()` | User-visible text, intuitive |
| 3rd | `get_by_label()` | Form elements by label |
| 4th | `get_by_placeholder()` | Inputs by placeholder |
| 5th | `get_by_test_id()` | data-testid attributes |
| 6th | `locator()` with CSS | Fragile — breaks if HTML structure changes |
| 7th | `locator()` with XPath | Most fragile — avoid if possible |

## Selenium Comparison

| Selenium | Playwright |
|----------|------------|
| `driver.find_element(By.ID, "x")` | `page.locator("#x")` |
| `driver.find_element(By.CLASS_NAME, "x")` | `page.locator(".x")` |
| `driver.find_element(By.CSS_SELECTOR, "x")` | `page.locator("x")` |
| `driver.find_element(By.XPATH, "//x")` | `page.locator("xpath=//x")` |
| `driver.find_elements(By.CSS_SELECTOR, "x")` | `page.locator("x").all()` |
| No equivalent | `page.get_by_role("button", name="Submit")` |
| No equivalent | `page.get_by_text("Hello")` |

## Key Concept: Strictness
Playwright locators are STRICT — if a locator matches more than 1 element,
it throws an error when you try to act on it. This is GOOD — prevents bugs.

Solutions when multiple matches:
- `locator.nth(0)` — pick by index
- `locator.first` / `locator.last` — shortcuts
- `locator.filter(has_text="...")` — narrow down
- Use a more specific locator