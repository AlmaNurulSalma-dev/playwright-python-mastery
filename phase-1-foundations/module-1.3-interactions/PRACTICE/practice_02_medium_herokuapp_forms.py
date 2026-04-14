"""
Module 1.3 — Practice 2 (Medium)
File: practice_02_medium_herokuapp_forms.py
Date: 2026-04-09

TASK:
=====
Interact with multiple form elements di the-internet.herokuapp.com.
Script ini harus mengerjakan 3 tasks secara berurutan:

TASK A — Login:
1. Buka https://the-internet.herokuapp.com/login
2. Fill username "tomsmith" dan password "SuperSecretPassword!"
3. Submit form menggunakan keyboard (press Enter, JANGAN click button)
4. Print flash message yang muncul setelah login (pakai locator + text_content)
5. Print URL setelah login

TASK B — Dropdown:
1. Buka https://the-internet.herokuapp.com/dropdown
2. Select "Option 1" menggunakan VALUE
3. Print current selected value (pakai page.input_value)
4. Select "Option 2" menggunakan LABEL
5. Print current selected value

TASK C — Checkboxes:
1. Buka https://the-internet.herokuapp.com/checkboxes
2. Print status awal kedua checkboxes (checked atau unchecked)
3. Check checkbox 1 (yang awalnya unchecked)
4. Uncheck checkbox 2 (yang awalnya checked)
5. Print status akhir kedua checkboxes
6. Check checkbox 1 LAGI — buktikan bahwa check() tidak toggle
7. Print status final

REQUIREMENTS:
- Satu browser, satu context, satu page (reuse page untuk semua tasks)
- Gunakan page.press() untuk submit login (bukan click)
- Gunakan page.locator().nth() untuk checkboxes
- Print clear labels supaya output mudah dibaca

HINTS:
- Flash message selector: "#flash"
- locator.text_content() untuk dapetin text
- locator.is_checked() untuk cek checkbox state
- page.input_value(selector) untuk dapetin current dropdown value
"""

# Write your code below this line
# ============================================================================

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()
     
    # TASK A
    page.goto("https://the-internet.herokuapp.com/login")
     
    page.fill("input#username", "tomsmith")
    page.fill("input#password", "SuperSecretPassword!")
     
    page.press("input#password", "Enter")
    
    element = page.locator("#flash")
     
    print(f"Flash message: {element.text_content()}") #Print flash message yang muncul setelah login (pakai locator + text_content)
    print(f"URL after login: {page.url}")
     
     
    # TASK B
    
    page.goto("https://the-internet.herokuapp.com/dropdown")
    page.select_option("#dropdown", value="1")
    print(f"Current selected value: {page.input_value('#dropdown')}")
    
    page.select_option("#dropdown", label="Option 2")
    print(f"Current selected value: {page.input_value('#dropdown')}")
    
    
    # TASK C
    page.goto("https://the-internet.herokuapp.com/checkboxes")
    checkbox1 = page.locator("input[type='checkbox']").nth(0)
    checkbox2 = page.locator("input[type='checkbox']").nth(1)
    print(checkbox1.is_checked())
    print(checkbox2.is_checked())
    
    checkbox1.check()
    checkbox2.uncheck()
    print(f"Checkbox 1 status after check(): {checkbox1.is_checked()}")
    print(f"Checkbox 2 status after uncheck(): {checkbox2.is_checked()}")
    
    checkbox1.check() 
    print(f"Checkbox 1 status after check() again: {checkbox1.is_checked()}") 
    
    browser.close()