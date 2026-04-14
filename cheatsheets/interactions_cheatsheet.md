# 🖱️ Playwright Interactions Cheatsheet

## Click Types

### Basic Clicks

```python
# Regular click
page.click("button")

# Double click
page.dblclick("button")
# or
page.click("button", click_count=2)

# Triple click — selects entire paragraph
page.click("p.text", click_count=3)

# Right click — opens context menu
page.click("button", button="right")

# Middle click — opens link in new tab (browser behavior)
page.click("a", button="middle")
```

### Click with Timing

```python
# Slow click — hold mousedown before releasing
# Normal: mousedown → mouseup (instant)
# Delay:  mousedown → wait 200ms → mouseup
page.click("button", delay=200)

# Use for: long-press menus, anti-bot, drag preparation
```

### Click at Position

```python
# Click specific coordinates within element
page.click("canvas", position={"x": 100, "y": 50})

# Use for: canvas elements, image maps, custom UI components
```

### Click with Keyboard Modifiers

```python
# Ctrl + Click — open link in new tab
page.click("a", modifiers=["Control"])

# Shift + Click — select range, extend selection
page.click("item", modifiers=["Shift"])

# Alt + Click — some apps have alt-click actions
page.click("element", modifiers=["Alt"])

# Meta + Click — Cmd on Mac
page.click("element", modifiers=["Meta"])

# Multiple modifiers
page.click("element", modifiers=["Control", "Shift"])
```

### Force Click

```python
# Skip all actionability checks (visibility, enabled, stable)
# USE AS LAST RESORT — if Playwright says element not visible but you know it's there
page.click("button", force=True)
```

### Click with Timeout

```python
# Custom timeout (default is 30000ms = 30s)
page.click("button", timeout=5000)    # wait max 5 seconds
page.click("button", timeout=60000)   # wait max 60 seconds
```

### Click with Trial Run

```python
# Check if click WOULD work without actually clicking
page.click("button", trial=True)
# Throws error if element not clickable — useful for testing
```

---

## Hover

```python
# Basic hover
page.hover("nav .menu-item")

# Hover at specific position
page.hover("element", position={"x": 10, "y": 20})

# Hover with modifiers
page.hover("element", modifiers=["Shift"])

# Force hover
page.hover("element", force=True)

# Use for: dropdown menus, tooltips, preview popups
```

---

## Fill & Type

```python
# fill() — INSTANT, auto-clears first, no key events per character
page.fill("input#email", "alma@example.com")

# type() — character by character, fires key events
page.type("input#search", "playwright", delay=100)

# Clear an input
page.fill("input#email", "")
```

| | fill() | type() |
|--|--------|--------|
| Speed | Instant | Slow (char by char) |
| Auto-clear | Yes | No |
| Key events | No (just input event) | Yes (keydown, keypress, keyup per char) |
| Use when | 99% of the time | Autocomplete, search, reactive fields |

---

## Keyboard Actions

```python
# Press a key on focused element
page.press("input#search", "Enter")
page.press("input", "Tab")
page.press("input", "Escape")
page.press("input", "Backspace")

# Keyboard shortcuts
page.press("body", "Control+a")      # Select all
page.press("body", "Control+c")      # Copy
page.press("body", "Control+v")      # Paste
page.press("body", "Control+z")      # Undo
page.press("body", "Control+Shift+z") # Redo

# Arrow keys
page.press("input", "ArrowUp")
page.press("input", "ArrowDown")
page.press("input", "ArrowLeft")
page.press("input", "ArrowRight")

# Function keys
page.press("body", "F5")             # Refresh
page.press("body", "F12")            # DevTools

# Press with delay (hold key down)
page.press("input", "Shift+a", delay=100)
```

### Special Key Names

| Key | Name |
|-----|------|
| Enter | `Enter` |
| Tab | `Tab` |
| Escape | `Escape` |
| Space | `Space` |
| Backspace | `Backspace` |
| Delete | `Delete` |
| Arrow keys | `ArrowUp`, `ArrowDown`, `ArrowLeft`, `ArrowRight` |
| Home/End | `Home`, `End` |
| Page Up/Down | `PageUp`, `PageDown` |
| Modifiers | `Shift`, `Control`, `Alt`, `Meta` |
| Function | `F1` - `F12` |

---

## Dropdowns (Select)

```python
# Select by value attribute
page.select_option("select#country", value="id")

# Select by visible text (label)
page.select_option("select#country", label="Indonesia")

# Select by index (0-based)
page.select_option("select#country", index=2)

# Select multiple (for <select multiple>)
page.select_option("select#colors", value=["red", "blue", "green"])

# Returns list of selected values
selected = page.select_option("select#country", label="Indonesia")
print(selected)  # → ["id"]
```

---

## Checkboxes & Radio Buttons

```python
# Check — no-op if already checked
page.check("input#agree")

# Uncheck — no-op if already unchecked
page.uncheck("input#newsletter")

# Check with force
page.check("input#terms", force=True)

# Verify state
is_checked = page.is_checked("input#agree")
print(is_checked)  # → True or False

# Selenium comparison:
# Selenium: element.click() (doesn't care about current state — could uncheck!)
# Playwright: page.check() (smart — only checks if not already checked)
```

---

## File Upload

```python
# Single file
page.set_input_files("input[type='file']", "path/to/file.pdf")

# Multiple files
page.set_input_files("input[type='file']", ["file1.pdf", "file2.jpg"])

# Clear file selection
page.set_input_files("input[type='file']", [])
```

---

## Drag and Drop

```python
# Drag source to target
page.drag_and_drop("#draggable", "#droppable")

# With force
page.drag_and_drop("#source", "#target", force=True)
```

---

## Focus

```python
# Focus on an element (like clicking into an input without typing)
page.focus("input#search")

# Use for: triggering focus events, preparing for keyboard input
```

---

## Common Selector Patterns

```python
# By ID
page.click("#submit-btn")

# By class
page.click(".btn-primary")

# By tag
page.click("button")

# By attribute
page.click("input[type='submit']")
page.click("a[href='/login']")
page.click("[data-testid='login-btn']")

# By text content
page.click("text=Login")
page.click("a:text('Next')")
page.click("button:has-text('Submit')")   # substring match

# By CSS combinators
page.click("form > button")              # direct child
page.click("nav a")                      # descendant
page.click("h2 + p")                     # adjacent sibling

# By nth match
page.click(".item >> nth=0")             # first match
page.click(".item >> nth=-1")            # last match

# Combine multiple conditions
page.click("button:text('Save'):visible")
```

---

## Actionability Checks

Before performing any action, Playwright auto-checks:

| Check | What it means |
|-------|---------------|
| Visible | Element is not hidden (display:none, visibility:hidden) |
| Stable | Element is not moving/animating |
| Enabled | Element is not disabled |
| Receives events | No other element is blocking it (overlay, modal) |
| Editable | For fill/type — element accepts input |

If any check fails, Playwright **waits and retries** until timeout. This is why you rarely need explicit waits in Playwright!

To skip these checks: `force=True` (use as last resort).