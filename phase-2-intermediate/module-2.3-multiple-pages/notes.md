# Module 2.3 — Multiple Pages & Contexts

## Recap from Module 1.2

Browser
  ├── Context A (isolated session — own cookies, storage)
  │   ├── Page 1 (tab — shares cookies with Page 2)
  │   └── Page 2
  └── Context B (isolated — different cookies from A)
      └── Page 3

## New Concepts in This Module

### 1. Opening New Tabs

    # Open a new tab in same context (shares cookies!)
    page2 = context.new_page()
    page2.goto("https://example.com")

### 2. Handling Popups

    # Some links/buttons open a NEW window/tab (popup)
    # Use expect_popup() to catch it
    with page.expect_popup() as popup_info:
        page.click("a[target='_blank']")   # triggers new tab
    popup = popup_info.value               # the new Page object
    print(popup.url)                       # URL of the popup

### 3. Simulating Multiple Users

    # Each context = different user session
    context_admin = browser.new_context()
    context_user = browser.new_context()

    # Admin logs in
    admin_page = context_admin.new_page()
    admin_page.goto("/login")
    admin_page.fill("#user", "admin")

    # Regular user logs in (completely isolated!)
    user_page = context_user.new_page()
    user_page.goto("/login")
    user_page.fill("#user", "regular_user")

### 4. Saving & Reusing Session State

    # Save cookies + localStorage to file
    context.storage_state(path="auth_state.json")

    # Reuse in a new context — skip login!
    context2 = browser.new_context(storage_state="auth_state.json")
    page2 = context2.new_page()
    page2.goto("/dashboard")   # already logged in!

### 5. Cookie Management

    # Get all cookies
    cookies = context.cookies()

    # Add cookies manually
    context.add_cookies([{
        "name": "session_id",
        "value": "abc123",
        "domain": "example.com",
        "path": "/"
    }])

    # Clear all cookies
    context.clear_cookies()

## Selenium Comparison

| Task | Selenium | Playwright |
|------|----------|------------|
| New tab | driver.execute_script("window.open()") + switch | context.new_page() |
| Handle popup | driver.switch_to.window(handle) | page.expect_popup() |
| Multiple users | Multiple WebDriver instances (heavy!) | Multiple contexts (lightweight!) |
| Save session | Manual cookie extraction | context.storage_state() |
| Switch tabs | driver.switch_to.window(handle) — error prone | Just use the page variable directly |