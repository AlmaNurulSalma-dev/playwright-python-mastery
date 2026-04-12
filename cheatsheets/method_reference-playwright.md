# 🎭 Playwright Python — Complete Method Reference

> **These methods are specific to the Playwright library.**
> Every library has its own methods — Selenium, Requests, etc. all have different APIs.
>
> **Universal Python trick to explore ANY library's methods:**
> ```python
> dir(object)          # list all methods/attributes
> help(object.method)  # show docs + parameters
> type(object)         # show what class/type it is
> ```

**Official API Docs:** https://playwright.dev/python/docs/api/class-playwright

---

## Architecture Overview

```
sync_playwright()  →  Playwright (p)
    ├── p.chromium  →  BrowserType
    ├── p.firefox   →  BrowserType
    └── p.webkit    →  BrowserType
            │
            └── .launch()  →  Browser
                    │
                    ├── .new_context()  →  BrowserContext
                    │       │
                    │       └── .new_page()  →  Page  ← (you'll use this 90% of the time)
                    │               │
                    │               └── .locator()  →  Locator
                    │
                    └── .new_page()  →  Page (shortcut: auto-creates context)
```

---

## Layer 1: Playwright Object (`p`)

> Created by: `with sync_playwright() as p`

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `p.chromium` | BrowserType | Launcher for Chromium-based browsers |
| `p.firefox` | BrowserType | Launcher for Firefox |
| `p.webkit` | BrowserType | Launcher for WebKit (Safari engine) |
| `p.devices` | dict | Predefined device descriptors (iPhone, Pixel, etc.) |
| `p.selectors` | Selectors | Custom selector engine registration |

### Methods

| Method | Description |
|--------|-------------|
| `p.stop()` | Stop the Playwright server. Called automatically by `with` statement. |

---

## Layer 1.5: BrowserType (`p.chromium` / `p.firefox` / `p.webkit`)

> Used to launch browsers

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `name` | str | `'chromium'`, `'firefox'`, or `'webkit'` |
| `executable_path` | str | Path to the browser executable |

### Methods

#### `launch(**kwargs) → Browser`

Launch a new browser instance.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `headless` | bool | `True` | Run without visible window |
| `slow_mo` | float | `0` | Slow down every operation by ms |
| `channel` | str | — | Use installed browser: `'chrome'`, `'msedge'`, `'chrome-beta'` |
| `args` | list[str] | — | Extra browser CLI arguments |
| `executable_path` | str | — | Path to custom browser binary |
| `timeout` | float | `30000` | Max wait for launch (ms) |
| `devtools` | bool | `False` | Auto-open DevTools (Chromium only) |
| `downloads_path` | str | — | Where to save downloads |
| `proxy` | dict | — | Proxy: `{'server': 'http://proxy:8080'}` |
| `chromium_sandbox` | bool | `False` | Enable Chromium sandboxing |

#### `launch_persistent_context(user_data_dir, **kwargs) → BrowserContext`

Launch browser with persistent storage (cookies/localStorage survive restart). Accepts all `launch()` + `new_context()` params.

#### `connect(ws_endpoint) → Browser`

Connect to an existing browser instance via WebSocket.

---

## Layer 2: Browser Object

> Created by: `p.chromium.launch()`

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `contexts` | list[BrowserContext] | All open contexts |
| `is_connected()` | bool | Whether browser is still running |
| `version` | str | Browser version string |
| `browser_type` | BrowserType | The launcher that created this browser |

### Methods

#### `new_context(**kwargs) → BrowserContext`

