"""
Module 1.3 — Navigation & Basic Interactions
File: 03_keyboard_actions.py
Description: Keyboard actions - press(), shortcuts, and the keyboard object
Date: 2026-04-13
Phase: 1 - Foundations
Playwright Docs: https://playwright.dev/python/docs/input#keys-and-shortcuts
"""

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=800)
    page = browser.new_page()

    # ====================================================================
    # page.press() — Press a key on a focused element
    # Selenium equivalent: ActionChains(driver).send_keys(Keys.ENTER).perform()
    # Playwright: just page.press(selector, key) — so much simpler!
    # ====================================================================
    print("=== PRESS KEY ON ELEMENT ===\n")

    page.goto("https://quotes.toscrape.com/login")

    # Fill form then press Enter instead of clicking submit
    page.fill("input#username", "admin")
    page.fill("input#password", "admin")

    # Press Enter on the password field — submits the form!
    page.press("input#password", "Enter")
    print(f"  Pressed Enter to submit → {page.url}")

    # ====================================================================
    # PRESS TAB — Navigate between form fields
    # ====================================================================
    print("\n=== TAB NAVIGATION ===\n")

    page.goto("https://quotes.toscrape.com/login")

    # Click username field to focus it
    page.click("input#username")
    page.type("input#username", "admin", delay=50)

    # Press Tab to move to password field
    page.press("input#username", "Tab")
    print("  Tabbed from username to password")

    # Now password field is focused — type directly
    page.type("input#password", "admin", delay=50)
    print("  Typed password after Tab")

    page.press("input#password", "Enter")
    print(f"  Enter to submit → {page.url}")

    # ====================================================================
    # KEYBOARD SHORTCUTS — Select all, Copy, Paste
    # ====================================================================
    print("\n=== KEYBOARD SHORTCUTS ===\n")

    page.goto("https://quotes.toscrape.com/login")

    # Type something first
    page.fill("input#username", "hello_world")

    # Select all text in the input (Ctrl+A)
    page.press("input#username", "Control+a")
    print("  Ctrl+A: Selected all text")

    # Delete selected text
    page.press("input#username", "Backspace")
    print("  Backspace: Deleted selected text")

    # Type new text
    page.type("input#username", "new_text", delay=50)
    print("  Typed new text")

    # ====================================================================
    # page.keyboard — Lower-level keyboard control
    #
    # page.press() works on a SPECIFIC element
    # page.keyboard works GLOBALLY — no selector needed
    # ====================================================================
    print("\n=== GLOBAL KEYBOARD (page.keyboard) ===\n")

    page.goto("https://quotes.toscrape.com/login")
    page.click("input#username")

    # keyboard.type() — type text globally (wherever focus is)
    page.keyboard.type("typed_via_keyboard", delay=50)
    print("  keyboard.type(): Typed into focused element")

    # keyboard.press() — press key globally
    page.keyboard.press("Tab")
    print("  keyboard.press('Tab'): Moved to next field")

    page.keyboard.type("secret123", delay=50)
    print("  keyboard.type(): Typed password")

    # keyboard.down() and keyboard.up() — hold and release keys
    # Useful for: key combinations, holding Shift while clicking, etc.
    page.keyboard.press("Enter")
    print(f"  keyboard.press('Enter'): Submitted → {page.url}")

    # ====================================================================
    # HOLD KEY DOWN — keyboard.down() / keyboard.up()
    # ====================================================================
    print("\n=== HOLD KEY (down/up) ===\n")

    page.goto("https://quotes.toscrape.com/login")
    page.click("input#username")

    # Hold Shift → type → Release Shift = UPPERCASE
    page.keyboard.down("Shift")
    page.keyboard.type("hello")       # → "HELLO" because Shift is held
    page.keyboard.up("Shift")
    page.keyboard.type(" world")      # → " world" normal case

    # Result in input: "HELLO world"
    value = page.input_value("input#username")
    print(f"  Shift held + type: '{value}'")

    # ====================================================================
    # page.press() vs page.keyboard.press() — When to use which?
    # ====================================================================
    print("""
=== COMPARISON ===

page.press(selector, key):
  ✅ Targets specific element
  ✅ Auto-waits for element to be ready
  ✅ Use 90% of the time

page.keyboard.press(key):
  ✅ Global — no selector needed
  ✅ Works wherever focus currently is
  ✅ Has .down() and .up() for holding keys
  ⚠️ No auto-wait — you must ensure focus is correct

page.keyboard.type(text):
  ✅ Types globally, character by character
  ✅ Fires all key events
  ⚠️ Different from page.type() — no selector!
""")

    browser.close()
    print("✅ Keyboard actions complete!")