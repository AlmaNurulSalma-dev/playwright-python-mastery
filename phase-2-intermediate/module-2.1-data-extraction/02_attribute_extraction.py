"""
Module 2.1 — Data Extraction Mastery
File: 02_attribute_extraction.py
Description: Extracting attributes — href, src, data-*, class, and more
Date: 2026-04-26
Phase: 2 - Intermediate
Playwright Docs: https://playwright.dev/python/docs/locators#get-attribute
"""

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=300)
    page = browser.new_page()

    # ====================================================================
    # get_attribute() — Extract any HTML attribute
    # ====================================================================
    print("=== get_attribute() BASICS ===\n")

    page.goto("https://quotes.toscrape.com")

    # Extract href from link
    # <a href="/page/2/">Next</a>
    next_link = page.get_by_role("link", name="Next")
    href = next_link.get_attribute("href")
    print(f"  Next link href: {href}")

    # Extract href from author links
    first_author_link = page.locator(".quote").first.locator("a[href*='author']").first
    author_href = first_author_link.get_attribute("href")
    print(f"  Author link href: {author_href}")

    # ====================================================================
    # EXTRACTING FROM MULTIPLE ELEMENTS
    # ====================================================================
    print("\n=== EXTRACT FROM MULTIPLE ELEMENTS ===\n")

    # Get ALL author links on the page
    author_links = page.locator("a[href*='author']").all()
    print(f"  Found {len(author_links)} author links:")

    seen = set()
    for link in author_links:
        href = link.get_attribute("href")
        text = link.text_content().strip()
        if href not in seen:
            seen.add(href)
            print(f"    {text} → {href}")

    # ====================================================================
    # EXTRACTING TAG LINKS — Building full URLs
    # ====================================================================
    print("\n=== BUILDING FULL URLS ===\n")

    # Tags have relative URLs like "/tag/love/"
    # We need to build full URL: "https://quotes.toscrape.com/tag/love/"
    base_url = "https://quotes.toscrape.com"

    tag_links = page.locator(".tag").all()
    print(f"  Found {len(tag_links)} tags on page:")
    for i, tag in enumerate(tag_links[:5]):  # first 5 only
        tag_text = tag.text_content()
        tag_href = tag.get_attribute("href")
        full_url = base_url + tag_href
        print(f"    {i+1}. '{tag_text}' → {full_url}")

    # ====================================================================
    # EXTRACTING FROM BOOKS.TOSCRAPE.COM — More complex
    # ====================================================================
    print("\n=== BOOKS.TOSCRAPE.COM ===\n")

    page.goto("https://books.toscrape.com")

    # Extract book data: title, price, rating, image, link
    books = page.locator("article.product_pod").all()
    print(f"  Found {len(books)} books\n")

    books_data = []
    for book in books[:5]:  # first 5 only
        # Title is in the <a> tag's title attribute!
        # <a href="..." title="A Light in the Attic">
        title = book.locator("h3 a").get_attribute("title")

        # Price
        price = book.locator(".price_color").text_content()

        # Rating — stored as a CSS class!
        # <p class="star-rating Three">
        rating_element = book.locator(".star-rating")
        rating_class = rating_element.get_attribute("class")
        # "star-rating Three" → extract "Three"
        rating = rating_class.split(" ")[-1]

        # Image source
        img_src = book.locator("img").get_attribute("src")

        # Book link (relative URL)
        book_href = book.locator("h3 a").get_attribute("href")

        books_data.append({
            "title": title,
            "price": price,
            "rating": rating,
            "image": img_src,
            "link": book_href,
        })

        print(f"  📚 {title}")
        print(f"     Price: {price}")
        print(f"     Rating: {rating} stars")
        print(f"     Image: {img_src}")
        print(f"     Link: {book_href}")
        print()

    # ====================================================================
    # COMMON ATTRIBUTES REFERENCE
    # ====================================================================
    print("""
=== COMMON ATTRIBUTES TO EXTRACT ===

Links:
  get_attribute("href")           → URL the link points to
  get_attribute("target")         → "_blank", "_self", etc.

Images:
  get_attribute("src")            → image URL
  get_attribute("alt")            → image description
  get_attribute("width")          → image width
  get_attribute("height")         → image height

Forms:
  get_attribute("type")           → "text", "password", "email", etc.
  get_attribute("name")           → form field name
  get_attribute("placeholder")    → placeholder text
  get_attribute("value")          → default value (use input_value() for current value!)
  get_attribute("disabled")       → "true" or None
  get_attribute("readonly")       → "true" or None

Data attributes:
  get_attribute("data-id")        → custom data
  get_attribute("data-price")     → custom data
  get_attribute("data-category")  → custom data

Style/Class:
  get_attribute("class")          → CSS classes
  get_attribute("id")             → element ID
  get_attribute("style")          → inline styles

NOTE: get_attribute() returns None if attribute doesn't exist!
  href = link.get_attribute("data-nonexistent")
  print(href)  # → None
""")

    browser.close()
    print("✅ Attribute extraction complete!")