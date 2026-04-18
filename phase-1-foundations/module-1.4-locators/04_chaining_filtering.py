"""
Module 1.4 — Locators (The Modern Way)
File: 04_chaining_filtering.py
Description: Chaining locators, filtering, nth(), first, last, and_(), or_()
Date: 2026-04-09
Phase: 1 - Foundations
Playwright Docs: https://playwright.dev/python/docs/locators#filtering-locators
"""

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()

    # ====================================================================
    # CHAINING — Locator inside locator (parent → child)
    # ====================================================================
    print("=== CHAINING ===\n")

    page.goto("https://quotes.toscrape.com")

    # Get first quote, then find author INSIDE it
    first_quote = page.locator(".quote").first
    author = first_quote.locator(".author")
    text = first_quote.locator(".text")

    print(f"  Quote: {text.text_content()[:50]}...")
    print(f"  Author: {author.text_content()}")

    # Chain deeper — tags inside a quote
    tags = first_quote.locator(".tag")
    print(f"  Tags count: {tags.count()}")
    for i in range(tags.count()):
        print(f"    Tag {i}: {tags.nth(i).text_content()}")

    # ====================================================================
    # FILTERING with has_text= — Narrow down by text content
    # ====================================================================
    print("\n=== FILTER by has_text ===\n")

    # Find ALL quotes (10 on this page)
    all_quotes = page.locator(".quote")
    print(f"  All quotes: {all_quotes.count()}")

    # Filter: only quotes that CONTAIN "Einstein" somewhere
    einstein_quotes = all_quotes.filter(has_text="Einstein")
    print(f"  Einstein quotes: {einstein_quotes.count()}")

    # Get the text of each Einstein quote
    for i in range(einstein_quotes.count()):
        quote = einstein_quotes.nth(i)
        text = quote.locator(".text").text_content()[:60]
        print(f"    {i + 1}. {text}...")

    # Filter for another author
    tolkien_quotes = all_quotes.filter(has_text="Tolkien")
    print(f"\n  Tolkien quotes: {tolkien_quotes.count()}")

    # ====================================================================
    # FILTERING with has= — Narrow down by child locator
    # ====================================================================
    print("\n=== FILTER by has= (child locator) ===\n")

    # Find quotes that have a tag "life"
    quotes_about_life = all_quotes.filter(
        has=page.locator(".tag", has_text="life")
    )
    print(f"  Quotes with tag 'life': {quotes_about_life.count()}")

    for i in range(quotes_about_life.count()):
        author = quotes_about_life.nth(i).locator(".author").text_content()
        print(f"    By: {author}")

    # ====================================================================
    # nth(), first, last — Pick by position
    # ====================================================================
    print("\n=== POSITION SELECTORS ===\n")

    quotes = page.locator(".quote")
    total = quotes.count()

    # first and last are PROPERTIES (no parentheses!)
    first_author = quotes.first.locator(".author").text_content()
    last_author = quotes.last.locator(".author").text_content()

    # nth() is a METHOD (with parentheses, 0-based index)
    third_author = quotes.nth(2).locator(".author").text_content()
    fifth_author = quotes.nth(4).locator(".author").text_content()

    print(f"  Total quotes: {total}")
    print(f"  First (quotes.first): {first_author}")
    print(f"  Last (quotes.last): {last_author}")
    print(f"  Third (quotes.nth(2)): {third_author}")
    print(f"  Fifth (quotes.nth(4)): {fifth_author}")

    # ====================================================================
    # .all() — Get list of ALL matching locators
    # ====================================================================
    print("\n=== .all() — Loop through all matches ===\n")

    all_authors = page.locator(".quote .author").all()
    print(f"  Found {len(all_authors)} authors:")

    for i, author_loc in enumerate(all_authors, start=1):
        print(f"    {i}. {author_loc.text_content()}")

    # ====================================================================
    # and_() / or_() — Combine locators with logic
    # ====================================================================
    print("\n=== and_() / or_() ===\n")

    page.goto("https://the-internet.herokuapp.com/checkboxes")

    checkboxes = page.get_by_role("checkbox")
    print(f"  All checkboxes: {checkboxes.count()}")

    # and_() — must match BOTH conditions
    # Example: find element that is BOTH a link AND contains "Next"
    page.goto("https://quotes.toscrape.com")

    next_link = page.get_by_role("link").and_(page.get_by_text("Next"))
    print(f"  Link AND text 'Next': {next_link.text_content()}")

    # or_() — match EITHER condition
    # Example: find elements that are "Next" OR "Previous"
    nav_links = page.get_by_text("Next").or_(page.get_by_text("Previous"))
    print(f"  'Next' OR 'Previous': {nav_links.count()} match(es)")

    # ====================================================================
    # CHAINING MULTIPLE FILTERS — Real scraping scenario
    # ====================================================================
    print("\n=== REAL SCENARIO: Complex filtering ===\n")

    page.goto("https://quotes.toscrape.com")

    # Task: Find the FIRST quote by Einstein that has tag "inspirational"
    result = (
        page.locator(".quote")                              # all quotes
        .filter(has_text="Einstein")                        # only Einstein
        .filter(has=page.locator(".tag", has_text="inspirational"))  # with tag "inspirational"
        .first                                              # first match
    )

    quote_text = result.locator(".text").text_content()[:60]
    author = result.locator(".author").text_content()
    print(f"  Found: {quote_text}...")
    print(f"  By: {author}")

    # ====================================================================
    # EXTRACTING ALL DATA — Common scraping pattern
    # ====================================================================
    print("\n=== SCRAPING PATTERN: Extract all quotes ===\n")

    all_quotes = page.locator(".quote").all()
    data = []

    for quote_el in all_quotes:
        data.append({
            "text": quote_el.locator(".text").text_content(),
            "author": quote_el.locator(".author").text_content(),
            "tags": quote_el.locator(".tag").all_text_contents(),
        })

    # Print first 3
    for i, item in enumerate(data[:3], start=1):
        print(f"  {i}. {item['text'][:50]}...")
        print(f"     Author: {item['author']}")
        print(f"     Tags: {', '.join(item['tags'])}")
        print()

    browser.close()
    print("✅ Chaining & filtering complete!")