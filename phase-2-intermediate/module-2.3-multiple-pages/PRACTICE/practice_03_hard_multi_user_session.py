from playwright.sync_api import sync_playwright, expect
import json
import os

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=300)
    contexta = browser.new_context()
    pagea = contexta.new_page()
    contextb = browser.new_context()
    pageb = contextb.new_page()

    pagea.goto("https://quotes.toscrape.com/login")
    pagea.fill("input#username", "admin")
    pagea.fill("input#password", "admin")
    pagea.click("input[type='submit']")
    
    logged_in_a = pagea.get_by_role("link", name="Logout").count() > 0
    print(f"Context A logged in: {logged_in_a}")
    
    pageb.goto("https://quotes.toscrape.com")
    logged_in_b = pageb.get_by_role("link", name="Logout").count() > 0
    print(f"Context B logged in: {logged_in_b}")
    
    pagea.goto("https://quotes.toscrape.com/page/2")
    pageb.goto("https://quotes.toscrape.com/page/3")
    
    quotes_data = []
    quote_in_a = pagea.locator(".quote").all()
    quote_in_b = pageb.locator(".quote").all()
    for quote in quote_in_a:
        text = quote.locator(".text").inner_text()
        author = quote.locator(".author").inner_text()
        quotes_data.append({"context": "A", "text": text, "author": author})
    
    # Verify they're on different pages using expect() with URL
    expect(pagea).to_have_url("https://quotes.toscrape.com/page/2")
    expect(pageb).to_have_url("https://quotes.toscrape.com/page/3")
    
    contexta.storage_state(path="PRACTICE/admin_session.json")

    contexta.close()
    contextb.close()
    
    contextc = browser.new_context(storage_state="PRACTICE/admin_session.json")
    pagec = contextc.new_page()
    pagec.goto("https://quotes.toscrape.com")
    logged_in_c = pagec.get_by_role("link", name="Logout").count() > 0
    
    contextd = browser.new_context()
    paged = contextd.new_page()
    paged.goto("https://quotes.toscrape.com")
    logged_in_d = paged.get_by_role("link", name="Logout").count() > 0
    print(f"Context D logged in: {logged_in_d}")
    
    #popup handling
    contexte = browser.new_context()
    pagee = contexte.new_page()
    pagee.goto("https://the-internet.herokuapp.com/windows")
    
    with pagee.expect_popup() as popup_info:
        pagee.get_by_role("link", name="Click Here").click()
    popup = popup_info.value
    popup_text = popup.locator("h3").text_content()
    popup.close()
        
    print("===== MULTI-USER SESSION MANAGER =====")
    print("STEP 1 - User Setup:")
    print(f"  Admin logged in: {logged_in_a}")
    print(f"  Guest logged in: {logged_in_b}")
    print(f"  Isolated sessions: {logged_in_a != logged_in_b}")
    
    print("STEP 2 - Parallel Browsing:")
    print(f"  Admin (page 2): {len(quote_in_a)} quotes extracted")
    print(f"  Guest (page 3): {len(quote_in_b)} quotes extracted")
    print(f"  On different pages: {logged_in_a != logged_in_b}")
    
    print("STEP 3 - Session Saved:")
    print(f"   Admin session saved to: PRACTICE/admin_session.json")
    
    print("STEP 4 - Session Restored:")
    print(f"    Restored admin logged in: {logged_in_c == True}")
    print(f"   Fresh context logged in: {logged_in_d == True}")
    
    print("STEP 5 - Popup")
    print(f"  Popup text: {popup_text}")
    
    