"""
Module 1.2 — Architecture Deep Dive
File: 01_browser_context_page.py
Description: Understanding the 3-layer model - Browser → Context → Page
Date: 2026-04-09
Phase: 1 - Foundations
Playwright Docs: https://playwright.dev/python/docs/browser-contexts
"""

from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    # ====================================================================
    # LAYER 1: BROWSER
    # Think of this as opening the Chrome application itself
    # ====================================================================
    browser = p.chromium.launch(headless=False, slow_mo=500)
    print(f"Browser version: {browser.version}")
    print(f"Contexts at start: {len(browser.contexts)}")  # → 0

    # ====================================================================
    # LAYER 2: CONTEXT
    # Think of this as opening an incognito window
    # Each context has its OWN cookies, localStorage, cache — fully isolated
    # ====================================================================
    context = browser.new_context()
    print(f"Contexts after new_context(): {len(browser.contexts)}")  # → 1

    # ====================================================================
    # LAYER 3: PAGE
    # Think of this as opening a new tab inside that incognito window
    # Pages in the SAME context share cookies and session
    # ====================================================================
    page1 = context.new_page()
    page1.goto("https://quotes.toscrape.com")
    print(f"\nPage 1 title: {page1.title()}")
    print(f"Pages in context: {len(context.pages)}")  # → 1

    # Open another tab in SAME context — shares cookies!
    page2 = context.new_page()
    page2.goto("https://books.toscrape.com")
    print(f"Page 2 title: {page2.title()}")
    print(f"Pages in context: {len(context.pages)}")  # → 2

    # ====================================================================
    # THE SHORTCUT: browser.new_page()
    # This secretly does: browser.new_context() → context.new_page()
    # Convenient but creates a NEW context every time!
    # ====================================================================
    shortcut_page = browser.new_page()  # new context + new page in one call
    shortcut_page.goto("https://quotes.toscrape.com/page/2/")
    print(f"\nShortcut page title: {shortcut_page.title()}")
    print(f"Total contexts now: {len(browser.contexts)}")  # → 2 (original + shortcut)

    # ====================================================================
    # PROOF: Let's verify the hierarchy
    # ====================================================================
    print("\n===== HIERARCHY =====")
    for i, ctx in enumerate(browser.contexts):
        print(f"  Context {i}: {len(ctx.pages)} page(s)")
        for j, pg in enumerate(ctx.pages):
            print(f"    Page {j}: {pg.url}")

    # ====================================================================
    # CLEANUP
    # Close order: pages → contexts → browser (or just close browser)
    # ====================================================================
    browser.close()  # closes everything — all contexts and pages
    print("\n✅ Browser closed — all contexts and pages gone")