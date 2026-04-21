"""
Module 1.5 — Auto-Waiting & Assertions
File: 03_timeouts.py
Description: Configuring timeouts at every level — per-action, per-page, global
Date: 2026-04-20
Phase: 1 - Foundations
Playwright Docs: https://playwright.dev/python/docs/actionability#timeouts
"""

from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()

    # ====================================================================
    # DEFAULT TIMEOUTS
    #
    # Playwright has 3 types of timeouts:
    #   1. Action timeout    → click, fill, hover, etc. (default 30s)
    #   2. Navigation timeout → goto, go_back, reload  (default 30s)
    #   3. Expect timeout    → expect() assertions     (default 5s)
    # ====================================================================
    print("=== DEFAULT TIMEOUTS ===\n")
    print("  Action timeout:     30000ms (30s)")
    print("  Navigation timeout: 30000ms (30s)")
    print("  Expect timeout:      5000ms (5s)")

    # ====================================================================
    # LEVEL 1: PER-ACTION TIMEOUT
    # Override timeout for a SINGLE action
    # ====================================================================
    print("\n=== LEVEL 1: PER-ACTION TIMEOUT ===\n")

    page.goto("https://quotes.toscrape.com")

    # Click with custom timeout — only THIS click waits max 5s
    page.click("a:text('Next')", timeout=5000)
    print(f"  click(timeout=5000): Clicked Next → {page.url}")

    # Fill with custom timeout
    page.go_back()
    page.goto("https://the-internet.herokuapp.com/login")
    page.fill("input#username", "tomsmith", timeout=3000)
    print("  fill(timeout=3000): Filled username")

    # Navigation with custom timeout
    page.goto("https://quotes.toscrape.com", timeout=10000)
    print("  goto(timeout=10000): Navigated with 10s max")

    # expect() with custom timeout
    expect(page).to_have_title("Quotes to Scrape", timeout=3000)
    print("  expect(timeout=3000): Title verified")

    # ====================================================================
    # LEVEL 2: PER-PAGE DEFAULT TIMEOUT
    # Change default for ALL actions on this page
    # ====================================================================
    print("\n=== LEVEL 2: PER-PAGE TIMEOUT ===\n")

    # Set default timeout for all actions on this page
    page.set_default_timeout(10000)  # 10 seconds
    print("  set_default_timeout(10000): All actions now wait max 10s")

    # These all use the 10s default now
    page.goto("https://quotes.toscrape.com")
    page.click("a:text('Next')")
    print(f"  click() used 10s default → {page.url}")

    # Navigation has its OWN default (separate from actions)
    page.set_default_navigation_timeout(15000)  # 15 seconds
    print("  set_default_navigation_timeout(15000): goto/back/forward now wait max 15s")

    page.goto("https://quotes.toscrape.com")
    print("  goto() used 15s navigation default")

    # Per-action timeout OVERRIDES page default
    page.click("a:text('Next')", timeout=3000)
    print("  click(timeout=3000): Overrides page default of 10s for this click only")

    # ====================================================================
    # LEVEL 3: GLOBAL EXPECT TIMEOUT
    # Change default for ALL expect() assertions
    # ====================================================================
    print("\n=== LEVEL 3: GLOBAL EXPECT TIMEOUT ===\n")

    # Change default expect timeout
    expect.set_options(timeout=8000)
    print("  expect.set_options(timeout=8000): All expect() now wait max 8s")

    expect(page).to_have_url("https://quotes.toscrape.com/page/2/")
    print("  expect() used 8s default")

    # Per-assertion timeout still overrides global
    expect(page.locator("h1")).to_be_visible(timeout=2000)
    print("  expect(timeout=2000): Overrides global 8s for this assertion only")

    # ====================================================================
    # TIMEOUT ERROR — What happens when timeout is exceeded
    # ====================================================================
    print("\n=== TIMEOUT ERROR DEMO ===\n")

    try:
        # Try to find an element that doesn't exist — with short timeout
        page.click("#this-element-does-not-exist", timeout=2000)
    except Exception as e:
        error_msg = str(e)[:100]
        print(f"  ❌ TimeoutError after 2s: {error_msg}...")
        print("  → Playwright waited 2 seconds, element never appeared, then raised error")

    print("\n  This is GOOD — you know exactly what went wrong and how long it waited!")

    # ====================================================================
    # expect() TIMEOUT ERROR
    # ====================================================================
    print("\n=== EXPECT TIMEOUT ERROR ===\n")

    try:
        # Assert wrong title — will timeout
        expect(page).to_have_title("Wrong Title", timeout=2000)
    except AssertionError as e:
        print(f"  ❌ AssertionError after 2s: Title didn't match")
        print(f"  → expect() retried for 2 seconds, title never changed to 'Wrong Title'")

    # ====================================================================
    # TIMEOUT HIERARCHY — Who wins?
    # ====================================================================
    print("""
=== TIMEOUT HIERARCHY ===

Priority (highest wins):
  1. Per-action:  page.click(selector, timeout=5000)     ← HIGHEST
  2. Per-page:    page.set_default_timeout(10000)
  3. Default:     30000ms (built-in)                      ← LOWEST

For navigation:
  1. Per-call:    page.goto(url, timeout=5000)            ← HIGHEST
  2. Per-page:    page.set_default_navigation_timeout(15000)
  3. Per-page:    page.set_default_timeout(10000)
  4. Default:     30000ms                                  ← LOWEST

For expect():
  1. Per-assertion: expect(loc).to_be_visible(timeout=3000) ← HIGHEST
  2. Global:        expect.set_options(timeout=8000)
  3. Default:       5000ms                                   ← LOWEST
""")

    # ====================================================================
    # BEST PRACTICES
    # ====================================================================
    print("""
=== TIMEOUT BEST PRACTICES ===

1. DON'T lower defaults too much
   page.set_default_timeout(1000)  ← too aggressive, will cause flaky results

2. DO increase for slow pages
   page.goto(url, timeout=60000)   ← 60s for very slow sites

3. DON'T use wait_for_timeout() as a solution
   page.wait_for_timeout(5000)     ← this is just time.sleep()! Avoid!

4. DO use expect() instead of sleep
   ❌ page.wait_for_timeout(3000)  → always waits 3s even if ready in 0.5s
   ✅ expect(loc).to_be_visible()  → waits ONLY as long as needed

5. Reasonable defaults:
   Actions:    10000-30000ms (10-30s)
   Navigation: 30000-60000ms (30-60s)
   Expect:      5000-10000ms (5-10s)
""")

    # Reset timeouts to defaults before closing
    page.set_default_timeout(30000)
    page.set_default_navigation_timeout(30000)
    expect.set_options(timeout=5000)

    browser.close()
    print("✅ Timeouts complete!")