"""
Module 2.1 — Data Extraction Mastery
File: 01_text_extraction.py
Description: All text extraction methods — text_content, inner_text, inner_html, input_value
Date: 2026-04-21
Phase: 2 - Intermediate
Playwright Docs: https://playwright.dev/python/docs/locators#extract-text
"""

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=300)
    page = browser.new_page()

    # ====================================================================
    # text_content() vs inner_text()
    # ====================================================================
    print("=== text_content() vs inner_text() ===\n")

    page.goto("https://quotes.toscrape.com")

    first_quote = page.locator(".quote").first

    # text_content() — raw text, includes ALL text nodes
    tc = first_quote.text_content()
    print(f"  text_content():\n    {tc[:100]}...\n")

    # inner_text() — rendered text, what user actually sees
    it = first_quote.inner_text()
    print(f"  inner_text():\n    {it[:100]}...\n")

    # For simple elements they're usually the same
    author = first_quote.locator(".author")
    print(f"  Author text_content(): '{author.text_content()}'")
    print(f"  Author inner_text():   '{author.inner_text()}'")

    # ====================================================================
    # inner_html() — get HTML structure inside element
    # ====================================================================
    print("\n=== inner_html() ===\n")

    html = first_quote.inner_html()
    print(f"  inner_html() (first 200 chars):\n    {html[:200]}...\n")
    # This returns the raw HTML — useful for understanding structure

    # ====================================================================
    # all_text_contents() vs all_inner_texts()
    # Get text from MULTIPLE elements at once
    # ====================================================================
    print("=== all_text_contents() — Multiple elements ===\n")

    # Get ALL authors on the page at once — returns a list!
    all_authors = page.locator(".author").all_text_contents()
    print(f"  All authors: {all_authors}")
    print(f"  Count: {len(all_authors)}")

    # Get ALL tags from first quote
    tags = first_quote.locator(".tag").all_text_contents()
    print(f"\n  First quote tags: {tags}")

    # Compare with looping manually — same result, but all_text_contents() is faster!
    tags_manual = []
    for tag in first_quote.locator(".tag").all():
        tags_manual.append(tag.text_content())
    print(f"  Manual loop tags: {tags_manual}")
    print(f"  Same result? {tags == tags_manual}")

    # ====================================================================
    # input_value() — for form elements
    # ====================================================================
    print("\n=== input_value() ===\n")

    page.goto("https://the-internet.herokuapp.com/login")

    # Fill some inputs
    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("secret123")

    # Read back the values
    username_val = page.get_by_label("Username").input_value()
    password_val = page.get_by_label("Password").input_value()
    print(f"  Username value: '{username_val}'")
    print(f"  Password value: '{password_val}'")

    # text_content() on inputs returns EMPTY — value is in the attribute!
    username_text = page.locator("input#username").text_content()
    print(f"  text_content() on input: '{username_text}' (empty!)")
    print(f"  input_value() on input:  '{username_val}' (correct!)")

    # ====================================================================
    # PRACTICAL: Extract structured data from quotes page
    # ====================================================================
    print("\n=== PRACTICAL: Structured extraction ===\n")

    page.goto("https://quotes.toscrape.com")

    quotes = page.locator(".quote").all()
    data = []

    for quote in quotes:
        data.append({
            "text": quote.locator(".text").text_content().strip(),
            "author": quote.locator(".author").text_content().strip(),
            "author_link": quote.locator("a[href*='author']").first.get_attribute("href"),
            "tags": quote.locator(".tag").all_text_contents(),
        })

    # Print first 3
    for i, item in enumerate(data[:3], start=1):
        print(f"  {i}. {item['text'][:50]}...")
        print(f"     Author: {item['author']}")
        print(f"     Author link: {item['author_link']}")
        print(f"     Tags: {', '.join(item['tags'])}")
        print()

    browser.close()
    print("✅ Text extraction complete!")