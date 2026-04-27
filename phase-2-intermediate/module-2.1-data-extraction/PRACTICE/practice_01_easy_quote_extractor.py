"""
Module 2.1 — Practice 1 (Easy)
File: practice_01_easy_quote_extractor.py
Date: 2026-04-21

TASK:
=====
Extract ALL data from quotes.toscrape.com page 1 using EVERY extraction method
you learned. Prove you understand the difference between each method.

1. Buka https://quotes.toscrape.com
2. For the FIRST quote only, demonstrate ALL extraction methods:
   a. text_content() on the quote text
   b. inner_text() on the quote text
   c. inner_html() on the quote container
   d. get_attribute("href") on the author link
   e. all_text_contents() on all tags
3. Print each result with clear labels showing WHICH method was used

4. Then extract ALL 10 quotes on the page into a list of dicts:
   - text (use text_content, strip it)
   - author (use text_content)
   - author_link (use get_attribute on the author <a> tag)
   - tags (use all_text_contents)

5. Print summary:
   Total quotes: 10
   Unique authors: X
   Total tags collected: X

REQUIREMENTS:
- Show ALL 5 extraction methods on the first quote
- Use locator chaining for nested elements
- Use .all() for looping all quotes
- Use set() for unique authors

HINTS:
- Author link selector: a[href*='author']
- The quote text element has class "text"
- inner_html() returns raw HTML — will show <span> tags etc.
"""

# Write your code below this line
# ============================================================================

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://quotes.toscrape.com")
    
    first_quote = page.locator(".quote").first
    
    tc = first_quote.locator(".text").text_content()
    it = first_quote.locator(".text").inner_text()
    ih = first_quote.inner_html()
    ga = first_quote.locator("a[href*='author']").get_attribute("href")
    atc = first_quote.locator(".tag").all_text_contents()
    print(f"Text Content: {tc}")
    print(f"Inner Text: {it}")
    print(f"Inner HTML: {ih}")
    print(f"Author URL: {ga}")
    print(f"Tags: {atc}")

    quotes = page.locator(".quote").all()
    quote_data = []
    for quote in quotes:
        text = quote.locator(".text").text_content().strip()
        author = quote.locator(".author").text_content()
        author_link = quote.locator("a[href*='author']").get_attribute("href")
        tags = quote.locator(".tag").all_text_contents()
        quote_data.append({
            "text": text,
            "author": author,
            "author_link": author_link,
            "tags": tags
        })
        
    print("SUMMARY OF QUOTES:")
    print(f"Total quotes: {len(quote_data)}")
    print(f"Unique authors: {len(set(q['author'] for q in quote_data))}")
    print(f"Total tags collected: {sum(len(q['tags']) for q in quote_data)}")