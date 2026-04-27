# Module 2.1 — Data Extraction Mastery

## Text Extraction Methods

| Method | Returns | Use for |
|--------|---------|---------|
| `text_content()` | Raw text (ignores CSS) | Getting ALL text, even hidden |
| `inner_text()` | Rendered text (respects CSS) | Getting text user SEES |
| `inner_html()` | HTML inside element | Getting HTML structure |
| `input_value()` | Form input value | Reading input/select/textarea |
| `get_attribute(name)` | Attribute value | href, src, data-*, class, id |
| `all_text_contents()` | List of text (all matches) | Multiple elements at once |
| `all_inner_texts()` | List of rendered text | Multiple visible elements |

## text_content() vs inner_text()

```html

  Hello
  Hidden
  World

```

- `text_content()` → "Hello Hidden World" (includes hidden text)
- `inner_text()` → "Hello World" (respects CSS, skips hidden)

## Extracting Attributes

```python
# Get href from link
link.get_attribute("href")           # → "/page/2/"

# Get image source
img.get_attribute("src")             # → "images/photo.jpg"

# Get data attributes
element.get_attribute("data-id")     # → "12345"
element.get_attribute("data-price")  # → "29.99"

# Get class list
element.get_attribute("class")       # → "product featured sale"
```

## JavaScript Evaluation

```python
# Run JS on page — access anything JavaScript can
page.evaluate("document.title")
page.evaluate("window.innerWidth")
page.evaluate("document.querySelectorAll('.item').length")

# Run JS on specific element
locator.evaluate("el => el.getBoundingClientRect()")
locator.evaluate("el => el.dataset.price")

# Run JS on ALL matching elements
locator.evaluate_all("els => els.map(el => el.textContent)")
```

## Common Scraping Patterns

```python
# Pattern 1: Extract list of items
items = page.locator(".product").all()
data = []
for item in items:
    data.append({
        "name": item.locator(".name").text_content(),
        "price": item.locator(".price").text_content(),
    })

# Pattern 2: Extract from table
rows = page.locator("table tr").all()
for row in rows:
    cells = row.locator("td").all_text_contents()

# Pattern 3: Extract links
links = page.locator("a").all()
for link in links:
    href = link.get_attribute("href")
    text = link.text_content()
```