# Setup Guide

## Prerequisites
- Python 3.10+
- VS Code with Python & Pylance extensions

## Installation
```bash
pip install -r requirements.txt
playwright install
```

## VS Code Extensions
- Python (Microsoft)
- Pylance
- Playwright Test for VSCode (optional)

## Verify Installation
```bash
python -c "from playwright.sync_api import sync_playwright; print('Playwright ready!')"
```
