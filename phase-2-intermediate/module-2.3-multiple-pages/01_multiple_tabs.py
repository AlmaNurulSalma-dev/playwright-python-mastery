"""
Module 2.3 — Multiple Pages & Contexts
File: 01_multiple_tabs.py
Description: Opening, managing, and switching between multiple tabs
Date: 2026-04-21
Phase: 2 - Intermediate
Playwright Docs: https://playwright.dev/python/docs/pages
"""

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    context = browser.new_context()

    # ====================================================================
    # OPENING MULTIPLE TABS IN SAME CONTEXT
    # ====================================================================
    print("=== MULTIPLE TABS ===\n")

    # Tab 1
    page1 = context.new_page()
    page1.goto("https://quotes.toscrape.com")
    print(f"  Tab 1: {page1.title()} — {page1.url}")

    # Tab 2 — same context, shares cookies!
    page2 = context.new_page()
    page2.goto("https://books.toscrape.com")
    print(f"  Tab 2: {page2.title()} — {page2.url}")

    # Tab 3
    page3 = context.new_page()
    page3.goto("https://the-internet.herokuapp.com")
    print(f"  Tab 3: {page3.title()} — {page3.url}")

    # List all open pages
    print(f"\n  Total open tabs: {len(context.pages)}")
    for i, pg in enumerate(context.pages):
        print(f"    Tab {i}: {pg.url}")

    # ====================================================================
    # NO "SWITCHING" NEEDED — Just use the variable!
    #
    # Selenium: driver.switch_to.window(handle) — complex, error-prone
    # Playwright: just use page1, page2, page3 — each is independent!
    # ====================================================================
    print("\n=== NO SWITCHING NEEDED ===\n")

    # Work on tab 1
    page1_title = page1.title()
    print(f"  Working on Tab 1: {page1_title}")

    # Work on tab 3 — NO switch needed!
    page3_title = page3.title()
    print(f"  Working on Tab 3: {page3_title}")

    # Back to tab 2 — still NO switch!
    page2_title = page2.title()
    print(f"  Working on Tab 2: {page2_title}")

    print("  ✅ No switching! Just use the page variable directly.")

    # ====================================================================
    # HANDLING POPUPS — Links that open in new tab
    # ====================================================================
    print("\n=== HANDLING POPUPS ===\n")

    page4 = context.new_page()
    page4.goto("https://the-internet.herokuapp.com/windows")

    print(f"  Before popup: {len(context.pages)} tabs open")

    # Click "Click Here" which opens a new window
    with page4.expect_popup() as popup_info:
        page4.get_by_role("link", name="Click Here").click()

    popup = popup_info.value
    print(f"  Popup opened: {popup.url}")
    print(f"  Popup title: {popup.title()}")
    print(f"  After popup: {len(context.pages)} tabs open")

    # You can interact with the popup just like any page
    popup_text = popup.locator("h3").text_content()
    print(f"  Popup content: {popup_text}")

    # Close the popup
    popup.close()
    print(f"  After closing popup: {len(context.pages)} tabs open")

    # ====================================================================
    # CLOSING INDIVIDUAL TABS
    # ====================================================================
    print("\n=== CLOSING TABS ===\n")

    print(f"  Before closing: {len(context.pages)} tabs")

    page3.close()
    print(f"  Closed tab 3: {len(context.pages)} tabs remaining")

    page2.close()
    print(f"  Closed tab 2: {len(context.pages)} tabs remaining")

    # page1 and page4 still alive!
    print(f"  Tab 1 still accessible: {page1.url}")
    print(f"  Tab 4 still accessible: {page4.url}")

    # ====================================================================
    # PARALLEL DATA EXTRACTION FROM MULTIPLE TABS
    # ====================================================================
    print("\n=== PARALLEL EXTRACTION ===\n")

    # Open 3 different sites simultaneously
    sites = [
        {"name": "quotes", "url": "https://quotes.toscrape.com"},
        {"name": "books", "url": "https://books.toscrape.com"},
        {"name": "herokuapp", "url": "https://the-internet.herokuapp.com"},
    ]

    pages = {}
    for site in sites:
        pg = context.new_page()
        pg.goto(site["url"])
        pages[site["name"]] = pg

    # Extract data from each — no switching needed!
    print(f"  Quotes title: {pages['quotes'].title()}")
    print(f"  Books title: {pages['books'].title()}")
    print(f"  Herokuapp title: {pages['herokuapp'].title()}")

    # Close all
    for pg in pages.values():
        pg.close()

    print(f"\n  Tabs remaining: {len(context.pages)}")

    browser.close()
    print("\n✅ Multiple tabs complete!")