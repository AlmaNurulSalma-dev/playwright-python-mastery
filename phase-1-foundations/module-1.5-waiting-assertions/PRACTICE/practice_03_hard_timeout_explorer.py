from playwright.sync_api import sync_playwright, expect
import re

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    
    DEFAULT_TIMEOUT = 10000
    NAV_TIMEOUT = 15000
    EXPECT_TIMEOUT = 8000
    
    #TIMEOUT HIERARCHY TEST:
    page.set_default_timeout(DEFAULT_TIMEOUT)
    page.goto("https://quotes.toscrape.com", timeout=NAV_TIMEOUT)
    expect.set_options(timeout=EXPECT_TIMEOUT)
    
    expect(page).to_have_title(re.compile(r"Quotes.*"))
    next_link = page.get_by_role("link", name="Next")
    next_link.click()
    
    print(f"timeouts: default={DEFAULT_TIMEOUT} navigation={NAV_TIMEOUT} expect={EXPECT_TIMEOUT}")
    
    #PER-ACTION OVERRIDE TEST:
    next_link.click(timeout=3000)
    expect(page).to_have_url(re.compile(r"page/2"), timeout=2000)
    print(f"Override: click used 3s, expect used 2s (not page defaults)")
    
    #TIMEOUT ERROR HANDLING:
    try:
        page.click("#nonexistent-element", timeout=2000)
    except Exception as e1:
        print(f"Timeout error caught: {e1}")
        
    try: 
        expect(page).to_have_title("ini title bohongan aja yg sebetulnya gaada", timeout=2000)
    except Exception as e2:
        print(f"Timeout error caught: {e2}")
        
    print("Both errors caught — script continues!")

    #RESET AND VERIFY:
    page.set_default_timeout(30000)
    page.set_default_navigation_timeout(30000)
    expect.set_options(timeout=5000)
    
    print(f"After reset: default={DEFAULT_TIMEOUT} navigation={NAV_TIMEOUT} expect={EXPECT_TIMEOUT}")
    
    #Print full report:
    print("===== TIMEOUT EXPLORER REPORT =====")
    print("HIERARCHY TEST:")
    print(f"  Default: {DEFAULT_TIMEOUT}")
    print(f"  Navigation default: {NAV_TIMEOUT}")
    print(f"  Expect default: {EXPECT_TIMEOUT}")
    print("All actions completed with custom timeouts ✅")
    
    print("OVERRIDE TEST:")
    print(f"  click(timeout={3000}): Override page default")
    print(f"  expect(timeout={2000}): Overrides global expect")
    
    print("ERROR HANDLING:")
    print(f"  Action timeout caught: {e1}")
    print(f"  Expect timeout caught: {e2}")
    
    print("Reset:")
    print("All timeouts restored to defaults ✅")

    browser.close()
    
    