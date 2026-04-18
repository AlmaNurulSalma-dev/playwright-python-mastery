# 🎯 Locator Cheatsheet — Module 1.4

## Priority Order (Playwright Official Recommendation)

1. `get_by_role()` ⭐ BEST
2. `get_by_label()` ⭐ For form inputs
3. `get_by_placeholder()`
4. `get_by_text()`
5. `get_by_alt_text()`
6. `get_by_title()`
7. `get_by_test_id()`
8. `locator()` with CSS
9. `locator()` with XPath — avoid

## get_by_* Methods

```python
# By role (what the element IS)
page.get_by_role("button", name="Login")
page.get_by_role("link", name="Next")
page.get_by_role("heading", name="Welcome", level=1)
page.get_by_role("textbox", name="Username")
page.get_by_role("checkbox")
page.get_by_role("combobox")              # <select> dropdown

# By label (form input's label)
page.get_by_label("Email Address")

# By placeholder
page.get_by_placeholder("Enter your name")

# By visible text
page.get_by_text("Einstein")              # substring match
page.get_by_text("Einstein", exact=True)  # exact match
page.get_by_text(re.compile(r"^The"))     # regex match

# By image alt text
page.get_by_alt_text("Company Logo")

# By title attribute (tooltip)
page.get_by_title("Click to submit")

# By data-testid
page.get_by_test_id("login-btn")
```

## CSS Selectors

```python
page.locator("#username")                        # by ID
page.locator(".quote")                           # by class
page.locator("button")                           # by tag
page.locator("input[type='submit']")             # by attribute
page.locator("input[type='text'][name='user']")  # multiple attributes
page.locator(".quote .author")                   # descendant (any depth)
page.locator("div > span")                       # direct child only
page.locator("a[href='/login']")                 # by href
```

## XPath Selectors

```python
page.locator("xpath=//h1")                              # by tag
page.locator("xpath=//*[@id='username']")                # by ID
page.locator("xpath=//div[@class='quote']")              # by class
page.locator("xpath=//a[text()='Login']")                # by exact text
page.locator("xpath=//span[contains(text(),'world')]")   # contains text
page.locator("xpath=//small[@class='author']/..")        # go UP to parent
```

## Position Selectors

```python
locator.first           # first match (property!)
locator.last            # last match (property!)
locator.nth(0)          # by index, 0-based (method!)
locator.nth(2)          # third element
locator.count()         # how many matches
```

## Chaining (Parent → Child)

```python
# Find child inside parent
quote = page.locator(".quote").first
author = quote.locator(".author")           # .author INSIDE this quote
tags = quote.locator(".tag")                # all .tags INSIDE this quote
```

## Filtering

```python
# Filter by text content
page.locator(".quote").filter(has_text="Einstein")

# Filter by child element
page.locator(".quote").filter(has=page.locator(".tag", has_text="life"))

# Chain multiple filters
page.locator(".quote").filter(has_text="Einstein").filter(has=page.locator(".tag", has_text="inspirational")).first
```

## Combining Locators

```python
# AND — must match BOTH
page.get_by_role("link").and_(page.get_by_text("Next"))

# OR — match EITHER
page.get_by_text("Next").or_(page.get_by_text("Previous"))
```

## Getting Data

```python
locator.text_content()         # raw text (ignores CSS visibility)
locator.inner_text()           # rendered text (respects CSS)
locator.inner_html()           # HTML inside element
locator.input_value()          # value of input/select/textarea
locator.get_attribute("href")  # any attribute value
locator.is_visible()           # bool
locator.is_checked()           # bool (checkbox/radio)
locator.is_enabled()           # bool
locator.all_text_contents()    # list of text for ALL matches
locator.all()                  # list of Locator objects
```

## Common Scraping Pattern

```python
# Extract structured data from multiple elements
quotes = page.locator(".quote").all()
data = []
for quote in quotes:
    data.append({
        "text": quote.locator(".text").text_content(),
        "author": quote.locator(".author").text_content(),
        "tags": quote.locator(".tag").all_text_contents(),
    })
```