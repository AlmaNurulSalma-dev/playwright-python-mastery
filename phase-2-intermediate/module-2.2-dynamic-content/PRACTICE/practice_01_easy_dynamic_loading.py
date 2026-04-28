"""
Module 2.2 — Practice 1 (Easy)
File: practice_01_easy_dynamic_loading.py
Date: 2026-04-21

TASK:
=====
Test ALL 4 wait_for_selector states using the-internet.herokuapp.com.

1. VISIBLE STATE — https://the-internet.herokuapp.com/dynamic_loading/1
   a. Click Start
   b. Wait for loading spinner to become HIDDEN (state="hidden")
   c. Wait for result to become VISIBLE (state="visible")
   d. Extract and print the result text

2. ATTACHED STATE — https://the-internet.herokuapp.com/dynamic_loading/2
   a. Click Start
   b. Wait for result element to be ATTACHED (state="attached")
   c. Then wait for it to be VISIBLE
   d. Extract and print the result text

3. Print summary:
   Test 1 (hidden→visible): [result text] ✅
   Test 2 (attached→visible): [result text] ✅

REQUIREMENTS:
- Use get_by_role("button", name="Start") for clicking
- Use wait_for_selector() with explicit state= parameter
- Use BOTH state="hidden" (wait for spinner) and state="visible" (wait for result)
- Extract text using .text_content() from the wait_for_selector return value
- NO wait_for_timeout or time.sleep!

HINTS:
- Spinner selector: "#loading"
- Result selector: "#finish h4"
- wait_for_selector returns an ElementHandle — you can call .text_content() on it
"""

# Write your code below this line
# ============================================================================

from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=300)
    page = browser.new_page()
    
    # Test Visible State
    page.goto("https://the-internet.herokuapp.com/dynamic_loading/1")
    with page.expect_response("**/dynamic_loading/1") as response_info:
        page.get_by_role("button", name="Start").click()
        page.wait_for_selector("#loading", state="hidden")
        element1 = page.wait_for_selector("#finish h4", state="visible")
        result1 = element1.text_content()
    response = response_info.value
    print(f"  Response URL: {response.url}")
    print(f"  Status: {response.status}")
    print(f"  Result: {result1}")
    print("  ✅ Caught the API response!")
    
    # Test Attached State
    page.goto("https://the-internet.herokuapp.com/dynamic_loading/2")
    with page.expect_response("**/dynamic_loading/2") as response_info:
        page.get_by_role("button", name="Start").click()
        page.wait_for_selector("#finish h4", state="attached")
        element2 =page.wait_for_selector("#finish h4", state="visible")
        result2 = element2.text_content()
    response = response_info.value
    print(f"  Response URL: {response.url}")
    print(f"  Status: {response.status}")
    print(f"  Result: {result2}")
    print("  ✅ Caught the API response!")
    
    # Print Summary
    print("\n=== Summary ===")
    print(f"Test 1 (hidden → visible): {result1}")
    print(f"Test 2 (not in DOM → created): {result2}")