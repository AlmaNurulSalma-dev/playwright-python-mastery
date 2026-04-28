# Module 2.2 — Handling Dynamic Content

## The Problem

Modern websites don't send all data in the initial HTML.
Instead, they load content dynamically using:
- AJAX/fetch calls (load data from API after page loads)
- Infinite scroll (load more as you scroll down)
- Lazy loading (images/content load when visible)
- Click-to-load ("Load More" buttons)
- SPA frameworks (React, Vue, Angular — render via JavaScript)

## Waiting Strategies

### 1. wait_for_selector() — Wait for element to exist/appear
```python
# Wait for element to appear in DOM
page.wait_for_selector(".results")

# Wait for element to be visible
page.wait_for_selector(".results", state="visible")

# Wait for element to disappear (loading spinner gone)
page.wait_for_selector(".spinner", state="hidden")

# Wait for element to be removed from DOM entirely
page.wait_for_selector(".spinner", state="detached")
```

States:
- `"attached"` — element exists in DOM (default)
- `"detached"` — element removed from DOM
- `"visible"` — element is visible on screen
- `"hidden"` — element is hidden or removed

### 2. wait_for_load_state() — Wait for page load phase
```python
page.wait_for_load_state("domcontentloaded")  # HTML parsed
page.wait_for_load_state("load")              # all resources loaded
page.wait_for_load_state("networkidle")       # no requests for 500ms
```

### 3. wait_for_url() — Wait for URL to change
```python
page.wait_for_url("**/dashboard")
page.wait_for_url(re.compile(r"/page/\d+"))
```

### 4. wait_for_function() — Wait for JS condition
```python
# Wait until JavaScript variable is ready
page.wait_for_function("window.dataLoaded === true")

# Wait until certain number of elements exist
page.wait_for_function("document.querySelectorAll('.item').length > 10")
```

### 5. expect_response() — Wait for specific API call
```python
with page.expect_response("**/api/products") as response_info:
    page.click("#load-more")
response = response_info.value
data = response.json()
```

## Infinite Scroll Pattern
```python
while True:
    # Step 1: Count how many items exist NOW
    previous_count = page.locator(".item").count()
    # e.g., 10 items
    
    # Step 2: Scroll to the very bottom of the page
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    # document.body.scrollHeight = total page height
    # scrollTo(0, height) = scroll to bottom
    
    # Step 3: Wait for new content to load
    page.wait_for_timeout(1000)   # 1 second for AJAX to fetch + render
    
    # Step 4: Count again — did new items appear?
    new_count = page.locator(".item").count()
    # e.g., 20 items (10 new ones loaded!)
    
    # Step 5: Compare
    if new_count == previous_count:
        break   # same count = no new items = we're at the bottom!
    # else: loop again — scroll more!
```

## Selenium Comparison
| Task | Selenium | Playwright |
|------|----------|------------|
| Wait for element | WebDriverWait + EC | Auto-wait or wait_for_selector |
| Wait for API | No built-in | expect_response() |
| Wait for JS condition | WebDriverWait + custom | wait_for_function() |
| Infinite scroll | Manual scroll + sleep | evaluate scroll + wait |