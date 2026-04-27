"""
Module 2.1 — Practice 2 (Medium)
File: practice_02_medium_book_scraper.py
Date: 2026-04-21

TASK:
=====
Build a book data extractor for books.toscrape.com.

1. Buka https://books.toscrape.com
2. Extract ALL 20 books on page 1:
   - title (from <a> tag's title attribute — NOT text_content, karena text truncated!)
   - price (from .price_color text_content)
   - rating (from .star-rating class attribute — extract the word: "One", "Two", etc.)
   - image_url (from <img> tag's src attribute)
   - book_link (from <h3 a> tag's href attribute)
   - availability (from .availability text_content, stripped)

3. Convert rating words to numbers:
   One=1, Two=2, Three=3, Four=4, Five=5

4. Find and print:
   - Total books: 20
   - Highest rated book(s): title + rating
   - Lowest rated book(s): title + rating
   - Most expensive book: title + price
   - Cheapest book: title + price
   - Average price (convert "£XX.XX" to float for calculation)

5. Print all books sorted by rating (highest first):
   1. ⭐⭐⭐⭐⭐ A Light in the Attic — £51.77
   2. ⭐⭐⭐⭐  The Grand Design — £13.76
   ...

REQUIREMENTS:
- Use get_attribute("title") for full book title (NOT text_content)
- Use get_attribute("class") + string manipulation for rating
- Convert price string to float for comparison
- Use sorted() with key= for sorting
- Star emoji: "⭐" * rating_number

HINTS:
- Price to float: float(price.replace("£", ""))
- Rating map: {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
- Sort: sorted(books, key=lambda b: b["rating_num"], reverse=True)
- Stars: "⭐" * book["rating_num"]
"""

# Write your code below this line
# ============================================================================

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://books.toscrape.com")
    
    books_data = []
    books = page.locator("article.product_pod").all()
    for book in books:
        title = book.locator("h3 a").get_attribute("title")
        price = book.locator(".price_color").text_content()
        rating = book.locator(".star-rating").get_attribute("class").split(" ")[-1]
        image_url = book.locator("img").get_attribute("src")
        book_link = book.locator("h3 a").get_attribute("href")
        availability = book.locator(".availability").text_content().strip()
        
        books_data.append({
            "title": title,
            "price": price,
            "rating": rating,
            "image_url": image_url,
            "book_link": book_link,
            "availability": availability
        })
        
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    for book in books_data:
        book["rating_num"] = rating_map[book["rating"]]
        
    print(f"Total books: {len(books_data)}")
    print(f"Highest rated book(s): {max(books_data, key=lambda x: x['rating_num'])['title']}")
    print(f"Lowest rated book(s): {min(books_data, key=lambda x: x['rating_num'])['title']}")
    print(f"Most expensive book(s): {max(books_data, key=lambda x: float(x['price'][1:]))['title']}")
    print(f"Cheapest book(s): {min(books_data, key=lambda x: float(x['price'][1:]))['title']}")
    print(f"Average price: {sum(float(book['price'][1:]) for book in books_data) / len(books_data):.2f}")
    
    print("Books sorted by rating highet to lowest")
    for book in sorted(books_data, key=lambda x: x['rating_num'], reverse=True):
        print(f"  {book['title']} - {book['rating']} stars - {book['price']}")
        