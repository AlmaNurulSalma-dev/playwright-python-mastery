# Module 1.2 — Architecture Deep Dive

## The 3-Layer Model

Playwright punya 3 layer hierarchy. Ini WAJIB dipahami:
Browser          → like opening Chrome app
└── Context    → like an incognito window (isolated session)
└── Page  → like a tab inside that window

### Why 3 layers?

| Layer | What it is | Analogy | Shares with other instances? |
|-------|-----------|---------|------------------------------|
| Browser | The browser process | Chrome.exe running | Everything (it's the app) |
| Context | Isolated session | Incognito window | NOTHING — cookies, storage all separate |
| Page | A tab | Browser tab | Shares cookies/storage WITH same context |

### Key Insight
- Pages in the SAME context → share cookies, localStorage, session
- Pages in DIFFERENT contexts → completely isolated (like 2 different people)
- This is how you simulate multiple users WITHOUT opening multiple browsers!

### Selenium Comparison
| Scenario | Selenium | Playwright |
|----------|----------|------------|
| Open browser | `webdriver.Chrome()` | `p.chromium.launch()` |
| New tab | Complicated (execute_script + switch) | `context.new_page()` |
| Isolated session | Launch ANOTHER browser entirely | `browser.new_context()` |
| Multiple users | Multiple WebDriver instances (heavy!) | Multiple contexts (lightweight!) |

### sync_api vs async_api
| | sync_api | async_api |
|--|---------|-----------|
| Import | `from playwright.sync_api import sync_playwright` | `from playwright.async_api import async_playwright` |
| Style | Normal sequential code | Uses `async/await` |
| Use when | Learning, simple scripts | Production, parallel tasks |
| Speed | One thing at a time | Multiple things simultaneously |