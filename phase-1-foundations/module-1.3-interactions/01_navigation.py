"""
Module 1.3 — Navigation & Basic Interactions
File: 01_navigation.py
Description: Page navigation - goto, back, forward, reload, wait_until options
Date: 2026-04-13
Phase: 1 - Foundations
Playwright Docs: https://playwright.dev/python/docs/navigations
"""

from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()

    # ====================================================================
    # page.goto() — Navigate to a URL
    # ====================================================================
    print("=== NAVIGATION ===\n")

    # Basic navigation
    page.goto("https://quotes.toscrape.com")
    print(f"1. Navigated to: {page.url}")

    # Click a link to go to page 2
    page.click("a:text('Next')")
    print(f"2. Clicked Next: {page.url}")

    # ====================================================================
    # page.go_back() / page.go_forward() — Browser history
    # ====================================================================
    page.go_back()
    print(f"3. Went back: {page.url}")

    page.go_forward()
    print(f"4. Went forward: {page.url}")

    # ====================================================================
    # page.reload() — Refresh the page
    # ====================================================================
    page.reload()
    print(f"5. Reloaded: {page.url}")

    # ====================================================================
    # goto() with wait_until — Control WHEN navigation is "done"
    #
    # 'commit'          → fastest — server responded
    # 'domcontentloaded' → HTML is parsed, DOM ready
    # 'load'            → all resources loaded (DEFAULT)
    # 'networkidle'     → no requests for 500ms (slowest, safest)
    # ====================================================================
    print("\n=== WAIT_UNTIL OPTIONS ===\n")

    options = ['commit', 'domcontentloaded', 'load', 'networkidle']

    for option in options:
        start = time.time()
        page.goto("https://quotes.toscrape.com", wait_until=option)
        elapsed = time.time() - start
        print(f"  wait_until='{option}': {elapsed:.2f}s")

    # ====================================================================
    # Navigation info
    # ====================================================================
    print("\n=== PAGE INFO ===\n")
    page.goto("https://books.toscrape.com")
    print(f"  URL: {page.url}")
    print(f"  Title: {page.title()}")
    print(f"  Content length: {len(page.content())} characters")

    browser.close()
    print("\n✅ Navigation complete!")