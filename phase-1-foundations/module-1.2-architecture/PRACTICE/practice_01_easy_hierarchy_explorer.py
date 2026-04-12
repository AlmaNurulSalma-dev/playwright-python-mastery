"""
Module 1.2 — Practice 1 (Easy)
File: practice_01_easy_hierarchy_explorer.py
Date: 2026-04-09

TASK:
=====
Buat script yang mendemonstrasikan 3-layer hierarchy Playwright:

1. Launch Chromium (headful, slow_mo=500)
2. Buat 1 context
3. Di dalam context itu, buat 2 pages:
   - Page 1: buka https://quotes.toscrape.com
   - Page 2: buka https://books.toscrape.com
4. Print hierarchy report seperti ini:

   ===== HIERARCHY REPORT =====
   Browser version: XXX
   Total contexts: 1
     Context 0: 2 page(s)
       Page 0: Quotes to Scrape | https://quotes.toscrape.com/
       Page 1: All products | Books to Scrape ... | https://books.toscrape.com/

5. Close browser

REQUIREMENTS:
- Gunakan browser.contexts untuk akses semua contexts
- Gunakan context.pages untuk akses semua pages
- Gunakan nested loop (loop di dalam loop) untuk print hierarchy
- Setiap page harus print title DAN url

HINTS:
- browser.contexts returns list of contexts
- context.pages returns list of pages
- enumerate() bisa bantu untuk dapetin index
"""

# Write your code below this line
# ============================================================================

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    context = browser.new_context()
    
    page1 = context.new_page()
    page1.goto("https://quotes.toscrape.com")
    
    page2 = context.new_page()
    page2.goto("https://books.toscrape.com")
    
    print("\n===== HIERARCHY REPORT =====")
    print(f"Browser version: {browser.version}")
    print(f"Total contexts: {len(browser.contexts)}")
    for ctx_index, ctx in enumerate(browser.contexts):
        print(f"  Context {ctx_index}: {len(ctx.pages)} page(s)")
        for page_index, page in enumerate(ctx.pages):
            print(f"    Page {page_index}: {page.title()} | {page.url}")

    browser.close()

