"""
Module 1.3 — Practice 3 (Hard)
File: practice_03_hard_herokuapp_explorer.py
Date: 2026-04-09

TASK:
=====
Buat "Herokuapp Feature Explorer" yang otomatis test beberapa halaman
di the-internet.herokuapp.com dan generate report.

Harus test halaman berikut (dalam satu script, satu browser):

1. HOVER TEST — https://the-internet.herokuapp.com/hovers
   - Hover over semua 3 user profiles
   - Extract nama yang muncul setelah hover (h5 element di dalam .figure)
   - Simpan ke results

2. LOGIN TEST — https://the-internet.herokuapp.com/login
   - Login dengan username "tomsmith", password "SuperSecretPassword!"
   - Submit pakai page.press() Enter (BUKAN click)
   - Verify: extract flash message
   - Simpan success/fail ke results

3. DROPDOWN TEST — https://the-internet.herokuapp.com/dropdown
   - Select semua options satu per satu (Option 1, lalu Option 2)
   - Untuk setiap selection, record: label yang dipilih dan value-nya
   - Simpan ke results

4. CHECKBOX TEST — https://the-internet.herokuapp.com/checkboxes
   - Record initial state of both checkboxes
   - Toggle both (check yang unchecked, uncheck yang checked)
   - Record final state
   - Simpan ke results

5. Print SUMMARY REPORT di akhir:

   ===== HEROKUAPP EXPLORER REPORT =====

   HOVER TEST:
     Profile 1: user1
     Profile 2: user2
     Profile 3: user3

   LOGIN TEST:
     Status: SUCCESS
     Message: You logged into a secure area!

   DROPDOWN TEST:
     Option 1 → value: 1
     Option 2 → value: 2

   CHECKBOX TEST:
     Checkbox 1: unchecked → checked
     Checkbox 2: checked → unchecked

   Tests completed: 4/4

REQUIREMENTS:
- Satu browser, satu page (reuse untuk semua tests)
- Gunakan headless mode
- Collect ALL results ke satu dictionary atau list, print summary di akhir
- Gunakan page.locator() dan .nth() untuk checkboxes dan hover profiles
- Gunakan page.press() untuk login (bukan click)
- Handle hover properly — hover dulu baru extract text

HINTS:
- Hover profiles: page.locator(".figure") → loop with .nth(i) → .hover() → get h5 text
- Flash message: page.locator("#flash").text_content().strip()
- Dropdown value: page.input_value("#dropdown")
- Checkboxes: page.locator("input[type='checkbox']").nth(0).is_checked()
- Use a dict like: results = {"hover": [], "login": {}, "dropdown": [], "checkbox": {}}
"""

# Write your code below this line
# ============================================================================

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    results = {"hover": [], "login": {}, "dropdown": [], "checkbox": {}}
    
    # HOVER TEST
    page.goto("https://the-internet.herokuapp.com/hovers")
    for i in range(3):
        profile = page.locator(".figure").nth(i)
        profile.hover()
        name = profile.locator("h5").text_content().strip()
        results["hover"].append(name)
    
    # LOGIN TEST
    page.goto("https://the-internet.herokuapp.com/login")
    page.fill("input#username", "tomsmith")
    page.fill("input#password", "SuperSecretPassword!")
    page.press("input#password", "Enter")
    
    flash_message = page.locator("#flash").text_content().strip()
    results["login"]["status"] = "SUCCESS" if "You logged into a secure area!" in flash_message else "FAIL"
    results["login"]["message"] = flash_message
    
    # DROPDOWN TEST
    page.goto("https://the-internet.herokuapp.com/dropdown")
    for option in ["Option 1", "Option 2"]:
        page.select_option("#dropdown", label=option)
        value = page.input_value("#dropdown")
        results["dropdown"].append({"label": option, "value": value})
    
    # CHECKBOX TEST
    page.goto("https://the-internet.herokuapp.com/checkboxes")
    checkbox1 = page.locator("input[type='checkbox']").nth(0)
    checkbox2 = page.locator("input[type='checkbox']").nth(1)
    
    initial_state1 = "checked" if checkbox1.is_checked() else "unchecked"
    initial_state2 = "checked" if checkbox2.is_checked() else "unchecked"
    
    checkbox1.check()  # Check the first checkbox
    checkbox2.uncheck()  # Uncheck the second checkbox
    
    final_state1 = "checked" if checkbox1.is_checked() else "unchecked"
    final_state2 = "checked" if checkbox2.is_checked() else "unchecked"
    
    results["checkbox"]["checkbox1"] = f"{initial_state1} → {final_state1}"
    results["checkbox"]["checkbox2"] = f"{initial_state2} → {final_state2}"
    
    # Print SUMMARY REPORT
    print("===== HEROKUAPP EXPLORER REPORT =====")
    print("\nHOVER TEST:")
    for idx, name in enumerate(results["hover"], start=1):
        print(f"  Profile {idx}: {name}")
    print("\nLOGIN TEST:")
    print(f"  Status: {results['login']['status']}")
    print(f"  Message: {results['login']['message']}")
    print("\nDROPDOWN TEST:")
    for option in results["dropdown"]:
        print(f"  {option['label']} → value: {option['value']}")
    print("\nCHECKBOX TEST:")
    print(f"  Checkbox 1: {results['checkbox']['checkbox1']}")
    print(f"  Checkbox 2: {results['checkbox']['checkbox2']}")
    print("\nTests completed: 4/4")
    