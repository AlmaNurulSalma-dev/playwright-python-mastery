"""
Module 2.1 — Practice 3 (Hard)
File: practice_03_hard_deep_scraper.py
Date: 2026-04-21

TASK:
=====
Build a "Deep Quote Scraper" that scrapes quotes.toscrape.com AND
follows links to extract ADDITIONAL data from author pages.

1. Buka https://quotes.toscrape.com
2. Extract all 10 quotes (text, author, tags) from page 1
3. Collect all UNIQUE author page links (e.g., /author/Albert-Einstein)
4. For EACH unique author, visit their author page and extract:
   - Full name (from <h3 class="author-title">)
   - Birth date (from <span class="author-born-date">)
   - Birth location (from <span class="author-born-location">)
   - Bio (first 100 characters of <div class="author-description">)
5. Combine quote data with author data
6. Use page.evaluate() to get at least ONE piece of data
   (e.g., total number of elements on author page, or page scroll height)
7. Save everything to a JSON file: output/deep_quotes.json

8. Print report:

   ===== DEEP SCRAPER REPORT =====

   Authors Found: 5

   Author: Albert Einstein
     Born: March 14, 1879 in Ulm, Germany
     Bio: In 1879, Albert Einstein was born in Ulm, Germany. He compl...
     Quotes (2):
       1. "The world as we have created it..."
       2. "There are only two ways to live..."

   Author: J.K. Rowling
     Born: July 31, 1965 in Yate, South Gloucestershire, England
     Bio: ...
     Quotes (1):
       1. "It is our choices, Harry..."

   ... (all authors)

   Total quotes: 10
   Unique authors: X
   Pages visited: X (1 main + X author pages)

REQUIREMENTS:
- Scrape main page + visit each UNIQUE author page
- Use get_attribute() for author page links
- Build full URL from relative links (base_url + href)
- Use locator chaining on author pages
- Use page.evaluate() at least once
- Save to JSON with json.dump()
- Navigate BACK to main page is NOT needed — just goto each author page
- Use headless for speed

HINTS:
- Unique authors: use set() to avoid visiting same author twice
- Author page URL: "https://quotes.toscrape.com" + "/author/Albert-Einstein"
- Author page selectors:
    h3.author-title
    span.author-born-date
    span.author-born-location
    div.author-description
- Group quotes by author: use a dict with author name as key
- page.evaluate("document.querySelectorAll('*').length") for total elements
"""

# Write your code below this line
# ============================================================================

import json

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://quotes.toscrape.com")
    
    quotes_data = []
    quotes = page.locator(".quote").all()
    for quote in quotes:
        text = quote.locator(".text").text_content().strip()
        author = quote.locator(".author").text_content()
        tags = quote.locator(".tag").all_text_contents()
        quotes_data.append({
            "text": text,
            "author": author,
            "tags": tags,
            "author_link": quote.locator("a[href*='author']").first.get_attribute("href")
        })
        
    unique_author = set(q["author"] for q in quotes_data)
    
    author_data = {}
    for author in unique_author:
        author_link = next((q["author_link"] for q in quotes_data if q["author"] == author), None)
        page.goto("https://quotes.toscrape.com" + author_link)
        author_data[author] = {
            "full_name": author,
            "birth_date": page.locator(".author-born-date").text_content(),
            "birth_location": page.locator(".author-born-location").text_content(),
            "bio": page.locator(".author-description").text_content()[:100]
        }
        title = page.evaluate("document.title")
        print(f"  document.title: {title}")
    
    print("===== DEEP SCRAPER REPORT =====")
    print(f"Authors found: {len(unique_author)}")
    authors_info = {}
    for author in unique_author:
        print(f"  Author: {author}")
        print(f"    Born: {author_data[author]['birth_date']} in {author_data[author]['birth_location']}")
        print(f"    Bio: {author_data[author]['bio']}")
        print(f"    Quotes({len([q for q in quotes_data if q['author'] == author])})")
        authors_info[author] = {
            "birth_date": author_data[author]['birth_date'],
            "birth_location": author_data[author]['birth_location'],
            "bio": author_data[author]['bio']
        }

    print(f"Total quotes: {len(quotes_data)}")
    print(f"Unique authors: {len(unique_author)}")    
    print(f"Pages visited: 1 (main page) + {len(unique_author)} (author pages)")
    
    with open("output/deep_quotes.json", "w", encoding="utf-8") as f:
        json.dump(quotes_data, f, indent=2, ensure_ascii=False)
        
    browser.close()