Create an isolated browser context (like incognito window).

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `viewport` | dict | `{'width': 1280, 'height': 720}` | Window size |
| `user_agent` | str | — | Custom User-Agent string |
| `locale` | str | — | Locale: `'en-US'`, `'id-ID'`, `'zh-CN'` |
| `timezone_id` | str | — | Timezone: `'Asia/Jakarta'` |
| `geolocation` | dict | — | Fake location: `{'latitude': -6.2, 'longitude': 106.8}` |
| `permissions` | list[str] | — | Grant: `['geolocation', 'notifications']` |
| `color_scheme` | str | — | `'dark'`, `'light'`, `'no-preference'` |
| `storage_state` | str/dict | — | Load saved cookies/localStorage from file |
| `record_video_dir` | str | — | Directory to save video recordings |
| `record_video_size` | dict | — | Video size: `{'width': 1280, 'height': 720}` |
| `proxy` | dict | — | Proxy settings for this context |
| `http_credentials` | dict | — | HTTP auth: `{'username': '...', 'password': '...'}` |
| `extra_http_headers` | dict | — | Headers added to every request |
| `ignore_https_errors` | bool | `False` | Ignore SSL certificate errors |
| `java_script_enabled` | bool | `True` | Enable/disable JavaScript |
| `has_touch` | bool | `False` | Enable touch events |
| `is_mobile` | bool | `False` | Enable mobile emulation |
| `device_scale_factor` | float | `1` | Device pixel ratio (2 = retina) |

#### `new_page(**kwargs) → Page`

Shortcut: creates a new context + new page in one call. Accepts same params as `new_context()`.

#### `close()`

Close browser and all pages/contexts. **Always call this!**

---

## Layer 2.5: BrowserContext

> Created by: `browser.new_context()`
> Think of it as an incognito window — isolated cookies, storage, cache.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `pages` | list[Page] | All open pages in this context |
| `browser` | Browser | Parent browser object |

### Methods

| Method | Description |
|--------|-------------|
| `new_page()` | Open a new page (tab) in this context |
| `close()` | Close context and all its pages |
| `storage_state(path=)` | Get/save cookies + localStorage as JSON (save login!) |
| `add_cookies(cookies)` | Add cookies (list of dict) |
| `cookies(urls=)` | Get all cookies, optionally filtered by URL |
| `clear_cookies()` | Remove all cookies |
| `grant_permissions(permissions, origin=)` | Grant permissions like geolocation |
| `set_geolocation(geolocation)` | Set fake geolocation for all pages |
| `route(url, handler)` | Intercept network requests |
| `unroute(url)` | Remove route handler |
| `expect_page()` | Wait for a new page (popup/tab) to open |

### Events

| Event | Description |
|-------|-------------|
| `on('page')` | New page created in context |
| `on('close')` | Context was closed |
| `on('request')` | Network request was made |
| `on('response')` | Network response received |

---

## Layer 3: Page Object ⭐

> Created by: `browser.new_page()` or `context.new_page()`
> **This is the object you'll use 90% of the time!**

### Navigation

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `goto(url)` | `url` (str), `wait_until` ('load'\|'domcontentloaded'\|'networkidle'\|'commit'), `timeout` (float), `referer` (str) | Response or None | Navigate to URL |
| `go_back()` | `wait_until`, `timeout` | Response or None | Browser back button |
| `go_forward()` | `wait_until`, `timeout` | Response or None | Browser forward button |
| `reload()` | `wait_until`, `timeout` | Response or None | Refresh page |

### Page Info

| Method/Property | Returns | Description |
|----------------|---------|-------------|
| `title()` | str | Page title (from `<title>` tag via `document.title`) |
| `url` ⚠️ property | str | Current URL (**no parentheses!**) |
| `content()` | str | Full HTML source |
| `viewport_size` ⚠️ property | dict or None | `{'width': int, 'height': int}` |

### Locators (Modern Way — RECOMMENDED)

| Method | Key Parameters | Returns | Description |
|--------|---------------|---------|-------------|
| `locator(selector)` | `selector` (str), `has_text` (str/regex), `has` (Locator) | Locator | Find by CSS or XPath |
| `get_by_role(role)` | `role` (str), `name` (str/regex), `checked`, `disabled`, `exact` | Locator | **RECOMMENDED** — by ARIA role |
| `get_by_text(text)` | `text` (str/regex), `exact` (bool) | Locator | Find by text content |
| `get_by_label(text)` | `text` (str/regex), `exact` (bool) | Locator | Find form element by `<label>` |
| `get_by_placeholder(text)` | `text` (str/regex), `exact` (bool) | Locator | Find input by placeholder |
| `get_by_alt_text(text)` | `text` (str/regex), `exact` (bool) | Locator | Find by alt text (images) |
| `get_by_title(text)` | `text` (str/regex), `exact` (bool) | Locator | Find by title attribute |
| `get_by_test_id(test_id)` | `test_id` (str/regex) | Locator | Find by `data-testid` |

