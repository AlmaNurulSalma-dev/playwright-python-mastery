"""
Module 1.4 — Locators (The Modern Way)
File: 03_get_by_text_label.py
Description: get_by_text, get_by_label, get_by_placeholder, and other user-facing locators
Date: 2026-04-09
Phase: 1 - Foundations
Playwright Docs: https://playwright.dev/python/docs/locators
"""

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()

    # ====================================================================
    # get_by_text() — Find by VISIBLE TEXT
    # Super intuitive — "find the thing that says X"
    # ====================================================================
    print("=== get_by_text() ===\n")

    page.goto("https://quotes.toscrape.com")

    # Substring match (default)
    einstein = page.get_by_text("Einstein")
    print(f"  get_by_text('Einstein'): {einstein.count()} match(es)")

    # Exact match — use exact=True
    einstein_exact = page.get_by_text("Einstein", exact=True)
    print(f"  get_by_text('Einstein', exact=True): {einstein_exact.count()} match(es)")

    # Regex match
    import re
    starts_with_a = page.get_by_text(re.compile(r"^A"))
    print(f"  Regex starts with 'A': {starts_with_a.count()} match(es)")
    
# r"^"        # starts with
# r"$"        # ends with
# r"."        # any single character
# r"*"        # 0 or more of previous
# r"+"        # 1 or more of previous
# r"?"        # 0 or 1 of previous (optional)
# r"\d"       # any digit (0-9)
# r"\w"       # any word character (letters, digits, underscore)
# r"\s"       # any whitespace (space, tab, newline)
# r"{3}"      # exactly 3 of previous
# r"{2,5}"    # 2 to 5 of previous
# r"[abc]"    # any of: a, b, or c
# r"[A-Z]"    # any uppercase letter
# r"(a|b)"    # a OR b

    # ====================================================================
    # get_by_label() — Find form elements by their <label>
    # Super useful for forms!
    # ====================================================================
    print("\n=== get_by_label() ===\n")

    page.goto("https://the-internet.herokuapp.com/login")

    # HTML: <label for="username">Username</label>
    #       <input id="username" type="text">
    #
    # get_by_label finds the INPUT, not the label!
    username_input = page.get_by_label("Username")
    username_input.fill("tomsmith")
    print(f"  Filled by label 'Username': {username_input.input_value()}")

    password_input = page.get_by_label("Password")
    password_input.fill("SuperSecretPassword!")
    print(f"  Filled by label 'Password': {password_input.input_value()}")

    # ====================================================================
    # get_by_placeholder() — Find by placeholder text
    # ====================================================================
    print("\n=== get_by_placeholder() ===\n")

    page.goto("https://scrapethissite.com/pages/forms/")

    # HTML: <input placeholder="Search by Team Name">
    search_input = page.get_by_placeholder("Search by Team Name")
    if search_input.count() > 0:
        search_input.fill("Montreal")
        print(f"  Filled by placeholder: {search_input.input_value()}")
    else:
        print("  Placeholder not found on this page")

    # ====================================================================
    # get_by_alt_text() — Find images by alt text
    # ====================================================================
    print("\n=== get_by_alt_text() ===\n")

    page.goto("https://the-internet.herokuapp.com/")

    # Most images here don't have alt text, but demonstrating syntax:
    # HTML: <img alt="Company Logo" src="logo.png">
    # page.get_by_alt_text("Company Logo")
    print("  Syntax: page.get_by_alt_text('Company Logo')")
    print("  Finds: <img alt='Company Logo' src='logo.png'>")

    # ====================================================================
    # get_by_title() — Find by title attribute (tooltip on hover)
    # ====================================================================
    print("\n=== get_by_title() ===\n")

    # HTML: <button title="Click to submit">Submit</button>
    # page.get_by_title("Click to submit")
    print("  Syntax: page.get_by_title('Click to submit')")
    print("  Finds: <button title='Click to submit'>")

    # ====================================================================
    # get_by_test_id() — Find by data-testid attribute
    # Best for developer-controlled test stability
    # ====================================================================
    print("\n=== get_by_test_id() ===\n")

    # HTML: <button data-testid="login-submit">Login</button>
    # page.get_by_test_id("login-submit")
    print("  Syntax: page.get_by_test_id('login-submit')")
    print("  Finds: <button data-testid='login-submit'>")
    print("  BEST for: apps where developer adds data-testid attributes")
    print("            Super stable — not affected by CSS/class changes")

    # ====================================================================
    # COMPLETE LOGIN USING get_by_ METHODS
    # ====================================================================
    print("\n=== REAL EXAMPLE: Login with get_by_ methods ===\n")

    page.goto("https://the-internet.herokuapp.com/login")

    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("SuperSecretPassword!")
    page.get_by_role("button", name="Login").click()

    print(f"  Logged in → {page.url}")

    flash = page.locator("#flash").text_content().strip()
    print(f"  Flash message: {flash[:50]}...")

    # ====================================================================
    # COMPARISON: Same task, different locator styles
    # ====================================================================
    print("""
=== COMPARING LOCATOR STYLES ===

Task: Click the "Login" button

CSS selector:
  page.locator("button[type='submit']").click()
  ⚠️ Fragile — breaks if button type changes

Text selector:
  page.locator("button:text('Login')").click()
  ⚠️ Better, but still CSS-based

get_by_text():
  page.get_by_text("Login").click()
  ⚠️ Matches LINK too if there's <a>Login</a>

get_by_role() + name:  ⭐ BEST
  page.get_by_role("button", name="Login").click()
  ✅ Matches only BUTTONS named "Login"
  ✅ Survives HTML/CSS changes
  ✅ Most readable
""")

    # ====================================================================
    # PRIORITY ORDER (Playwright's official recommendation)
    # ====================================================================
    print("""
=== LOCATOR PRIORITY (USE IN THIS ORDER) ===

1. get_by_role()         ⭐ BEST — accessibility-first
2. get_by_label()        ⭐ For form inputs
3. get_by_placeholder()  For inputs without labels
4. get_by_text()         For non-interactive text
5. get_by_alt_text()     For images
6. get_by_title()        For title attributes
7. get_by_test_id()      When developer adds data-testid
8. locator() with CSS    Last resort — fragile
9. locator() with XPath  Avoid unless absolutely needed
""")

    browser.close()
    print("✅ get_by_* methods complete!")