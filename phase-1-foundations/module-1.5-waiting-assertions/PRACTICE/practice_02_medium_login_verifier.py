"""
Module 1.5 — Practice 2 (Medium)
File: practice_02_medium_login_verifier.py
Date: 2026-04-09

TASK:
=====
Build a "Login Verifier" that tests login with CORRECT and WRONG credentials,
using expect() to verify every step.

TEST A — Correct Login:
1. Buka https://the-internet.herokuapp.com/login
2. Use expect() to verify:
   - Page title contains "The Internet"
   - Username input is visible and editable
   - Login button is enabled
3. Fill username "tomsmith", password "SuperSecretPassword!"
4. Click Login button using get_by_role()
5. Use expect() to verify after login:
   - URL contains "/secure"
   - Flash message is visible
   - Flash message contains "You logged into a secure area!"

TEST B — Wrong Login:
1. Buka https://the-internet.herokuapp.com/login (fresh)
2. Fill username "wronguser", password "wrongpass"
3. Click Login
4. Use expect() to verify after failed login:
   - URL still contains "/login" (did NOT redirect)
   - Flash message is visible
   - Flash message contains "Your username is invalid!"

Print summary:
   ===== LOGIN VERIFIER =====
   Test A (correct login): ALL ASSERTIONS PASSED ✅
   Test B (wrong login): ALL ASSERTIONS PASSED ✅

REQUIREMENTS:
- Use expect() for EVERY verification (minimum 6 expect() calls per test)
- Use get_by_role() and get_by_label() for finding elements
- Use re.compile() for URL pattern matching
- Use to_contain_text() for flash messages (not to_have_text — flash has extra whitespace)

HINTS:
- expect(page).to_have_title(re.compile(r"The Internet"))
- expect(page).to_have_url(re.compile(r"/secure"))
- expect(locator).to_contain_text("You logged into")
- Flash message: page.locator("#flash")
"""

# Write your code below this line
# ============================================================================

from playwright.sync_api import sync_playwright, expect
import re

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    
    print("TEST A")
    page.goto("https://the-internet.herokuapp.com/login")
    title_a = page.title()
    expect(page).to_have_title(re.compile(r"The Internet"))
    label_username = page.get_by_label("Username")
    expect(label_username).to_be_visible()
    expect(label_username).to_be_editable()
    login_button = page.get_by_role("button", name="Login")
    expect(login_button).to_be_enabled()
    page.locator("input#username").fill("tomsmith")
    page.locator("input#password").fill("SuperSecretPassword!")
    login_button = page.get_by_role("button", name="Login")
    login_button.click()
    flash_message = page.locator("#flash")
    expect(page).to_have_url(re.compile(r"/secure"))
    expect(flash_message).to_be_visible()
    expect(flash_message).to_contain_text("You logged into a secure area!")


    print("TEST B")
    page.goto("https://the-internet.herokuapp.com/login")
    
    title_b = page.title()
    expect(page).to_have_title(re.compile(r"The Internet"))
    username_label = page.get_by_label("Username")
    expect(username_label).to_be_visible()
    expect(username_label).to_be_editable()
    button_login = page.get_by_role("button", name="Login")
    expect(button_login).to_be_enabled()
    
    page.locator("input#username").fill("wronguser")
    page.locator("input#password").fill("wrongpass")
    login_button = page.get_by_role("button", name="Login")
    login_button.click()
    expect(page).to_have_url(re.compile(r"/login"))
    expect(flash_message).to_be_visible()
    expect(flash_message).to_contain_text("Your username is invalid!")


    print("===== LOGIN VERIFIER =====")
    print(f"Test A (correct login): ALL ASSERTIONS PASSED ✅")
    print(f"Test B (incorrect login): ALL ASSERTIONS PASSED ✅")

    browser.close()
    
    

    