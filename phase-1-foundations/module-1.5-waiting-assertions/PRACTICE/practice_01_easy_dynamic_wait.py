"""
Module 1.5 — Practice 1 (Easy)
File: practice_01_easy_dynamic_wait.py
Date: 2026-04-09

TASK:
=====
Demonstrate Playwright's auto-wait with dynamic loading pages.

1. Buka https://the-internet.herokuapp.com/dynamic_loading/1
   (This page has a HIDDEN element that becomes visible after clicking Start)
2. Click the "Start" button
3. Extract the text that appears after loading (should be "Hello World!")
4. Print the result
5. Assert the result equals "Hello World!" using expect()

6. Buka https://the-internet.herokuapp.com/dynamic_loading/2
   (This page CREATES an element after clicking Start — it doesn't exist in DOM initially)
7. Click "Start"
8. Extract the text
9. Assert the text using expect()

10. Print summary:
    Test 1 (hidden element): Hello World! ✅
    Test 2 (rendered element): Hello World! ✅

REQUIREMENTS:
- Use get_by_role() to find and click the Start button
- Use expect() to verify results (NOT Python assert)
- Use locator chaining for extracting text (#finish h4)
- NO wait_for_timeout or time.sleep — let auto-wait handle everything

HINTS:
- Start button: page.get_by_role("button", name="Start")
- Result text: page.locator("#finish h4")
- expect(locator).to_have_text("Hello World!")
"""

# Write your code below this line
# ============================================================================

from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    
    page.goto("https://the-internet.herokuapp.com/dynamic_loading/1")
    start_button = page.get_by_role("button", name="Start")
    start_button.click()
    text_hello = page.locator("#finish h4")
    expect(text_hello).to_be_visible()
    expect(text_hello).to_have_text("Hello World!")
    hasil1 = text_hello.text_content()
    print(f"Element {hasil1} is visible!")
    
    
    page.goto("https://the-internet.herokuapp.com/dynamic_loading/2")
    tombol_start = page.get_by_role("button", name="Start")
    tombol_start.click()
    text_halamankedua = page.locator("#finish h4")
    expect(text_halamankedua).to_be_visible()
    expect(text_halamankedua).to_have_text("Hello World!")
    hasil2 = text_halamankedua.text_content()
    print(f"Element {hasil2} is visible on page 2!")


    print("===== SUMMARY =====")
    print(f"Test 1 (hidden element): {hasil1}")
    print(f"Test 2 (rendered element): {hasil2}")
    browser.close()