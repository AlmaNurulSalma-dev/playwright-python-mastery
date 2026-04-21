"""
Module 1.5 — Auto-Waiting & Assertions
File: 01_auto_wait.py
Description: How Playwright auto-waits for elements before every action
Date: 2026-04-20
Phase: 1 - Foundations
Playwright Docs: https://playwright.dev/python/docs/actionability
"""

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()

    # ====================================================================
    # AUTO-WAIT IN ACTION
    #
    # Playwright automatically waits for elements before EVERY action.
    # You DON'T need to write wait code — it's built in!
    # ====================================================================
    print("=== AUTO-WAIT DEMO ===\n")

    page.goto("https://the-internet.herokuapp.com/dynamic_loading/1")
    print(f"  Page: {page.url}")
    print("  This page has a hidden element that appears after clicking Start")

    # Click the start button — Playwright auto-waits for it to be clickable
    page.get_by_role("button", name="Start").click()
    print("  Clicked Start — element is loading...")

    # The text "Hello World!" appears after a few seconds
    # Playwright auto-waits for it to be visible before getting text!
    result = page.locator("#finish h4").text_content()
    print(f"  Result: {result}")
    print("  ✅ Playwright waited automatically — no sleep() needed!")

    # ====================================================================
    # ANOTHER EXAMPLE — Dynamic loading (element rendered after)
    # ====================================================================
    print("\n=== DYNAMIC LOADING (RENDERED AFTER) ===\n")

    page.goto("https://the-internet.herokuapp.com/dynamic_loading/2")
    print("  This page CREATES the element after clicking Start (not just show)")

    page.get_by_role("button", name="Start").click()
    print("  Clicked Start — waiting for element to be created...")

    result = page.locator("#finish h4").text_content()
    print(f"  Result: {result}")
    print("  ✅ Auto-waited for element to EXIST and have text!")

    # ====================================================================
    # WHAT SELENIUM WOULD NEED
    # ====================================================================
    print("""
=== SELENIUM COMPARISON ===

Selenium for the same task:
  from selenium.webdriver.support.ui import WebDriverWait
  from selenium.webdriver.support import expected_conditions as EC
  from selenium.webdriver.common.by import By

  driver.find_element(By.CSS_SELECTOR, "button").click()
  
  element = WebDriverWait(driver, 10).until(
      EC.visibility_of_element_located((By.CSS_SELECTOR, "#finish h4"))
  )
  print(element.text)

  → 3 extra imports + 3 extra lines just for waiting!

Playwright:
  page.click("button")
  result = page.locator("#finish h4").text_content()

  → 0 extra imports, 0 extra lines. Just works!
""")

    # ====================================================================
    # AUTO-WAIT FOR FORM INTERACTIONS
    # ====================================================================
    print("=== AUTO-WAIT WITH FORMS ===\n")

    page.goto("https://the-internet.herokuapp.com/login")

    # Each of these auto-waits for the element to be:
    # visible + stable + enabled + editable (for inputs)
    page.get_by_label("Username").fill("tomsmith")          # waits for input
    page.get_by_label("Password").fill("SuperSecretPassword!")  # waits for input
    page.get_by_role("button", name="Login").click()         # waits for button

    print(f"  Logged in → {page.url}")
    print("  ✅ Every action auto-waited — no explicit waits needed!")

    # ====================================================================
    # WHAT AUTO-WAIT CHECKS (Actionability)
    # ====================================================================
    print("""
=== ACTIONABILITY CHECKS (before every action) ===

For click():
  ✓ Element is visible (not hidden)
  ✓ Element is stable (not animating)
  ✓ Element is enabled (not disabled)
  ✓ Element receives events (not blocked by overlay)

For fill() / type():
  ✓ All of the above, PLUS:
  ✓ Element is editable (accepts input)

For check() / uncheck():
  ✓ All of the above, PLUS:
  ✓ Element is a checkbox or radio button

These checks happen AUTOMATICALLY before every action.
If any check fails, Playwright RETRIES until timeout.
""")

    browser.close()
    print("✅ Auto-wait demo complete!")