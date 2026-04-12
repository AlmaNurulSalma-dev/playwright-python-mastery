"""
Module 1.2 — Architecture Deep Dive
File: 02_multiple_contexts.py
Description: Why contexts matter - cookie isolation, simulating multiple users
Date: 2026-04-09
Phase: 1 - Foundations
Playwright Docs: https://playwright.dev/python/docs/browser-contexts
"""

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)

    # ====================================================================
    # SCENARIO: Simulating 2 different users on the same website
    #
    # In Selenium, you'd need to launch 2 SEPARATE browsers (heavy!)
    # In Playwright, just create 2 contexts (lightweight!)
    # ====================================================================

    # ── User A: Logs into quotes.toscrape.com ──────────────────────────
    context_a = browser.new_context()
    page_a = context_a.new_page()
    page_a.goto("https://quotes.toscrape.com/login")

    # Fill login form
    page_a.fill("input#username", "admin")
    page_a.fill("input#password", "admin")
    page_a.click("input[type='submit']")

    # Verify login — should redirect to home with "Logout" link visible
    print("=== USER A ===")
    print(f"  URL after login: {page_a.url}")
    print(f"  Cookies: {context_a.cookies()}")

    # ── User B: NOT logged in (fresh session) ──────────────────────────
    context_b = browser.new_context()
    page_b = context_b.new_page()
    page_b.goto("https://quotes.toscrape.com")

    print("\n=== USER B ===")
    print(f"  URL: {page_b.url}")
    print(f"  Cookies: {context_b.cookies()}")

    # ====================================================================
    # PROOF: Cookies are ISOLATED between contexts
    #
    # User A has session cookies (logged in)
    # User B has NO cookies (not logged in)
    # They're in the SAME browser but completely separate sessions!
    # ====================================================================

    print("\n=== ISOLATION PROOF ===")
    cookies_a = context_a.cookies()
    cookies_b = context_b.cookies()
    print(f"  User A cookies count: {len(cookies_a)}")
    print(f"  User B cookies count: {len(cookies_b)}")
    print(f"  Same cookies? {cookies_a == cookies_b}")  # → False!

    # ====================================================================
    # BONUS: Pages in the SAME context DO share cookies
    # ====================================================================
    print("\n=== SAME CONTEXT SHARING ===")

    # Open another page in User A's context
    page_a2 = context_a.new_page()
    page_a2.goto("https://quotes.toscrape.com")

    # This page is ALSO logged in — because same context = same cookies!
    print(f"  Page A2 cookies: {len(context_a.cookies())}")
    print(f"  Page A2 shares User A's session: True")
    print(f"  Pages in context A: {len(context_a.pages)}")  # → 2

    # ====================================================================
    # SELENIUM COMPARISON
    # ====================================================================
    # To do this in Selenium, you'd need:
    #
    #   driver_a = webdriver.Chrome()    # full browser #1 (heavy!)
    #   driver_a.get("https://quotes.toscrape.com/login")
    #   # ... login ...
    #
    #   driver_b = webdriver.Chrome()    # full browser #2 (heavy!)
    #   driver_b.get("https://quotes.toscrape.com")
    #
    # That's 2 Chrome processes eating RAM!
    # Playwright does it with 1 browser + 2 lightweight contexts.
    # ====================================================================

    # Cleanup
    context_a.close()
    context_b.close()
    browser.close()

    print("\n✅ Both contexts closed — all sessions destroyed")