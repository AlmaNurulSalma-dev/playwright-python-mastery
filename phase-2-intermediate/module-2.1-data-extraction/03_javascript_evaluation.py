"""
Module 2.1 — Data Extraction Mastery
File: 03_javascript_evaluation.py
Description: Using page.evaluate() and locator.evaluate() to run JavaScript for data extraction
Date: 2026-04-26
Phase: 2 - Intermediate
Playwright Docs: https://playwright.dev/python/docs/evaluating
"""

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=300)
    page = browser.new_page()

    # ====================================================================
    # page.evaluate() — Run JavaScript on the page
    # ====================================================================
    print("=== page.evaluate() BASICS ===\n")

    page.goto("https://quotes.toscrape.com")

    # Get page title via JS
    title = page.evaluate("document.title")
    print(f"  document.title: {title}")

    # Get current URL via JS
    url = page.evaluate("window.location.href")
    print(f"  window.location.href: {url}")

    # Get page dimensions
    width = page.evaluate("window.innerWidth")
    height = page.evaluate("window.innerHeight")
    print(f"  Window size: {width} x {height}")

    # Count elements via JS
    quote_count = page.evaluate("document.querySelectorAll('.quote').length")
    print(f"  Quote count (via JS): {quote_count}")

    # Get scroll position
    scroll = page.evaluate("window.scrollY")
    print(f"  Scroll position: {scroll}")

    # ====================================================================
    # page.evaluate() with ARROW FUNCTIONS
    # For more complex JS, use arrow functions: () => { ... }
    # ====================================================================
    print("\n=== ARROW FUNCTIONS ===\n")

    # Extract all author names using JavaScript
    authors = page.evaluate("""
        () => {
            const elements = document.querySelectorAll('.author');
            return Array.from(elements).map(el => el.textContent);
        }
    """)
    print(f"  Authors via JS: {authors}")

    # Extract structured data using JavaScript
    first_quote_js = page.evaluate("""
        () => {
            const quote = document.querySelector('.quote');
            return {
                text: quote.querySelector('.text').textContent,
                author: quote.querySelector('.author').textContent,
                tags: Array.from(quote.querySelectorAll('.tag')).map(t => t.textContent)
            };
        }
    """)
    print(f"  First quote via JS:")
    print(f"    Text: {first_quote_js['text'][:50]}...")
    print(f"    Author: {first_quote_js['author']}")
    print(f"    Tags: {first_quote_js['tags']}")

    # ====================================================================
    # locator.evaluate() — Run JS on a SPECIFIC element
    # 'el' parameter = the DOM element the locator found
    # ====================================================================
    print("\n=== locator.evaluate() ===\n")

    first_quote = page.locator(".quote").first

    # Get element's bounding box (position and size)
    rect = first_quote.evaluate("el => el.getBoundingClientRect()")
    print(f"  Bounding box: x={rect['x']:.0f}, y={rect['y']:.0f}, w={rect['width']:.0f}, h={rect['height']:.0f}")

    # Get element's class list
    classes = first_quote.evaluate("el => el.className")
    print(f"  Class name: '{classes}'")

    # Get number of child elements
    child_count = first_quote.evaluate("el => el.children.length")
    print(f"  Child elements: {child_count}")

    # Get tag names of children
    child_tags = first_quote.evaluate("el => Array.from(el.children).map(c => c.tagName)")
    print(f"  Child tag names: {child_tags}")

    # ====================================================================
    # locator.evaluate_all() — Run JS on ALL matching elements
    # 'els' parameter = array of ALL matching DOM elements
    # ====================================================================
    print("\n=== locator.evaluate_all() ===\n")

    # Get all quote texts using evaluate_all
    all_texts = page.locator(".text").evaluate_all(
        "els => els.map(el => el.textContent.substring(0, 50))"
    )
    print(f"  All quote texts (first 50 chars each):")
    for i, text in enumerate(all_texts[:5], start=1):
        print(f"    {i}. {text}...")

    # Get all author names + their links in one JS call
    author_data = page.locator(".quote").evaluate_all("""
        els => els.map(el => ({
            name: el.querySelector('.author').textContent,
            link: el.querySelector('a[href*="author"]').getAttribute('href')
        }))
    """)
    print(f"\n  Author data via evaluate_all:")
    for item in author_data[:3]:
        print(f"    {item['name']} → {item['link']}")

    # ====================================================================
    # PRACTICAL: Extract data not accessible via locators
    # ====================================================================
    print("\n=== PRACTICAL: Hidden data ===\n")

    page.goto("https://books.toscrape.com")

    # Get data from computed styles (not in HTML attributes)
    first_book = page.locator("article.product_pod").first
    computed_color = first_book.evaluate(
        "el => getComputedStyle(el.querySelector('.price_color')).color"
    )
    print(f"  Price text color (computed): {computed_color}")

    # Check if element is inside viewport
    is_in_viewport = first_book.evaluate("""
        el => {
            const rect = el.getBoundingClientRect();
            return rect.top >= 0 && rect.bottom <= window.innerHeight;
        }
    """)
    print(f"  First book in viewport: {is_in_viewport}")

    # ====================================================================
    # SCROLLING with evaluate — useful for infinite scroll pages
    # ====================================================================
    print("\n=== SCROLL WITH JS ===\n")

    scroll_before = page.evaluate("window.scrollY")
    print(f"  Scroll before: {scroll_before}")

    # Scroll down 500 pixels
    page.evaluate("window.scrollBy(0, 500)")
    page.wait_for_timeout(500)  # brief wait for scroll animation

    scroll_after = page.evaluate("window.scrollY")
    print(f"  Scroll after: {scroll_after}")

    # Scroll to bottom of page
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)

    scroll_bottom = page.evaluate("window.scrollY")
    print(f"  Scroll at bottom: {scroll_bottom}")

    # ====================================================================
    # WHEN TO USE evaluate() vs Playwright methods
    # ====================================================================
    print("""
=== WHEN TO USE evaluate() ===

USE Playwright methods (preferred):
  ✅ locator.text_content()        → get text
  ✅ locator.get_attribute("href") → get attribute
  ✅ locator.input_value()         → get input value
  ✅ locator.is_visible()          → check visibility
  ✅ locator.count()               → count elements

USE evaluate() when Playwright CAN'T do it:
  ✅ Computed CSS styles            → getComputedStyle()
  ✅ JavaScript variables on page   → window.__DATA__
  ✅ Complex DOM traversal          → parentNode, siblings
  ✅ Scroll manipulation            → window.scrollBy()
  ✅ Canvas/WebGL data              → canvas.toDataURL()
  ✅ LocalStorage/SessionStorage    → localStorage.getItem()
  ✅ Performance metrics            → performance.timing
""")

    browser.close()
    print("✅ JavaScript evaluation complete!")