"""
Module 1.1 — Setup & Environment
File: 02_headless_vs_headful.py
Description: Difference between headless and headful mode + slow_mo for debugging
Date: 2026-04-09
Phase: 1 - Foundations
Playwright Docs: https://playwright.dev/python/docs/browsers#launching-a-browser
"""

import time
from playwright.sync_api import sync_playwright

# ============================================================================
# HEADFUL MODE — Browser window VISIBLE (you can see what's happening)
# Use for: debugging, development, learning
# ============================================================================
print("=" * 50)
print("1. HEADFUL MODE (headless=False)")
print("=" * 50)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://quotes.toscrape.com")
    print(f"   Title: {page.title()}")
    print(f"   URL:   {page.url}")

    # Give yourself time to see the browser
    time.sleep(2)

    browser.close()
    print("   ✅ Browser was VISIBLE — you saw it open and close\n")


# ============================================================================
# HEADLESS MODE — Browser runs INVISIBLY in background (default)
# Use for: production scraping, CI/CD, speed
# ============================================================================
print("=" * 50)
print("2. HEADLESS MODE (headless=True — DEFAULT)")
print("=" * 50)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # same as launch() with no args
    page = browser.new_page()

    page.goto("https://quotes.toscrape.com")
    print(f"   Title: {page.title()}")
    print(f"   URL:   {page.url}")

    # Screenshot to prove it worked (since you can't see the browser)
    page.screenshot(path="phase-1-foundations/module-1.1-setup/headless_screenshot.png")

    browser.close()
    print("   ✅ Browser was INVISIBLE — but still worked! Check the screenshot.\n")


# ============================================================================
# SLOW_MO — Slows down EVERY action (great for debugging)
# Value is in milliseconds. 1000 = 1 second delay per action.
# ============================================================================
print("=" * 50)
print("3. SLOW_MO MODE (slow_mo=1000)")
print("=" * 50)

with sync_playwright() as p:
    # Every action will have a 1-second pause — watch it step by step!
    browser = p.chromium.launch(headless=False, slow_mo=1000)
    page = browser.new_page()

    page.goto("https://quotes.toscrape.com")     # pause 1s
    page.click("a:text('Next')")                  # pause 1s, then click
    print(f"   Page 2 title: {page.title()}")
    print(f"   Page 2 URL:   {page.url}")

    page.screenshot(path="phase-1-foundations/module-1.1-setup/slowmo_page2.png")

    browser.close()
    print("   ✅ Every action had a 1-second delay — easier to follow!\n")


# ============================================================================
# SPEED COMPARISON — Headless is faster!
# ============================================================================
print("=" * 50)
print("4. SPEED COMPARISON")
print("=" * 50)

with sync_playwright() as p:
    # Headless speed
    start = time.time()
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://quotes.toscrape.com")
    _ = page.title()
    browser.close()
    headless_time = time.time() - start

    # Headful speed
    start = time.time()
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://quotes.toscrape.com")
    _ = page.title()
    browser.close()
    headful_time = time.time() - start

    print(f"   Headless: {headless_time:.2f}s")
    print(f"   Headful:  {headful_time:.2f}s")
    print(f"   Headless is ~{headful_time/headless_time:.1f}x faster!\n")


print("🎯 SUMMARY:")
print("   headless=True  → invisible, fast    → use for production/scraping")
print("   headless=False → visible, slower    → use for debugging/learning")
print("   slow_mo=1000   → 1s delay per step  → use when debugging interactions")