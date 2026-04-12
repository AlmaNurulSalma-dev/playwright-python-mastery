"""
Module 1.2 — Architecture Deep Dive
File: 03_sync_vs_async.py
Description: Understanding sync vs async API - when and why to use each
Date: 2026-04-09
Phase: 1 - Foundations
Playwright Docs: https://playwright.dev/python/docs/library#sync-api
"""

import time
import asyncio
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright

URLS = [
    "https://quotes.toscrape.com",
    "https://books.toscrape.com",
    "https://quotes.toscrape.com/page/2/",
]

# ========================================================================
# SYNC API — One thing at a time (sequential)
#
# Think of it like a single cashier at a store:
#   Customer 1 → serve → done → Customer 2 → serve → done → ...
# ========================================================================

def run_sync():
    print("=" * 50)
    print("SYNC MODE — Sequential")
    print("=" * 50)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        for url in URLS:
            page.goto(url)
            title = page.title()
            print(f"  ✅ {title}")

        browser.close()


# ========================================================================
# ASYNC API — Multiple things simultaneously (concurrent)
#
# Think of it like 3 cashiers at a store:
#   Customer 1 → Cashier A ─┐
#   Customer 2 → Cashier B ─┼→ all served at the same time!
#   Customer 3 → Cashier C ─┘
# ========================================================================

async def run_async():
    print("\n" + "=" * 50)
    print("ASYNC MODE — Concurrent")
    print("=" * 50)

    async with async_playwright() as p:
        browser = await p.chromium.launch()

        # Create separate pages for each URL (concurrent workers)
        async def scrape_page(url):
            page = await browser.new_page()
            await page.goto(url)
            title = await page.title()
            print(f"  ✅ {title}")
            await page.close()

        # asyncio.gather() runs ALL tasks at the same time!
        await asyncio.gather(
            scrape_page(URLS[0]),
            scrape_page(URLS[1]),
            scrape_page(URLS[2]),
        )

        await browser.close()


# ========================================================================
# SPEED COMPARISON
# ========================================================================

# Time sync
start = time.time()
run_sync()
sync_time = time.time() - start
print(f"  ⏱️ Sync total: {sync_time:.2f}s")

# Time async
start = time.time()
asyncio.run(run_async())
async_time = time.time() - start
print(f"  ⏱️ Async total: {async_time:.2f}s")

# Results
print("\n" + "=" * 50)
print("COMPARISON")
print("=" * 50)
print(f"  Sync:  {sync_time:.2f}s (one page at a time)")
print(f"  Async: {async_time:.2f}s (all pages simultaneously)")
if async_time < sync_time:
    print(f"  🚀 Async was {sync_time/async_time:.1f}x faster!")

# ========================================================================
# KEY DIFFERENCES SUMMARY
# ========================================================================
print("""
╔═══════════════════════════════════════════════════════════════╗
║                   SYNC vs ASYNC CHEATSHEET                   ║
╠═══════════════════════════════════════════════════════════════╣
║                                                              ║
║  SYNC                          ASYNC                         ║
║  ─────────────────────         ─────────────────────         ║
║  from sync_api import          from async_api import         ║
║  with sync_playwright()        async with async_playwright() ║
║  browser = p.chromium.launch() browser = await p...launch()  ║
║  page.goto(url)                await page.goto(url)          ║
║  page.title()                  await page.title()            ║
║                                                              ║
║  WHEN TO USE:                  WHEN TO USE:                  ║
║  • Learning / prototyping      • Production scraping         ║
║  • Simple single-page tasks    • Multiple pages/sites        ║
║  • Quick scripts               • Speed matters               ║
║  • Easier to read/debug        • Scale matters               ║
║                                                              ║
║  HOW IT WORKS:                 HOW IT WORKS:                 ║
║  A → B → C (one by one)        A ─┐                          ║
║                                 B ─┼→ all at once            ║
║                                 C ─┘                          ║
╚═══════════════════════════════════════════════════════════════╝
""")