# """
# Module 1.1 — Practice 2 (Medium)
# File: practice_02_medium_browser_benchmark.py
# Date: 2026-04-09

# TASK:
# =====
# Buat sebuah browser benchmark tool yang:

# 1. Test SEMUA 3 browser engines (Chromium, Firefox, WebKit)
# 2. Untuk SETIAP browser, lakukan:
#    a. Launch dalam HEADLESS mode
#    b. Buka https://quotes.toscrape.com
#    c. Ukur berapa lama waktu dari launch sampai page title berhasil diambil
#    d. Ambil User-Agent menggunakan page.evaluate()
#    e. Ambil screenshot dan simpan dengan format: "benchmark_{nama_browser}.png"
#    f. Close browser
# 3. Setelah semua browser di-test, print summary table seperti ini:

#    ============ BENCHMARK RESULTS ============
#    Browser      Time       User-Agent (first 50 chars)
#    chromium     1.23s      Mozilla/5.0 (Windows NT 10.0; Win64; x64) Appl...
#    firefox      1.45s      Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:1...
#    webkit       1.67s      Mozilla/5.0 (Windows NT 10.0; Win64; x64) Appl...
   
#    🏆 Fastest: chromium (1.23s)
#    🐢 Slowest: firefox (1.67s)

# REQUIREMENTS:
# - Gunakan dictionary dan loop (jangan copy-paste code 3 kali!)
# - Gunakan time.time() untuk mengukur waktu
# - Print results harus rapi dan aligned
# - Tampilkan browser tercepat DAN terlambat
# - Semua screenshot harus tersimpan di folder PRACTICE

# HINTS:
# - Ingat pattern: browsers = {"chromium": p.chromium, ...}
# - f-string formatting: f"{variable:<12s}" untuk left-align 12 chars
# - Simpan results ke list of dicts, lalu sort untuk cari min/max
# """

# # Write your code below this line
# # ============================================================================

import time
from playwright.sync_api import sync_playwright

URL = "https://quotes.toscrape.com"

with sync_playwright() as p:
    
    browsers = {
        "chromium": p.chromium,
        "firefox": p.firefox,
        "webkit": p.webkit,
    }
    
    benchmark_results = []

    for name, browser_type in browsers.items():
        start = time.time()
        
        browser = browser_type.launch(headless=False)
        page = browser.new_page()
        page.goto(URL)
        title = page.title()
        sisa_waktu = time.time() - start
        user_agent = page.evaluate("navigator.userAgent")
        
        SCREENSHOT_DIR = "phase-1-foundations/module-1.1-setup/PRACTICE"
        page.screenshot(path=f"{SCREENSHOT_DIR}/benchmark_{name}.png")
        
        benchmark_results.append({
            "browser": name,
            "time": sisa_waktu,
            "user_agent": user_agent
        })
        
        browser.close()
        
    print(f"=========== BENCHMARK RESULTS ===========")
    print(f"{'Browser':<12} {'Time':<10} {'User-Agent (first 50 chars)':<50}")
    print(f"{'-'*70}")
    
    for result in benchmark_results:
        print(f"{result['browser']:<12} {result['time']:<10.2f}s {result['user_agent'][:50]:<50}")
    
    fastest = min(benchmark_results, key=lambda x: x['time'])
    slowest = max(benchmark_results, key=lambda x: x['time'])
    
    print(f"\n Fastest: {fastest['browser']} ({fastest['time']:.2f}s)")
    print(f" Slowest: {slowest['browser']} ({slowest['time']:.2f}s)")