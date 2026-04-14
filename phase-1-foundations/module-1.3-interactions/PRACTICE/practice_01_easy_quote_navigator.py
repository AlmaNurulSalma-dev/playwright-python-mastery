"""
Module 1.3 — Practice 1 (Easy)
File: practice_01_easy_quote_navigator.py
Date: 2026-04-09

TASK:
=====
Buat script yang navigate through quotes.toscrape.com:

1. Buka https://quotes.toscrape.com (headful, slow_mo=500)
2. Print judul halaman dan URL
3. Click link "Next" untuk ke page 2
4. Print URL page 2
5. Click "Next" lagi untuk ke page 3
6. Print URL page 3
7. Go back ke page 2 (pakai go_back)
8. Print URL — buktikan kamu di page 2
9. Go back lagi ke page 1
10. Reload page 1
11. Print "Navigation complete!"

REQUIREMENTS:
- Gunakan page.click() dengan text selector untuk click "Next"
- Gunakan page.go_back() untuk navigate back
- Gunakan page.reload()
- Print URL di setiap langkah supaya bisa di-verify

HINTS:
- Text selector: "a:text('Next')"
- page.url adalah property (tanpa parentheses)
"""

# Write your code below this line
# ============================================================================

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    
    browser = p.chromium.launch(headless=False, slow_mo = 500)
    page = browser.new_page()
    
    page.goto("https://quotes.toscrape.com")
    
    print(f"Title: {page.title()}")
    print(f"URL: {page.url}")
    
    page.click("a:text('Next')")
    print(f"URL page 2: {page.url}")
    
    page.click("a:text('Next')")
    print(f"URL page 3: {page.url}")
    
    page.go_back()
    print(f"URL after going back: {page.url}")
    
    page.go_back()
    
    page.reload()
    print("Navigation complete!")
    
    browser.close()
    