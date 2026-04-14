"""
Module 1.3 — Navigation & Basic Interactions
File: 02_click_and_fill.py
Description: Clicking elements, filling forms, and the difference between fill() and type()
Date: 2026-04-13
Phase: 1 - Foundations
Playwright Docs: https://playwright.dev/python/docs/input
"""

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=800)
    page = browser.new_page()

    # ====================================================================
    # SCENARIO: Login to quotes.toscrape.com
    # This demonstrates fill() and click() in a real form
    # ====================================================================
    print("=== LOGIN FORM ===\n")

    page.goto("https://quotes.toscrape.com/login")
    print(f"  Page: {page.url}")

    # fill() — clears the input first, then sets the value INSTANTLY
    # Selenium equivalent: element.clear() + element.send_keys("admin")
    page.fill("input#username", "admin")
    print("  Filled username")

    page.fill("input#password", "admin")
    print("  Filled password")

    # click() — clicks an element
    # Selenium equivalent: driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    page.click("input[type='submit']")
    print(f"  Clicked submit → Redirected to: {page.url}")

    # ====================================================================
    # fill() vs type() — What's the difference?
    # ====================================================================
    print("\n=== fill() vs type() ===\n")

    page.goto("https://quotes.toscrape.com/login")

    # fill() — INSTANT, no key events fired per character
    # Good for: most form filling, fast, reliable
    page.fill("input#username", "fill_demo")
    print("  fill(): Set value instantly (like Ctrl+A → paste)")

    # Clear it first for next demo
    page.fill("input#username", "")

    # type() — types ONE CHARACTER AT A TIME, fires keydown/keypress/keyup per char
    # Good for: autocomplete fields, search bars that react to each keystroke
    page.type("input#username", "type_demo", delay=100)
    print("  type(): Typed character by character (with 100ms delay)")

    # ====================================================================
    # WHEN TO USE WHICH?
    #
    # fill()  → 99% of the time. Fast, reliable, clears automatically.
    # type()  → When the website REACTS to individual keystrokes:
    #           - Search autocomplete (Google search, dropdown suggestions)
    #           - Real-time validation ("username available!" as you type)
    #           - Character counters (Twitter/X post length)
    # ====================================================================

    # ====================================================================
    # DIFFERENT CLICK TYPES
    # ====================================================================
    print("\n=== CLICK VARIATIONS ===\n")

    page.goto("https://quotes.toscrape.com")

    # Basic click
    page.click("a:text('Next')")
    print(f"  click(): Navigated to {page.url}")

    page.go_back()

    # Double click — useful for selecting text, opening files in file managers
    # (no visible effect on this site, but showing the syntax)
    page.dblclick(".tag-item a")
    print("  dblclick(): Double-clicked a tag")

    page.go_back()

    # Click with options
    page.click("a:text('Next')", delay=200)  # 200ms between mousedown and mouseup
    print(f"  click(delay=200): Slow click → {page.url}")

    page.go_back()

    # Force click — bypasses visibility/actionability checks
    # Use when Playwright says "element is not visible" but you know it's there
    # page.click("selector", force=True)
    print("  click(force=True): Skips actionability checks (use as last resort!)")

    # ====================================================================
    # CLICKING BY DIFFERENT SELECTORS
    # ====================================================================
    print("\n=== SELECTOR TYPES FOR CLICK ===\n")

    page.goto("https://quotes.toscrape.com")

    # By CSS selector
    page.click(".tag-item a")
    print(f"  CSS selector '.tag-item a': {page.url}")
    page.go_back()

    # By text content — super convenient!
    page.click("a:text('Next')")
    print(f"  Text selector 'a:text(Next)': {page.url}")
    page.go_back()

    # By CSS attribute
    page.click("a[href='/page/2/']")
    print(f"  Attribute selector: {page.url}")
    page.go_back()

    # ====================================================================
    # Selenium comparison summary:
    #
    # Selenium:
    #   element = driver.find_element(By.ID, "username")
    #   element.clear()
    #   element.send_keys("admin")
    #   driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    #
    # Playwright:
    #   page.fill("#username", "admin")
    #   page.click("input[type='submit']")
    #
    # Playwright = fewer lines, auto-clear, auto-wait!
    # ====================================================================

    browser.close()
    print("\n✅ Click and fill complete!")