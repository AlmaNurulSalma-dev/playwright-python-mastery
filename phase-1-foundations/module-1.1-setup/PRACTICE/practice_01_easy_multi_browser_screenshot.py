# """
# Module 1.1 — Practice 1 (Easy)
# File: practice_01_easy_multi_browser_screenshot.py
# Date: 2026-04-09

# TASK:
# =====
# Buat script yang melakukan hal berikut:

# 1. Buka website https://books.toscrape.com menggunakan Chromium dalam HEADFUL mode
# 2. Print judul halaman dan URL-nya ke terminal
# 3. Ambil screenshot dan simpan di folder PRACTICE dengan nama "books_chromium.png"
# 4. Sekarang buka website yang SAMA menggunakan Firefox dalam HEADLESS mode
# 5. Ambil screenshot dan simpan dengan nama "books_firefox.png"
# 6. Print pesan "Done!" di akhir

# REQUIREMENTS:
# - Gunakan `with sync_playwright() as p:` (satu block saja, jangan dua)
# - Pastikan semua browser di-close dengan benar
# - Screenshot path harus relative ke folder PRACTICE ini

# HINTS:
# - Kamu bisa launch dan close multiple browsers dalam satu 'with' block
# - Ingat perbedaan headless=True dan headless=False
# """

# Write your code below this line
# ============================================================================

from playwright.sync_api import sync_playwright

URL = "https://books.toscrape.com"
SCREENSHOT_DIR = "phase-1-foundations/module-1.1-setup/PRACTICE"


with sync_playwright() as p:
    
    browsers = {
        "chromium": p.chromium,
        "firefox": p.firefox,
    }
    
    for name, browser_type in browsers.items():
        print(f"===== Testing: {name.upper()} =====")
        browser = browser_type.launch(headless=(name == "firefox"))
        page = browser.new_page()
        page.goto(URL)
        
        print(f"Title: {page.title()}")
        print(f"URL: {page.url}")
        
        page.screenshot(path=f"{SCREENSHOT_DIR}/books_{name}.png")
    
        browser.close()

print(f"DONE!")