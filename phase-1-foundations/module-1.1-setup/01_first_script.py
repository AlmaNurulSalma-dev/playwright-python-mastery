"""
Module 1.1 — Setup & Environment
File: 01_first_script.py
Description: First Playwright script - launch browser, navigate, take screenshot
Date: 2026-04-09
Phase: 1 - Foundations
Playwright Docs: https://playwright.dev/python/docs/intro
"""

from playwright.sync_api import sync_playwright

# sync_playwright() is a context manager — like opening a file with 'with'
# It starts the Playwright server and gives you access to browser launchers
with sync_playwright() as p:
    # Launch Chromium browser (headful so you can SEE it)
    browser = p.chromium.launch(headless=False)

    # Create a new page (like opening a new tab)
    page = browser.new_page()

    # Navigate to a website
    page.goto("https://quotes.toscrape.com")

    # Print the page title
    print(f"Page title: {page.title()}")

    # Take a screenshot
    # page.screenshot(path="phase-1-foundations/module-1.1-setup/first_screenshot.png")
    # print("Screenshot saved!")

    # Close the browser
    browser.close()

print("Done! Your first Playwright script ran successfully 🎭")