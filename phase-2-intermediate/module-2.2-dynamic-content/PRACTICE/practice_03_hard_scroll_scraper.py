"""
Module 2.2 — Practice 3 (Hard)
File: practice_03_hard_scroll_scraper.py
Date: 2026-04-21

TASK:
=====
Build a "Multi-Page Dynamic Scraper" that combines MULTIPLE wait strategies
to scrape quotes.toscrape.com across 3 pages.

For EACH of the first 3 pages:

1. Wait for quotes to be loaded:
   - Use wait_for_function() to confirm at least 10 quotes exist on page:
     "document.querySelectorAll('.quote').length >= 10"

2. Extract all quotes (text, author, tags)

3. Wait for and catch the navigation response:
   - Use expect_response() with the Next link click
   - Record response status code
   - ONLY if not on page 3 (last page to scrape)

4. After clicking Next, use wait_for_url() to confirm page changed

5. Take screenshot of each page

After all 3 pages scraped, print report:

   ===== DYNAMIC SCRAPER REPORT =====

   Page 1:
     Quotes: 10
     Response status: 200
     URL: https://quotes.toscrape.com/
     Screenshot: page_1.png

   Page 2:
     Quotes: 10
     Response status: 200
     URL: https://quotes.toscrape.com/page/2/
     Screenshot: page_2.png

   Page 3:
     Quotes: 10
     Response status: N/A (last page, no navigation)
     URL: https://quotes.toscrape.com/page/3/
     Screenshot: page_3.png

   Total quotes: 30
   Unique authors: X
   All response statuses: [200, 200]

REQUIREMENTS:
- Use wait_for_function() to verify quotes loaded on each page
- Use expect_response() to catch navigation responses
- Use wait_for_url() to confirm page changes
- Use while or for loop for 3 pages
- Collect all data in list of dicts
- Screenshots in PRACTICE folder
- Handle page 3 differently (no Next click needed)
- Use headless mode

HINTS:
- wait_for_function: "document.querySelectorAll('.quote').length >= 10"
- expect_response: "**/page/**" for pagination responses
- wait_for_url: re.compile(r"/page/\d+")
- On page 3, skip expect_response and next click
- Response statuses: keep a list, append each status
"""

# Write your code below this line
# ============================================================================

from playwright.sync_api import sync_playwright
import re

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=300)
    page = browser.new_page()
    page.goto("https://quotes.toscrape.com")
    
    quotes_data = []
    response_statuses = []
    
    # Print Report
    print("===== DYNAMIC SCRAPER REPORT =====")

    for page_num in range(1, 4):              # 3 pages
        page.wait_for_function("document.querySelectorAll('.quote').length >= 10")
        quotes = page.locator(".quote").all()
        for quote in quotes:                  # extract ALL 10 quotes
            quotes_data.append({
                "text": quote.locator(".text").text_content().strip(),
                "author": quote.locator(".author").text_content().strip(),
                "tags": quote.locator(".tag").all_text_contents(),
            })
                
        page.screenshot(path=f"PRACTICE/quotes_page_{page_num}.png")                 # once per page
        
        if page_num < 3:                      # don't click Next on last page
            with page.expect_response("**/page/**") as response_info:
                page.get_by_role("link", name="Next").click()
            page.wait_for_url(re.compile(r"/page/\d+"))
            response_statuses.append(response_info.value.status)
        else:
            response_info = None
            print("Reached last page, no more navigation.")
        print(f"  Page {page_num}")
        print(f"      Total Quotes: {len(quotes_data)}")
        print(f"      Unique authors: {len(set(q['author'] for q in quotes_data))}")
        print(f"      All Response statuses: {response_statuses}")
        print("")
    
    browser.close()
            

    
    