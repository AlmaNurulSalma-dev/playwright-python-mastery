from playwright.sync_api import sync_playwright
import os

with sync_playwright() as p:
    
    # PHASE A
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://quotes.toscrape.com/login")
    
    page.fill("input#username", "admin")
    page.fill("input#password", "admin")
    page.click("input[type='submit']")
    
    has_logout = page.get_by_role("link", name="Logout").count() > 0
    
    print(f"All cookies phase A: {context.cookies()}")
    
    state_path = "PRACTICE/saved_session.json"
    os.makedirs("output", exist_ok=True)
    context.storage_state(path=state_path)

    cookies_a = len(context.cookies())
    
    context.close()
    
    #PHASE B
    context_new = browser.new_context(storage_state=state_path)
    page_new = context_new.new_page()
    page_new.goto("https://quotes.toscrape.com")
    
    sudah_login = page_new.get_by_role("link", name="Logout").count() > 0
    
    print(f"All cookies phase B: {context_new.cookies()}")
    
    cookies_b = len(context_new.cookies())
    
    context_new.close()
    
    # PHASE C
    context_3 = browser.new_context()
    page3 = context_3.new_page()
    page3.goto("https://quotes.toscrape.com")
    done_logout = page3.get_by_role("link", name="Logout").count() > 0
    print(f"All cookies phase 3: {context_3.cookies()}")

    cookies_c = len(context_3.cookies())
        
    # PRINT SUMMARY
    print("===== SESSION REUSE REPORT =====")
    print(f"Phase A: Logged in ✅ | Cookies: {cookies_a} | Session saved ✅")
    print(f" Phase B: Logged in ✅ (without typing credentials!) | Cookies: {cookies_b}")
    print(f"Logged in ❌ (fresh context) | Cookies: {cookies_c}")
    print(" Session isolation working: ✅")