"""
Module 2.2 — Handling Dynamic Content
File: 02_wait_for_response.py
Description: Catching API responses, waiting for network requests, and wait_for_function
Date: 2026-04-27
Phase: 2 - Intermediate
Playwright Docs: https://playwright.dev/python/docs/api/class-page#page-expect-response
"""

from playwright.sync_api import sync_playwright, expect
import re

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=300)
    page = browser.new_page()

    # ====================================================================
    # expect_response() — Catch specific API responses
    # ====================================================================
    print("=== expect_response() ===\n")

    page.goto("https://the-internet.herokuapp.com/dynamic_loading/2")

    # Listen for the response that comes after clicking Start
    with page.expect_response("**/dynamic_loading/2/start") as response_info:
        page.get_by_role("button", name="Start").click()

    response = response_info.value
    print(f"  Response URL: {response.url}")
    print(f"  Status: {response.status}")
    print(f"  Response body: {response.text()[:100]}...")
    print("  ✅ Caught the API response!")

    # ====================================================================
    # expect_response() with lambda — More flexible matching
    # ====================================================================
    print("\n=== expect_response() with lambda ===\n")

    page.goto("https://quotes.toscrape.com")

    # Catch ANY response with status 200 from this domain
    with page.expect_response(
        lambda response: response.status == 200 and "toscrape" in response.url
    ) as response_info:
        page.get_by_role("link", name="Next").click()

    response = response_info.value
    print(f"  Caught response: {response.url}")
    print(f"  Status: {response.status}")
    print("  ✅ Lambda filter worked!")

    # ====================================================================
    # wait_for_url() — Wait for URL to change
    # ====================================================================
    print("\n=== wait_for_url() ===\n")

    page.goto("https://the-internet.herokuapp.com/login")

    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("SuperSecretPassword!")
    page.get_by_role("button", name="Login").click()

    # Wait until URL changes to /secure
    page.wait_for_url("**/secure")
    print(f"  URL changed to: {page.url}")
    print("  ✅ Login redirect detected!")

    # With regex
    page.goto("https://quotes.toscrape.com")
    page.get_by_role("link", name="Next").click()
    page.wait_for_url(re.compile(r"/page/\d+"))
    print(f"  URL matched regex: {page.url}")

    # ====================================================================
    # wait_for_function() — Wait for JavaScript condition
    # ====================================================================
    print("\n=== wait_for_function() ===\n")

    page.goto("https://quotes.toscrape.com")

    # Wait until page has at least 5 quote elements
    page.wait_for_function(
        "document.querySelectorAll('.quote').length >= 5"
    )
    count = page.locator(".quote").count()
    print(f"  Quotes on page: {count}")
    print("  ✅ wait_for_function confirmed 5+ quotes exist!")

    # Wait until page is fully scrollable
    page.wait_for_function(
        "document.body.scrollHeight > window.innerHeight"
    )
    scroll_height = page.evaluate("document.body.scrollHeight")
    window_height = page.evaluate("window.innerHeight")
    print(f"  Page height: {scroll_height}, Window: {window_height}")
    print("  ✅ Page is scrollable!")

    # ====================================================================
    # wait_for_load_state() — Wait for page load phase
    # ====================================================================
    print("\n=== wait_for_load_state() ===\n")

    page.goto("https://books.toscrape.com", wait_until="commit")
    print(f"  After commit: {page.url}")

    # Wait for additional load states
    page.wait_for_load_state("domcontentloaded")
    print("  ✅ DOM content loaded")

    page.wait_for_load_state("load")
    print("  ✅ All resources loaded")

    page.wait_for_load_state("networkidle")
    print("  ✅ Network idle")

    # ====================================================================
    # PRACTICAL: Combining wait strategies
    # ====================================================================
    print("\n=== PRACTICAL: Login + Wait + Extract ===\n")

    page.goto("https://the-internet.herokuapp.com/login")

    # Fill and submit
    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("SuperSecretPassword!")
    page.get_by_role("button", name="Login").click()

    # Strategy 1: Wait for URL change
    page.wait_for_url("**/secure")

    # Strategy 2: Wait for success element
    page.wait_for_selector("#flash.success", state="visible")

    # Strategy 3: Verify with expect
    expect(page.locator("#flash")).to_contain_text("You logged into")

    flash = page.locator("#flash").text_content().strip()
    print(f"  Login success: {flash[:50]}...")
    print("  ✅ Three wait strategies combined!")

    # ====================================================================
    # CHOOSING THE RIGHT WAIT STRATEGY
    # ====================================================================
    print("""
=== WHICH WAIT STRATEGY TO USE ===

Auto-wait (do nothing):
  page.click("#btn")
  page.locator(".text").text_content()
  → USE FOR: most interactions, Playwright handles it

wait_for_selector(selector, state=):
  page.wait_for_selector(".results", state="visible")
  → USE FOR: waiting for element to appear/disappear

wait_for_url(pattern):
  page.wait_for_url("**/dashboard")
  → USE FOR: after login, pagination, redirects

wait_for_load_state(state):
  page.wait_for_load_state("networkidle")
  → USE FOR: after actions that trigger page reloads

wait_for_function(js_expression):
  page.wait_for_function("document.querySelectorAll('.item').length > 10")
  → USE FOR: complex JS conditions, counting elements

expect_response(url_pattern):
  with page.expect_response("**/api/data") as r:
  → USE FOR: catching API data directly (fastest scraping!)

expect(locator).to_be_visible():
  expect(page.locator(".result")).to_be_visible()
  → USE FOR: assertions in test/verification flow

wait_for_timeout(ms):
  page.wait_for_timeout(1000)
  → USE FOR: last resort only! Rate limiting, infinite scroll
""")

    browser.close()
    print("✅ Wait for response complete!")