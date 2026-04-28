"""
Module 2.2 — Practice 2 (Medium)
File: practice_02_medium_multi_wait.py
Date: 2026-04-21

TASK:
=====
Build a "Wait Strategy Tester" that demonstrates 4 different wait methods
on the-internet.herokuapp.com.

TEST A — wait_for_selector:
1. Buka https://the-internet.herokuapp.com/dynamic_loading/2
2. Click Start
3. Use wait_for_selector("#finish h4", state="visible")
4. Print result text

TEST B — wait_for_url:
1. Buka https://the-internet.herokuapp.com/login
2. Fill username "tomsmith", password "SuperSecretPassword!"
3. Click Login button
4. Use wait_for_url("**/secure") to confirm redirect
5. Print current URL

TEST C — wait_for_function:
1. Buka https://quotes.toscrape.com
2. Use wait_for_function() to wait until page has 10 quotes:
   "document.querySelectorAll('.quote').length >= 10"
3. Count and print number of quotes

TEST D — expect_response:
1. Buka https://the-internet.herokuapp.com/dynamic_loading/2
2. Use expect_response() to catch the response when Start is clicked
3. Print response URL and status code

Print summary:
   ===== WAIT STRATEGY TESTER =====
   Test A (wait_for_selector): "Hello World!" ✅
   Test B (wait_for_url): /secure ✅
   Test C (wait_for_function): 10 quotes ✅
   Test D (expect_response): status 200 ✅

REQUIREMENTS:
- One browser, one page (reuse)
- Use 4 DIFFERENT wait methods (one per test)
- Use get_by_role() for buttons
- Use get_by_label() for form inputs
- NO wait_for_timeout!

HINTS:
- wait_for_selector returns ElementHandle
- wait_for_url accepts glob patterns with **
- wait_for_function takes JS expression string
- expect_response needs with statement
"""

# Write your code below this line
# ============================================================================

from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=300)
    page = browser.new_page()
    
    # Test A
    page.goto("https://the-internet.herokuapp.com/dynamic_loading/2")
    page.get_by_role("button", name="Start").click()
    element = page.wait_for_selector("#finish h4", state="visible")
    print(f"Test A Result: {element.text_content()}")
    
    # Test B
    page.goto("https://the-internet.herokuapp.com/login")
    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("SuperSecretPassword!")
    page.get_by_role("button", name="Login").click()
    page.wait_for_url("**/secure")
    test_b_url = page.url
    print(f"Test B URL: {test_b_url}")
    
    # Test C
    page.goto("https://quotes.toscrape.com")
    page.wait_for_function("document.querySelectorAll('.quote').length >= 10")
    print(f"Test C Quotes: {page.locator('.quote').count()}")
    
    # Test D
    page.goto("https://the-internet.herokuapp.com/dynamic_loading/2")
    with page.expect_response("https://the-internet.herokuapp.com/dynamic_loading/2") as response_info:
        page.get_by_role("button", name="Start").click()
        
    print(f"Test D Response URL: {response_info.value.url}")
    print(f"Test D Status: {response_info.value.status}")
        
    # Print Summary:
    print(f"Test A (wait_for_selector): {element.text_content()} ✅")
    print(f"Test B (wait_for_url): {test_b_url} ✅")
    print(f"Test C (wait_for_function): {page.locator('.quote').count()} ✅")
    print(f"Test D (expect_response): {response_info.value.status} ✅")