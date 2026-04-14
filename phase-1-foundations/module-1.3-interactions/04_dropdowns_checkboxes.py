"""
Module 1.3 — Navigation & Basic Interactions
File: 04_dropdowns_checkboxes.py
Description: Handling dropdowns, checkboxes, radio buttons, and other form elements
Date: 2026-04-09
Phase: 1 - Foundations
Playwright Docs: https://playwright.dev/python/docs/input#select-options
Practice site: https://the-internet.herokuapp.com
"""

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=800)

    # ====================================================================
    # DROPDOWNS — page.select_option()
    # Selenium: Select(element).select_by_value("2")
    # Playwright: page.select_option("select", value="2")
    # ====================================================================
    print("=== DROPDOWNS ===\n")

    page = browser.new_page()
    page.goto("https://the-internet.herokuapp.com/dropdown")

    # Select by value attribute: <option value="1">Option 1</option>
    page.select_option("#dropdown", value="1")
    print(f"  Selected by value='1'")

    # Select by visible label text
    page.select_option("#dropdown", label="Option 2")
    print(f"  Selected by label='Option 2'")

    # Select by index (0-based, index 0 is usually "Please select...")
    page.select_option("#dropdown", index=1)
    print(f"  Selected by index=1")

    # Get current selected value
    value = page.input_value("#dropdown")
    print(f"  Current value: {value}")

    page.close()

    # ====================================================================
    # CHECKBOXES — page.check() / page.uncheck()
    #
    # Selenium: element.click() — DANGEROUS! Toggles state.
    #   If already checked, click() UNCHECKS it!
    #
    # Playwright: page.check() — SMART! Only checks if not already checked.
    #   page.uncheck() — Only unchecks if not already unchecked.
    # ====================================================================
    print("\n=== CHECKBOXES ===\n")

    page = browser.new_page()
    page.goto("https://the-internet.herokuapp.com/checkboxes")

    # Check current state
    checkbox1 = page.locator("input[type='checkbox']").nth(0)
    checkbox2 = page.locator("input[type='checkbox']").nth(1)

    print(f"  Before:")
    print(f"    Checkbox 1 checked: {checkbox1.is_checked()}")
    print(f"    Checkbox 2 checked: {checkbox2.is_checked()}")

    # Check checkbox 1 (it's unchecked by default)
    checkbox1.check()
    print(f"\n  After checkbox1.check():")
    print(f"    Checkbox 1 checked: {checkbox1.is_checked()}")  # → True

    # Check it AGAIN — no-op! Already checked, won't toggle.
    checkbox1.check()
    print(f"\n  After checkbox1.check() AGAIN:")
    print(f"    Checkbox 1 checked: {checkbox1.is_checked()}")  # → still True!

    # Uncheck checkbox 2
    checkbox2.uncheck()
    print(f"\n  After checkbox2.uncheck():")
    print(f"    Checkbox 2 checked: {checkbox2.is_checked()}")  # → False

    page.close()

    # ====================================================================
    # HOVER — page.hover()
    # Selenium: ActionChains(driver).move_to_element(element).perform()
    # Playwright: page.hover(selector) — one line!
    # ====================================================================
    print("\n=== HOVER ===\n")

    page = browser.new_page()
    page.goto("https://the-internet.herokuapp.com/hovers")

    # Hover over user profiles to reveal hidden info
    profiles = page.locator(".figure")
    count = profiles.count()
    print(f"  Found {count} profiles")

    for i in range(count):
        profile = profiles.nth(i)
        profile.hover()

        # After hover, hidden text becomes visible
        name = profile.locator("h5").text_content()
        print(f"  Hovered profile {i + 1}: {name}")

    page.close()

    # ====================================================================
    # PUTTING IT ALL TOGETHER — Complete form interaction
    # Using a different practice site with more form elements
    # ====================================================================
    print("\n=== COMPLETE FORM DEMO ===\n")

    page = browser.new_page()
    page.goto("https://the-internet.herokuapp.com/login")

    # Fill text inputs
    page.fill("#username", "tomsmith")
    page.fill("#password", "SuperSecretPassword!")
    print("  Filled username and password")

    # Click login button
    page.click("button[type='submit']")
    print(f"  Clicked login → {page.url}")

    # Verify login success
    flash_message = page.locator("#flash").text_content()
    print(f"  Flash message: {flash_message.strip()}")

    page.close()

    # ====================================================================
    # SUMMARY
    # ====================================================================
    print("""
=== INTERACTION SUMMARY ===

Dropdowns:
  page.select_option(selector, value="...")    → by value attribute
  page.select_option(selector, label="...")    → by visible text
  page.select_option(selector, index=N)        → by position

Checkboxes:
  page.check(selector)     → check (smart: no-op if already checked)
  page.uncheck(selector)   → uncheck (smart: no-op if already unchecked)
  locator.is_checked()     → check current state

Hover:
  page.hover(selector)     → hover over element

Selenium comparison:
  Selenium checkbox: element.click() → TOGGLES (dangerous!)
  Playwright checkbox: page.check()  → only checks if needed (safe!)

  Selenium hover: ActionChains(driver).move_to_element(e).perform()
  Playwright hover: page.hover(selector)
""")

    browser.close()
    print("✅ Dropdowns & checkboxes complete!")