"""
Module 1.1 — Setup & Environment
File: 03_browser_types.py
Description: Testing all 3 browser engines - Chromium, Firefox, WebKit
Date: 2026-04-09
Phase: 1 - Foundations
Playwright Docs: https://playwright.dev/python/docs/browsers
"""

import time
from playwright.sync_api import sync_playwright

URL = "https://quotes.toscrape.com"
SCREENSHOT_DIR = "phase-1-foundations/module-1.1-setup"

with sync_playwright() as p:

    # ========================================================================
    # Playwright bundles 3 browser engines:
    #
    # 1. Chromium  → basis of Chrome, Edge, Brave, Opera
    # 2. Firefox   → Mozilla's browser engine (Gecko)
    # 3. WebKit    → basis of Safari (yes, you can test Safari on Windows!)
    #
    # Selenium comparison:
    #   Selenium needs separate drivers for each browser (chromedriver, geckodriver)
    #   Playwright bundles everything — just switch p.chromium to p.firefox!
    # ========================================================================

    browsers = {
        "chromium": p.chromium,
        "firefox":  p.firefox,
        "webkit":   p.webkit,
    }

    results = []

    for name, browser_type in browsers.items():
        print(f"\n{'=' * 50}")
        print(f"Testing: {name.upper()}")
        print(f"{'=' * 50}")

        # Time the full cycle
        start = time.time()

        browser = browser_type.launch(headless=False)
        page = browser.new_page()
        page.goto(URL)

        title = page.title()
        url = page.url
        # User-Agent tells the website what browser is visiting
        user_agent = page.evaluate("navigator.userAgent")

        page.screenshot(path=f"{SCREENSHOT_DIR}/{name}_screenshot.png")

        elapsed = time.time() - start
        browser.close()

        results.append({
            "name": name,
            "title": title,
            "user_agent": user_agent,
            "time": elapsed,
        })

        print(f"   Title:      {title}")
        print(f"   URL:        {url}")
        print(f"   Time:       {elapsed:.2f}s")
        print(f"   User-Agent: {user_agent[:80]}...")
        print(f"   Screenshot: {SCREENSHOT_DIR}/{name}_screenshot.png")


    # ========================================================================
    # SUMMARY
    # ========================================================================
    print(f"\n{'=' * 50}")
    print("SPEED COMPARISON")
    print(f"{'=' * 50}")

    for r in sorted(results, key=lambda x: x["time"]):
        print(f"   {r['name']:10s} → {r['time']:.2f}s")

    fastest = min(results, key=lambda x: x["time"])
    print(f"\n   🏆 Fastest: {fastest['name']} ({fastest['time']:.2f}s)")


    # ========================================================================
    # USING INSTALLED CHROME/EDGE (channel parameter)
    # ========================================================================
    print(f"\n{'=' * 50}")
    print("BONUS: Using your installed Chrome browser")
    print(f"{'=' * 50}")
    print("   Instead of bundled Chromium, you can use YOUR Chrome:")
    print('   browser = p.chromium.launch(channel="chrome")')
    print('   browser = p.chromium.launch(channel="msedge")')
    print()
    print("   When to use which?")
    print("   • p.chromium.launch()              → bundled Chromium (default, reliable)")
    print('   • p.chromium.launch(channel="chrome") → your installed Chrome')
    print('   • p.chromium.launch(channel="msedge") → your installed Edge')
    print("   • p.firefox.launch()               → bundled Firefox")
    print("   • p.webkit.launch()                → bundled WebKit (Safari engine)")
    print()
    print("   💡 For scraping: stick with default Chromium — most reliable.")
    print("   💡 For testing: test all 3 to ensure cross-browser compatibility!")


    # ========================================================================
    # DEVICE EMULATION (Preview — covered more in Module 2)
    # ========================================================================
    print(f"\n{'=' * 50}")
    print("BONUS: Device Emulation (quick preview)")
    print(f"{'=' * 50}")

    # p.devices has predefined configs for phones and tablets
    iphone = p.devices["iPhone 13"]
    print(f"   iPhone 13 config: {iphone}")
    # Output: {'user_agent': '...', 'viewport': {'width': 390, 'height': 844}, ...}

    browser = p.chromium.launch(headless=False)
    # Pass device config to new_context — it sets viewport, user_agent, etc.
    context = browser.new_context(**iphone)
    page = context.new_page()
    page.goto(URL)

    page.screenshot(path=f"{SCREENSHOT_DIR}/iphone_screenshot.png")
    print(f"   Viewport:   {page.viewport_size}")
    print(f"   Screenshot: {SCREENSHOT_DIR}/iphone_screenshot.png")
    print("   👆 Check it — the page renders as if on an iPhone!")

    time.sleep(2)
    browser.close()


print("\n🎯 MODULE 1.1 COMPLETE!")
print("   You now know:")
print("   ✅ How to install Playwright")
print("   ✅ Headless vs headful mode")
print("   ✅ slow_mo for debugging")
print("   ✅ All 3 browser engines (Chromium, Firefox, WebKit)")
print("   ✅ Channel parameter for installed browsers")
print("   ✅ Device emulation basics")