"""
Module 2.3 — Multiple Pages & Contexts
File: 02_session_state.py
Description: Saving login sessions, cookie management, and reusing auth state
Date: 2026-04-21
Phase: 2 - Intermediate
Playwright Docs: https://playwright.dev/python/docs/auth
"""

from playwright.sync_api import sync_playwright, expect
import json
import os

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)

    # ====================================================================
    # STEP 1: Login and save session state
    # ====================================================================
    print("=== STEP 1: Login & Save Session ===\n")

    context1 = browser.new_context()
    page = context1.new_page()
    page.goto("https://quotes.toscrape.com/login")

    # Login
    page.fill("input#username", "admin")
    page.fill("input#password", "admin")
    page.click("input[type='submit']")

    # Verify login
    expect(page).to_have_url("https://quotes.toscrape.com/")
    print(f"  Logged in! URL: {page.url}")

    # Check cookies BEFORE saving
    cookies = context1.cookies()
    print(f"  Cookies after login: {len(cookies)}")
    for cookie in cookies:
        print(f"    {cookie['name']}: {cookie['value'][:30]}...")

    # SAVE session state — cookies + localStorage to JSON file
    state_path = "output/auth_state.json"
    os.makedirs("output", exist_ok=True)
    context1.storage_state(path=state_path)
    print(f"\n  ✅ Session saved to {state_path}")

    context1.close()

    # ====================================================================
    # STEP 2: Reuse saved session — skip login!
    # ====================================================================
    print("\n=== STEP 2: Reuse Saved Session ===\n")

    # Create NEW context with saved state — already logged in!
    context2 = browser.new_context(storage_state=state_path)
    page2 = context2.new_page()

    # Go directly to the site — no login needed!
    page2.goto("https://quotes.toscrape.com")

    # Verify we're logged in by checking for "Logout" link
    logout_link = page2.get_by_role("link", name="Logout")
    expect(logout_link).to_be_visible()
    print(f"  ✅ Logged in WITHOUT typing credentials!")
    print(f"  URL: {page2.url}")
    print(f"  Logout link visible: {logout_link.is_visible()}")

    # Check cookies — they were loaded from file!
    cookies2 = context2.cookies()
    print(f"  Cookies loaded: {len(cookies2)}")

    context2.close()

    # ====================================================================
    # STEP 3: Cookie management — manual control
    # ====================================================================
    print("\n=== STEP 3: Cookie Management ===\n")

    context3 = browser.new_context()
    page3 = context3.new_page()
    page3.goto("https://quotes.toscrape.com")

    # Check cookies — fresh context, should be minimal
    cookies_before = context3.cookies()
    print(f"  Cookies before: {len(cookies_before)}")

    # Add cookies manually
    context3.add_cookies([
        {
            "name": "my_custom_cookie",
            "value": "hello_playwright",
            "domain": "quotes.toscrape.com",
            "path": "/",
        },
        {
            "name": "tracking_id",
            "value": "abc123xyz",
            "domain": "quotes.toscrape.com",
            "path": "/",
        },
    ])

    cookies_after = context3.cookies()
    print(f"  Cookies after adding: {len(cookies_after)}")
    for cookie in cookies_after:
        print(f"    {cookie['name']}: {cookie['value']}")

    # Filter cookies by URL
    toscrape_cookies = context3.cookies("https://quotes.toscrape.com")
    print(f"\n  Cookies for toscrape: {len(toscrape_cookies)}")

    # Clear all cookies
    context3.clear_cookies()
    cookies_cleared = context3.cookies()
    print(f"  Cookies after clear: {len(cookies_cleared)}")
    print("  ✅ All cookies removed!")

    context3.close()

    # ====================================================================
    # STEP 4: Multiple users simultaneously
    # ====================================================================
    print("\n=== STEP 4: Multiple Users ===\n")

    # User A — logged in (using saved state)
    context_a = browser.new_context(storage_state=state_path)
    page_a = context_a.new_page()
    page_a.goto("https://quotes.toscrape.com")

    # User B — not logged in (fresh context)
    context_b = browser.new_context()
    page_b = context_b.new_page()
    page_b.goto("https://quotes.toscrape.com")

    # Compare
    a_has_logout = page_a.get_by_role("link", name="Logout").count() > 0
    b_has_logout = page_b.get_by_role("link", name="Logout").count() > 0

    print(f"  User A logged in: {a_has_logout}")
    print(f"  User B logged in: {b_has_logout}")
    print(f"  Isolated? {a_has_logout != b_has_logout}")
    print("  ✅ Same browser, different sessions!")

    # Check cookies are different
    cookies_a = context_a.cookies()
    cookies_b = context_b.cookies()
    print(f"\n  User A cookies: {len(cookies_a)}")
    print(f"  User B cookies: {len(cookies_b)}")
    print(f"  Same cookies? {cookies_a == cookies_b}")

    context_a.close()
    context_b.close()

    # ====================================================================
    # WHAT THE SAVED STATE FILE LOOKS LIKE
    # ====================================================================
    print("\n=== SAVED STATE FILE ===\n")

    if os.path.exists(state_path):
        with open(state_path, "r") as f:
            state_data = json.load(f)
        print(f"  File: {state_path}")
        print(f"  Keys: {list(state_data.keys())}")
        print(f"  Cookies count: {len(state_data.get('cookies', []))}")
        print(f"  Origins count: {len(state_data.get('origins', []))}")

    # ====================================================================
    # USE CASES FOR SESSION STATE
    # ====================================================================
    print("""
=== WHEN TO USE SESSION STATE ===

1. Skip login in tests — login once, save, reuse in all tests
2. Resume scraping — save session, continue later without re-login
3. Multiple environments — save prod login, save staging login, switch easily
4. Avoid rate limiting — login normally once, reuse to avoid suspicious repeated logins
5. Debugging — save state when error occurs, reload to reproduce exact session
""")

    browser.close()
    print("✅ Session state complete!")