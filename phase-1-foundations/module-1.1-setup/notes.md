# Module 1.1 — Notes

## Playwright vs Selenium Setup
| Aspect | Selenium | Playwright |
|--------|----------|------------|
| Install | `pip install selenium` + download driver | `pip install playwright` + `playwright install` |
| Browser drivers | Manual download, version matching | Auto-bundled, always compatible |
| Browsers | Chrome, Firefox, Edge, Safari (limited) | Chromium, Firefox, WebKit |
| Speed | Slower (WebDriver protocol) | Faster (CDP/direct protocol) |

## What `playwright install` downloads
- Chromium (open-source base of Chrome)
- Firefox
- WebKit (Safari engine — test Safari on Windows!)
