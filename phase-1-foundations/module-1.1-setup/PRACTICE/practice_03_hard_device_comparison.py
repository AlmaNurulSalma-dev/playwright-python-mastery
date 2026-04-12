# """
# Module 1.1 — Practice 3 (Hard)
# File: practice_03_hard_device_comparison.py
# Date: 2026-04-09

# TASK:
# =====
# Buat sebuah "Cross-Device Screenshot Comparison Tool" yang:

# 1. Definisikan 3 device configurations:
#    a. Desktop  → viewport: 1920x1080, TANPA device emulation
#    b. Tablet   → gunakan p.devices["iPad Pro 11"]
#    c. Mobile   → gunakan p.devices["iPhone 13"]

# 2. Untuk SETIAP device config:
#    a. Launch Chromium dalam HEADLESS mode
#    b. Buat context dengan viewport/device settings yang sesuai
#    c. Buka https://books.toscrape.com
#    d. Ambil FULL PAGE screenshot (hint: ada parameter untuk ini!)
#    e. Print informasi: device name, viewport size, page title, dan URL
#    f. Close browser

# 3. Setelah semua selesai, print summary:

#    ============ DEVICE COMPARISON ============
#    Device       Viewport          Title
#    desktop      1920 x 1080       All products | Books to Scrape - Sandbox
#    tablet       834 x 1194        All products | Books to Scrape - Sandbox
#    mobile       390 x 844         All products | Books to Scrape - Sandbox

# 4. Simpan semua screenshots dengan format: "device_{device_name}.png"

# REQUIREMENTS:
# - Gunakan loop (JANGAN copy-paste code 3 kali)
# - Untuk desktop, kamu perlu set viewport MANUAL via new_context(viewport={...})
# - Untuk tablet dan mobile, gunakan p.devices dan unpack dengan **
# - Gunakan full_page=True untuk screenshot
# - Handle the fact that desktop doesn't use p.devices differently from tablet/mobile
#   (hint: kamu bisa bikin list of dicts dengan config yang berbeda-beda)

# HINTS:
# - Desktop context: browser.new_context(viewport={"width": 1920, "height": 1080})
# - Device context: browser.new_context(**p.devices["iPhone 13"])
# - Think about how to structure your configs so the loop can handle both cases
# - page.viewport_size gives you the current viewport as a dict
# """

# # Write your code below this line
# # ============================================================================

from playwright.sync_api import sync_playwright

URL = "https://books.toscrape.com"
SCREENSHOT_DIR = "phase-1-foundations/module-1.1-setup/PRACTICE"

with sync_playwright() as p:
    
    device_configs = [
        {"name": "desktop", "viewport": {"width": 1920, "height": 1080}, "device": None},
        {"name": "tablet", "viewport": None, "device": p.devices["iPad Pro 11"]},
        {"name": "mobile", "viewport": None, "device": p.devices["iPhone 13"]}
    ]
    
    results = []
    
    for config in device_configs:
        print(f"===== Testing: {config['name'].upper()} =====")
    
        browser = p.chromium.launch(headless=True)
        if config["device"] is None:
            context = browser.new_context(viewport=config["viewport"])
        else:
            context = browser.new_context(**config["device"])
            
        page = context.new_page()
        page.goto(URL)
        
        page.screenshot(path=f"{SCREENSHOT_DIR}/device_{config['name']}.png", full_page=True)
        
        results.append({
            "device": config["name"],
            "viewport": page.viewport_size,
            "title": page.title(),
            "url": page.url
        })
        
        print(f"Device: {config['name']}")
        print(f"Viewport: {page.viewport_size}")
        print(f"Title: {page.title()}")
        print(f"URL: {page.url}")
        
        browser.close()
        
    print(f"=========== DEVICE COMPARISON ===========")
    print(f"{'Device':<12} {'Viewport':<15} {'Title':<50}")        
    print(f"{'-'*77}")
        
    for result in results:
        print(f"{result['device']:<12} {result['viewport']['width']} x {result['viewport']['height']:<10} {result['title'][:50]:<50}")
    