"""
Module 1.4 — Practice 3 (Hard)
File: practice_03_hard_multi_page_scraper.py
Date: 2026-04-09

TASK:
=====
Build a "Multi-Page Quote Scraper" that scrapes the FIRST 3 PAGES
of quotes.toscrape.com using modern locator methods.

1. Start at https://quotes.toscrape.com
2. For EACH of the first 3 pages:
   a. Extract all quotes (text, author, tags) using locator chaining
   b. Store page number with each quote
   c. Take screenshot: "page_{number}.png" in PRACTICE folder
   d. Navigate to next page using get_by_role("link", name="Next")
3. After scraping all 3 pages, analyze the data:
   a. Total quotes collected
   b. Unique authors found (no duplicates)
   c. Most common author (who appears most)
   d. All unique tags found
4. Print full report:

   ===== MULTI-PAGE SCRAPER REPORT =====

   Pages scraped: 3
   Total quotes: 30
   Unique authors: X

   Most common author: [name] (X quotes)

   Unique tags: tag1, tag2, tag3, ...

   Page 1 quotes:
     1. "The world..." — Einstein [life, inspirational]
     2. "..." — ...
   Page 2 quotes:
     ...
   Page 3 quotes:
     ...

REQUIREMENTS:
- Use get_by_role("link", name="Next") for pagination (NOT CSS selector)
- Use locator chaining for data extraction
- Use .all() to loop through quotes
- Use .all_text_contents() for tags
- Screenshots saved in PRACTICE folder
- Find unique authors (hint: Python set)
- Find most common author (hint: count occurrences)
- Truncate quote text to 50 characters

HINTS:
- Navigation: page.get_by_role("link", name="Next").click()
- Set for unique items: unique_authors = set()
- Count with list: authors_list.count("Einstein")
- Or use collections.Counter
"""

# Write your code below this line
# ============================================================================

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://quotes.toscrape.com/")
    
    dicts = []
    
    for page_num in range(1, 4):
        quotes = page.locator(".quote").all()
        for quote in quotes:
            text = quote.locator(".text").text_content()
            author = quote.locator(".author").text_content()
            tags = quote.locator(".tag").all_text_contents()
            dicts.append({"text": text, "author": author, "tags": tags, "page": page_num})
        page.screenshot(path=f"PRACTICE/{page_num}.png")
        if page_num < 3:
            page.get_by_role("link", name="Next").click()
        
    total_quotes = len(dicts)
    unique_authors = set([quote["author"] for quote in dicts])
    authors_list = [quote["author"] for quote in dicts]
    most_common_author = max(set(authors_list), key=authors_list.count)
    unique_tags = set(tag for quote in dicts for tag in quote["tags"])
    
    print("===== MULTI-PAGE SCRAPER REPORT =====")
    print(f"Pages scraped: 3")
    print(f"Total quotes: {total_quotes}")
    print(f"Unique authors: {len(unique_authors)}")
    print(f"Most common author: {most_common_author} ({authors_list.count(most_common_author)} quotes)")
    print(f"Unique tags: {', '.join(unique_tags)}")
    for pg in range(1, 4):
      print(f"\nPage {pg} quotes:")
      page_quotes = [q for q in dicts if q["page"] == pg]
      for i, q in enumerate(page_quotes, start=1):
        print(f"  {i}. \"{q['text'][:50]}...\" — {q['author']} [{', '.join(q['tags'])}]")

    browser.close()