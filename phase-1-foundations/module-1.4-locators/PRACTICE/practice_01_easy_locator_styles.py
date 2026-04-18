from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()
    page.goto("https://the-internet.herokuapp.com/login")
    
    user_input_css = page.locator("input#username")
    user_input_label = page.get_by_label("Username")
    user_input_role = page.get_by_role("textbox", name="Username")
    
    # CSS
    user_input_css.fill("tomsmith")
    print(f"filled by css: {user_input_css.input_value()}")
    user_input_css.fill("")    # clear for next method

    # Label
    user_input_label.fill("tomsmith")
    print(f"filled by label: {user_input_label.input_value()}")
    user_input_label.fill("")  # clear for next method

    # Role
    user_input_role.fill("tomsmith")
    print(f"filled by role: {user_input_role.input_value()}")
    
    login_button_css = page.locator("button[type='submit']")
    login_button_text = page.get_by_text("Login")
    login_button_role = page.get_by_role("button", name="Login")
    
    print(f"login button by css: {login_button_css.text_content()}")
    print(f"login button by text: {login_button_text.text_content()}")
    print(f"login button by role: {login_button_role.text_content()}")
    
    print("====== SUMMARY ======")
    print("most readable method: get_by_role()")    