"""
Module 1.2 — Practice 3 (Hard)
File: practice_03_hard_multi_user_scraper.py
Date: 2026-04-09

TASK:
=====
Buat "Multi-User Scraper" yang simulate 3 users browsing simultaneously,
masing-masing dengan device dan viewport berbeda.

1. Launch Chromium (headless)
2. Define 3 user profiles:
   - User "alice": Desktop viewport (1920x1080), buka https://quotes.toscrape.com
   - User "bob": Tablet (gunakan p.devices["iPad Pro 11"]), buka https://quotes.toscrape.com/page/2/
   - User "charlie": Mobile (gunakan p.devices["iPhone 13"]), buka https://books.toscrape.com

3. Untuk SETIAP user:
   a. Buat context TERPISAH dengan viewport/device settings yang sesuai
   b. Buat page di context tersebut
   c. Navigate ke URL user tersebut
   d. Extract: page title, viewport size, user agent (via page.evaluate)
   e. Ambil screenshot: "user_{name}.png" di folder PRACTICE
   f. Close context (bukan browser — browser dipakai bareng!)

4. Print summary:

   ===== MULTI-USER SUMMARY =====
   User         Device     Viewport        Title
   alice        desktop    1920 x 1080     Quotes to Scrape
   bob          tablet     834 x 1194      Quotes to Scrape
   charlie      mobile     390 x 844       All products | ...

   Total contexts created: 3
   All isolated? YES (each user has own session)

5. Close browser

REQUIREMENTS:
- Gunakan list of dicts untuk user profiles (seperti Practice 3 Module 1.1)
- Satu browser saja, JANGAN launch browser per user
- Setiap user punya context SENDIRI (isolated sessions)
- Gunakan loop — jangan copy-paste code 3 kali
- Handle desktop (manual viewport) vs device (p.devices) dengan if/else
- Close CONTEXT di akhir setiap iteration, bukan browser

HINTS:
- Ini gabungan dari Module 1.1 (devices, viewport) + Module 1.2 (contexts)
- browser.new_context(viewport=...) untuk desktop
- browser.new_context(**p.devices[...]) untuk tablet/mobile
- Collect results ke list, print summary setelah loop
- browser.close() cuma sekali di paling akhir
"""

# Write your code below this line
# ============================================================================

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
   browser = p.chromium.launch(headless=True)
   
   users = [
      {"user": "alice", "device": "viewport", "viewport": (1920, 1080), "url": "https://quotes.toscrape.com"},
      {"user": "bob", "device": "iPad Pro 11", "url": "https://quotes.toscrape.com/page/2/"},
      {"user": "charlie", "device": "iPhone 13", "url": "https://books.toscrape.com"}
   ]
   
   results = []
   
   for user in users:
      if user["device"] == "viewport":
         context = browser.new_context(viewport={"width": user["viewport"][0], "height": user["viewport"][1]})
      else:
         context = browser.new_context(**p.devices[user["device"]])
      
      page = context.new_page()
      page.goto(user["url"])
      
      title = page.title()
      viewport_size = page.viewport_size
      user_agent = page.evaluate("() => navigator.userAgent")
      
      print(f"{user['user']} | {user['device']} | {viewport_size['width']} x {viewport_size['height']} | {title}")
      
      page.screenshot(path=f"PRACTICE/user_{user['user']}.png")
      
      results.append({
            "user": user["user"],
            "device": user["device"],
            "viewport": page.viewport_size,
            "title": page.title()
        })
      
      context.close()

   print("\n===== MULTI-USER SUMMARY =====")
   for result in results:
      print(f"{result['user']} | {result['device']} | {result['viewport']} | {result['title']}")
   print(f"Total contexts created: {len(results)}")
   
   print(f"All isolated? YES")
   browser.close()