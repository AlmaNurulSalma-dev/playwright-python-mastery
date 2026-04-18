"""
Module 1.4 — Practice 2 (Medium)
File: practice_02_medium_quote_filter.py
Date: 2026-04-09

TASK:
=====
Build a "Quote Filter Tool" that extracts quotes from quotes.toscrape.com
using chaining and filtering.

1. Buka https://quotes.toscrape.com
2. Extract ALL quotes on the page using locator chaining:
   - For each quote, get: text, author, and list of tags
   - Store in a list of dicts
3. Filter quotes by author using .filter(has_text=):
   - Print how many quotes by "Einstein"
   - Print how many quotes by "Tolkien"
4. Filter quotes by tag using .filter(has=):
   - Find quotes tagged "life"
   - Find quotes tagged "inspirational"
5. Print summary report:

   ===== QUOTE FILTER REPORT =====
   Total quotes on page: 10

   By Author:
     Einstein: 2 quote(s)
     Tolkien: 1 quote(s)

   By Tag:
     life: X quote(s)
     inspirational: X quote(s)

   All Quotes:
     1. "The world as..." — Einstein [inspirational, life]
     2. "It is our choices..." — Tolkien [abilities]
     ...

REQUIREMENTS:
- Use page.locator().all() to loop through quotes
- Use .filter(has_text=) for author filtering
- Use .filter(has=page.locator()) for tag filtering
- Use .all_text_contents() for getting all tags
- Truncate quote text to 50 characters in output

HINTS:
- All quotes: page.locator(".quote")
- Quote text: quote.locator(".text").text_content()
- Author: quote.locator(".author").text_content()
- Tags: quote.locator(".tag").all_text_contents()
"""

# Write your code below this line
# ============================================================================

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://quotes.toscrape.com/")
    
    dicts = []
    
    quote = page.locator(".quote").all()
    for i in range(len(quote)):
        text = quote[i].locator(".text").text_content()
        author = quote[i].locator(".author").text_content()
        tags = quote[i].locator(".tag").all_text_contents()
        dicts.append({"text": text, "author": author, "tags": tags})


    einstein_quotes = page.locator(".quote").filter(has_text="Einstein")
    print(f"Einstein quotes: {einstein_quotes.count()}")
    tolkien_quotes = page.locator(".quote").filter(has_text="Tolkien")
    print(f"Tolkien quotes: {tolkien_quotes.count()}")
    
    
    life_quotes = page.locator(".quote").filter(has=page.locator(".tag", has_text="life"))
    inspirational_quotes = page.locator(".quote").filter(has=page.locator(".tag", has_text="inspirational"))

    
    print("===== QUOTE FILTER REPORT =====")
    print(f"Total quotes on page: {len(quote)}")
    print(f"By Author:\n  Einstein: {einstein_quotes.count()} quote(s)\n  Tolkien: {tolkien_quotes.count()} quote(s)")
    print(f"By Tag:\n  life: {life_quotes.count()} quote(s)\n  inspirational: {inspirational_quotes.count()} quote(s)")
    print("All Quotes:")
    for i in range(len(quote)):
        text = quote[i].locator(".text").text_content()[:50]
        author = quote[i].locator(".author").text_content()
        tags = quote[i].locator(".tag").all_text_contents()
        print(f"  {i + 1}. \"{text}...\" — {author} [{', '.join(tags)}]")
    browser.close()
    