**ARIA roles:** `'button'`, `'link'`, `'heading'`, `'textbox'`, `'checkbox'`, `'radio'`, `'combobox'`, `'listbox'`, `'tab'`, `'tabpanel'`, `'navigation'`, `'dialog'`, `'alert'`, `'img'`, `'list'`, `'listitem'`, `'row'`, `'cell'`, `'table'`, `'menuitem'`

### Interactions

| Method | Key Parameters | Description |
|--------|---------------|-------------|
| `click(selector)` | `selector`, `button` ('left'\|'right'\|'middle'), `click_count` (int), `delay` (float), `position` (dict), `modifiers` (list), `force` (bool), `timeout` | Click element |
| `dblclick(selector)` | Same as click | Double-click |
| `fill(selector, value)` | `selector`, `value` (str), `force`, `timeout` | Clear + fill input (**instant**, no key events) |
| `type(selector, text)` | `selector`, `text` (str), `delay` (float), `timeout` | Type char by char (**simulates real typing**) |
| `press(selector, key)` | `selector`, `key` (str: `'Enter'`, `'Tab'`, `'Control+a'`), `delay`, `timeout` | Press keyboard key/shortcut |
| `hover(selector)` | `selector`, `position`, `modifiers`, `force`, `timeout` | Hover mouse over element |
| `check(selector)` | `selector`, `force`, `timeout` | Check checkbox (no-op if already checked) |
| `uncheck(selector)` | `selector`, `force`, `timeout` | Uncheck checkbox |
| `select_option(selector)` | `selector`, `value` (str/list), `label` (str/list), `index` (int/list) | Select dropdown option → returns list[str] |
| `set_input_files(selector, files)` | `selector`, `files` (str/list) | Upload file(s) to `<input type="file">` |
| `focus(selector)` | `selector`, `timeout` | Focus on element |
| `drag_and_drop(source, target)` | `source`, `target`, `force`, `timeout` | Drag element to target |

**`fill()` vs `type()`:**
- `fill()` = instant replace (like paste) — use for most cases
- `type()` = simulates real keystroke events — use when site reacts to each keypress

### Waiting

| Method | Key Parameters | Returns | Description |
|--------|---------------|---------|-------------|
| `wait_for_selector(selector)` | `selector`, `state` ('attached'\|'detached'\|'visible'\|'hidden'), `timeout` | ElementHandle or None | Wait for element |
| `wait_for_load_state(state)` | `state` ('load'\|'domcontentloaded'\|'networkidle'), `timeout` | — | Wait for page load state |
| `wait_for_url(url)` | `url` (str/regex/callable), `timeout` | — | Wait for URL to match |
| `wait_for_timeout(timeout)` | `timeout` (float, ms) | — | Hard wait ⚠️ **AVOID — last resort only** |
| `wait_for_function(expression)` | `expression` (str JS), `arg`, `timeout`, `polling` | — | Wait for JS to return truthy |
| `wait_for_event(event)` | `event` (str), `predicate` (callable), `timeout` | — | Wait for event to fire |
| `expect_response(url)` | `url_or_predicate` (str/regex/callable), `timeout` | Response | Wait for network response (use with `with`) |
| `expect_request(url)` | `url_or_predicate`, `timeout` | Request | Wait for network request |
| `expect_popup()` | `predicate`, `timeout` | Page | Wait for popup/new tab |
| `expect_download()` | `predicate`, `timeout` | Download | Wait for file download |
| `expect_file_chooser()` | `predicate`, `timeout` | FileChooser | Wait for file chooser dialog |
| `expect_console_message()` | `predicate`, `timeout` | ConsoleMessage | Wait for console.log |

### Capture / Output

#### `screenshot(**kwargs) → bytes`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `path` | str | — | File path to save (png/jpeg) |
| `full_page` | bool | `False` | Capture entire scrollable page |
| `type` | str | `'png'` | `'png'` or `'jpeg'` |
| `quality` | int | — | 0-100, JPEG only |
| `clip` | dict | — | Crop: `{'x': 0, 'y': 0, 'width': 500, 'height': 300}` |
| `omit_background` | bool | `False` | Transparent background (png only) |
| `timeout` | float | — | Max wait (ms) |

