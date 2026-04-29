from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    context1 = browser.new_context()

    # Open 3 tabs in the SAME context:
    sites = [
        {"name": "tab1", "url": "https://quotes.toscrape.com"},
        {"name": "tab2", "url": "https://books.toscrape.com"},
        {"name": "tab3", "url": "https://the-internet.herokuapp.com"},
    ]

    pages = {}
    for site in sites:
        pg = context1.new_page()
        pg.goto(site["url"])
        pages[site["name"]] = pg
        
    # extract data
    for page in pages:
        print(f"  Title: {pages[page].title()}")
        print(f"  URL: {pages[page].url}")
        print(f"  Number of links on the page: {pages[page].locator('a').count()}")
    
    # print report
    print("===== MULTI-TAB REPORT =====")
    print("Tab      Title                               URL                         Links")
    for page in pages:
        print(f"{page:<8} {pages[page].title():<35} {pages[page].url} {pages[page].locator('a').count()}")
    
    tab2_title = pages["tab2"].title()
    
    pages["tab2"].close()
    
    print(f"After closing {tab2_title}:")
    print(f"    Tabs remaining: {len(context1.pages)}")
    print(f"Tab 1 accessible: {'tab1' in pages and not pages['tab1'].is_closed()}")
    print(f"Tab 2 accessible: {'tab2' in pages and not pages['tab2'].is_closed()}")
