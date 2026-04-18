"""
Module 1.4 — Locators (The Modern Way)
File: 02_get_by_role.py
Description: get_by_role() — the #1 RECOMMENDED way to find elements
Date: 2026-04-09
Phase: 1 - Foundations
Playwright Docs: https://playwright.dev/python/docs/locators#locate-by-role
"""

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()

    # ====================================================================
    # WHY get_by_role()?
    #
    # It finds elements by their ARIA role — what the element IS,
    # not how it looks in HTML. This is:
    #   1. More readable — get_by_role("button") vs locator("input[type='submit']")
    #   2. More resilient — works even if HTML class/id changes
    #   3. Accessibility-first — same way screen readers find elements
    #
    # Selenium has NO equivalent for this!
    # ====================================================================

    # ====================================================================
    # FINDING BUTTONS
    # ====================================================================
    print("=== BUTTONS ===\n")

    page.goto("https://the-internet.herokuapp.com/login")

    # Find button by role + name (visible text or aria-label)
    login_btn = page.get_by_role("button", name="Login")
    print(f"  Found button: {login_btn.text_content()}")
    print(f"  Visible: {login_btn.is_visible()}")

    # Compare with CSS — which is more readable?
    # CSS:  page.locator("button[type='submit']")     ← what type is it?
    # Role: page.get_by_role("button", name="Login")  ← it's a Login button!

    # ====================================================================
    # FINDING LINKS
    # ====================================================================
    print("\n=== LINKS ===\n")

    page.goto("https://quotes.toscrape.com")

    # Find link by name
    login_link = page.get_by_role("link", name="Login")
    print(f"  Found link: '{login_link.text_content()}'")

    # Find "Next" link
    next_link = page.get_by_role("link", name="Next")
    print(f"  Found link: '{next_link.text_content()}'")
    next_link.click()
    print(f"  Clicked Next → {page.url}")

    # ====================================================================
    # FINDING HEADINGS
    # ====================================================================
    print("\n=== HEADINGS ===\n")

    page.goto("https://the-internet.herokuapp.com")

    # Find any heading
    main_heading = page.get_by_role("heading", name="Welcome to the-internet")
    print(f"  Main heading: {main_heading.text_content()}")

    # Find heading by level (h1, h2, h3...)
    h1 = page.get_by_role("heading", level=1)
    print(f"  H1: {h1.text_content()}")

    # ====================================================================
    # FINDING FORM ELEMENTS
    # ====================================================================
    print("\n=== FORM ELEMENTS ===\n")

    page.goto("https://the-internet.herokuapp.com/login")

    # Textbox — finds <input type="text"> and <textarea>
    username = page.get_by_role("textbox", name="Username")
    username.fill("tomsmith")
    print(f"  Filled textbox 'Username': {username.input_value()}")

    # ====================================================================
    # FINDING CHECKBOXES
    # ====================================================================
    print("\n=== CHECKBOXES ===\n")

    page.goto("https://the-internet.herokuapp.com/checkboxes")

    # Find all checkboxes
    checkboxes = page.get_by_role("checkbox")
    print(f"  Found {checkboxes.count()} checkboxes")

    # Filter by checked state
    # Note: this site's checkboxes don't have labels,
    # so we use nth() to pick specific ones
    first_cb = checkboxes.nth(0)
    first_cb.check()
    print(f"  Checkbox 1 checked: {first_cb.is_checked()}")

    # ====================================================================
    # THE name= PARAMETER — How it works
    # ====================================================================
    print("\n=== HOW name= WORKS ===\n")

    page.goto("https://the-internet.herokuapp.com/login")

    # name= matches against the element's "accessible name", which comes from:
    #   1. Visible text content: <button>Login</button> → name="Login"
    #   2. aria-label: <button aria-label="Close">X</button> → name="Close"
    #   3. <label>: <label for="user">Username</label> → name="Username"
    #   4. placeholder: <input placeholder="Enter email"> → name="Enter email"
    #   5. title attribute: <button title="Submit form"> → name="Submit form"

    print("  name= matches 'accessible name' which comes from:")
    print("    1. Visible text: <button>Login</button>")
    print("    2. aria-label: <button aria-label='Close'>X</button>")
    print("    3. <label>: <label for='user'>Username</label>")
    print("    4. placeholder: <input placeholder='Enter email'>")
    print("    5. title attribute: <button title='Submit'>")

    # exact= parameter — strict matching
    # By default, name= is substring match (case-insensitive)
    login_btn = page.get_by_role("button", name="login")  # matches "Login" (case-insensitive)
    print(f"\n  name='login' (case-insensitive): {login_btn.is_visible()}")

    # With exact=True — must match exactly
    login_btn_exact = page.get_by_role("button", name="Login", exact=True)
    print(f"  name='Login' (exact): {login_btn_exact.is_visible()}")

    # ====================================================================
    # COMMON ROLES REFERENCE
    # ====================================================================
    print("""
=== COMMON ARIA ROLES ===

Interactive:
  "button"      → <button>, <input type="submit/button/reset">
  "link"        → <a href="...">
  "textbox"     → <input type="text/email/password/search">, <textarea>
  "checkbox"    → <input type="checkbox">
  "radio"       → <input type="radio">
  "combobox"    → <select> (dropdown)
  "slider"      → <input type="range">

Structure:
  "heading"     → <h1> - <h6> (use level= to specify)
  "list"        → <ul>, <ol>
  "listitem"    → <li>
  "table"       → <table>
  "row"         → <tr>
  "cell"        → <td>
  "navigation"  → <nav>

Display:
  "img"         → <img>
  "dialog"      → <dialog>, modal popups
  "alert"       → alert messages
  "tab"         → tab elements
  "tabpanel"    → tab content panels
""")

    browser.close()
    print("✅ get_by_role() complete!")