#### `pdf(**kwargs) → bytes`

⚠️ **Chromium headless ONLY**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `path` | str | — | File path to save |
| `format` | str | `'Letter'` | `'Letter'`\|`'Legal'`\|`'Tabloid'`\|`'A0'`-`'A6'` |
| `width` / `height` | str | — | Custom size: `'8.5in'` |
| `scale` | float | `1` | 0.1 - 2.0 |
| `print_background` | bool | `False` | Include background colors/images |
| `landscape` | bool | `False` | Landscape orientation |
| `margin` | dict | — | `{'top': '1cm', 'bottom': '1cm', 'left': '1cm', 'right': '1cm'}` |
| `page_ranges` | str | — | e.g. `'1-5, 8'` |

### JavaScript Execution

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `evaluate(expression)` | `expression` (str JS), `arg` (optional) | Any | Run JS, return result |
| `evaluate_handle(expression)` | `expression`, `arg` | JSHandle | Run JS, return handle |
| `add_script_tag()` | `url`/`path`/`content` | — | Inject `<script>` |
| `add_style_tag()` | `url`/`path`/`content` | — | Inject `<style>` |

```python
# Examples
page.evaluate("document.title")
page.evaluate("window.scrollY")
page.evaluate("() => document.querySelectorAll('.quote').length")
```

### Dialogs

| Method | Description |
|--------|-------------|
| `on('dialog', handler)` | Listen for alert/confirm/prompt |
| `expect_event('dialog')` | Wait for dialog to appear |

```python
# Auto-dismiss all dialogs
page.on('dialog', lambda d: d.accept())
```

### Frames (iframes)

| Method/Property | Returns | Description |
|----------------|---------|-------------|
| `frame(name=, url=)` | Frame or None | Get frame by name or URL |
| `frames` ⚠️ property | list[Frame] | All frames in page |
| `main_frame` ⚠️ property | Frame | The main frame |
| `frame_locator(selector)` | FrameLocator | Interact with iframe content |

### Network

| Method | Parameters | Description |
|--------|-----------|-------------|
| `route(url, handler)` | `url` (str/regex), `handler` (callable) | Intercept requests |
| `unroute(url)` | `url` (str/regex) | Remove route handler |
| `set_extra_http_headers(headers)` | `headers` (dict) | Set headers for all future requests |

```python
# Block images for faster scraping
page.route("**/*.{png,jpg,jpeg,gif}", lambda route: route.abort())
```

### Page Lifecycle

| Method | Parameters | Description |
|--------|-----------|-------------|
| `close()` | — | Close this page/tab |
| `is_closed()` | — | Check if page was closed → bool |
| `bring_to_front()` | — | Focus this tab |
| `pause()` | — | **Open Playwright Inspector** for debugging! |
| `set_viewport_size(size)` | `size` (dict: `{'width': int, 'height': int}`) | Resize viewport |
| `set_default_timeout(timeout)` | `timeout` (float, ms) | Default timeout for all actions |
| `set_default_navigation_timeout(timeout)` | `timeout` (float, ms) | Default timeout for navigation |

### Page Events

| Event | Description |
|-------|-------------|
| `on('load')` | Page finished loading |
| `on('domcontentloaded')` | DOM content loaded |
| `on('close')` | Page was closed |
| `on('console')` | `console.log()` called in page |
| `on('request')` | Network request made |
| `on('response')` | Network response received |
| `on('requestfailed')` | Network request failed |
| `on('dialog')` | Alert/confirm/prompt appeared |
| `on('download')` | Download started |
| `on('filechooser')` | File chooser opened |
| `on('popup')` | New page/popup opened |
| `on('crash')` | Page crashed |

---

## Layer 4: Locator Object

> Created by: `page.locator()`, `page.get_by_role()`, etc.
> **Locators are LAZY — they don't search until you perform an action!**

### Actions

