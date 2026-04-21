"""
Module 1.5 — Auto-Waiting & Assertions
File: 02_expect_api.py
Description: expect() API — Playwright's built-in assertion library with auto-retry
Date: 2026-04-20
Phase: 1 - Foundations
Playwright Docs: https://playwright.dev/python/docs/test-assertions
"""

from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()

    # ====================================================================
    # expect() — Playwright's assertion API
    #
    # Unlike Python's assert (instant check, no retry):
    #   assert page.title() == "Quotes"  # ❌ fails if title not loaded yet
    #
    # expect() AUTO-RETRIES until timeout (default 5s):
    #   expect(page).to_have_title("Quotes")  # ✅ retries until match!
    # ====================================================================

    # ====================================================================
    # PAGE ASSERTIONS
    # ====================================================================
    print("=== PAGE ASSERTIONS ===\n")

    page.goto("https://quotes.toscrape.com")

    # Assert page title
    expect(page).to_have_title("Quotes to Scrape")
    print("  ✅ to_have_title('Quotes to Scrape') — passed")

    # Assert page URL
    expect(page).to_have_url("https://quotes.toscrape.com/")
    print("  ✅ to_have_url('https://quotes.toscrape.com/') — passed")

    # Partial URL match with regex
    import re
    expect(page).to_have_url(re.compile(r"quotes\.toscrape"))
    print("  ✅ to_have_url(regex) — passed")

    # ====================================================================
    # ELEMENT VISIBILITY ASSERTIONS
    # ====================================================================
    print("\n=== VISIBILITY ASSERTIONS ===\n")

    # Assert element is visible
    heading = page.locator("h1")
    expect(heading).to_be_visible()
    print(f"  ✅ h1 to_be_visible() — passed (text: '{heading.text_content()}')")

    # Assert element is hidden (useful for modals, loaders)
    # We check something that doesn't exist
    fake_element = page.locator("#nonexistent-loader")
    expect(fake_element).to_be_hidden()
    print("  ✅ #nonexistent-loader to_be_hidden() — passed")

    # ====================================================================
    # TEXT ASSERTIONS
    # ====================================================================
    print("\n=== TEXT ASSERTIONS ===\n")

    first_quote = page.locator(".quote").first

    # Assert exact text match
    author = first_quote.locator(".author")
    expect(author).to_have_text("Albert Einstein")
    print(f"  ✅ to_have_text('Albert Einstein') — passed")

    # Assert contains text (substring)
    expect(author).to_contain_text("Einstein")
    print(f"  ✅ to_contain_text('Einstein') — passed")

    # Assert with regex
    expect(author).to_have_text(re.compile(r"^Albert"))
    print(f"  ✅ to_have_text(regex starts with 'Albert') — passed")

    # ====================================================================
    # FORM ELEMENT ASSERTIONS
    # ====================================================================
    print("\n=== FORM ASSERTIONS ===\n")

    page.goto("https://the-internet.herokuapp.com/login")

    # Fill form first
    page.get_by_label("Username").fill("tomsmith")

    # Assert input value
    expect(page.get_by_label("Username")).to_have_value("tomsmith")
    print("  ✅ to_have_value('tomsmith') — passed")

    # Assert input is editable
    expect(page.get_by_label("Username")).to_be_editable()
    print("  ✅ to_be_editable() — passed")

    # Assert input is enabled
    expect(page.get_by_label("Username")).to_be_enabled()
    print("  ✅ to_be_enabled() — passed")

    # ====================================================================
    # CHECKBOX ASSERTIONS
    # ====================================================================
    print("\n=== CHECKBOX ASSERTIONS ===\n")

    page.goto("https://the-internet.herokuapp.com/checkboxes")

    checkbox1 = page.locator("input[type='checkbox']").nth(0)
    checkbox2 = page.locator("input[type='checkbox']").nth(1)

    # Assert checkbox state
    expect(checkbox1).not_to_be_checked()
    print("  ✅ checkbox1 not_to_be_checked() — passed (unchecked by default)")

    expect(checkbox2).to_be_checked()
    print("  ✅ checkbox2 to_be_checked() — passed (checked by default)")

    # Check it, then assert
    checkbox1.check()
    expect(checkbox1).to_be_checked()
    print("  ✅ checkbox1 to_be_checked() after check() — passed")

    # ====================================================================
    # ATTRIBUTE ASSERTIONS
    # ====================================================================
    print("\n=== ATTRIBUTE ASSERTIONS ===\n")

    page.goto("https://quotes.toscrape.com")

    next_link = page.get_by_role("link", name="Next")

    # Assert element has specific attribute
    expect(next_link).to_have_attribute("href", "/page/2/")
    print("  ✅ to_have_attribute('href', '/page/2/') — passed")

    # Assert element has specific class
    first_quote = page.locator(".quote").first
    expect(first_quote).to_have_class(re.compile(r"quote"))
    print("  ✅ to_have_class(regex 'quote') — passed")

    # ====================================================================
    # COUNT ASSERTIONS
    # ====================================================================
    print("\n=== COUNT ASSERTIONS ===\n")

    quotes = page.locator(".quote")
    expect(quotes).to_have_count(10)
    print("  ✅ to_have_count(10) — 10 quotes on page")

    tags = page.locator(".tag-item")
    tag_count = tags.count()
    expect(tags).to_have_count(tag_count)
    print(f"  ✅ to_have_count({tag_count}) — sidebar tags")

    # ====================================================================
    # NEGATIVE ASSERTIONS (not_to_*)
    # ====================================================================
    print("\n=== NEGATIVE ASSERTIONS ===\n")

    expect(page.locator("h1")).not_to_be_hidden()
    print("  ✅ not_to_be_hidden() — h1 is visible")

    expect(page.locator("h1")).not_to_have_text("Wrong Title")
    print("  ✅ not_to_have_text('Wrong Title') — h1 doesn't say this")

    expect(page.locator(".quote")).not_to_have_count(0)
    print("  ✅ not_to_have_count(0) — there ARE quotes on page")

    # ====================================================================
    # expect() vs assert — KEY DIFFERENCE
    # ====================================================================
    print("""
=== expect() vs Python assert ===

Python assert (INSTANT — no retry):
  assert page.title() == "Quotes to Scrape"
  # ❌ If title hasn't loaded yet → AssertionError immediately!

Playwright expect (AUTO-RETRY — waits up to 5s):
  expect(page).to_have_title("Quotes to Scrape")
  # ✅ Keeps checking every few ms until title matches or timeout!
  dan dia bisa di configure timeout nya, misal 10s:
  expect(page).to_have_title("Quotes to Scrape", timeout=10000)

ALWAYS use expect() for web assertions — pages are dynamic,
elements take time to update!

Selenium comparison:
  Selenium has NO built-in retry assertions.
  You must combine WebDriverWait + custom conditions.
  Playwright's expect() does it in one line!
""")

    # ====================================================================
    # COMPLETE ASSERTIONS REFERENCE
    # ====================================================================
    print("""
=== ALL expect() ASSERTIONS ===

Page:
  expect(page).to_have_title(title)
  expect(page).to_have_url(url)

Visibility:
  expect(locator).to_be_visible()
  expect(locator).to_be_hidden()

Text:
  expect(locator).to_have_text(text)       # exact match
  expect(locator).to_contain_text(text)    # substring

Form:
  expect(locator).to_have_value(value)
  expect(locator).to_be_editable()
  expect(locator).to_be_enabled()
  expect(locator).to_be_disabled()

Checkbox:
  expect(locator).to_be_checked()

Attributes:
  expect(locator).to_have_attribute(name, value)
  expect(locator).to_have_class(class)
  expect(locator).to_have_id(id)
  expect(locator).to_have_css(property, value)

Count:
  expect(locator).to_have_count(count)

Negative (prefix with not_to_):
  expect(locator).not_to_be_visible()
  expect(locator).not_to_have_text(text)
  expect(locator).not_to_be_checked()
  ... (every assertion has a not_ version)

All accept timeout= parameter:
  expect(locator).to_be_visible(timeout=10000)  # wait up to 10s
""")

    browser.close()
    print("✅ expect() API complete!")