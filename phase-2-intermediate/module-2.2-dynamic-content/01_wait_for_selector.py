"""
Module 2.2 — Handling Dynamic Content
File: 01_wait_for_selector.py
Description: wait_for_selector() — waiting for elements to appear, disappear, or change state
Date: 2026-04-21
Phase: 2 - Intermediate
Playwright Docs: https://playwright.dev/python/docs/api/class-page#page-wait-for-selector
"""

from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()

    # ====================================================================
    # SCENARIO 1: Element hidden, then becomes visible
    # the-internet.herokuapp.com/dynamic_loading/1
    # Element exists in DOM but is hidden, revealed after clicking Start
    # ====================================================================
    print("=== SCENARIO 1: Hidden → Visible ===\n")

    page.goto("https://the-internet.herokuapp.com/dynamic_loading/1")

    page.get_by_role("button", name="Start").click()

    # wait_for_selector with state="visible" — wait until element is SEEN
    element = page.wait_for_selector("#finish h4", state="visible")
    text = element.text_content()
    print(f"  Result: {text}")
    print("  ✅ Waited for hidden element to become visible")

    # ====================================================================
    # SCENARIO 2: Element doesn't exist, then gets created
    # the-internet.herokuapp.com/dynamic_loading/2
    # Element is NOT in DOM, gets rendered after clicking Start
    # ====================================================================
    print("\n=== SCENARIO 2: Not in DOM → Created ===\n")

    page.goto("https://the-internet.herokuapp.com/dynamic_loading/2")

    page.get_by_role("button", name="Start").click()

    # state="attached" (default) — wait until element EXISTS in DOM
    element = page.wait_for_selector("#finish h4", state="attached")
    text = element.text_content()
    print(f"  Result: {text}")
    print("  ✅ Waited for element to be created in DOM")

    # ====================================================================
    # SCENARIO 3: Wait for loading spinner to DISAPPEAR
    # ====================================================================
    print("\n=== SCENARIO 3: Wait for spinner to disappear ===\n")

    page.goto("https://the-internet.herokuapp.com/dynamic_loading/1")

    page.get_by_role("button", name="Start").click()

    # Wait for the loading indicator to become hidden
    page.wait_for_selector("#loading", state="hidden")
    print("  ✅ Loading spinner disappeared!")

    # Now safe to extract data
    result = page.locator("#finish h4").text_content()
    print(f"  Result after spinner gone: {result}")

    # ====================================================================
    # SCENARIO 4: wait_for_selector with timeout
    # ====================================================================
    print("\n=== SCENARIO 4: Custom timeout ===\n")

    page.goto("https://the-internet.herokuapp.com/dynamic_loading/2")
    page.get_by_role("button", name="Start").click()

    try:
        # Wait max 2 seconds — might not be enough!
        element = page.wait_for_selector("#finish h4", state="visible", timeout=2000)
        print(f"  Result: {element.text_content()}")
    except Exception as e:
        print(f"  ❌ Timeout after 2s: {str(e)[:80]}...")

    # Try again with longer timeout
    page.goto("https://the-internet.herokuapp.com/dynamic_loading/2")
    page.get_by_role("button", name="Start").click()

    element = page.wait_for_selector("#finish h4", state="visible", timeout=10000)
    print(f"  ✅ Result with 10s timeout: {element.text_content()}")

    # ====================================================================
    # wait_for_selector STATES REFERENCE
    # ====================================================================
    print("""
=== wait_for_selector STATES ===

state="attached"  (default)
  → Wait until element EXISTS in DOM
  → Element might be hidden — doesn't matter
  → Use: waiting for JS to create an element

state="detached"
  → Wait until element is REMOVED from DOM
  → Use: waiting for modal/popup to fully close

state="visible"
  → Wait until element is VISIBLE on screen
  → Must exist AND not be hidden
  → Use: waiting for content to show after loading

state="hidden"
  → Wait until element is HIDDEN or REMOVED
  → Use: waiting for spinner/loader to disappear
""")

    # ====================================================================
    # wait_for_selector vs auto-wait vs expect
    # ====================================================================
    print("""
=== WHEN TO USE WHICH ===

Auto-wait (built into every action):
  page.click("#button")
  page.locator("#result").text_content()
  → Use: most cases! Actions auto-wait for element.

wait_for_selector():
  page.wait_for_selector("#result", state="visible")
  → Use: when you need to wait for state CHANGE
  → Element hidden → visible, or element created/removed

expect():
  expect(locator).to_be_visible()
  → Use: assertions with auto-retry
  → Verifying state, not waiting for action

All three wait — but for different purposes!
""")

    browser.close()
    print("✅ wait_for_selector complete!")