| Method | Description |
|--------|-------------|
| `click()` | Click the element |
| `dblclick()` | Double-click |
| `fill(value)` | Clear and fill input |
| `type(text)` | Type text char by char |
| `press(key)` | Press keyboard key |
| `check()` | Check checkbox |
| `uncheck()` | Uncheck checkbox |
| `select_option()` | Select dropdown option |
| `hover()` | Hover over element |
| `focus()` | Focus the element |
| `set_input_files(files)` | Upload files |
| `drag_to(target_locator)` | Drag to another locator |
| `scroll_into_view_if_needed()` | Scroll element into view |
| `screenshot(path=)` | Screenshot this specific element |
| `dispatch_event(type)` | Dispatch DOM event (e.g. `'click'`, `'input'`) |

### Data Extraction

| Method | Returns | Description |
|--------|---------|-------------|
| `inner_text()` | str | Rendered text (respects CSS visibility) |
| `text_content()` | str | Raw text content (ignores CSS) |
| `inner_html()` | str | Inner HTML of element |
| `input_value()` | str | Current value of input/textarea/select |
| `get_attribute(name)` | str or None | Attribute value: `locator.get_attribute('href')` |
| `count()` | int | Number of matching elements |
| `all()` | list[Locator] | List of all matching Locators |
| `all_inner_texts()` | list[str] | `inner_text()` for all matches |
| `all_text_contents()` | list[str] | `text_content()` for all matches |
| `evaluate(expression)` | Any | Run JS on this element |
| `evaluate_all(expression)` | Any | Run JS on all matching elements |
| `is_visible()` | bool | Is element visible? |
| `is_hidden()` | bool | Is element hidden? |
| `is_enabled()` | bool | Is element enabled? |
| `is_disabled()` | bool | Is element disabled? |
| `is_checked()` | bool | Is checkbox/radio checked? |
| `is_editable()` | bool | Is element editable? |
| `bounding_box()` | dict or None | `{'x', 'y', 'width', 'height'}` |

### Filtering & Chaining

| Method/Property | Description |
|----------------|-------------|
| `filter(has_text=, has=)` | Narrow down matches |
| `nth(index)` | Select by index (0-based) |
| `first` ⚠️ property | First matching element |
| `last` ⚠️ property | Last matching element |
| `locator(selector)` | Find child: `parent.locator('.child')` |
| `get_by_role(role)` | Find child by role |
| `get_by_text(text)` | Find child by text |
| `and_(locator)` | Must match BOTH locators |
| `or_(locator)` | Must match EITHER locator |

### Assertions (with `expect`)

```python
from playwright.sync_api import expect
```

| Assertion | Description |
|-----------|-------------|
| `expect(locator).to_be_visible()` | Element is visible |
| `expect(locator).to_be_hidden()` | Element is hidden |
| `expect(locator).to_be_enabled()` | Element is enabled |
| `expect(locator).to_be_disabled()` | Element is disabled |
| `expect(locator).to_be_checked()` | Checkbox is checked |
| `expect(locator).to_be_editable()` | Element is editable |
| `expect(locator).to_have_text(text)` | Text content matches |
| `expect(locator).to_contain_text(text)` | Contains text (substring) |
| `expect(locator).to_have_value(value)` | Input value matches |
| `expect(locator).to_have_attribute(name, value)` | Attribute matches |
| `expect(locator).to_have_class(class)` | CSS class matches |
| `expect(locator).to_have_count(count)` | Number of matches |
| `expect(locator).to_have_css(property, value)` | CSS property matches |
| `expect(locator).to_have_id(id)` | ID attribute matches |
| `expect(page).to_have_url(url)` | Page URL matches |
| `expect(page).to_have_title(title)` | Page title matches |

---

## Discover Methods Yourself

Save this as `discover_methods.py` and run it:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    page = context.new_page()

    print("=" * 60)
    print("PLAYWRIGHT OBJECT:")
    print([m for m in dir(p) if not m.startswith('_')])

    print("\nBROWSER:")
    print([m for m in dir(browser) if not m.startswith('_')])

    print("\nCONTEXT:")
    print([m for m in dir(context) if not m.startswith('_')])

    print("\nPAGE:")
    print([m for m in dir(page) if not m.startswith('_')])

    print("\nLOCATOR:")
    locator = page.locator("body")
    print([m for m in dir(locator) if not m.startswith('_')])

    browser.close()
```

> **Tip:** In VS Code with Pylance, just type `page.` and autocomplete shows all available methods!