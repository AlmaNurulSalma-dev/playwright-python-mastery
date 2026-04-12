"""
Module 1.2 — Practice 2 (Medium)
File: practice_02_medium_isolation_proof.py
Date: 2026-04-09

TASK:
=====
Buktikan bahwa contexts itu ISOLATED tapi pages dalam context yang SAMA itu SHARING.

1. Launch Chromium (headless)
2. Buat 2 contexts: context_login dan context_guest
3. Di context_login:
   a. Buat page, buka https://quotes.toscrape.com/login
   b. Login dengan username "admin", password "admin"
   c. Setelah login, buat page KEDUA di context_login yang SAMA
   d. Buka https://quotes.toscrape.com di page kedua ini
4. Di context_guest:
   a. Buat page, buka https://quotes.toscrape.com
5. Print comparison report:

   ===== ISOLATION PROOF =====
   
   Context: LOGIN
     Page 1 (logged in manually): [cookies count] cookies
     Page 2 (same context, no login): [cookies count] cookies
     → Pages share cookies? YES (same count!)
   
   Context: GUEST
     Page 1 (never logged in): [cookies count] cookies
   
   Cross-context isolated? YES (login cookies != guest cookies)

6. Close browser

REQUIREMENTS:
- Gunakan context.cookies() untuk dapetin cookies
- Buktikan page 2 di context_login punya cookies SAMA dengan page 1
  (karena mereka share context)
- Buktikan context_guest punya cookies BERBEDA dari context_login
- Print cookie counts, bukan isi cookiesnya

HINTS:
- Setelah login, cookies otomatis ada di context (bukan di page)
- Page baru di context yang sama langsung "inherit" cookies
- len(context.cookies()) untuk count
"""

# Write your code below this line
# ============================================================================

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    context_login = browser.new_context()
    page_login1 = context_login.new_page()
    page_login1.goto("https://quotes.toscrape.com/login")
    page_login1.fill("input#username", "admin")
    page_login1.fill("input#password", "admin")
    page_login1.click("input[type='submit']")
    
    page_login2 = context_login.new_page()
    page_login2.goto("https://quotes.toscrape.com")
    
    context_guest = browser.new_context()
    page_guest = context_guest.new_page()
    page_guest.goto("https://quotes.toscrape.com")
    
    print("\n===== ISOLATION PROOF =====")
    print("\nContext: LOGIN")
    print(f"  Page 1 (logged in manually): {len(context_login.cookies())} cookies")
    print(f"  Page 2 (same context, no login): {len(context_login.cookies())} cookies")
    print(f"  → Pages share cookies? {'YES' if len(context_login.cookies()) == len(context_login.cookies()) else 'NO'}")
    
    print("\nContext: GUEST")
    print(f"  Page 1 (never logged in): {len(context_guest.cookies())} cookies")
    print(f"  → Cross-context isolated? {'YES' if len(context_guest.cookies()) != len(context_login.cookies()) else 'NO'}")
    browser.close()
    
    