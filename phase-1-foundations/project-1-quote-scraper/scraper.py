"""
Mini Project 1 — Quote Scraper
File: scraper.py
Description: Scrapes all quotes from quotes.toscrape.com
Date: 2026-04-21
Phase: 1 - Foundations

OUTPUT:
  - output/quotes.json (all quotes with text, author, tags, page number)
  - output/screenshots/page_X.png (screenshot per page)

REQUIREMENTS:
  1. Scrape ALL pages (not just the first one)
  2. For each quote, extract: text, author, tags, page number
  3. Use modern locators (get_by_role, locator chaining, .all())
  4. Use expect() to verify navigation (URL changes after clicking Next)
  5. Save all data to output/quotes.json
  6. Take screenshot of each page in output/screenshots/
  7. Print progress while scraping (e.g., "Scraping page 1... found 10 quotes")
  8. Print final summary (total quotes, unique authors, pages scraped)
  9. Handle the last page gracefully (no "Next" link on last page!)
  10. Use headless mode for speed

STRUCTURE:
  - Use a while loop (you don't know how many pages there are!)
  - Check if "Next" link exists before clicking
  - Collect all data in a list of dicts
  - Use json module to save output

HINTS:
  - import json
  - json.dump(data, file, indent=2, ensure_ascii=False)
  - Check Next exists: page.get_by_role("link", name="Next").count() > 0
  - Or use: page.locator(".next > a").count() > 0
  - Screenshot: page.screenshot(path=f"output/screenshots/page_{num}.png")
  - After clicking Next: expect(page).to_have_url(re.compile(r"page/\d+"))
"""

# YOUR CODE HERE
# ===========================================================================

from playwright.sync_api import sync_playwright, expect
import json
import re

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://quotes.toscrape.com/")
    
    quotes_data = []
    
    page_number = 1
    
    while True:
      all_quotes = page.locator(".quote").all()
      print(f"Scraping page {page_number}... found {len(all_quotes)} quotes")
      for quote in all_quotes:
        quotes_data.append({
            "text": quote.locator(".text").text_content(),
            "author": quote.locator(".author").text_content(),
            "tags": [tag.text_content() for tag in quote.locator(".tag").all()],
            "page_number": page_number
          })
      if page.get_by_role("link", name="Next").count() > 0:
        page.get_by_role("link", name="Next").click()
        expect(page).to_have_url(re.compile(r"page/\d+"))
      else:
        break
      page.screenshot(path=f"output/screenshots/page_{page_number}.png")
      page_number += 1
        
    with open("output/quotes.json", "w", encoding="utf-8") as f:
        json.dump(quotes_data, f, indent=2, ensure_ascii=False)
        
    print("===== FINAL SUMMARY =====")
    print(f"Total quotes: {len(quotes_data)}")
    print(f"Unique authors: {len(set(q['author'] for q in quotes_data))}")
    print(f"Pages scraped: {page_number}")
        
    browser.close()
    