"""
Module 1.4 — Locators (The Modern Way)
File: 01_css_xpath.py
Description: CSS selectors and XPath locators — the traditional way
Date: 2026-04-09
Phase: 1 - Foundations
Playwright Docs: https://playwright.dev/python/docs/locators
"""

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()
    page.goto("https://quotes.toscrape.com")

    # ====================================================================
    # CSS SELECTORS — Same syntax as Selenium's By.CSS_SELECTOR
    # ====================================================================
    print("=== CSS SELECTORS ===\n")

    # By tag
    heading = page.locator("h1")
    print(f"  By tag 'h1': {heading.text_content()}")

    # By class
    first_quote = page.locator(".quote").first
    print(f"  By class '.quote' (first): {first_quote.locator('.text').text_content()[:50]}...")

    # By ID (if exists)
    # page.locator("#some-id")

    # By attribute
    next_link = page.locator("a[href='/page/2/']")
    print(f"  By attribute 'a[href=/page/2/]': {next_link.text_content()}")

    # By tag + class
    quote_texts = page.locator("span.text")
    print(f"  By 'span.text' count: {quote_texts.count()} quotes on this page")

    # Nested selectors (descendant)
    author_in_quote = page.locator(".quote .author")
    print(f"  By '.quote .author' (first): {author_in_quote.first.text_content()}")

    # Direct child selector
    # page.locator("div > span")  # span that is DIRECT child of div

    # Multiple conditions
    # page.locator("input[type='text'][name='username']")

    # ====================================================================
    # XPATH SELECTORS — Prefix with "xpath="
    # ====================================================================
    print("\n=== XPATH SELECTORS ===\n")

    # Basic XPath
    h1 = page.locator("xpath=//h1")
    print(f"  XPath '//h1': {h1.text_content()}")

    # XPath by attribute
    next_xpath = page.locator("xpath=//a[@href='/page/2/']")
    print(f"  XPath by href: {next_xpath.text_content()}")

    # XPath by text content
    login_link = page.locator("xpath=//a[text()='Login']")
    print(f"  XPath by text 'Login': {login_link.text_content()}")

    # XPath with contains
    quotes_xpath = page.locator("xpath=//span[contains(@class, 'text')]")
    print(f"  XPath contains class 'text': {quotes_xpath.count()} matches")

    # ====================================================================
    # CSS vs XPATH — When to use which?
    # ====================================================================
    print("""
=== CSS vs XPATH ===

CSS Selectors:
  ✅ Shorter, more readable
  ✅ Faster performance
  ✅ Used in most Playwright examples
  ❌ Cannot traverse UP the DOM (child → parent)

XPath:
  ✅ Can traverse UP (child → parent)
  ✅ Can select by text content natively
  ✅ More powerful for complex selections
  ❌ Longer syntax, harder to read
  ❌ Slightly slower

RECOMMENDATION: Use CSS by default, XPath when you need
to go UP the DOM tree or do complex text matching.

BUT ACTUALLY: Playwright's get_by_*() methods are BETTER
than both CSS and XPath for most cases! (Next file!)
""")

    # ====================================================================
    # LOCATOR STRICTNESS — Important concept!
    # ====================================================================
    print("=== STRICTNESS DEMO ===\n")

    all_quotes = page.locator(".quote")
    print(f"  .quote matches: {all_quotes.count()} elements")

    # This would ERROR because multiple matches:
    # all_quotes.click()  # ❌ Error: strict mode violation

    # Solutions:
    print(f"  .first: {all_quotes.first.locator('.author').text_content()}")
    print(f"  .last: {all_quotes.last.locator('.author').text_content()}")
    print(f"  .nth(0): {all_quotes.nth(0).locator('.author').text_content()}")
    print(f"  .nth(4): {all_quotes.nth(4).locator('.author').text_content()}")

    # Get ALL as list
    all_list = all_quotes.all()
    print(f"\n  .all() returned {len(all_list)} locators:")
    for i, q in enumerate(all_list[:3]):  # first 3 only
        author = q.locator(".author").text_content()
        print(f"    Quote {i}: by {author}")

    browser.close()
    print("\n✅ CSS & XPath locators complete!")